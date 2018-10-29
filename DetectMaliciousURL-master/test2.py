import csv
import pandas as pd
reader=csv.reader(open('G:\\新生成的数据\\functions_clones_not_four.csv',encoding='utf-8'))
reader2=csv.reader(open('G:\\新生成的数据\\functions_clones_four.csv',encoding='utf-8'))
reader3=csv.reader(open('G:\\新生成的数据\\functions_false_four.csv',encoding='utf-8'))
reader1=csv.reader(open('G:/data_test.csv',encoding='utf-8'))
num1=0
num2=0
data=[]
for i,row in enumerate(reader):
    if i>0 :
        print(row)
        if row[-2]=='1' and num1<=1000:
            row[2]=row[1]
            data.append(row[1:])
            num1+=1
            print(row)
            print('+_+_+_+_+')
        else:
            if num1>1000 and num1<=2000:
                break

for i,row in enumerate(reader):
    if i>0 :
        print(row)
        if num1 > 1000 and num1 <= 2000:
            data.append(row[1:])
            num1 += 1
            print(row)
        else:
            if num1 > 2000:
                break
for i,row in enumerate(reader):
    if i>0 :
        if row[-2]=='2' and num2<=2000:
            data.append(row[1:])
            num2+=1
            print(row)
num3=0
for i,row in enumerate(reader1):
    if i>0 :
        if row[-2]=='3' and num3<=3000:
            data.append(row[1:])
            num3+=1
        else:
            if row[-2]=='4':
                data.append(row[1:])
n=0
for i,row in enumerate(reader2):
    if i>0 :
        if row[-2]=='2' and n<=1000:
            data.append(row[1:])
            n+=1
        else:
            if n>1000:
                break
num4=0
for i,row in enumerate(reader3):
    if i>0 :
        if row[-2]=='4' and num4<=2000:
            data.append(row[1:])
            num4+=1
        else:
            if num4>2000:
                break
from random import shuffle
shuffle(data)
test3 = pd.DataFrame(data=data)
test3.to_csv('G:/new_new_data_test.csv', encoding="utf-8")

