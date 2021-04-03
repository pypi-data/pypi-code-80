#! -*- coding: utf-8 -*-
# 测试代码可用性: 结合MLM的Gibbs采样

from tqdm import tqdm
import numpy as np
from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import to_array

config_path = '/home/xiaoguzai/下载/chinese_L-12_H-768_A-12/bert_config.json'
checkpoint_path = '/home/xiaoguzai/下载/chinese_L-12_H-768_A-12/bert_model.ckpt'
dict_path = '/home/xiaoguzai/下载/chinese_L-12_H-768_A-12/vocab.txt'

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_transformer_model(
    config_path=config_path, checkpoint_path=checkpoint_path, with_mlm=True
)  # 建立模型，加载权重

sentences = []
#init_sent = u'科学技术是第一生产力。'  # 给定句子或者None
init_sent = None
minlen, maxlen = 8, 32
steps = 10000
converged_steps = 1000
vocab_size = tokenizer._vocab_size
#vocab_size = 21128

if init_sent is None:
    length = np.random.randint(minlen, maxlen + 1)
    print('length = ')
    print(length)
    #length = 30
    tokens = ['[CLS]'] + ['[MASK]'] * length + ['[SEP]']
    token_ids = tokenizer.tokens_to_ids(tokens)
    print('token_ids = ')
    print(token_ids)
    #token_ids = [101,103,103,...,102]
    segment_ids = [0] * len(token_ids)
    #segment_ids = [0,0,0,...,0]
    print('segment_ids = ')
    print(segment_ids)
else:
    token_ids, segment_ids = tokenizer.encode(init_sent)
    length = len(token_ids) - 2
    print('###token_ids = ')
    print(token_ids)
    print('###segment_ids = ')
    print(segment_ids)
    #token_ids = [101,4906,2110,...102]
    #segment_ids = [0,0,0,...0]
print('tokenizer._token_mask_id = ')
print(tokenizer._token_mask_id)
#tokenizer._token_mask_id = 103
print('***length = ')
print(length)
#如果之前的init_sent为None的情况，则这里随便选择内容进行替换
#使用全部的mask之后，就偏向于本身预训练中高频出现的文本
for _ in tqdm(range(steps), desc='Sampling'):
    # Gibbs采样流程：随机mask掉一个token，然后通过MLM模型重新采样这个token。
    #steps = 10000，这样构造相应的10000次
    i = np.random.choice(length) + 1
    #i = 1
    token_ids[i] = tokenizer._token_mask_id
    #token_ids = [101,4906,2110,2825,3318,3221,5018,671,4495,772,1213,511,102]
    probas = model.predict(to_array([token_ids], [segment_ids]))[0, i]
    print('!!!probas = ')
    print(np.array(probas).shape)
    #输出的probas = (21128,)
    #probas = [5.8375575e-15 9.1522571e-15 7.6063245e-15 ... 4.3807121e-14 3.9159718e-13 1.1422677e-13]
    #使用bert模型计算出每一个句子对应的概率内容
    token = np.random.choice(vocab_size, p=probas)
    #从概率内容中选取一个补充上去
    #mask掉之后输出probas = (21128,)，可以视为与这个句子(准确地说是与句子之中[MASK]掉部分)
    #的概率内容
    token_ids[i] = token
    print('###token_ids = ')
    print(token_ids)
    #token_ids = [101,4906,2110,2825,3318,3221,5018,671,4495,772,1213,511,102]
    sentences.append(tokenizer.decode(token_ids))
    #sengtences = ['科学技术是第一生产力']
print('converged_steps = ')
print(converged_steps)
#converged_steops = 1000
print('###sentences = ')
print(sentences)
print(u'部分随机采样结果：')
for _ in range(10):
    #print(np.random.choice(sentences[converged_steps:]))
    print(np.random.choice(sentences[:]))