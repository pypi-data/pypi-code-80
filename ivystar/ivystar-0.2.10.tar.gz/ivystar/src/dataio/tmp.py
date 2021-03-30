from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import subprocess

from pyarrow.parquet import ParquetDataSet
import pyarrow.parquet as pq
import pyarrow as pa
from libraries.hive_metastore.ThriftHiveMetastore import Client


def connect_hive() -> Client:
    """
    通过thrift连接hive metastore服务端
    """
    transport = TSocket.TSocket(host, int(port))
    transport = TTransport.TBufferedTransport(transport)
    transport.open()
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    return ThriftHiveMetastore.Client(protocol)

def write_table(client: Client, database: str, table: str, dataframe: DataFrame, partitions: list = None):
    """
    提供给用户将dataFrame写入hive表中的方式

    Examples:
        client = connect_hive(host, port)
         df = pd.DataFrame({
            'index': [1, 2, 3],
            'name': ['xiaoming', 'xiaowang', 'xiaozhang'],
            'prt_dt': ['2020', '2019', '2020']
        })

        partition_cols = ['prt_dt']
        write_table(client, database, table, df, partition_cols)
    
    Args:
    client(Client):hive客户端，通过thrift协议访问hive metastore
    database(str):数据库
    table(str):表名
    dataframe(pandas.DataFrame):pandas.DataFrame
    partitions(list):分区信息

    raise:
        HiveDatabaseNOTEXIST:Hive库不存在时抛出异常
        HiveTableNOTEXIST:Hive表不存在时抛出异常

    """
    # 1、连接hive服务端
    client = connect_hive(host, port)

    # 2、检查数据库是否存在，如果不存在则抛出异常
    databases = client.get_all_databases()
    if database not in databases:
        raise HiveDatabaseNOTEXIST('Hive database is not exist.')

    # 3、创建hive表，如果表名重复则抛出异常
    tables = client.get_all_tables(database)
    if table not in tables:
        raise HiveTableNOTEXIST('Hive table is not exist.')

    # 4、将pandas中字段int64类型转为int
    columns = dataframe.columns
    int64_fields = {}
    float64_fields = {}
    for field in columns:
        if pd.api.types.is_int64_dtype(dataframe[field]):
            int64_fields[field] = 'int32'

        if pd.api.types.is_float_dtype(dataframe[field]):
            float64_fields[field] = 'float32'
    transfer_fields = dict(int64_fields, **float64_fields)
    transfer_df = dataframe.astype(transfer_fields)

    # 5、将dataframe写入hive表中
    table_hdfs_path = client.get_table(database, table).sd.location
    table = pa.Table.from_pandas(transfer_df)
    pq.write_to_dataset(
        table=table, root_path=table_hdfs_path, partition_cols=partitions)

    # 6、写入分区表时需刷新元数据信息(msck repair table ***)
    shell = "hive -e 'msck repair table {}' ".format('train_data.telecom_train')
    subprocess.Popen(shell,shell=True)

def read_table(data_source: DataSource, database: str, table: str, partitions: list = None) -> DataFrame:
    """
    提供给用户根据hive库名和表名访问数据的方式-->dataframe（thrift、urllib、pyarrow、pyhdfs）

   Examples:
        client = connect_hive(host, port)
        read_table(client,'test','test')

    Args:
        client(Client):hive客户端，通过thrift协议访问hive metastore
        database(str):hive库名
        table(str):hive表名
        partitions(list):hive表分区（用户需按照分区目录填写）,如果查询所有数据，则无需填写分区

    Return:
        pandas.dataframe
    """
    # 1、连接hive服务端
    client = connect_hive(host, port)

    # 2、查询hive表元数据
    table = client.get_table(database, table)
    table_hdfs_path = table.sd.location

    logging.info('table_hdfs_path:' + table_hdfs_path)
    print(table_hdfs_path)

    # 3、判断hive是否为分区表,当用户没有输入partitions时需查找所有分区数据
    if partitions is not None:
        table_hdfs_path = [
            table_hdfs_path + constant.FILE_SEPARATION + x for x in partitions][0]
        dataframe = pq.ParquetDataset(
            table_hdfs_path).read().to_pandas()
        # pyarrow访问分区目录时，dataframe不含分区列，因此需添加分区列信息
        for partition in partitions:
            index = partition.find('=')
            field = partition[:index]
            field_value = partition[index + 1:]
            dataframe[field] = field_value
    else:
        dataframe = pq.ParquetDataset(
            table_hdfs_path).read().to_pandas()
    return dataframe
