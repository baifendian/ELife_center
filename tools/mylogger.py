# -*- coding: utf-8 -*- 
'''
该日志类可以把不同级别的日志输出到不同的日志文件中
''' 
import os
import sys
import time
import logging
import logging.handlers
import inspect
from os import makedirs



_loggingdict={}

class TNLog(object):
    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    def __init__(self,level='noset',logname='default',handlers=None,name=None):
        self.__loggers = {}
        if not name:
            self.name=logname
        else:
            self.name=name
        self.handlers={}
        self._setlogfile(logname=logname,handlers=self.handlers)
        self.createHandlers()
        logLevels = self.handlers.keys()
        for level in logLevels:
            logger = logging.getLogger(level)
            #如果不指定level，获得的handler似乎是同一个handler? 
            fmt='[%(asctime)s](%(levelname)s, %(name)s,%(lineno)d): %(message)s'
            format2=logging.Formatter(fmt) 
            self.handlers[level].setFormatter(format2)          
            logger.addHandler(self.handlers[level])
            #print level
            lev='lev=logging.'+level.upper()
            exec(lev)
            #print lev
            logger.setLevel(int(lev))
            
            self.__loggers.update({level:logger})
        #print self.__loggers

    def getLogMessage(self,level,message):
        frame,filename,lineNo,functionName,code,unknowField = inspect.stack()[2]
        '''日志格式：[时间] [类型] [记录代码] 信息''' 
        return "[%s] [%s] [%s - %s - %s] %s" %(self.printfNow(),level,filename,lineNo,functionName,message)
    
    def info(self,message):
        #message = self.getLogMessage("info",message)
        self.__loggers["info"].info(message)
    
    def error(self,message):
        #message = self.getLogMessage("error",message)
        self.__loggers["error"].error(message)
    
    def warning(self,message):
        #message = self.getLogMessage("warning",message)
        self.__loggers['warning'].warning(message)

    
    def debug(self,message):
        #message = self.getLogMessage("debug",message)
        self.__loggers['debug'].debug(message)

    
    def critical(self,message):
        #message = self.getLogMessage("critical",message)
        self.__loggers['critical'].critical(message)


    def createHandlers(self):
        logLevels = self.handlers.keys()
        for level in logLevels:
            path = os.path.abspath(self.handlers[level])
            #print level,'ddddddddddddd'
            self.handlers[level]= logging.handlers.RotatingFileHandler(path)
            #self.handlers[level] = logging.FileHandler(path)

    def _setlogfile(self,handlers=None,logname='default'):
        if not os.path.exists('logs/%s'%logname):
            makedirs('logs/%s'%logname)
        default_handlers = {
                'notset':"logs/%s/%s_notset.log"%(logname,logname),
                'debug':"logs/%s/%s_debug.log"%(logname,logname),
                'info':"logs/%s/%s_info.log"%(logname,logname),
                'warning':"logs/%s/%s_warning.log"%(logname,logname),
                "error":"logs/%s/%s_error.log"%(logname,logname),
                'critical':"logs/%s/%s_critical.log"%(logname,logname)
                }
        if handlers:
            default_handlers.update(handlers)
        self.handlers.update(default_handlers)

def setlogfile(logname='default',handlers=None):      
    if not logname in _loggingdict.keys():
        logger = TNLog(logname=logname,handlers=handlers)
        logger._setlogfile(logname=logname,handlers=handlers)
        _loggingdict[logname]=logger
    
def get_log(logname='default'):
    if not logname in _loggingdict.keys():
        setlogfile(logname=logname)
    return _loggingdict[logname]
if __name__ == "__main__":
    logger=get_log(logname='tm')
    logger.debug("debug")   
    logger.info("info")
    logger.warning("warning")  
    logger.error("error")   
    logger.critical("critical")
    s2=get_log(logname='tb')
    s2.info('ni mei de')
    logger.warning('mmmmmmmmmmmmmmmmm')
    get_log('ss').error('mmmmmmmdfsfsfsfsfs')
    
    
