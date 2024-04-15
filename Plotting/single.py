
# importing the module
import pandas as pd
 
# read specific columns of csv file using Pandas
df = pd.read_csv("buffer.csv", usecols=['ACCELEROMETER_X','ACCELEROMETER_Y','ACCELEROMETER_Z', 'Time'])
print(df)

df.to_csv('acc.csv')