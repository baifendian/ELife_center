#coding=utf-8
'''
Created on 2016年7月6日

@author: BFD_389
'''
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
import hashlib
import json
import zlib
import base64
import goods_manage
import user_manage
import random
from codis_manage import codis_manager
def zip_data(data):
    return base64.b64encode(zlib.compress(data, zlib.Z_BEST_SPEED))
def test_goods():

    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    json_object=redis_client.get_one_content('e_live_user', 'user_test1')
    print json_object
    user1=user_manage.User(json_object)
    print user1.name
    #small_image=open('761073794488571189.png','rb').read()
    for i in range(1,20):
        goods={
           'name':'商品%d'%i,
           
           'small_image':'http://172.24.3.175:8000/static/img/761073794488571189.png',
           
            'goodsid':i,
            'is_routette':1,
            'is_credit_exchange':1,
            'credit_exchange':34,
            'probability':0.3,
            'lucky_draw_credits':20,
              
           }
        #goods=zip_data(small_image)
        
        goods=json.dumps(goods,ensure_ascii=False,encoding='utf-8')
        #goods=goods.encode('utf-8')
        redis_client.set_one_content('e_live_goods', i, goods)
        
    
    json_object=redis_client.get_one_content('e_live_goods', i)
    print json_object

def del_goods():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0) 
    result=redis_client.get_all_content('e_live_goods')
    for key in result.keys():
        redis_client.client.hdel('e_live_goods',key)
    print redis_client.client.hlen('e_live_goods')

def del_users():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0) 
    result=redis_client.get_all_content('e_live_users')
    for key in result.keys():
        redis_client.client.hdel('e_live_users',key)
    print redis_client.client.hlen('e_live_users')
def test_user():   
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    password='bfd_test1'
    md5=hashlib.md5()
    md5.update(password)
    password=md5.hexdigest()
    for user in open('user.txt').readlines():
        print user
        print json.loads(user)
        user=user_manage.User(user)
        user.name=user.name.lower()
        user.logo='http://192.168.188.176:8000/static/images/user/'+user.logo
        
    
        redis_client.set_one_content('e_live_users', user.name, user.object_to_json())
    #one_user=redis_client.get_one_content('e_live_users', 'bfd_test1')
    #user2=user_manage.User(one_user)
    #print user2.password
    #print user2.password==password

def test_logo():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    routette_image='http://192.168.188.176:8000/static/img/911313290023851437.png'
    title_image='http://192.168.188.176:8000/static/img/154240156699238893.png'
    json_object=redis_client.set_one_content('e_live_logo', 'routette_image', routette_image)
    json_object=redis_client.set_one_content('e_live_logo', 'title_image', title_image)
def get_user():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    one_user=redis_client.get_one_content('e_live_users', 'billy')
    print one_user
    user2=user_manage.User(one_user)
    print user2.password
    print user2.object_to_json()

def get_goods():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    one_user=redis_client.get_one_content('e_live_goods', '1049')
    print one_user
    a=redis_client.get_all_content('e_live_goods')
    print len(a)
    for i in sorted(a.keys()):
        print i
        print json.loads(a[i])['is_credit_exchange']
        print type(json.loads(a[i])['is_lucky_goods'])
def put_goods():
    redis_client=codis_manager.RedisClient('172.24.3.175',6380,0)
    goods_file=open('item_data.txt')
    id =10000
    #small_image=open('761073794488571189.png','rb').read()
    for line in goods_file.readlines():
        print line
        print id
        goods_old=json.loads(line.strip())
        if goods_old['purpose']==1:
            is_lucky=1
            is_exchange=0
        elif goods_old['purpose']==2:
            is_lucky=0
            is_exchange=1
        goods={   
                   'goodsid':goods_old['prodid'],
                   'name':goods_old['name'],
                   'material':'',
                   'usage':'',
                   'url':goods_old.get('url',''),
                   'use_range':'',
                   'time_range':'',
                   'lottery_time':goods_old['sexpire'],
                   'credit_exchange':goods_old['point'],
                   'probability':goods_old['sexpire'],
                   'small_image':'http://192.168.188.176:8000/static/images/'+goods_old['images']['small'],
                   'large_image':'http://192.168.188.176:8000/static/images/'+goods_old['images']['big'],
                   'medium_image':'http://192.168.188.176:8000/static/images/'+goods_old['images']['medium'],
                   'normal_image':'192.168.188.176:8000/static/images/'+goods_old['images']['normal'],
                   'raw_image':'192.168.188.176:8000/static/images/'+goods_old['images']['raw'],
                   'introduction':goods_old['brief'],
                   #'lucky_draw_credits':99,
                   'lucky_people_num':0,
                   'credit_exchange_people_num':0,
                   'is_credit_exchange':is_exchange,
                   'is_new_goods':random.choice([0,1]),
                   'is_lucky_goods':is_lucky,
                   'lucky_draw_credits':10,
                   'priceseg':goods_old['priceseg'],
                   'price':goods_old['price'],
                   'type':goods_old['type'],
                   'num':goods_old['num'],
           }
        #goods=zip_data(small_image)
        
        goods=json.dumps(goods,ensure_ascii=False,encoding='utf-8')
        #goods=goods.encode('utf-8')
        redis_client.set_one_content('e_live_goods', goods_old['prodid'], goods)
        id+=1
if __name__=="__main__":
    import urllib2,urllib,hashlib
    password=hashlib.md5()
    password.update('bfd_test1')
    password=password.hexdigest()
    url='http://192.168.188.176:8000/user_manage/friends_invitation/'
    #url='http://127.0.0.1:8000/user_manage/routette/'
    headers={'content-type':'application/json',
             }
    post={'username':'Terry','password':'96e79218965eb72c92a549dd5a330112','goodsid':1001}
    post=urllib.urlencode(post)
    req=urllib2.Request(url,data=post)
    res=urllib2.urlopen(req)
    print res.read()
    #get_user('bfd_test1')
    #test_goods()
    #del_users()
    #test_user()
    #del_goods()
    
    #put_goods()
    #get_goods()
    #test_logo()
    
    get_user()