import csv
def read_data(path):
    read=csv.reader(open(path))
    text=''
    for i,row in enumerate(read):
        if i>0:
            # print(row[1:])
            text+=str(row[1])
            text+=':'
            text+=str(row[2])
            print(text)
if __name__ == '__main__':
    path='F:\\2018年暑假科研\\CNN\\my_clone\\mid_cnn_recommend_sim.csv'
    read_data(path)