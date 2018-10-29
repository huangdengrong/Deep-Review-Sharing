import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helper_new
import word2vec_helpers
import pandas as pd
# Parameters
# ==================================================

# Data Parameters
#./是当前目录  ../是父级目录  /是根目录
tf.flags.DEFINE_string("input_text_file", "G:/data_test.csv", "Label file for test text data source.")
# tf.flags.DEFINE_string("input_text_file", "../data/data2.csv", "Test text data source to evaluate.")
tf.flags.DEFINE_string("single_url",None,"single url to evaluate")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_boolean("eval_train", True, "Evaluate on all training data")
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
FLAGS.flag_values_dict()
def test(path,checkpoint_path):

    print("\nParameters:")
    for attr, value in sorted(FLAGS.__flags.items()):
        print("{}={}".format(attr.upper(), value))
    print("")

    # validate
    # ==================================================

    # validate checkout point file
    checkpoint_file = tf.train.latest_checkpoint(
        checkpoint_path)  # 我们可以使用tf.train.latest_checkpoint（）来自动获取最后一次保存的模型。
    if checkpoint_file is None:
        print("Cannot find a valid checkpoint file!")
        exit(0)
    print("Using checkpoint file : {}".format(checkpoint_file))

    # 加载word2vec_model
    # 若出现”./”开头的参数，会从”./”开头的参数的上一个参数开始拼接。
    # trained_word2vec_model_file = os.path.join(checkpoint_path, "..", "trained_word2vec.model")
    trained_word2vec_model_file ='F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/runs/1539606045/trained_word2vec.model'
    if not os.path.exists(trained_word2vec_model_file):
        print("Word2vec model file \'{}\' doesn't exist!".format(trained_word2vec_model_file))
    print("Using word2vec model file : {}".format(trained_word2vec_model_file))

    # validate training params file
    training_params_file = 'F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/runs/1539606045/training_params.pickle'
    # training_params_file = os.path.join(checkpoint_path, "..", "training_params.pickle")
    if not os.path.exists(training_params_file):
        print("Training params file \'{}\' is missing!".format(training_params_file))
    print("Using training params file : {}".format(training_params_file))

    # Load params
    params = data_helper_new.loadDict(training_params_file)
    print("type of params: {}".format(type(params)))
    num_labels = int(params['num_labels'])
    max_document_length = int(params['max_document_length'])
    # x_raw1, y_test = data_helper_new.load_data_and_labels(FLAGS.input_text_file)
    x_raw, name = data_helper_new.load_data_and_names(path)
    # x_raw+=x_raw1
    # Get Embedding vector x_test
    sentences, max_document_length = data_helper_new.padding_sentences(x_raw, '<PADDING>',
                                                                       padding_sentence_length=max_document_length)
    x_test = np.array(word2vec_helpers.embedding_sentences(sentences, file_to_load=trained_word2vec_model_file))
    print("x_test.shape = {}".format(x_test.shape))
    # Evaluation
    # ==================================================
    print("\nEvaluating...\n")
    checkpoint_file = tf.train.latest_checkpoint(checkpoint_path)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
            allow_soft_placement=FLAGS.allow_soft_placement,
            log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            # tf.train.import_meta_graph函数给出model.ckpt-n.meta的路径后会加载图结构，并返回saver对象
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            # saver.restore函数给出model.ckpt-n的路径后会自动寻找参数名-值文件进行加载
            saver.restore(sess, checkpoint_file)
            # Get the placeholders from the graph by name
            # tf.Graph.get_operation_by_name(name)	根据名称返回操作节点
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            batches = data_helper_new.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)
            all_scores = []
            def add_score(score):
                for k in score:
                    all_scores.append(k)

            scores = graph.get_operation_by_name("output/scores").outputs[0]
            for x_test_batch in batches:
                score = sess.run(scores, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                add_score(score)
            # Save the evaluation to a csv
            print(all_scores)
            all_data = []
            def cal_data():
                for k in range(len(name)):
                    data = []
                    data.append(name[k])
                    all_scores[k][0]=abs(all_scores[k][0])
                    data.append(all_scores[k][0])
                    all_data.append(data)
            cal_data()
            test3 = pd.DataFrame(data=all_data)
            test3.to_csv('F:/2018年暑假科研/CNN/my_clone/method_sim.csv', encoding="gbk")
if __name__ == '__main__':
    path="F:/2018年暑假科研/CNN/my_clone/method_merge.csv"
    checkpoint_path = "F:/2018年暑假科研/CNN/CNN相关文件/DetectMaliciousURL-master/model/runs/1539606045/checkpoints"
    test(path,checkpoint_path)
