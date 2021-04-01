#!encoding=utf-8

import tensorflow as tf
filename_queue = tf.train.string_input_producer([tfrecords_filename])

