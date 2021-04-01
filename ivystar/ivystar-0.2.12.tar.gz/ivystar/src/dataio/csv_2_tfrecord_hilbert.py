#!encoding=utf-8

'''
1. 将csv文件保存为tfrecord文件,供后续的应用.
2. tfrecord支持并发,面元分割,切片等操作, 应用成本更低,效率更高,且易于版本管理.
3. 作为代价,转换以后的数据,会增加5倍的体积
4. 针对不同的数据集结构需要修改文件再转换
'''

import pandas as pd
import tensorflow as tf
print(tf.__version__) # 打印tf版本

input_csv_file = "./csv_data/hilbert/test_data.csv" # 下载hilbert数据集,并保存与本地
output_tfrecord_file = "./csv_data/hilbert/test_data.tfrecords" # 定义输出数据集

hilbert_frame = pd.read_csv(input_csv_file,sep=',') # 读取hilbert数据集

row_count = hilbert_frame.shape[0]
col_count = hilbert_frame.shape[1]
print(row_count, col_count) # 打印数据集的尺寸

with tf.io.TFRecordWriter(output_tfrecord_file) as writer:
    for i in range(row_count):
        example = tf.train.Example(
            features=tf.train.Features(
                feature={
                    "x": tf.train.Feature(float_list=tf.train.FloatList(value=[hilbert_frame.iloc[i,0]])),
                    "y": tf.train.Feature(float_list=tf.train.FloatList(value=[hilbert_frame.iloc[i,1]])),
                }
            )
        )
        writer.write(record=example.SerializeToString())
    writer.close()

