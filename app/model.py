import pickle

cols = ['Age', 'DailyRate', 'Department', 'DistanceFromHome', 'Education', 'EducationField', 'EmployeeNumber', 'EnvironmentSatisfaction', 'Gender', 'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobRole', 'JobSatisfaction', 'MaritalStatus', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'OverTime',
        'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager', 'Non-Travel', 'Travel_Frequently', 'Travel_Rarely']
# data=[]
process_data = []
input_data = []

raw_df = pd.read_excel(
    r"C:\Users\pc\Desktop\資料分析\WA_Fn-UseC_-HR-Employee-Attrition_Data_First_Processes_SMOTE_2.xls")
ndarray = raw_df.value
raw_df = raw_df[cols]


# =============================================================================
# for i in range(0,len(cols),1):
#     inp=input("請輸入"+cols[i]+":")
#     data.append(inp)
# =============================================================================

for i in range(0, len(cols), 1):
    max_num = max(raw_df[cols[i]])
    min_num = min(raw_df[cols[i]])
    pro_num = (float(data[i])-min_num)/(max_num-min_num)
    process_data.append(pro_num)

input_data.append(process_data)


pickle_in = open('app/model/randomforest.pickle', 'rb')
forest = pickle.load(pickle_in)

predict_result = forest.predict(input_data)
print(predict_result)
