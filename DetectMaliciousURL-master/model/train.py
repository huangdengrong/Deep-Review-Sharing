# -*- coding: utf-8 -*-
import data_helper_new ,word2vec_helpers
import tensorflow as tf
import os ,time, datetime
import numpy as np
from sklearn.cross_validation import train_test_split
from URLCNN import *
import matplotlib.pyplot as plt
import csv
import tempfile
# Parameters
# =======================================================

# Data loading parameters
# tf.flags.DEFINE_string("data_file" ,"G:/new_data_test.csv", "Data source")
tf.flags.DEFINE_string("clone_data_file" ,"G:/new_new_data_test.csv", "Data source")
tf.flags.DEFINE_string("local_data_file" ,"F:\\2018年暑假科研\\CNN\\my_clone\\method_merge_test.csv", "Data source")
tf.flags.DEFINE_integer("num_labels", 1, "Number of labels for data. (default: 2)")
#
# # Model hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 64, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "1,3,5,7,9", "Comma-spearated filter sizes (default: '1,3,5,7,9')")
tf.flags.DEFINE_integer("num_filters", 128, "Number of filters per filter size (default: 128)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")
tf.flags.DEFINE_integer("sequence_length", 400, "sequnce length of url embedding (default: 100)")
#
# # Training paramters
tf.flags.DEFINE_integer("batch_size", 32, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 500, "Evalue model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 500, "Save model after this many steps (defult: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")
#
# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
# Parse parameters from commands
FLAGS = tf.flags.FLAGS
FLAGS.flag_values_dict()
# 用于保存模型
timestamp = str(int(time.time()))
out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))#用于创建参数保存的文件夹
print("Writing to {}\n".format(out_dir))
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
# Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
checkpoint_prefix = os.path.join(checkpoint_dir, "model")#创建checkpoints的保存模型的地址
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)
def data_del(path,path_my):#用于加载语料库
    sentences = []
    reader = csv.reader(open(path,encoding='utf-8'))
    reader1 = csv.reader(open(path_my,encoding='gbk'))
    for i, row in enumerate(reader):
        if i > 0:
            sentences.append(row[1] + row[2])
    for i, row in enumerate(reader1):
        sentences.append(row[1] + row[2])
    return sentences
def data_preprocess(all_data):
    # Load data
    print("Loading data...")
    if not os.path.exists(os.path.join(out_dir,"data_x.npy")):
          x, y = data_helper_new.load_data_and_labels(FLAGS.clone_data_file)
          # Get embedding vector
          all_sentences,all_max_document_length=data_helper_new.padding_sentences(all_data, '<PADDING>',padding_sentence_length=FLAGS.sequence_length)
          sentences, max_document_length = data_helper_new.padding_sentences(x, '<PADDING>',padding_sentence_length=FLAGS.sequence_length)
          print(len(sentences[0]))
          if not os.path.exists(os.path.join(out_dir,"trained_word2vec.model")):
              word2vec_helpers.word2vec_model(all_sentences, embedding_size = FLAGS.embedding_dim, file_to_save = os.path.join(out_dir, 'trained_word2vec.model'))
              x = np.array(word2vec_helpers.embedding_sentences(sentences, file_to_load=os.path.join(out_dir, 'trained_word2vec.model')))
          else:
              print('w2v model found...')
              # word2vec_helpers.word2vec_model(all_sentences, embedding_size = FLAGS.embedding_dim, file_to_save = os.path.join(out_dir, 'trained_word2vec.model'),file_to_load=os.path.join(out_dir, 'trained_word2vec.model'))
              x=np.array(word2vec_helpers.embedding_sentences(sentences, file_to_load=os.path.join(out_dir, 'trained_word2vec.model')))
              # x = np.array(word2vec_helpers.embedding_sentences(sentences, embedding_size = FLAGS.embedding_dim, file_to_save = os.path.join(out_dir, 'trained_word2vec.model'),file_to_load=os.path.join(out_dir, 'trained_word2vec.model')))
          y = np.array(y)
          del sentences
          del all_sentences
    else:
          print('data found...')
          x= np.load(os.path.join(out_dir,"data_x.npy"))
          y= np.load(os.path.join(out_dir,"data_y.npy"))
    print("x.shape = {}".format(x.shape))
    print("y.shape = {}".format(y.shape))

    # Save params
    if not os.path.exists(os.path.join(out_dir,"training_params.pickle")):
        training_params_file = os.path.join(out_dir, 'training_params.pickle')
        params = {'num_labels' : FLAGS.num_labels, 'max_document_length' : max_document_length}
        data_helper_new.saveDict(params, training_params_file)#用于保存数据字典
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)  # split into training and testing set 80/20 ratio
    del x,y
    return x_train, x_test, y_train, y_test
all_data=data_del(FLAGS.clone_data_file,FLAGS.local_data_file)
x_train, x_test, y_train, y_test =data_preprocess(all_data)
#用于计算精确度
def cal_accuracy(score,label):
    num_true=0.0
    for k in range(len(score)):
        if (score[k][0]<=0.25) and (score[k][0]>=0) and (label[k][0]<=0.25)and (label[k][0]>=0):
            num_true+=1
        else:
            if (score[k][0] <=0.5) and (score[k][0] >= 0.25) and (label[k][0] <=0.5) and (label[k][0] >= 0.25):
                num_true+=1
            else:
                if (score[k][0] <=0.75) and (score[k][0] >= 0.5) and (label[k][0] <=0.75) and (label[k][0] >= 0.5):
                    num_true += 1
                else:
                    if (score[k][0]<=1) and (score[k][0]>=0.75) and (label[k][0]<=1)and (label[k][0]>=0.75):
                        num_true += 1
    return (num_true/len(score))
#用于进行训练模型
def train():
    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        #可以设置tf.ConfigProto()中参数allow_soft_placement=True，允许tf自动选择一个存在并且可用的设备来运行操作。
        #设置tf.ConfigProto()中参数log_device_placement = True ,可以获取到 operations 和 Tensor 被指派到哪个设备(几号CPU或几号GPU)上运行
        # ,会在终端打印出各项操作是在哪个设备上运行的
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            cnn = URLCNN(
                sequence_length=x_train.shape[1],
                num_classes=y_train.shape[1],
                embedding_size=FLAGS.embedding_dim,
                filter_sizes=list(map(int, FLAGS.filter_sizes.split(","))),
                num_filters=FLAGS.num_filters,
                l2_reg_lambda=FLAGS.l2_reg_lambda)

            # Define Training procedure
            optimizer = tf.train.AdamOptimizer(1e-3)
            grads_and_vars = optimizer.compute_gradients(cnn.loss)
            global_step = tf.Variable(0, name="global_step", trainable=False)
            train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

            # Keep track of gradient values and sparsity (optional)
            grad_summaries = []
            for g, v in grads_and_vars:
                if g is not None:
                    grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
                    sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
                    grad_summaries.append(grad_hist_summary)
                    grad_summaries.append(sparsity_summary)
            grad_summaries_merged = tf.summary.merge(grad_summaries)

            # Output directory for models and summaries
            print("Writing to {}\n".format(out_dir))

            # Summaries for loss and accuracy
            loss_summary = tf.summary.scalar("loss", cnn.loss)
            # acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

            # Train Summaries
            train_summary_op = tf.summary.merge([loss_summary, grad_summaries_merged])
            train_summary_dir = os.path.join(out_dir, "summaries", "train")
            train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)#指定一个文件用来保存图。
            #可以调用其add_summary（）方法将训练过程数据保存在filewriter指定的文件中

            # Dev summaries
            dev_summary_op = tf.summary.merge([loss_summary])
            dev_summary_dir = os.path.join(out_dir, "summaries", "dev")#定义一个写入summary的目标文件
            dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph)

            # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
            checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
            checkpoint_prefix = os.path.join(checkpoint_dir, "model")
            if not os.path.exists(checkpoint_dir):
                os.makedirs(checkpoint_dir)
            #tf.global_variables或者tf.all_variables都是获取程序中的变量
            saver = tf.train.Saver(tf.global_variables(), max_to_keep=FLAGS.num_checkpoints)
            # 即max_to_keep=5，保存最近的5个模型
            #max_to_keep 参数，这个是用来设置保存模型的个数，默认为5，即 max_to_keep=5，
            # 保存最近的5个模型。如果你想每训练一代（epoch)就想保存一次模型，则可以将 max_to_keep设置为None或者0，
            # Initialize all variables
            sess.run(tf.global_variables_initializer())
            all_loss=[]
            def train_step(x_batch, y_batch):
                """
                A single training step
                """
                feed_dict = {
                    cnn.input_x: x_batch,
                    cnn.input_y: y_batch,
                    cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
                }
                _, step, summaries, loss,score= sess.run(
                    [train_op, global_step, train_summary_op, cnn.loss,cnn.scores],
                    feed_dict)
                time_str = datetime.datetime.now().isoformat()

                if step % 50 == 0:
                    print("{}: step {}, loss {:g}".format(time_str, step, loss))
                    print(cal_accuracy(score,y_batch))
                    all_loss.append(loss)
                    # print(score)

                train_summary_writer.add_summary(summaries, step)

            def dev_step(x_batch, y_batch, writer=None):
                """
                Evaluates model on a dev set
                """
                feed_dict = {
                    cnn.input_x: x_batch,
                    cnn.input_y: y_batch,
                    cnn.dropout_keep_prob: 1.0
                }
                step, summaries, loss,score = sess.run(
                    [global_step, dev_summary_op, cnn.loss,cnn.scores],
                    feed_dict)
                time_str = datetime.datetime.now().isoformat()
                print("{}: step {}, loss {:g}".format(time_str, step, loss))
                print(cal_accuracy(score,y_test))
                if writer:
                    writer.add_summary(summaries, step)

            # Generate batches
            batches = data_helper_new.batch_iter(
                list(zip(x_train, y_train)), FLAGS.batch_size, FLAGS.num_epochs)

            # Training loop. For each batch...
            for batch in batches:
                x_batch, y_batch = zip(*batch)
                train_step(x_batch, y_batch)
                #tf.train.global_step()用来获取当前sess的global_step值
                current_step = tf.train.global_step(sess, global_step)
                if current_step % FLAGS.evaluate_every == 0:
                    print("\nEvaluation:")
                    dev_step(x_test, y_test, writer=dev_summary_writer)
                    print("")
                    #使用Saver.save()方法保存模型：sess：表示当前会话，当前会话记录了当前的变量值
                    #checkpoint_dir + 'model.ckpt'：表示存储的文件名 ,global_step：表示当前是第几步
                    #打开名为“checkpoint”的文件，可以看到保存记录，和最新的模型存储位置。
                if current_step % FLAGS.checkpoint_every == 0:
                    path = saver.save(sess, checkpoint_prefix, global_step=current_step)
                    #第二个参数表示保存的路径，第三个参数将训练的次数作为后缀加入到模型名字中。
                    print("Saved model checkpoint to {}\n".format(path))
            plt.figure()  # 画图之前首先设置figure对象，此函数相当于设置一块自定义大小的画布，使得后面的图形输出在这块规定了大小的画布上，其中参数figsize设置画布大小
            plt.subplot()
            time=range(len(all_loss))
            plt.plot(all_loss,time)
            plt.title("value of loss")
            plt.xlabel("times of train")
            plt.ylabel("loss")
            plt.show()
            feed_dict = {
                cnn.input_x: x_test,
                cnn.input_y: y_test,
                cnn.dropout_keep_prob: 1.0
            }
            step, summaries, loss,score= sess.run(
                [global_step, dev_summary_op, cnn.loss,cnn.scores],
                feed_dict)
            print(y_test)
            print(score)
            print(cal_accuracy(score,y_test))
train()








