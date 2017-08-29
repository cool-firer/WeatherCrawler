# coding: utf8

import logging

class Logger():
    def __init__(self, logger_name='root', log_level=logging.INFO, file_name=None, console=True):
        '''
            @param logger_name: 日志名
            @param log_level: 日志级别
            @param file_name: 日志文件
            @param console: 输出到控制台
        '''
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        if file_name:
            fh = logging.FileHandler(file_name)
            fh.setLevel(log_level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            
        if console:
            ch = logging.StreamHandler()
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def getLogger(self):
        return self.logger
