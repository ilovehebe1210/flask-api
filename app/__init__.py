# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 20:50:23 2021

@author: SASAD
"""
import numpy as np
import pandas as pd
import json
from pandas.io.json import json_normalize
from flask import Flask, jsonify,request
from flask_cors import CORS
from json import dumps
from flask import Flask, make_response
import pickle
from json import dumps
from flask import make_response


def MTable(x):
    x=int(x)
    if x>=0 and x<=3:
        return '組距1 3以下'
    elif x>=3 and x<=7:
        return '組距2 3-7'
    else:
        return '組距3 7以上'
       
def MTable2(x, p, d):
    x=int(x)
    if x <= d[p][0.25]:
        return str(d[p][0.25])+'後標' 
    elif x <= d[p][0.5]: 
        return str(d[p][0.5])+'均標'
    else:
        return str(d[p][0.75])+'前標'


app = Flask(__name__)
CORS(app)
@app.route('/test')
def oops():
     return 'hello!!'

@app.route('/getdata')
def getdata():
     raw_df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
     inserValuejs = raw_df.to_json(orient = 'records')
     inserValues=json.loads(inserValuejs)
     return make_response(dumps(inserValues))

@app.route('/predict',methods=['POST'])
def  postInput():
    inserValues=request.get_json()
    cols_data=['Age','BusinessTravel','DailyRate','Department','DistanceFromHome','Education','EducationField','EmployeeNumber','EnvironmentSatisfaction','Gender','HourlyRate','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MaritalStatus','MonthlyIncome','MonthlyRate','NumCompaniesWorked','OverTime','PercentSalaryHike','PerformanceRating','RelationshipSatisfaction','StockOptionLevel','TotalWorkingYears','TrainingTimesLastYear','WorkLifeBalance','YearsAtCompany','YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager']
    cols =['Age','DailyRate','Department','DistanceFromHome','Education','EducationField','EmployeeNumber','EnvironmentSatisfaction','Gender','HourlyRate','JobInvolvement','JobLevel','JobRole','JobSatisfaction','MaritalStatus','MonthlyIncome','MonthlyRate','NumCompaniesWorked','OverTime','PercentSalaryHike','PerformanceRating','RelationshipSatisfaction','StockOptionLevel','TotalWorkingYears','TrainingTimesLastYear','WorkLifeBalance','YearsAtCompany','YearsInCurrentRole','YearsSinceLastPromotion','YearsWithCurrManager']
    #data_2=['41','1102','Sales','1','2','Life Sciences','1','2','Female','94','3','2','Sales Executive','4','Single','5993','19479','8','Yes','11','3','1','0','8','0','1','6','4','0','5']


    data=[]
    process_data=[]
    #act=[]
    input_data=[]
    raw_df = pd.read_excel("WA_Fn-UseC_-HR-Employee-Attrition_Data_First_Processes_SMOTE_2.xls")
    raw_df =raw_df[cols]

    for x in range(0,len(inserValues),1):
        
       for i in range(0,len(cols_data),1):
           if i==1:
               bus=bus=inserValues[x]['BusinessTravel']
           else:
               data.append(inserValues[x][cols_data[i]])    
       #print(len(inserValues))
       #print(data)
       de={'Sales':0,'Research & Development':1,'Human Resources':2}
       data[2]=de[data[2]]
       edu={'Life Sciences':0,'Medical':1,'Marketing':2,'Technical Degree':3,'Human Resources':4,'Other':5}
       data[5]=edu[data[5]]
        
       gen={'Female':0,'Male':1}
       data[8]=gen[data[8]]
        
       job_roel={'Sales Executive':0,'Research Scientist':1,'Laboratory Technician':2,'Manufacturing Director':3,'Healthcare Representative':4,'Manager':5,'Sales Representative':6,'Research Director':7,'Human Resources':8}
       data[12]=job_roel[data[12]]

       mar={'Divorced':0,'Single':1,'Married':2}
       data[14]=mar[data[14]]

       over_time={'Yes':0,'No':1}
       data[18]=over_time[data[18]]
 
       for y in range(0,30,1):   
           max_num=max(raw_df[cols[y]])
           min_num=min(raw_df[cols[y]])
           pro_num=round(((float(data[y])-min_num)/(max_num-min_num)),16)
           process_data.append(pro_num)
            
       if bus == 'Non-Travel':
           process_data.append(float(1))
           process_data.append(float(0))
           process_data.append(float(0))
       elif bus == 'Travel_Frequently':
           process_data.append(float(0))
           process_data.append(float(1))
           process_data.append(float(0))
       elif bus == 'Travel_Rarely':
           process_data.append(float(0))
           process_data.append(float(0))
           process_data.append(float(1))
        
        #print(process_data)
       input_data.append(process_data)
       data=[]
       process_data=[]
       
    print(input_data)
     
    pickle_in = open("randomforest.pickle",'rb')
    forest = pickle.load(pickle_in)
    predict_result = forest.predict(input_data)
    score = forest.predict_proba(input_data)
    print(predict_result)
    predict_result=list(predict_result)
     
    for i in range(0,len(inserValues)):
         inserValues[i]['Predict_result']=predict_result[i]
         inserValues[i]['Turnover_rate']=score[i][1]
     
    return make_response(dumps(inserValues))


@app.route('/analysis',methods=['POST'])
def  postInput2():
     # 取得前端傳過來的值
     inserValues=request.get_json()
     df=pd.DataFrame(inserValues)
    
     sent_data=[]
    
     #overtime
     dept_att=df.groupby(['OverTime','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='OverTime',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['OverTime'][i]==dept_att['OverTime']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('OverTime').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='OverTime',y='Rate',title='OverTime wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="OverTime")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     
    
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
     
     #business travel
     dept_att=df.groupby(['BusinessTravel','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='BusinessTravel',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['BusinessTravel'][i]==dept_att['BusinessTravel']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('BusinessTravel').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='BusinessTravel',y='Rate',title='OverTime wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="BusinessTravel")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     
     
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #stockoptionlevel
     dept_att=df.groupby(['StockOptionLevel','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='StockOptionLevel',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['StockOptionLevel'][i]==dept_att['StockOptionLevel']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('StockOptionLevel').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='StockOptionLevel',y='Rate',title='StockOptionLevel wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="StockOptionLevel")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     
     
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #JobInvolvement
     dept_att=df.groupby(['JobInvolvement','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='JobInvolvement',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['JobInvolvement'][i]==dept_att['JobInvolvement']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('JobInvolvement').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='JobInvolvement',y='Rate',title='JobInvolvement wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="JobInvolvement")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     
     
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #JobSatisfaction
     dept_att=df.groupby(['JobSatisfaction','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='JobSatisfaction',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['JobSatisfaction'][i]==dept_att['JobSatisfaction']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('JobSatisfaction').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='JobSatisfaction',y='Rate',title='JobSatisfaction wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="JobSatisfaction")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #MaritalStatus
     dept_att=df.groupby(['MaritalStatus','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='MaritalStatus',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['MaritalStatus'][i]==dept_att['MaritalStatus']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('MaritalStatus').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='MaritalStatus',y='Rate',title='MaritalStatus wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="MaritalStatus")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
    
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     
     
     #CompanyNum
     
     
     df['CompanyNum'] = df['NumCompaniesWorked'].apply(MTable)
    
     dept_att=df.groupby(['CompanyNum','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='CompanyNum',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['CompanyNum'][i]==dept_att['CompanyNum']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('CompanyNum').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     
     final_df=pd.merge(Tra_att,dept_att,on="CompanyNum")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     #fig=px.bar(final_df,x='CompanyNum',y='Mani',title='MaritalStatus wise Counts of People in an Organization')
     #fig.show()
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #EnvironmentSatisfaction
     dept_att=df.groupby(['EnvironmentSatisfaction','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='EnvironmentSatisfaction',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['EnvironmentSatisfaction'][i]==dept_att['EnvironmentSatisfaction']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('EnvironmentSatisfaction').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     final_df=pd.merge(Tra_att,dept_att,on="EnvironmentSatisfaction")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     #fig=px.bar(final_df,x='EnvironmentSatisfaction',y='Mani',title='EnvironmentSatisfaction wise Counts of People in an Organization')
     #fig.show()
    
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
    
     #Age
     df['Age'] = df['Age'].astype('float')
     df['Age']=round(df['Age'],-1)
     dept_att=df.groupby(['Age','Attrition']).apply(lambda x:x['Age'].count()).reset_index(name='Counts')
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['Age'][i]==dept_att['Age']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('Age').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     final_df=pd.merge(Tra_att,dept_att,on="Age")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     #fig=px.bar(final_df,x='Age',y='Mani',title='Age wise Counts of People in an Organization')
     #fig.show()
     final_df2=final_df.groupby('Age').apply(lambda x:(x['Age']-5).astype('str')+'-'+(x['Age']+5).astype('str')).reset_index(name='Age-range')
     final_df3=pd.merge(final_df,final_df2,on="Age").drop('level_1',axis=1).drop('Age',axis=1)
     final_df3 = final_df3.reindex(columns=['Age-range','Attrition','Counts','Rate','Mani'])
     d_records = final_df3.to_dict('records')
     sent_data.append(d_records)
     
     #MonthlyIncome
     df['MonthlyIncome'] = df['MonthlyIncome'].astype('float')
     quantiles = df.quantile(q=[0.25,0.5,0.75])
     quantiles = quantiles.to_dict()
     
     df['MonthlyIncome'] = df['MonthlyIncome'].apply(MTable2,args=('MonthlyIncome',quantiles))
     
     dept_att=df.groupby(['MonthlyIncome','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='MonthlyIncome',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
         temp=dept_att[dept_att['MonthlyIncome'][i]==dept_att['MonthlyIncome']]
         Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
         dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('MonthlyIncome').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
    
     final_df=pd.merge(Tra_att,dept_att,on="MonthlyIncome")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     #fig=px.bar(final_df,x='MonthlyIncome',y='Mani',title='MaritalStatus wise Counts of People in an Organization')
     #fig.show()
    
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)
     
     
     return make_response(dumps(sent_data))

@app.route('/out_reason')
def  out_reason():
     # 取得前端傳過來的值
     df= pd.read_csv(r"C:\Users\pc\Desktop\資料分析\WA_Fn-UseC_-HR-Employee-Attrition.csv")
     sent_data=[]
     #overtime
     dept_att=df.groupby(['OverTime','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='OverTime',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['OverTime'][i]==dept_att['OverTime']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('OverTime').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='OverTime',y='Rate',title='OverTime wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="OverTime")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     final_df

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

#business travel
     dept_att=df.groupby(['BusinessTravel','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='BusinessTravel',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['BusinessTravel'][i]==dept_att['BusinessTravel']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('BusinessTravel').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='BusinessTravel',y='Rate',title='OverTime wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="BusinessTravel")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

#stockoptionlevel
     dept_att=df.groupby(['StockOptionLevel','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='StockOptionLevel',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['StockOptionLevel'][i]==dept_att['StockOptionLevel']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('StockOptionLevel').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='StockOptionLevel',y='Rate',title='StockOptionLevel wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="StockOptionLevel")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

#JobInvolvement
     dept_att=df.groupby(['JobInvolvement','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='JobInvolvement',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['JobInvolvement'][i]==dept_att['JobInvolvement']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('JobInvolvement').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
#fig=px.bar(Tra_att,x='JobInvolvement',y='Rate',title='JobInvolvement wise Counts of People in an Organization')
#fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="JobInvolvement")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

     #JobSatisfaction
     dept_att=df.groupby(['JobSatisfaction','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='JobSatisfaction',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['JobSatisfaction'][i]==dept_att['JobSatisfaction']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('JobSatisfaction').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     #fig=px.bar(Tra_att,x='JobSatisfaction',y='Rate',title='JobSatisfaction wise Counts of People in an Organization')
     #fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="JobSatisfaction")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

     #MaritalStatus
     dept_att=df.groupby(['MaritalStatus','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='MaritalStatus',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['MaritalStatus'][i]==dept_att['MaritalStatus']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('MaritalStatus').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
#fig=px.bar(Tra_att,x='MaritalStatus',y='Rate',title='MaritalStatus wise Counts of People in an Organization')
#fig.show()
     final_df=pd.merge(Tra_att,dept_att,on="MaritalStatus")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

     #MonthlyIncome
     quantiles = df.quantile(q=[0.25,0.5,0.75])

     print(type(quantiles))
     quantiles = quantiles.to_dict()

     print(type(df))

     df['MonthlyIncome'] = df['MonthlyIncome'].apply(MTable2,args=('MonthlyIncome',quantiles))
     dept_att=df.groupby(['MonthlyIncome','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='月收分類',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['MonthlyIncome'][i]==dept_att['MonthlyIncome']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('MonthlyIncome').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)

     final_df=pd.merge(Tra_att,dept_att,on="MonthlyIncome")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
#fig=px.bar(final_df,x='月收分類',y='Mani',title='MaritalStatus wise Counts of People in an Organization')
#fig.show()


     d_records = final_df.to_dict('records')
     sent_data.append(d_records)


     final_df=final_df.values
     low=float(final_df[0][0])
     hi=float(final_df[2][0])

#CompanyNum

   
     df['CompanyNum'] = df['NumCompaniesWorked'].apply(MTable)

     dept_att=df.groupby(['CompanyNum','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
     #fig=px.bar(dept_att,x='CompanyNum',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['CompanyNum'][i]==dept_att['CompanyNum']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('CompanyNum').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)

     final_df=pd.merge(Tra_att,dept_att,on="CompanyNum")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
#fig=px.bar(final_df,x='CompanyNum',y='Mani',title='MaritalStatus wise Counts of People in an Organization')
#fig.show()


     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

#EnvironmentSatisfaction
     dept_att=df.groupby(['EnvironmentSatisfaction','Attrition']).apply(lambda x:x['DailyRate'].count()).reset_index(name='Counts')
#fig=px.bar(dept_att,x='EnvironmentSatisfaction',y='Counts',color='Attrition',title='Department wise Counts of People in an Organization')
     dept_att['jinanhansome']=''
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['EnvironmentSatisfaction'][i]==dept_att['EnvironmentSatisfaction']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
     Tra_att=dept_att.groupby('EnvironmentSatisfaction').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     final_df=pd.merge(Tra_att,dept_att,on="EnvironmentSatisfaction")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
#fig=px.bar(final_df,x='EnvironmentSatisfaction',y='Mani',title='EnvironmentSatisfaction wise Counts of People in an Organization')
#fig.show()

     d_records = final_df.to_dict('records')
     sent_data.append(d_records)

#Age

     df['Age']=round(pd.Series(df['Age']),-1)
     print(type(df['Age']))
     dept_att=df.groupby(['Age','Attrition']).apply(lambda x:x['Age'].count()).reset_index(name='Counts')
     for i in range(len(dept_att)):
          temp=dept_att[dept_att['Age'][i]==dept_att['Age']]
          Attrition_Yes=dept_att[dept_att['Attrition'][i]==dept_att['Attrition']]
          dept_att.loc[i,'jinanhansome'] =(Attrition_Yes['Counts'].sum()-dept_att['Counts'][i])/(dept_att['Counts'].sum()-temp['Counts'].sum())
          Tra_att=dept_att.groupby('Age').apply(lambda x:x['Counts']/x['Counts'].sum()).reset_index(name='Rate')
     Tra_att=Tra_att[Tra_att['level_1']%2==1].drop('level_1',axis=1)
     final_df=pd.merge(Tra_att,dept_att,on="Age")
     final_df['Mani']=final_df['Rate']/final_df['jinanhansome']
     final_df=final_df[final_df['Attrition']=='Yes']
#fig=px.bar(final_df,x='Age',y='Mani',title='Age wise Counts of People in an Organization')
#fig.show()
     final_df2=final_df.groupby('Age').apply(lambda x:(x['Age']-5).astype('str')+'-'+(x['Age']+5).astype('str')).reset_index(name='Age-range')
     final_df3=pd.merge(final_df,final_df2,on="Age").drop('level_1',axis=1).drop('Age',axis=1)
     final_df3 = final_df3.reindex(columns=['Age','Attrition','Counts','Rate','Mani'])

     d_records = final_df3.to_dict('records')
     sent_data.append(d_records)
     
     
     compare=df
     cols=['Attrition','OverTime','BusinessTravel','StockOptionLevel','JobInvolvement','JobSatisfaction','MaritalStatus','EnvironmentSatisfaction','MonthlyIncome','NumCompaniesWorked','Age']
     col=['OverTime','BusinessTravel','StockOptionLevel','JobInvolvement','JobSatisfaction','MaritalStatus','MonthlyIncome','CompanyNum','EnvironmentSatisfaction','Age']

     print(sent_data)

     for i in range(0,len(cols)-2,1):
         globals()[col[i]]={}
         for x in range(0,len(sent_data[i]),1):
             globals()[col[i]][sent_data[i][x][col[i]]]=sent_data[i][x]['Mani']             
             if col[i] == "MonthlyIncome":
                 sent_0=sent_data[i][x][col[i]]
                 sent_1=sent_data[i][x][col[i]]
                 sent_2=sent_data[i][x][col[i]]
             
     Age_value={'2':sent_data[9][0]['Mani'],'3':sent_data[9][1]['Mani'],'4':sent_data[9][2]['Mani'],'5':sent_data[9][2]['Mani'],'6':sent_data[9][2]['Mani']}
          


     
        
     compare_data=compare[cols]
     compare_data=compare_data[compare_data["Attrition"] == "Yes"]
     compare_data=compare_data.drop("Attrition", axis = 1)
     compare_data_v=compare_data.values
     a=[]
     b=[]
     c=[]
     for i in range(0,len(compare_data_v),1):   
         compare_data_v[i][0]=OverTime[compare_data_v[i][0]]
         compare_data_v[i][1]=BusinessTravel[compare_data_v[i][1]]    
         compare_data_v[i][2]=StockOptionLevel[compare_data_v[i][2]]
         compare_data_v[i][3]=JobInvolvement[compare_data_v[i][3]]
         compare_data_v[i][4]=JobSatisfaction[compare_data_v[i][4]]
         compare_data_v[i][5]=MaritalStatus[compare_data_v[i][5]]
         compare_data_v[i][6]=EnvironmentSatisfaction[compare_data_v[i][6]]    
         compare_data_v[i][7]=income_value(compare_data_v[i][7],low,hi,sent_0,sent_1,sent_2)
         compare_data_v[i][7]=MonthlyIncome[compare_data_v[i][7]]    
         compare_data_v[i][8]=MTable(compare_data_v[i][8])
         compare_data_v[i][8]=CompanyNum[str(compare_data_v[i][8])]    
         compare_data_v[i][9]=str(int((round(compare_data_v[i][9],-1))/10))
         compare_data_v[i][9]=Age_value[compare_data_v[i][9]]

         max_thir=list(map(list(compare_data_v[i]).index, heapq.nlargest(3, compare_data_v[i])))
         a.append(str(col[max_thir[0]]))
         b.append(str(col[max_thir[1]]))
         c.append(str(col[max_thir[2]]))
     
     compare_data['reason']=a
     #compare_data['reason2']=b
     #compare_data['reason3']=c
     
     js = compare_data.to_dict(orient="records")
     print(len(compare_data))

     return make_response(dumps(js))
 
    
