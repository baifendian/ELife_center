#coding=utf-8
'''
Created on 2016年7月6日

@author: BFD_389
'''

import json

class User(object):
    ''' the class generate user and handle user object
    '''
    def __init__(self,json_object):
        try:
            dict_object=json.loads(json_object)
        except Exception,e:
            print e
        self.name=dict_object.get('name','noname')
        self.password=dict_object.get('password','nopassword')
        self.credits=dict_object.get('credits',0)
        self.like_goods=dict_object.get('like_goods',[])
        self.sign_in_day=dict_object.get('sign_in_day','')
        self.sign_in_num=dict_object.get('sign_in_num',0)
        self.logo=dict_object.get('logo','')
        self.statue=dict_object.get('statue',0)
    def object_to_json(self):
        attribute={
                   'name':self.name,
                   'password':self.password,
                   'credits':self.credits ,
                   'sign_in_day':self.sign_in_day,
                   'sign_in_num':self.sign_in_num,
                   'like_goods' :self.like_goods,  
                   'logo':self.logo,          
                   'statue':self.statue,     
                   }
        return json.dumps(attribute,ensure_ascii=False,encoding='utf-8')
    def object_to_dict(self):
        attribute={
                   'name':self.name,
                   #'password':self.password,
                   'credits':self.credits ,
                   'sign_in_num' :self.sign_in_num,
                   'logo':self.logo,                 
                   }
        return attribute