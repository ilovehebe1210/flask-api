# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 20:50:23 2021

@author: SASAD
"""
import numpy as np
import pickle
import pandas as pd
from flask import Flask, jsonify,request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/test')
def oops():
     return 'hello!!'

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
     
    pickle_in = open(r"/app/model/randomforest.pickle",'rb')
    forest = pickle.load(pickle_in)
    predict_result = forest.predict(input_data)
    score = forest.predict_proba(input_data)
    print(predict_result)
    predict_result=list(predict_result)
     
    for i in range(0,len(inserValues)):
         inserValues[i]['Predict_result']=predict_result[i]
         inserValues[i]['Turnover_rate']=score[i][1]
     
    return make_response(dumps(inserValues))

