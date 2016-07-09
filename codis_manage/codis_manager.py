#coding=utf-8
'''
Created on 2016年5月12日

@author: hth
'''
import redis
import threading

class RedisClient(threading.Thread):
    def __init__(self,host,port,db=0):
        threading.Thread.__init__(self)
        self.host=host
        self.port=port
        self.db=db
        self.client=self.connect(self.host, self.port, self.db)
        
    def connect(self,host,port,db=0):
        '''connect to codis
        '''
        pool = redis.ConnectionPool(host=host, port=port,db=db)
        client=redis.Redis(connection_pool=pool)
        return client
    def get_one_content(self,name,key):
        '''get one one hash value by key
        '''
        #result=self.client.rpop(queuename)
        result=self.client.hget(name, key)
        return result
    def set_one_content(self,name,key,value):
        '''set one hash value by key
        '''
        #self.client.lpush(queuename,value)
        self.client.hset(name, key, value)
        
    def get_all_content(self,name):
        result=self.client.hgetall(name)
        return result

if __name__=='__main__':
    import json
    redis_client=RedisClient('172.24.3.175',6380,0)
    user={'name':'测试1','passwd':124,'credis':99}
    print redis_client.set_one_content('e_live_user', 'user_test1', json.dumps(user,ensure_ascii=False,encoding='utf-8'))
    test=redis_client.get_one_content("e_live_user",'user_test1')   
    print test
    print json.loads(test)['name']