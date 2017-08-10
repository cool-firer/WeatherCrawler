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

    __connection = MongoClient('localhost', 27017)

    def __init__(self):
        self.client = self.__connection

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                if not cls.__instance:
                    cls.__instance = super(MongoDB, cls).__new__(cls, *args, **kwargs)
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

    def query(self, sql, params=None):
        pass

    def execute(self, sql, params=None):
        pass


    def __close(self, connect, cursor, commit=False):
        try:
            if commit:
                connect.commit()
            if cursor:
                cursor.close()
            if connect:
                connect.close()
        except Exception:
            exstr = traceback.format_exc()
            print(exstr)

