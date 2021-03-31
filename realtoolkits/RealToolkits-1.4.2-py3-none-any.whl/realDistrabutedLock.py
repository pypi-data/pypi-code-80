# -*- coding: UTF-8 -*-

"""
Real He的分布式锁，基于Redis
"""
import time
import redis
import uuid
from hashlib import md5


class RealDLock(object):
    """
    """
    # region 类成员
    __name_space = md5('RealDLock_name_space'.encode('ASCII')).hexdigest()
    __acquire_script = """
        -- KEYS: 锁的KEY，阻塞队列的KEY，消息通道的KEY，消息通道的KEY 
        -- ARGV: 锁的占位ID，锁的超时时间，是否阻塞抢（1、0），当前时间戳，过期时长（秒）
        -- 成功：1
        --       2 （递归） 
        -- 失败：0 
        -- ------------------------------------------------- 
        local set_stat = false
        if tonumber(ARGV[2]) == 0 then
            -- 如果不指定锁的超时时间
            set_stat = redis.call("set", KEYS[1], ARGV[1], 'NX')
        else
            -- 如果指定了锁的超时时间
            set_stat = redis.call("set", KEYS[1], ARGV[1], 'EX', ARGV[2], 'NX')
        end
        if set_stat then 
            -- 抢到锁
            -- 清空信号队列
            redis.call("del", KEYS[3])
            -- 不管自己在不在阻塞列表，都尝试把自己从阻塞列表中移除
            redis.call("hdel", KEYS[2], ARGV[1]) 
            -- 维护阻塞列表，清除时间过长的条目
            local expired = {}
            local all_waiting = redis.call("hgetall", KEYS[2])
            local tmp_key = ""
            local exp_idx = 1
            for i, v in ipairs(all_waiting) do
                if (i % 2 == 0) and (tonumber(v) - tonumber(ARGV[4]) > tonumber(ARGV[5])) then
                    expired[exp_idx] = tmp_key
                    exp_idx = exp_idx + 1
                else
                    tmp_key = v
                end
            end
            for i, v in ipairs(expired) do
                redis.call("hdel", KEYS[2], v) 
            end
            -- 返回抢锁成功
            return 1 
        else 
            -- 没抢到锁
            if tonumber(ARGV[3]) == 0 then
                -- 不阻塞抢，直接返回失败 
                return 0 
            end 
            if redis.call("get", KEYS[1]) == ARGV[1] then
                -- 递归锁，视作成功，但不刷新超时时间  
                return 2 
            end 
            -- 需要阻塞抢锁，把自己放入阻塞队列 
            redis.call("hset", KEYS[2], ARGV[1], ARGV[4]) 
            -- 然后再返回失败
            return 0 
        end 
        """  # 抢占锁的原子操作lua脚本
    __release_script = """
        -- KEYS: 锁的KEY，阻塞队列的KEY，消息通道的KEY 
        -- ARGV: 锁的占位ID 
        -- 成功：1
        -- 失败：0
        -- -------------------------------------------------
        -- 不管自己有没有占用，先把自己从阻塞列表中清出去
        redis.call("hdel", KEYS[2], ARGV[1]) 
        -- 读取当前谁占有此锁
        local tmp_value = redis.call("get", KEYS[1]) 
        if not tmp_value then
            -- 锁没有被占用，视作"释放成功" 
            return 1 
        end 
        if tmp_value == ARGV[1] then
            -- 如果是自己占用，释放它 
            redis.call("del",KEYS[1])
            -- 如果有还在抢锁的正在阻塞，发射锁已释放消息 
            if tonumber(redis.call("hlen", KEYS[2])) > 0 then 
                redis.call("rpush", KEYS[3], "u") 
            end
            -- 释放成功
            return 1
        else 
            -- 别人占用，释放失败
            return 0 
        end
        """  # 删除锁的原子操作lua脚本
    __query_script = """
        -- KEYS: 锁的KEY，阻塞队列的KEY，消息通道的KEY 
        -- ARGV: 
        -- 成功：1
        --       2 （递归） 
        -- 失败：0 
        -- ------------------------------------------------- 
        -- 查询当前上锁者
        local owner = redis.call("get",KEYS[1]) 
        if not owner then
            owner = "None"
        end 
        -- 查询锁当前剩余时间
        local ttl = tostring(redis.call("ttl",KEYS[1]))
        -- 查询阻塞列表长度
        local block_set_len = tostring(redis.call("hlen",KEYS[2]))
        -- 查询信号队列的长度
        local signal_list_len = tostring(redis.call("llen",KEYS[3]))
        return owner.."^||^"..ttl.."^||^"..block_set_len.."^||^"..signal_list_len
        """  # 查询锁信息的原子操作lua脚本
    # endregion

    # region 重写
    def __init__(self,
                 lock_name: str,
                 host: str,
                 timeout: (int, type(None)) = 0,
                 block: bool = False,
                 timeout_b: (int, type(None)) = 0,
                 port: int = 6379,
                 db: int = 0,
                 password: (str, type(None)) = None,
                 use_in_folk: bool = False):
        """
        初始化一个分布式锁
        如果 use_in_folk 为 True，则锁实例在超出生存期被del时不会自动释放对应的锁
        :param lock_name: 锁名称
        :param timeout: 锁超时时间(秒)，默认为None不超时（必须主动释放），无效类型或者不大于0视作None
        :param block: 是否阻塞争抢
        :param timeout_b: 阻塞抢锁超时时间(秒)，默认为None不超时（一直阻塞），无效类型或者不大于0视作None
        :param host: 承载锁的redis服务器地址
        :param port: 承载锁的redis服务器端口
        :param db: 承载锁的redis数据库序号
        :param password: 承载锁的redis服务器密码
        """
        # todo: 缺少对参数合法性的检测
        super(RealDLock, self).__init__()
        self.__conn = redis.StrictRedis(host=host,
                                        port=port,
                                        db=db,
                                        password=password,
                                        charset="utf-8",
                                        decode_responses=True)  # 访问redis的连接
        self.__name = lock_name  # 锁名称
        self.__lock_key = f'RealDLock_{lock_name}_' + self.__name_space  # 锁在redis中的存储键名
        self.__lock_value = str(uuid.uuid1())  # 当前锁实例的唯一ID
        self.__signal_list_name = f'RealDLock_{lock_name}_signal_list_' + self.__name_space  # 解锁信号队列名称
        self.__block_set_name = f'RealDLock_{lock_name}_block_count_' + self.__name_space  # 阻塞列表名称
        self.__timeout = timeout if isinstance(timeout, int) and timeout > 0 else 0  # 锁超时时限
        self.__block = block  # 是否阻塞抢锁
        self.__timeout_b = timeout_b if isinstance(timeout_b, int) and timeout_b > 0 else 0  # 抢锁阻塞时限
        self.__acquirer = self.__conn.register_script(self.__acquire_script)  # 注册争抢锁的脚本
        self.__releaser = self.__conn.register_script(self.__release_script)  # 注册释放锁的脚本
        self.__querier = self.__conn.register_script(self.__query_script)  # 注册释放锁的脚本
        self.__use_in_folk = use_in_folk  # 锁实例是否使用在进程folk的场景
        return

    def __enter__(self):
        """
        用于with上下文尝试抢锁
        :return:
            抢锁成功  锁实例自身
            抢锁失败  None
        """
        if not self.acquire_lock():
            raise Exception("acquire_lock failed")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        用于with上下文自动释放分布锁
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.release_lock()
        return True

    def __del__(self):
        """
        在不涉及"进程folk"的场景下，如果锁实例超出了生存期，理应释放自己拥有的锁
        :return:
        """
        if not self.__use_in_folk:
            self.release_lock()
        return

    # endregion

    # region 属性
    @property
    def name(self) -> str:
        return self.__name

    @property
    def uid(self) -> str:
        return self.__lock_value

    @property
    def timeout(self) -> int:
        return self.__timeout

    @property
    def block(self) -> bool:
        return self.__block

    @property
    def block_timeout(self) -> int:
        return self.__timeout_b
    # endregion

    # region 成员方法
    def acquire_lock(self) -> bool:
        """
        争抢分布锁
        如果锁实例初始化时指定了block为True，则此函数可能导致阻塞
        :return: 争抢结果
            成功  True
            失败  False
        """
        start_stramp = time.time()  # 获取开始抢锁的起始时间戳
        # 开始抢，直到成功或超时
        need_block = 1 if self.__block else 0
        curr_time = int(time.time())
        keys = [self.__lock_key, self.__block_set_name, self.__signal_list_name]
        args = [self.__lock_value, self.__timeout, need_block, curr_time, 7200]
        while True:
            # 调用lua脚本抢锁
            if self.__acquirer(keys=keys, args=args) > 0:
                # 抢到
                return True
            if not self.__block:
                # 不需要阻塞着抢，退出争抢循环
                break
            # 需要阻塞着一直抢，直到抢到或超时
            block_pttl = self.__timeout_b - (time.time() - start_stramp)  # 获取阻塞抢锁的剩余阻塞时间
            if block_pttl <= 0:
                # 所有阻塞时间都用完了，不再抢了
                break
            block_ttl = int(-(-block_pttl//1))
            lock_pttl = self.__conn.pttl(self.__lock_key)  # 获取当前锁的剩余时间
            lock_ttl = int(-((-lock_pttl/1000)//1))
            if lock_pttl > 0:
                # 等待 当前锁失效 vs 阻塞超时 中较早的那个时间
                self.__conn.blpop(self.__signal_list_name, timeout=min(block_ttl, lock_ttl))
                # 然后开始下一个循环抢
        # 没抢到
        return False

    def release_lock(self) -> bool:
        """
        释放分布锁
        只能释放自己抢占的锁
        :return: 释放结果
            释放成功  True
            释放失败  False （比如尝试释放非自己抢占的锁）
        """
        # 调用lua脚本释放锁
        keys = [self.__lock_key, self.__block_set_name, self.__signal_list_name]
        args = [self.__lock_value]
        return False if self.__releaser(keys=keys, args=args) == 0 else True

    def own_lock(self):
        """
        检测分布锁是否是被自己抢占
        :return:
            是  True
            否  False
        """
        return self.__lock_value == self.__conn.get(self.__lock_key)

    def in_locking(self):
        """
        检查当前锁释放在上锁状态（不管是不是自己锁的）
        :return:
            上锁    True
            未上锁  False
        """
        if self.__conn.get(self.__lock_key) is None:
            return False
        return True

    def lock_stat(self):
        """
        查询该分布式锁当前的状态
        :return:
            成功  结果list，[上锁者, 剩余时间, 阻塞列表长度, 信号队列长度]
            失败  None
        """
        keys = [self.__lock_key, self.__block_set_name, self.__signal_list_name]
        qry_back = self.__querier(keys=keys)
        if not isinstance(qry_back, str):
            return None
        return qry_back.split('^||^')
    # endregion
