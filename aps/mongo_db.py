# coding: utf8

import traceback
import threading
from pymongo import MongoClient

Lock = threading.Lock()

class MongoDB(object):
    '''
        mongodb class
    '''
    __instance = None

    #__connection = MongoClient('localhost', 27017)

    def __init__(self, *args, **kwargs):
        self.client = self.__connection

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(MongoDB, cls).__new__(cls, *args, **kwargs)
                    
                    if kwargs.get('auth', False) == False:
                        #uri = 'mongodb://localhost:27017/'
                        host = kwargs.get('host', 'localhost')
                        port = kwargs.get('port', '27017')
                        uri = 'mongodb://{host}:{port}/'.format(**{'host': host, 'port': port})
                    else:
                        uri = "mongodb://{user}:{password}@{host}/{authSource}?authMechanism={authMechanism}".format(**kwargs)
                    #uri = "mongodb://jc:jc@localhost/admin?authMechanism=SCRAM-SHA-1"
                    cls.__connection = MongoClient(uri)
            finally:
                Lock.release()
        return cls.__instance

    def insert(self, database, collection, data):
        '''
            @param database: 数据库名称
            @param collection: 集合
            @param data: 数据
        '''
        db = self.client[database]
        c = db[collection]
        c.insert_one(data)
    
    def drop(self, database, collection):
        '''
            @param database: 数据库名称
            @Param collection: 集合
        '''
        db = self.client[database]
        db[collection].drop()
    
    def remove(self, database, collection, condition):
        '''
            @param database: 数据库名称
            @param collection: 集合
            @param condition: 条件
        '''
        db = self.client[database]
        c = db[collection]
        c.remove(condition)

    def query(self, sql, params=None):
        pass

