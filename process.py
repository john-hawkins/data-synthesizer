import pandas as pd
import os

# PROCESS THE ENROLMENTS INTO INTERACTIONS DATA

df = pd.read_csv("assessments.csv")
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
temp = df.loc[:,['student_id','course','date']]

temp.columns = ["USER_ID", "ITEM_ID", "TIMESTAMP"]

train = temp[ temp['TIMESTAMP'] < "2020-01-01" ] 
test  = temp[ temp['TIMESTAMP'] > "2020-01-01" ] 

convert_dict = {'USER_ID': str,
                'ITEM_ID': str,
                'TIMESTAMP': int}

train = train.astype(convert_dict)
test  = test.astype(convert_dict)

train.to_csv("personalize/interactions_train.csv", header=True, index=False)
test.to_csv("personalize/interactions_test.csv", header=True, index=False)


# PROCESS THE USERS 
 
df = pd.read_csv("students.csv")
# 
#df['dob'] = pd.to_datetime(df['dob'], format='%Y-%m-%d', errors='coerce')
#df['registration'] = pd.to_datetime(df['registration'], format='%Y-%m-%d', errors='coerce')
#
#from dateutil.relativedelta import relativedelta
#
#def diff_in_years(newer, older):
#    return relativedelta(newer, older).years
#
#
#df['age'] = df.apply( lambda row: diff_in_years(row['registration'], row['dob']), axis=1 )

studs = df.loc[:,['student_id','age','education','major','language']]
studs.columns = ["USER_ID", "AGE", "EDU", "MAJOR", "LANG"]
 
convert_dict = {'USER_ID': str,
                'AGE': int,
                'EDU': str,
                'MAJOR': str,
                'LANG': str,
}

temp = studs.astype(convert_dict)
print(temp.dtypes)
temp.to_csv("personalize/users.csv", header=True, index=False)


# PROCESS THE ITEMS 
df = pd.read_csv("courses.csv")
df.columns = ["ITEM_ID","TITLE","LEVEL","MATH"]

convert_dict = {'ITEM_ID': str,
                'TITLE': str,
                'LEVEL': int,
                'MATH': int,
}
items = df.astype(convert_dict)
items.to_csv("personalize/items.csv", header=True, index=False)


