import csv
import pandas as pd
reader=csv.reader(open('G:/new_new_data_test.csv',encoding='utf-8'))
num=0
for i,row in enumerate(reader):
    if i>0 :
        if row[-2]=='3':
            num+=1
print(num)