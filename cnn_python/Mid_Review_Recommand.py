import csv
import re
import pandas as pd
def Recompile_Name(s):
    re_s = s.split('|')#先将俩个代码地址分割开来
    # print('re_s:'+str(re_s))
    reword0 = re.split('[\\\|/]',re_s[0])
    reword1 = re.split('[\\\|/]',re_s[1])
    # print('reword0:' + str(reword0))
    # print('reword1:' + str(reword1))
    final_word0 = re.split('[(|)]', reword0[-1])  # 将用户代码中的code.txt(6-13)这一部分提取出来
    final_word1 = re.split('[(|)]', reword1[-1])  # 将本地dataset中的code.txt(6-13)这一部分提取出来
    return final_word0,final_word1
def calculate_all_number(path):
    score=[]
    X_test_Function_name = []
    csv_reader = csv.reader(open(path, encoding='gbk'))
    for i,row in enumerate(csv_reader):
        if i>0:
            # print('row:'+str(row))
            score.append(row[2])
            X_test_Function_name.append(row[1])#将所有的方法名保存下来
    local_class_name = list()
    all_final_word = []  # 用于保存所有的final_word数据
    for i in range(len(X_test_Function_name)):
        final_word = []  # 用于将用户以及本地dataset的class名称以及方法所在的列保存下来
        final_word0, final_word1 = Recompile_Name(X_test_Function_name[i])
        for k in final_word0:
            if k:
                final_word.append(k)
        for k1 in final_word1:
            if k1:
                final_word.append(k1)
        final_word.append(score[i])  # 找到对于每一个数据集找到最大值
        # print(final_word)
        all_final_word.append(final_word)
        local_class_name.append(final_word1[-3])
    local_class_name = list(set(local_class_name))#找到所有非重复的本地代码的名称
    my_dictionary = {}  # 用于存储用户代码与本地代码的排列组合个数
    for key in local_class_name:
        my_dictionary[key] = [0, 0, 0]  # 第一个值是存储总共有多少个排列组合，第二个值存储有多少个是克隆对儿的排列组合,第三个值用来存放最后的值
    for key in local_class_name:
        for word in all_final_word:
            if key in word:
                # print(word)
                my_dictionary[key][0] += 1  # 用于统计score值得个数
                if word[-1]:  # 统计用户和本地代码俩者相似的方法个数
                    # print('key:'+str(key)+'   '+'word:'+str(word))
                    my_dictionary[key][1] += float(word[-1])
    for key in local_class_name:
        my_dictionary[key][2] = my_dictionary[key][1] / my_dictionary[key][0]
        # print(key + '    -----------     ' + str(my_dictionary[key][2]))
    new_dict = sorted(my_dictionary.items(), key=lambda d: d[1][2], reverse=True)
    csv_word = []
    for k in new_dict:
        s = []
        s.append(k[0])
        s.append(k[1][2])
        csv_word.append(s)
        # print(str(k[0])+':'+str(k[1][2]))
    test = pd.DataFrame(data=csv_word)
    test.to_csv('F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv', encoding='gbk')
    return my_dictionary
if __name__ == '__main__':
    path='F:\\2018年暑假科研\\CNN\\my_clone\\method_sim.csv'
    calculate_all_number(path)