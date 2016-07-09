#coding=utf-8
'''
Created on 2016年7月6日

@author: BFD_389
'''

import json

class Record(object):
    
    def __init__(self,json_object):
        dict_object={}
        try:
            dict_object=json.loads(json_object)
        except Exception,e:
            print e
        self.time=dict_object.get('time',)
        self.goods_name=dict_object.get('goods_name','no name')
        self.image=dict_object.get('image','')
        self.introduction=dict_object.get('introduction','no introduction')
        self.type=dict_object.get('type','')
        self.username=dict_object.get('username','')
        self.credits=dict_object.get('credits',0)
    def object_to_json(self):
        attribute={
                   'time':self.time,
                   'goods_name':self.goods_name,
                   'image':self.image,
                   'introduction':self.introduction,
                   'type':self.type,
                   'username':self.username,
                   'credits':self.credits,
                   }
        return json.dumps(attribute,ensure_ascii=False,encoding='utf-8')
    def object_to_dict(self):
        attribute={
                   'time':self.time[0:22],
                   'goods_name':self.goods_name,
                   'image':self.image,
                   'introduction':self.introduction,
                   'type':self.type,
                   'username':self.username,
                   'credits':self.credits,
                   }
        return attribute