import hdfs
import getpass


class HdfsBase:
    def __init__(self, url, root="/", timeout=1000, user=None):
        self.__hdfs_client = hdfs.InsecureClient(url, root=root, timeout=timeout, user=user)
    
    def get_client(self):
        return self.__hdfs_client

    def init_dir(self, target):
        '''
        初始化目标目录
        '''
        if self.__hdfs_client.status(target, strict=False):
            self.__hdfs_client.delete(target, recursive=True, skip_trash=True)
        self.__hdfs_client.makedirs(target)