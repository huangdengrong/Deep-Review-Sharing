import csv
import re
import pandas as pd
import numpy as np
import random
import pickle
def clean_str(string):#用于将数据中的非字母数字切分开
    string = re.sub(r"[^A-Za-z0-9\+\-\*\\=}{\[\]'>\"<,!\|\?()]", " ", string)
    string = re.sub(r"\+", " + ", string)
    string = re.sub(r"\-", " - ", string)
    string = re.sub(r"\*", " * ", string)
    string = re.sub(r"\\", " \ ", string)
    string = re.sub(r"=", " = ", string)
    string = re.sub(r"}", " } ", string)
    string = re.sub(r"{", " } ", string)
    string = re.sub(r"\[", " ] ", string)
    string = re.sub(r"\]", " ] ", string)
    string = re.sub(r"'", " ' ", string)
    string = re.sub(r'\"', ' " ', string)
    string = re.sub(r">", " > ", string)
    string = re.sub(r"<", " > ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\|", " | ", string)
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"\?", " ? ", string)
    string = re.sub(r"$", " $ ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
def getTokens(input):#将数据切分开
    input=clean_str(input)
    allTokens = []
    token = str(input)
    token = token.replace(' ', '/')
    tokens = token.split('/')
    tokens = [token for token in tokens if token!='']#将数据中的空格去除掉
    allTokens = allTokens + tokens
    return allTokens
def padding_sentences(input_sentences, padding_token, padding_sentence_length=None):#将sentence扩充成相同的维度
    sentences = [getTokens(sentence) for sentence in input_sentences]
    max_sentence_length = padding_sentence_length if padding_sentence_length is not None else max(
            [len(sentence) for sentence in sentences])
    i=0
    all_vector=[]
    for sentence in sentences:
        if len(sentence) > max_sentence_length:
            sentence = sentence[:max_sentence_length]
        else:
            sentence.extend([padding_token] * (max_sentence_length - len(sentence)))
        all_vector.append(sentence)
    return (all_vector, max_sentence_length)

def saveDict(input_dict, output_file):#将数据保存在本地
    with open(output_file, 'wb') as f:
        pickle.dump(input_dict, f)

def loadDict(dict_file):#用于加载数据
    with open(dict_file, 'rb') as f:
        output_dict = pickle.load(f)
    return output_dict
def process_label(y):#用于将label处理成我们标准的形式
    if y=='1':
        y=[0.875]
    else:
        if y=='2':
            y = [0.625]
        else:
            if y=='3':
                y = [0.375]
            else:
                if y=='4':
                    y = [0.125]
    return y
#此函数用于加载数据和标签
def load_data_and_labels(path):
    x=[]
    y=[]
    reader=csv.reader(open(path,encoding='utf-8'))
    for i,row in enumerate(reader):
        if i>0:
            if len(row[1])>150:#先提取前面的200个word
                row[1]=row[1][:150]
            if len(row[2])>150:
                row[2]=row[2][:150]
            x.append(row[1]+row[2])
            y.append(process_label(row[3]))
    return(x,y)
#此函数用于加载我们dataset中的data和name
def load_data_and_names(path):
    x = []
    y = []
    reader = csv.reader(open(path, encoding='gbk'))
    for i, row in enumerate(reader):
        if i > 0:
            if len(row[1])>200:#先提取前面的200个word
                row[1]=row[1][:200]
            if len(row[2])>200:
                row[2]=row[2][:200]
            x.append(row[1] + row[2])
            y.append(row[0])#用于加载文件名
    return (x, y)
#用于进行迭代加载数据进行训练
def batch_iter(data, batch_size, num_epochs, shuffle=True):
    '''
    Generate a batch iterator for a dataset
    '''
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((data_size - 1) / batch_size) + 1
    for epoch in range(num_epochs):
        if shuffle:
            # Shuffle the data at each epoch
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_idx: end_idx]
if __name__ == "__main__":
    file_path='G:/data_test.csv'
    load_data_and_labels(file_path)