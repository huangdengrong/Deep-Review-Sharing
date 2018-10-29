import csv
import re
import os
def _main(path,filename):
    pattern=r'\.|_'
    csv_reader = csv.reader(open(path, encoding='gbk'))
    rec_id=[]
    #去除csv文件的第一行
    for i,row in enumerate(csv_reader):
        if i>0:
            if i<=3:
                rec_id.append(re.split(pattern,row[1])[1]+'.txt')
                #只选择前三个相似度最高的代码的评论
    pathDir = os.listdir(filename)
    recommand=[]
    for key in rec_id:
        if key in pathDir:
            recommand.append('F:\\2018年暑假科研\\CNN\\my_clone\\review\\'+key)
            # print(key)
    text=''
    for key in recommand:
        with open(key) as a:
            read=a.read()
            text=text+read
    return text
if __name__ == '__main__':
    path='F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv'
    filename='F:/2018年暑假科研/CNN/my_clone/review'
    rec_id=_main(path,filename)
    # 选取排列好的前三个代码最为最终的推荐评论
    print(rec_id)