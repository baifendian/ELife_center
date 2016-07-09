#coding=utf-8
'''
Created on 2016年7月6日

@author: BFD_389
'''

import json

class Goods(object):
    '''the class use to generate database table Goods
    
    goodsid:
        the id of goods
    name:
        the name of goods
    material:
        the material of goods
    usage:
        the usage of goods
    url:
        the url of goods's detail
    
    use_range:
        not use
    time_range:
        the start time of time range 
    is_roulette:
        is or not to participate in roulette(0 or 1)
    is_credit_exchange:
        is or not to participate in credits exchange
    credits_exchange:
        exchange the goods need how many credits
    probability:
        the probability to get the goods by roulette
    '''
    def __init__(self,json_object):
        try:
            dict_object=json.loads(json_object)
        except Exception,e:
            print e
        self.id=dict_object.get('goodsid',0)
        self.name=dict_object.get('name','no name')
        self.material=dict_object.get('material','no material')
        self.usage=dict_object.get('usage','no usage')
        self.url=dict_object.get('url','no url')
        self.use_range=dict_object.get('use_range','no use_range')
        self.time_range=dict_object.get('time_range','no time_range')
        self.lottery_time=dict_object.get('lottery_time',''),
        self.is_routette=dict_object.get('is_routette',0)
        self.is_credit_exchange=dict_object.get('is_credit_exchange',0)
        self.is_new_goods=dict_object.get('is_new_goods',0)
        self.is_lucky_goods=dict_object.get('is_lucky_goods',0)
        self.credit_exchange=dict_object.get('credit_exchange',0)
        self.lucky_draw_credits=dict_object.get('lucky_draw_credits',0)
        self.probability=dict_object.get('probability',0)
        self.small_image=dict_object.get('small_image','')
        self.large_image=dict_object.get('large_image','')
        self.medium_image=dict_object.get('medium_image','')
        self.normal_image=dict_object.get('normal_image','')
        self.introduction=dict_object.get('introduction','no introduction')
        self.lucky_people_num=dict_object.get('lucky_people_num',0)
        self.credit_exchange_people_num=dict_object.get('credit_exchange_people_num',0)
        self.price=dict_object.get('price',0)
        self.type=dict_object.get('type','')
        self.priceseg=dict_object.get('priceseg',0)
        self.num=dict_object.get('num',0)
    def object_to_json(self):
        attribute={
                   'goodsid':self.id,
                   'name':self.name,
                   'material':self.material,
                   'usage':self.usage,
                   'url':self.url,
                   'use_range':self.use_range,
                   'time_range':self.time_range,
                   'lottery_time':self.lottery_time,
                   'is_routette':self.is_routette,
                   'is_credit_exchange':self.is_credit_exchange,
                   'is_new_goods':self.is_new_goods,
                   'is_lucky_goods':self.is_lucky_goods,
                   'credit_exchange':self.credit_exchange,
                   'probability':self.probability,
                   'small_image':self.small_image,
                   'large_image':self.large_image,
                   'medium_image':self.medium_image,
                   'normal_image':self.normal_image,
                   'introduction':self.introduction,
                   'lucky_draw_credits':self.lucky_draw_credits,
                   'lucky_people_num':self.lucky_people_num,
                   'credit_exchange_people_num':self.credit_exchange_people_num,
                   'price':self.price,
                   'type':self.type,
                   'priceseg':self.priceseg,
                   'num':self.num,
                   }
        return json.dumps(attribute,ensure_ascii=False,encoding='utf-8')
    def object_to_dict(self):
        attribute={
                   'goodsid':self.id,
                   'name':self.name,
                   'material':self.material,
                   'usage':self.usage,
                   'url':self.url,
                   'use_range':self.use_range,
                   'time_range':self.time_range,
                   'lottery_time':self.lottery_time,
                   'credit_exchange':self.credit_exchange,
                   'probability':self.probability,
                   'small_image':self.small_image,
                   'large_image':self.large_image,
                   'medium_image':self.medium_image,
                   'normal_image':self.normal_image,
                   'introduction':self.introduction,
                   'lucky_draw_credits':self.lucky_draw_credits,
                   'lucky_people_num':self.lucky_people_num,
                   'credit_exchange_people_num':self.credit_exchange_people_num,
                   'price':self.price,
                   'type':self.type,
                   'priceseg':self.priceseg,
                   'num':self.num,
                   }
        return attribute