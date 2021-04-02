import hashlib
import os

from cryptography.fernet import Fernet
from notetool.database import SqliteTable
from notetool.tool.log import log

local_secret_path = '~/.secret'
logger = log('tool')


def set_secret_path(path):
    global local_secret_path
    local_secret_path = path


def get_file_md5(path, chunk=1024 * 4):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            m.update(data)

    return m.hexdigest()


class SecretManage(SqliteTable):
    def __init__(self, secret_dir=None, cipher_key=None, *args, **kwargs):
        secret_dir = secret_dir or local_secret_path
        secret_dir = secret_dir.replace("~", os.environ['HOME'])
        secret_path = '{}/.secret.db'.format(secret_dir)

        super(SecretManage, self).__init__(
            secret_path, table_name='secret', *args, **kwargs)
        self.columns = ['secret_key', 'cate1', 'cate2',
                        'cate3', 'cate4', 'cate5', 'value']
        self.cipher_key = cipher_key
        self.create()

    def create(self):
        self.execute("""
                        create table if not exists {} (
                            secret_key            varchar(300)   primary key
                           ,cate1                 varchar(150)   DEFAULT ('')
                           ,cate2                 varchar(150)   DEFAULT ('')
                           ,cate3                 varchar(150)   DEFAULT ('')
                           ,cate4                 varchar(150)   DEFAULT ('')
                           ,cate5                 varchar(150)   DEFAULT ('')                                 
                           ,value                 varchar(1000)  DEFAULT ('')
                           )
                        """.format(self.table_name))

    def encrypt(self, text):
        if self.cipher_key is None:
            return text
        cipher = Fernet(bytes(self.cipher_key, encoding="utf8"))
        encrypted_text = cipher.encrypt(text.encode())
        return encrypted_text

    def decrypt(self, encrypted_text):
        if self.cipher_key is None:
            return encrypted_text
        cipher = Fernet(bytes(self.cipher_key, encoding="utf8"))
        decrypted_text = cipher.decrypt(encrypted_text)
        return decrypted_text.decode()

    def read(self, cate1, cate2=None, cate3=None, cate4=None, cate5=None, value=None, save=True, secret=False):
        if save:
            self.write(value, cate1, cate2, cate3, cate4, cate5, secret=secret)
        if value is not None:
            return value

        properties = {"cate1": cate1, "cate2": cate2,
                      "cate3": cate3, "cate4": cate4, "cate5": cate5}
        sql = "select value from table_name where {}".format(
            ' and '.join(self._properties2equal(properties)))
        results = self.select(sql)
        for res in results:
            value = res[0]
            if secret:
                value = self.decrypt(value)
            return value

    def write(self, value, cate1, cate2=None, cate3=None, cate4=None, cate5=None, secret=False):
        if value is None:
            return
        if secret:
            value = self.encrypt(value)
        key = self.get_secret_key(cate1, cate2, cate3, cate4, cate5)
        properties = {
            "secret_key": key,
            "cate1": cate1, "cate2": cate2, "cate3": cate3, "cate4": cate4, "cate5": cate5, "value": value,
        }

        self.insert(properties)

    @staticmethod
    def get_secret_key(cate1, cate2=None, cate3=None, cate4=None, cate5=None):
        return "{}-{}-{}-{}-{}".format(cate1, cate2 or '', cate3 or '', cate4 or '', cate5 or '')


def get_fernet(cipher_key=None):
    """
    从本地拿取加密的key
    :param cipher_key:传入的key
    :return:
    """
    secert = SecretManage()
    if cipher_key is not None:
        secert.write(value=cipher_key, cate1='secret', cate2='cipher_key')
    else:
        cipher_key = secert.read(cate1='secret', cate2='cipher_key')
        if cipher_key is None:
            cipher_key = str(Fernet.generate_key(), encoding="utf-8")
            secert.write(value=cipher_key, cate1='secret', cate2='cipher_key')
    return cipher_key


def encrypt(text, cipher_key=None):
    if cipher_key is None:
        cipher_key = get_fernet(cipher_key)
    cipher_key = bytes(cipher_key, encoding="utf8")
    cipher = Fernet(cipher_key)
    encrypted_text = cipher.encrypt(text.encode())

    return encrypted_text


def decrypt(encrypted_text, cipher_key=None):
    if cipher_key is None:
        cipher_key = get_fernet(cipher_key)
    cipher_key = bytes(cipher_key, encoding="utf8")
    cipher = Fernet(cipher_key)
    decrypted_text = cipher.decrypt(encrypted_text)

    return decrypted_text.decode()


def read_secret(cate1, cate2=None, cate3=None, cate4=None, cate5=None, value=None, save=True, secret=False):
    value = SecretManage().read(cate1=cate1, cate2=cate2, cate3=cate3, cate4=cate4, cate5=cate5, value=value, save=save,
                                secret=secret)
    return value


def write_secret(value, cate1, cate2=None, cate3=None, cate4=None, cate5=None, secret=False):
    SecretManage().write(value=value, cate1=cate1, cate2=cate2,
                         cate3=cate3, cate4=cate4, cate5=cate5, secret=secret)
