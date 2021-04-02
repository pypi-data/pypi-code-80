from redis import ConnectionPool, StrictRedis


class ExecRedisClients:
    def __init__(self, configs: dict, *args):
        """
        configs = dict('redis_clients_name_1': ip1, 'redis_clients_name_2': ip2...)
        args = dict('name'=redis_clients_name, 'db'=redis_db_num, **kwargs)
        """
        self.redis_config = args
        self.config = configs

    def __getitem__(self, client_name) -> StrictRedis:
        return self.clients[client_name]

    @property
    def clients(self):
        return {i['name']: StrictRedis(
            connection_pool=ConnectionPool(host=self.config[i.pop('name')], db=i.pop('db', 0)),
            decode_responses=True, **i) for i in self.redis_config}
