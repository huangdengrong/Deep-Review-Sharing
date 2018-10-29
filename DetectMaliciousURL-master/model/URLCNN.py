import tensorflow as tf
import numpy as np
slim = tf.contrib.slim

class URLCNN(object):
    '''
    A CNN for URL classification
    Uses and embedding layer, followed by a convolutional, max-pooling and softmax layer.
    '''
    '''
    sequence_length:代表的是一个句子的长度，即一个句子里面有几个word,每一个word表示为一个向量
    num_classes：代表label的个数
    embedding_size：代表每一个向量的维度
    filter_sizes：代表的是filter的个数，一般为[2,3,4]
    num_filters:代表每种filter有多少个
    l2_reg_lambda：代表的是使用l2正则化
    '''
    def __init__(
            self, sequence_length, num_classes,
            embedding_size, filter_sizes, num_filters, l2_reg_lambda=0.0):
        # Placeholders for input, output, dropout
        self.input_x = tf.placeholder(tf.float32, [None, sequence_length, embedding_size], name="input_x")
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
        '''上面的步骤是用来给input,output,dropout进行占坑'''
        # Keeping track of l2 regularization loss (optional)
        '''tf.constant:这个函数的作用是用值进行填充，创建一个张量'''
        l2_loss = tf.constant(0.0)

        # Embedding layer]
        self.embedded_chars = self.input_x
        '''
        f.expand_dims(input, axis=None, name=None, dim=None)
        Inserts a dimension of 1 into a tensor’s shape. 
        在指定的第axis位置增加一个维度
        '''
        self.embedded_chars_expended = tf.expand_dims(self.embedded_chars, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
                conv = tf.nn.conv2d(
                        self.embedded_chars_expended,
                        W,
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="conv")
                # Apply nonlinearity
                h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(
                        h,
                        ksize=[1, sequence_length - filter_size + 1, 1, 1],
                        strides=[1, 1, 1, 1],
                        padding="VALID",
                        name="pool")
                pooled_outputs.append(pooled)

        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool = tf.concat(pooled_outputs, 3)
        self.h_pool_flat = tf.reshape(self.h_pool, [-1, num_filters_total])
        epsilon = 1e-3
        with tf.name_scope("dropout"):
            self.h_drop = tf.nn.dropout(self.h_pool_flat, self.dropout_keep_prob)

        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)#用于计算损失函数
            l2_loss += tf.nn.l2_loss(b)
            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")
        #用于计算损失函数
        with tf.name_scope("loss"):
            self.loss = tf.reduce_mean(tf.square(self.scores - self.input_y)) + l2_reg_lambda * l2_loss
