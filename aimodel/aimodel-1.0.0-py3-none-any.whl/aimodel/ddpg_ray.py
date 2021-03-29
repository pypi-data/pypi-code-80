#########
import tensorflow as tf
from .Config import Config
import numpy as np
import os
import ray
import ray.experimental.tf_utils as tf_utils
import aiclient as client
import random
import traceback
import time

config = Config()
action_dim = config.action_dim
state_dim = config.state_dim
action_bound = config.action_bound
lstm_max_timestep = config.lstm_max_timestep

# all placeholder for tf
  



###############################  Actor  ####################################
class Actor(object):
    def __init__(self, sess, action_dim, action_bound, learning_rate, replacement, S, S_multi, S1_multi, is_training):
        self.sess = sess
        self.a_dim = action_dim
        self.action_bound = action_bound
        self.global_step = tf.Variable(0, trainable=False)
        self.lr = tf.train.exponential_decay(learning_rate=learning_rate, global_step=self.global_step, decay_steps=100, decay_rate=0.99, staircase=False)
        self.replacement = replacement
        self.t_replace_counter = 0  
        self.S = S
        self.S_multi = S_multi
        self.S1_multi = S1_multi
        self.is_training = is_training
        

        
        with tf.variable_scope('Actor'):
            # input s, output a
            self.a = self._build_net(self.S_multi, scope='eval_net', trainable=True, training=self.is_training)

            # input s_, output a, get a_ for critic
            self.a_ = self._build_net(self.S1_multi, scope='target_net', trainable=False, training=False)

            self.e_params = [i for i in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/eval_net') if 'moving' not in i.name]
            self.t_params = [i for i in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Actor/target_net') if 'moving' not in i.name]
            for param in self.e_params:
                tf.summary.histogram(param.name, param)
                tf.summary.scalar(param.name, tf.reduce_sum(param))


        if self.replacement['name'] == 'hard':
            self.t_replace_counter = 0
            self.hard_replace = [tf.assign(t, e) for t, e in zip(self.t_params, self.e_params)]
        else:
            self.soft_replace = [tf.assign(t, (1 - self.replacement['tau']) * t + self.replacement['tau'] * e)
                                 for t, e in zip(self.t_params, self.e_params)]
        tf.summary.scalar('learning_rate', self.lr)
        tf.summary.scalar('global_step', self.global_step)

    def _build_net(self, s, scope, trainable, training):
        with tf.variable_scope(scope):
#             init_w = tf.random_normal_initializer(0., 0.2)
#             init_b = tf.constant_initializer(0.1)
            init_w = tf.variance_scaling_initializer()
            init_b = tf.variance_scaling_initializer()
        
            net1 = tf.layers.dense(s, 4096,kernel_initializer=init_w, bias_initializer=init_b, name='layer1', trainable=trainable)
            norm_net1 = tf.nn.leaky_relu(tf.layers.batch_normalization(net1, trainable=trainable, training=training))
#             norm_net1 = tf.nn.leaky_relu(net1)
            net2 = tf.layers.dense(norm_net1, 8192, kernel_initializer=init_w, bias_initializer=init_b, name='layer2', trainable=trainable)
#             norm_net2 = tf.nn.leaky_relu(net2)
            norm_net2 = tf.nn.leaky_relu(tf.layers.batch_normalization(net2, trainable=trainable, training=training))
            net = tf.layers.dense(norm_net2, 1024, kernel_initializer=init_w, bias_initializer=init_b, name='layer3', trainable=trainable)
            norm_net = tf.nn.leaky_relu(tf.layers.batch_normalization(net, trainable=trainable, training=training))
#             norm_net = tf.nn.leaky_relu(net)
            lstm_cell = tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=2048, state_is_tuple=True)
            outputs, last_states = tf.compat.v1.nn.dynamic_rnn(cell=lstm_cell, dtype=tf.float32, inputs=norm_net)
            mean_states = tf.reduce_mean(outputs, reduction_indices=1)



            button = tf.layers.dense(mean_states, 7, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='button', trainable=trainable)
            move = tf.layers.dense(mean_states, 10, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='move', trainable=trainable)
            enemy = tf.layers.dense(mean_states, 3, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='enemy', trainable=trainable)
            pitch = tf.layers.dense(mean_states, 1, kernel_initializer=init_w,
                                          bias_initializer=init_b, name='pitch', trainable=trainable)
            move = tf.nn.softmax(tf.layers.batch_normalization(move, trainable=trainable, training=training))
            enemy = tf.nn.softmax(tf.layers.batch_normalization(enemy, trainable=trainable, training=training))
            button = tf.nn.softmax(tf.layers.batch_normalization(button, trainable=trainable, training=training))
            pitch = tf.nn.tanh(tf.layers.batch_normalization(pitch, trainable=trainable, training=training))
            
#             move = tf.nn.softmax(move)
#             enemy = tf.nn.softmax(enemy)
#             button = tf.nn.softmax(button)
#             pitch = tf.nn.tanh(pitch)
            action = tf.concat([move, enemy, button, pitch], axis=1, name='action')
        return action

    def learn(self, s_multi, s):   # batch update
        self.sess.run(self.train_op, feed_dict={self.S_multi: s_multi, self.S: s, self.is_training:True})

        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replace)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_a'] == 0:
                self.sess.run(self.hard_replace)
            self.t_replace_counter += 1

    def choose_action(self, s_multi):
        s = s_multi[-1, -1, :]    # single state
        a = self.sess.run(self.a, feed_dict={self.S_multi: s_multi, self.is_training:False})[0]
        # ############### 对move进行掩盖
        move_rate = a[:10]
#         print('掩盖前', move_rate)
        # 对不能通行的方向进行掩盖
        move_rate[np.hstack([s[29:37], np.array([1]*2)])==-2]=0
        move_sum = move_rate[:8].sum()
        if move_sum == 0 :
            temp = np.random.randint(5, size=10)
            move_rate = temp/temp.sum()
        else:
            move_rate = move_rate/move_rate.sum()
        a[:10] = move_rate
#         print('掩盖后', move_rate)
        # ############### 对enemy进行掩盖
        enemy_rate = a[10:13]
#         print('掩盖前', enemy_rate)
        if s[40:43].sum() != 0:
            enemy_rate[s[40:43]==False] = 0
            if enemy_rate.sum()==0:
                enemy_rate[s_t[40:43]==True] = 1
            enemy_rate = enemy_rate/enemy_rate.sum()
            a[10: 13] = enemy_rate
#         print('掩盖后', enemy_rate)
        # ############### 对button进行掩盖
        button_rate = a[13:20].copy()
        button_rate[np.array([1, s[5], s[9], 1, 1, 1, 1])==0] = 0
        if button_rate.sum()!=0:
            a[13:20] = button_rate/button_rate.sum()
        return  a # single action

    def add_grad_to_graph(self, a_grads):
        with tf.variable_scope('A_train'):
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            opt = tf.train.AdamOptimizer(self.lr)  # (- learning rate) for ascent policy
            
            with tf.control_dependencies(update_ops):
                self.policy_grads = tf.gradients(ys=self.a, xs=self.e_params, grad_ys=-a_grads)
                for i, v in enumerate(self.policy_grads):
                      if v is not None:
#                             self.policy_grads[i] = tf.clip_by_norm(v, 0.5) # clip gradients
                            tf.summary.histogram(v.name, v)
                self.train_op = opt.apply_gradients(zip(self.policy_grads, self.e_params),self.global_step)


###############################  Critic  ####################################

class Critic(object):
    def __init__(self, sess, state_dim, action_dim, learning_rate, gamma, replacement, a, a_, S, S1, R, S_multi, S1_multi, is_training):
        self.sess = sess
        self.s_dim = state_dim
        self.a_dim = action_dim
        self.lr = learning_rate
        self.gamma = gamma
        self.replacement = replacement
        self.log_all = []
        self.S = S
        self.S1 = S1
        self.R = R
        self.S_multi = S_multi
        self.S1_multi = S1_multi
        self.is_training = is_training


        with tf.variable_scope('Critic'):
            # Input (s, a), output q
            self.a = a
            self.q = self._build_net(self.S, self.a, 'eval_net', trainable=True)

            # Input (s_, a_), output q_ for q_target
            self.q_ = self._build_net(self.S1, a_, 'target_net', trainable=False)    # target_q is based on a_ from Actor's target_net

            self.e_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/eval_net')
            self.t_params = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='Critic/target_net')
            for param in self.e_params:
                tf.summary.histogram(param.name, param)
                tf.summary.scalar(param.name, tf.reduce_sum(param))
                
        with tf.variable_scope('target_q'):
            self.target_q = R + self.gamma * self.q_


        with tf.variable_scope('TD_error'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.target_q, self.q))
            critic_loss = tf.summary.scalar('critic_loss', self.loss)
            dq = tf.gradients(self.loss, self.q)
            tf.summary.histogram('critic_dq', dq)
            grads = tf.gradients(self.loss, self.e_params)
            for grad in grads:
                tf.summary.histogram(grad.name, grad)

        with tf.variable_scope('C_train'):
            self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

        with tf.variable_scope('a_grad'):
            self.a_grads = tf.gradients(self.q, a)[0]   # tensor of gradients of each sample (None, a_dim)
            tf.summary.histogram('a_grad', self.a_grads)

        if self.replacement['name'] == 'hard':
            self.t_replace_counter = 0
            self.hard_replacement = [tf.assign(t, e) for t, e in zip(self.t_params, self.e_params)]
        else:
            self.soft_replacement = [tf.assign(t, (1 - self.replacement['tau']) * t + self.replacement['tau'] * e)
                                     for t, e in zip(self.t_params, self.e_params)]


    def _build_net(self, s, a, scope, trainable):
        with tf.variable_scope(scope):
            init_w = tf.random_normal_initializer(0., 0.1)
            init_b = tf.constant_initializer(0.1)
            

            # 隐藏层第一层：多输入层
            n_l1 = 1024
            w1_s = tf.get_variable('w1_s', [self.s_dim, n_l1], initializer=init_w, trainable=trainable)
            w1_a = tf.get_variable('w1_a', [self.a_dim, n_l1], initializer=init_w, trainable=trainable)
            b1 = tf.get_variable('b1', [1, n_l1], initializer=init_b, trainable=trainable)
            net = tf.nn.relu(tf.matmul(s, w1_s) + tf.matmul(a, w1_a) + b1)


            # 隐藏层第二层：输出q值
            q = tf.layers.dense(net, 1, kernel_initializer=init_w, bias_initializer=init_b, trainable=trainable, name='h2')   # Q(s,a)
        return q

    def learn(self, s, a, r, s1, s_multi, s1_multi):
        self.sess.run(self.train_op, feed_dict={self.S: s, self.a: a, self.R: r, self.S1: s1, self.S_multi: s_multi, self.S1_multi: s1_multi, self.is_training:True})
        if self.replacement['name'] == 'soft':
            self.sess.run(self.soft_replacement)
        else:
            if self.t_replace_counter % self.replacement['rep_iter_c'] == 0:
                self.sess.run(self.hard_replacement)
            self.t_replace_counter += 1
            
            
class Model(object):
    def __init__(self, action_dim, action_bound, LR_A, REPLACEMENT, state_dim, LR_C, GAMMA, storageType, use_gpu, init_model_file=None):
        # 初始化client
        players = [{},{}]
        modelDirPath = '/'.join(str(init_model_file).split('/')[:-1])
        client.init(players, kafkaBrokers='hdp101.jg.6ght.com:9093', storageType=storageType, modelDirPath=modelDirPath)
        self.client = client
        if init_model_file:
            self.client.initModel()
        
        # all placeholder for tf
        with tf.name_scope('S'):
            S = tf.compat.v1.placeholder(shape=(None, state_dim), dtype = tf.float32, name='s')
        with tf.name_scope('R'):
            R = tf.compat.v1.placeholder(tf.float32, [None, 1], name='r')
        with tf.name_scope('S1'):
            S1 = tf.compat.v1.placeholder(tf.float32, shape=[None, state_dim], name='s1')  
        with tf.name_scope('S_multi'):
            S_multi = tf.compat.v1.placeholder(shape=(None, lstm_max_timestep, state_dim), dtype = tf.float32, name='s_multi')
        with tf.name_scope('S1_multi'):
            S1_multi = tf.compat.v1.placeholder(tf.float32, shape=(None, lstm_max_timestep, state_dim), name='s1_multi')
        is_training = tf.compat.v1.placeholder(tf.bool, name='is_training')
        if use_gpu:
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            self.sess = tf.compat.v1.Session(config=config)
        else:
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
            self.sess = tf.compat.v1.Session()
        self.actor = Actor(self.sess, action_dim, action_bound, LR_A, REPLACEMENT, S, S_multi, S1_multi, is_training)
        self.critic = Critic(self.sess, state_dim, action_dim, LR_C, GAMMA, REPLACEMENT, self.actor.a, self.actor.a_, S, S1, R, S_multi, S1_multi, is_training)
        self.actor.add_grad_to_graph(self.critic.a_grads)
        self.saver = tf.train.Saver()
        if not init_model_file:
            self.sess.run(tf.global_variables_initializer()) 
        else:
            self.saver.restore(self.sess, init_model_file)
        self.variables = tf_utils.TensorFlowVariables(self.critic.loss, self.sess)
#         self.target_init = tf.group([tf.assign(v_targ, v_main)
#                                      for v_main, v_targ in zip(get_vars('main'), get_vars('target'))])
     
        
    def set_weights(self, weights):
        '''
        weights为字典形式
        '''
        self.variables.set_weights(weights)
        print('重置tf的参数变量')
#         self.sess.run(self.target_init)
        
    def get_weights(self):
        weights = self.variables.get_weights()
        return weights
    
    def train(self, BATCH_SIZE):
        s = time.time()
        for _ in range(10):
            try:
                data = self.client.readModelOutput(BATCH_SIZE)           
                batch = [line.strip('\n').split('|') for line in data]
                random.shuffle(batch)
                # 整合数据为模型可用形式
                b_s_multi_timesteps = np.array([[eval(j.split('  ')[3]) for j in i] for i in batch])
                b_s = b_s_multi_timesteps[:, -1, :]
                b_s1_multi_timesteps = np.array([[eval(j.split('  ')[6]) for j in i] for i in batch])
                b_s1 = b_s1_multi_timesteps[:, -1, :]
                b_a = np.array([[eval(j.split('  ')[4]) for j in i][-1] for i in batch])
                b_r = np.array([[eval(j.split('  ')[5]) for j in i][-1] for i in batch]).reshape(-1, 1)
                dones = np.array([[eval(j.split('  ')[7]) for j in i][-1] for i in batch])
                break
            except:
                traceback.print_exc()
                client.writeLog('|'.join([traceback.format_exc(), 'trainer']))
                continue
        print('训练数据获取完成', time.time()-s)
        # 2、更新模型
        self.critic.learn(b_s, b_a, b_r, b_s1, b_s_multi_timesteps, b_s1_multi_timesteps)
        self.actor.learn(b_s_multi_timesteps, b_s)
        print('训练完成', time.time()-s)
        
    def save_model_file(self, model_savefile, uploadModelKafka):
        self.saver.save(self.sess, model_savefile)
        print('保存模型到本地')
        if uploadModelKafka:
            print('上传模型')
            time.sleep(10)
            self.client.uploadModel(model_savepath, 2, 60)[1]
        