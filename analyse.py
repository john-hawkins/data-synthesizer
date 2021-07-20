import pandas as pd

df = pd.read_csv("assessments.csv")

temp2 = df[ df['status']=="Withdraw" ]
temp = df[ df['result']=="Fail" ]

print( "Failure Rate:", len(temp)/len(df))
print( "Withdrawl Rate:", len(temp2)/len(df))

print( "Failure Breakdown")
print(temp2['type'].value_counts())


