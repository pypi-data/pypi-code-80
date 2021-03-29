import os

class Config():
    def __init__(self):
        # aws or alluxio
        self.storageType = 'aws'
        self.initmodel = True
        
        cwd = os.getcwd()
        self.rollout_timestep = 375
        
        self.LR_C = 0.0005
        self.LR_A = 0.08 * self.LR_C
        self.GAMMA = 0.99
        self.lstm_max_timestep = 16
        self.BATCH_SIZE = 128
        self.OUTPUT_GRAPH = False
        self.REPLACEMENT = [dict(name='soft', tau=0.01), dict(name='hard', rep_iter_a=600, rep_iter_c=500)][0] 
        
        self.output = 'output.txt'
        # 射线相关
        self.train_map = 3004
        self.reward_type = 2
        self.file_os = "./EnvPercept.so"
        self.file_map = "./map_bake/" + str(self.train_map) + ".bake"
        # 模型保存路径和文件
        self.model_savepath = os.path.join(cwd, "Model/")
        self.model_best_savepath = os.path.join(cwd, "Model_best/")
        if not os.path.exists(self.model_best_savepath):
            os.mkdir(self.model_best_savepath)
        if not os.path.exists(self.model_savepath):
            os.mkdir(self.model_savepath)
        self.model_savefile = os.path.join(self.model_savepath, "model.ckpt")
        self.avg_std = 'avg_std.npy'
        self.action_dim = 21
        self.state_dim = 223
        self.action_bound = {'pitch': 3, 'yaw': 3, 'move': 9.9, 'button': 9.9, 'enemy':2.9}
        self.epsilon = 0.5
        self.action_type = 'norandom'
        self.save_replay = False
        self.add_ray = True
        self.ray_s = 29
        self.ray_e = 37
        self.AI_ID = 2
        ############## 分布式环境相关 ############
        if os.environ.get('USE_GPU'):
            self.use_gpu = os.environ.get('USE_GPU') in ['True', 'true', True]
        else:
            self.use_gpu = False
        # 训练环境是否从已有的参数resore还是通过初始化方式给参数赋值 None\model_savefile(从kafka下载数据)
#         self.init_model_file = self.model_savefile
        self.init_model_file = None
        # 每个远程worker迭代训练的次数
        self.iterations = 5
        # woker个数
        self.num_train_worker = 6
        self.MAX_EPISODES = 2
        # self.model_savepath or None
        self.uploadModelKafka = None
        
        
        
        
        
        self.players = [{
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': False
                }, {
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': True
                }, {
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': False
                }, {
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': False
                }, {
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': False
                }, {
                    'weaponId': 10003,
                    'skillId0': 0,
                    'skillId1': 5,
                    'isMLAI': False
                }]