#coding=utf-8

# Create your views here.

import json
import hashlib
import random
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from data_manage import goods_manage,user_manage,record_manage
from codis_manage import codis_manager
import function_manage
from tools.mylogger import get_log
from ELife_center import settings

redis_client=codis_manager.RedisClient(settings.CODIS_ADDRESS,settings.CODIS_POET,settings.CODIS_DB)


@csrf_exempt
def login(request):
    '''login function
    login by username,password
    return the information of user
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':400,'msg':'not input username and password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    password=request.POST.get('password')
    if not user_name:
        result={'code':401,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    if not password:
        result={'code':402,'msg':'not input password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result=redis_client.get_all_content('e_live_users')
    if user_name not in result.keys():
        result={'code':403,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if password==user.password:
        #edit the statue ,tag the user have login
        user.statue=1
        redis_client.set_one_content(settings.USERS_HASH_NAME, user_name, user.object_to_json())
        result={'code':0,'msg':'ok','user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        result={'code':404,'msg':'the password erro'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def logout(request):
    '''logout function
    logout by username,and edit the statue of user
    
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':1200,'msg':'not input post parmameter'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':1201,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name not in result.keys():
        result={'code':1202,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if user.statue!=1:
        result={'code':1203,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    #user cancel the login statue
    user.statue=0
    redis_client.set_one_content(settings.USERS_HASH_NAME,user_name, user.object_to_json())
    result={'code':0,'msg':'ok'}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def routette(request):
    '''routette function
    retrun get the prize of level
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':500,'msg':'not input username and password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=request.POST.get('username')
    print username
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    if user.statue!=1:
        result={'code':501,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    #print user.object_to_json()
    if user.credits<10:
        result={'code':502,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        user.credits=user.credits-10
        redis_client.set_one_content(settings.USERS_HASH_NAME, username, user.object_to_json())
        
        prize,goods_id=function_manage.routette_lucky_draw(random.Random())
        goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
        goods=goods_manage.Goods(goods_obj)
        result={'code':0,'msg':'ok','prizelevel':prize,'user':user.object_to_dict(),'prize':goods.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt   
def credit_exchange(request):
    '''credit_exchange function
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':600,'msg':'not input username and password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    goods_id=request.POST.get('goodsid')
    username=request.POST.get('username')
    goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    goods=goods_manage.Goods(goods_obj)
    if user.statue!=1:
        result={'code':601,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    if user.credits<goods.credit_exchange:
        result={'code':602,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        get_log().debug( 'user credit001\t%d'%user.credits)
        user.credits=user.credits-goods.credit_exchange
        get_log().debug( 'user credit002\t%d'%user.credits)
        get_log().debug( 'goods_exchange \t%d'%goods.credit_exchange)
        goods.credit_exchange_people_num+=1
        redis_client.set_one_content(settings.USERS_HASH_NAME, username, user.object_to_json())
        redis_client.set_one_content(settings.GOODS_HASH_NAME,goods.id,goods.object_to_json())
        time_temp=str(datetime.datetime.now())
        exchange_log={
                      'username':user.name,
                      'time':time_temp,
                      'goods_name':goods.name,
                      'image':goods.large_image,
                      'introduction':goods.introduction,
                      'type':1,#0 is lucky draw,1 is exchange
                      'credits':goods.credit_exchange,
                      }
        redis_client.set_one_content(settings.RECORD_HASH_NAME, time_temp, json.dumps(exchange_log,ensure_ascii=False,encoding='utf-8'))
        result={'code':0,'msg':'ok','user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    

@csrf_exempt
def lucky_draw(request):
    '''lucky draw function
    
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':700,'msg':'not input username and goodsid'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    goods_id=request.POST.get('goodsid')
    username=request.POST.get('username')
    print goods_id
    print username
    goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    if user.statue!=1:
        result={'code':701,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    goods=goods_manage.Goods(goods_obj)
    print user.object_to_json()
    print goods.object_to_json()
    if user.credits<goods.lucky_draw_credits:
        result={'code':702,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        user.credits=user.credits-goods.lucky_draw_credits
        goods.lucky_people_num+=1
        time_temp=str(datetime.datetime.now())
        redis_client.set_one_content(settings.GOODS_HASH_NAME,goods.id,goods.object_to_json())
        redis_client.set_one_content(settings.USERS_HASH_NAME, username, user.object_to_json())
        lucky_drawl_log={
                      'username':user.name,
                      'time':time_temp,
                      'goods_name':goods.name,
                      'image':goods.large_image,
                      'introduction':goods.introduction,
                      'type':0,
                      'credits':goods.lucky_draw_credits,
                      }
        redis_client.set_one_content(settings.RECORD_HASH_NAME,time_temp , json.dumps(lucky_drawl_log,ensure_ascii=False,encoding='utf-8'))
        tmp=[i for i in range(100)]
        if random.choice(tmp)<50:
            lucky=1
        else:
            lucky=0
        result={'code':0,'msg':'ok','lucky':lucky,'user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def friends_invitation(request):
    '''invitation friends to add credits
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':600,'msg':'not input parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=request.POST.get('username')
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    if user.statue!=1:
        result={'code':601,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    url=''
    result={'code':0,'msg':'ok','url':url}    
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8')) 

@csrf_exempt    
def add_oil(request):
    '''friends add oil to user
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.GET:
        result={'code':600,'msg':'not input parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=request.GET.get('username')
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    '''
    if user.statue!=1:
        result={'code':601,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    '''
    user.credits+=10
    redis_client.set_one_content(settings.USERS_HASH_NAME,username, user.object_to_json())
    result={'code':0,'msg':'ok'}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
@csrf_exempt   
def sign_in(request):
    '''user sign in 
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':800,'msg':'not post parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name not in result.keys():
        result={'code':801,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if user.sign_in_day==str(datetime.date.today()):
        result={'code':802,'msg':'the username have sign in','user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    
    user.credits+=function_manage.signin_gain()
    user.sign_in_num+=1
    print user.sign_in_day
    print str(datetime.date.today())
    user.sign_in_day=str(datetime.date.today())
    redis_client.set_one_content(settings.USERS_HASH_NAME, user_name, user.object_to_json())
    result={'code':0,'msg':'ok','user':user.object_to_dict()}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt   
def get_new_goods(request):
    '''get the new goods information
    '''
    redis_client=function_manage.get_codis_connect()
    new_goods_list=[]
    result=redis_client.get_all_content(settings.GOODS_HASH_NAME)
    #print result
    for one in result.keys():
        one_good=goods_manage.Goods(result[one])
        if one_good.is_new_goods==1:
            new_goods_list.append(one_good.object_to_dict())
    result={'code':0,'msg':'ok','new_goods':new_goods_list}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
@csrf_exempt      
def get_like_goods(request):
    '''get the user like goods
    '''
    print '========================'
    if not request.POST:
        result={'code':900,'msg':'not post parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    print '--------------------------'
    if not function_manage.check_login(user_name):
        result={'code':901,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    print 'get_like_goods'
    print user_name
    goodses=function_manage.get_like_goods(user_name)
    result={'code':0,'msg':'ok','like_goods':goodses}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
@csrf_exempt
def get_credit_exchange_goods(request):
    '''get lucky draw goods
    '''
    exchange_goods=function_manage.get_exchange_goods()
    result={'credit_exchange_goods':exchange_goods}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))


@csrf_exempt
def get_records(request):
    redis_client=function_manage.get_codis_connect()
    record=[]
    if not request.POST:
        result={'code':1000,'msg':'not post parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    if not function_manage.check_login(user_name):
        result={'code':1001,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    db_result=redis_client.get_all_content(settings.RECORD_HASH_NAME)
    for key in sorted(db_result.keys()):
        one_log=record_manage.Record(db_result[key])
        if one_log.username==user_name:
            record.append(one_log.object_to_dict())
    result={'code':0,'msg':'ok','recordlist':record}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def get_lucky_draw_goods(request):
    '''get lucky draw goods
    '''
    lucky_draw_goods=function_manage.get_lucky_draw_goods()
    result={'lucky_draw_goods':lucky_draw_goods}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

def get_first_page(request):
    '''get the routette image,new goods
    '''
    redis_client=function_manage.get_codis_connect()
    routette_image=redis_client.get_one_content('e_live_logo', 'routette_image')
    tital_image=redis_client.get_one_content('e_live_logo', 'title_image')
    lucky_draw_goods=function_manage.get_lucky_draw_goods()[0:2]
    exchange_goods=function_manage.get_exchange_goods()[0:6]
    result={'routette_image':routette_image,
            'tital_image':tital_image,
            'lucky_draw_goods':lucky_draw_goods,
            'exchange_goods':exchange_goods
            }
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def get_user_information(request):
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':1100,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':1101,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name not in result.keys():
        result={'code':1103,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if user.statue!=1:
        result={'code':1104,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result={'code':0,'msg':'ok','user':user.object_to_dict()}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))