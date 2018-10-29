import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helper_new
import word2vec_helpers
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import sklearn as sk
# Parameters
# ==================================================

# Data Parameters
#./是当前目录  ../是父级目录  /是根目录
# tf.flags.DEFINE_string("input_text_file", "../data/data2.csv", "Test text data source to evaluate.")
tf.flags.DEFINE_string("input_text_file", "G:/new_new_data_test.csv", "Label file for test text data source.")
tf.flags.DEFINE_string("single_url",None,"single url to evaluate")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/runs/1539606045/checkpoints/", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", True, "Evaluate on all training data")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS.flag_values_dict()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# validate
# ==================================================

# validate checkout point file
checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)#我们可以使用tf.train.latest_checkpoint（）来自动获取最后一次保存的模型。
if checkpoint_file is None:
    print("Cannot find a valid checkpoint file!")
    exit(0)
print("Using checkpoint file : {}".format(checkpoint_file))

# 加载word2vec_model
#若出现”./”开头的参数，会从”./”开头的参数的上一个参数开始拼接。
trained_word2vec_model_file = os.path.join(FLAGS.checkpoint_dir, "..", "trained_word2vec.model")
if not os.path.exists(trained_word2vec_model_file):
    print("Word2vec model file \'{}\' doesn't exist!".format(trained_word2vec_model_file))
print("Using word2vec model file : {}".format(trained_word2vec_model_file))

# validate training params file
training_params_file = os.path.join(FLAGS.checkpoint_dir, "..", "training_params.pickle")
if not os.path.exists(training_params_file):
    print("Training params file \'{}\' is missing!".format(training_params_file))
print("Using training params file : {}".format(training_params_file))

# Load params
params = data_helper_new.loadDict(training_params_file)
print("type of params: {}".format(type(params)))
num_labels = int(params['num_labels'])
max_document_length = int(params['max_document_length'])
print(max_document_length)
x_raw, y_test = data_helper_new.load_data_and_labels(FLAGS.input_text_file)
# Get Embedding vector x_test
sentences, max_document_length = data_helper_new.padding_sentences(x_raw, '<PADDING>', padding_sentence_length = max_document_length)
x_test = np.array(word2vec_helpers.embedding_sentences(sentences, file_to_load = trained_word2vec_model_file))
print("x_test.shape = {}".format(x_test.shape))


# Evaluation
# ==================================================
print("\nEvaluating...\n")
checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variables
        #tf.train.import_meta_graph函数给出model.ckpt-n.meta的路径后会加载图结构，并返回saver对象
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        #saver.restore函数给出model.ckpt-n的路径后会自动寻找参数名-值文件进行加载
        saver.restore(sess, checkpoint_file)
        # Get the placeholders from the graph by name
        #tf.Graph.get_operation_by_name(name)	根据名称返回操作节点
        input_x = graph.get_operation_by_name("input_x").outputs[0]
        input_y = graph.get_operation_by_name("input_y").outputs[0]
        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
        batches = data_helper_new.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)
        # all_predictions = []
        all_scores = []
        def add_score( score):#用于将所有的得分值加起来
            for k in score:
                all_scores.append(abs(k))
        scores=graph.get_operation_by_name("output/scores").outputs[0]
        for x_test_batch in batches:
            score= sess.run(scores ,{input_x: x_test_batch, dropout_keep_prob: 1.0})
            add_score(score)
        def convert_num(y_test):#用于进行对label进行0-1分类
            y=[]
            for key in  y_test:
                if key[0]<0.25:
                    y.append(0)
                else:
                    if key[0] >= 0.25 and key[0] < 0.5:
                        y.append(1)
                    else:
                        if key[0] >= 0.5 and key[0] < 0.75:
                            y.append(2)
                        else:
                            if key[0] >=0.75:
                                y.append(3)
            return y
        def cal_recall_precision(y_test,all_scores,num1,num2):
            score_false=[]
            y_false=[]
            for key in all_scores:
                if key[0] >= num1 and key[0] < num2:
                    score_false.append(1)
                else:
                    score_false.append(0)
            for key in y_test:
                if key[0] >= num1 and key[0] < num2:
                    y_false.append(1)
                else:
                    y_false.append(0)
            return y_false,score_false
        def split_data(y_test,scores,value):#用于将数据中的中括号去掉
            y=[]
            s=[]
            for i,k in enumerate(y_test):
                if k[0]==value:
                    y.append(k[0])
                    s.append(scores[i][0])
            return y,s
        def cal_recall(confusion_matrix,all_num):#计算整体的recall和precision
            accu = [0, 0, 0, 0]
            column = [0, 0, 0,  0]
            line = [0, 0, 0,  0]
            accuracy = 0
            recall = 0
            precision = 0
            for i in range(0, 4):
                accu[i] = confusion_matrix[i][i]
            for i in range(0, 4):
                for j in range(0, 4):
                    column[i] += confusion_matrix[j][i]
            for i in range(0, 4):
                for j in range(0, 4):
                    line[i] += confusion_matrix[i][j]
            for i in range(0, 4):
                accuracy += float(accu[i]) / all_num
            for i in range(0, 4):
                if column[i] != 0:
                    recall += float(accu[i]) / column[i]
            recall = recall / 4
            for i in range(0, 4):
                if line[i] != 0:
                    precision += float(accu[i]) / line[i]
            precision = precision / 4
            f1_score=2*precision*recall/(precision+recall)
            return recall,precision,accuracy,f1_score

        #------------计算整体的recall 和precision
        convert_score=convert_num(all_scores)
        convert_y_test=convert_num(y_test)
        confusion = metrics.confusion_matrix(convert_score,convert_y_test)
        recall, precision,accurcay,f1_score=cal_recall(confusion,len(y_test))
        Recall = []
        Precision=[]
        F1=[]
        Recall.append(recall)
        Precision.append(precision)
        print('all_accuracy:'+str(accurcay))
        print('all_recall:'+str(recall))
        print('all_precision:'+str(precision))
        print('all_f1_score:'+str(f1_score))
        F1.append(f1_score)
        # ------------计算非克隆的recall 和precision
        y_false,score_false=cal_recall_precision(y_test,all_scores,0,0.25)
        recall_false=sk.metrics.precision_score(y_false, score_false)
        precision_false=sk.metrics.recall_score(y_false, score_false)
        y_false_f1_score=sk.metrics.f1_score(y_false, score_false)
        Recall.append(recall_false)
        Precision.append(precision_false)
        F1.append(y_false_f1_score)
        print("y_false_Precision", recall_false)
        print("y_false_Recall", precision_false)
        print("y_false_f1_score", y_false_f1_score)
        ##------------计算Clone 的recall 和precision
        y_clone1 ,score_clone1= cal_recall_precision(y_test, all_scores, 0.25, 0.5)
        recall_clone1 = sk.metrics.precision_score(y_clone1, score_clone1)
        precision_clone1 = sk.metrics.recall_score(y_clone1, score_clone1)
        y_clone1_f1_score=sk.metrics.f1_score(y_clone1, score_clone1)
        Recall.append(recall_clone1)
        Precision.append(precision_clone1)
        F1.append(y_clone1_f1_score)
        print("y_clone1_Precision", recall_clone1)
        print("y_clone1_Recall", precision_clone1)
        print("y_clone1_f1_score", y_clone1_f1_score)
        ##------------计算Clone2的recall 和precision
        y_clone2,score_clone2 = cal_recall_precision(y_test, all_scores, 0.5, 0.75)
        recall_clone2 = sk.metrics.precision_score(y_clone2, score_clone2)
        precision_clone2 = sk.metrics.recall_score(y_clone2, score_clone2)
        y_clone2_f1_score=sk.metrics.f1_score(y_clone2, score_clone2)
        Recall.append(recall_clone2)
        Precision.append(precision_clone2)
        F1.append(y_clone2_f1_score)
        print("y_clone2_Precision", recall_clone2)
        print("y_clone2_Recall", precision_clone2)
        print("y_clone2_f1_score", y_clone2_f1_score)
        ##------------计算Clone3的recall 和precision
        y_clone3,score_clone3 = cal_recall_precision(y_test, all_scores, 0.75, 2)
        recall_clone3 = sk.metrics.precision_score(y_clone3, score_clone3)
        precision_clone3 = sk.metrics.recall_score(y_clone3, score_clone3)
        y_clone3_f1_score = sk.metrics.f1_score(y_clone3, score_clone3)
        Recall.append(recall_clone3)
        Precision.append(precision_clone3)
        F1.append(y_clone3_f1_score)
        print("y_clone3_Precision", recall_clone3)
        print("y_clone3_Recall", precision_clone3)
        print("y_clone3_f1_score", y_clone3_f1_score)
        plt.figure(1)
        plt.subplot(211)
        plt.bar(['all_recall','recall_false','recall_clone1','recall_clone2','recall_clone3'],Recall,color='g')
        plt.xlabel('classes')
        plt.ylabel('recall')
        plt.title(u'recall')
        plt.subplot(212)
        plt.bar(['all_precision','precision_false','precision_clone1','precision_clone2','precision_clone3'], Precision,color='y')
        plt.xlabel('classes')
        plt.ylabel('precision')
        plt.title(u'precision')
        plt.figure(2)
        plt.subplot(211)
        plt.bar(['all_f1', 'f1_false', 'f1_clone1', 'f1_clone2', 'f1_clone3'],F1, color='r')
        plt.xlabel('classes')
        plt.ylabel('F1_Score')
        plt.title(u'f1_score')
        plt.show()
        # test3 = pd.DataFrame(data=all_scores)
        # test3.to_csv('G:/CNN相关文件/DetectMaliciousURL-master/data/ceshi.csv', encoding="gbk")