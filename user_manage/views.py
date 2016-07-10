#coding=utf-8

# Create your views here.

import json
import hashlib
import random
import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response
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
        result={'code':100,'msg':'not input username and password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    password=request.POST.get('password')
    if not user_name:
        result={'code':101,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    if not password:
        result={'code':102,'msg':'not input password'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    user_name=user_name.lower()
    if user_name not in result.keys():
        result={'code':103,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if password==user.password:
        #edit the status ,tag the user have login
        user.status=1
        redis_client.set_one_content(settings.USERS_HASH_NAME, user_name, user.object_to_json())
        result={'code':0,'msg':'ok','user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        result={'code':104,'msg':'the password erro'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def logout(request):
    '''logout function
    logout by username,and edit the status of user
    
    '''
    redis_client=function_manage.get_codis_connect()
    if not request.POST:
        result={'code':200,'msg':'not input post parmameter'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':201,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=user_name.lower()
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name not in result.keys():
        result={'code':202,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if user.status!=1:
        result={'code':203,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    #user cancel the login status
    user.status=0
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
        result={'code':500,'msg':'not input post parmameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=request.POST.get('username')
    if not username:
        result={'code':501,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=username.lower()
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    if not user_obj:
        result={'code':502,'msg':'the user not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=user_manage.User(user_obj)
    if user.status!=1:
        result={'code':504,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    #print user.object_to_json()
    if user.credits<settings.LUCKY_DRAW_CREDITS:
        result={'code':503,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        user.credits=user.credits-settings.LUCKY_DRAW_CREDITS
        redis_client.set_one_content(settings.USERS_HASH_NAME, username, user.object_to_json())
        lucky_draw_goods=function_manage.get_lucky_draw_items()
        prize_level,goods_id=function_manage.lucky_draw(random.Random(),lucky_draw_goods)
        if goods_id:
            goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
            goods=goods_manage.Goods(goods_obj)
            prize=goods.object_to_dict()
        else:
            prize={}
        result={'code':0,'msg':'ok','prizelevel':prize_level,'user':user.object_to_dict(),'prize':prize}
        #需要保存记录
        if prize_level!=0:
            time_temp=str(datetime.datetime.now())
            routette_log={
                      'username':user.name,
                      'time':time_temp,
                      'goods_name':goods.name,
                      #'goods_name':'%d level prize'%prize_level,
                      'image':goods.large_image,
                      'introduction':'%d level prize'%prize_level,
                      'type':2,#0 is lucky draw,1 is exchange,2 is routette
                      'credits':settings.LUCKY_DRAW_CREDITS,
                      }
            redis_client.set_one_content(settings.RECORD_HASH_NAME, time_temp, json.dumps(routette_log,ensure_ascii=False,encoding='utf-8'))
        
           
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt   
def credit_exchange(request):
    '''credit_exchange function
    '''
    redis_client=function_manage.get_codis_connect()
    goods_id=request.POST.get('goodsid')
    username=request.POST.get('username')
    if not goods_id or not username :
        result={'code':300,'msg':'input parameter error'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=username.lower()
    goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    goods=goods_manage.Goods(goods_obj)
    if user.status!=1:
        result={'code':301,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    if user.credits<goods.credit_exchange:
        result={'code':302,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        user.credits=user.credits-goods.credit_exchange
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
        result={'code':400,'msg':'not input username and goodsid'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    goods_id=request.POST.get('goodsid')
    username=request.POST.get('username')
    if not goods_id or not username :
        result={'code':401,'msg':'input parameter error'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=username.lower()
    goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, goods_id)
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    if user.status!=1:
        result={'code':402,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    goods=goods_manage.Goods(goods_obj)
    if user.credits<goods.lucky_draw_credits:
        result={'code':403,'msg':'the credits not enough'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    else:
        user.credits=user.credits-goods.lucky_draw_credits
        goods.lucky_people_num+=1
        time_temp=str(datetime.datetime.now())
        redis_client.set_one_content(settings.GOODS_HASH_NAME,goods.id,goods.object_to_json())
        redis_client.set_one_content(settings.USERS_HASH_NAME, username, user.object_to_json())
        lucky_draw_items=function_manage.get_lucky_draw_items()
        inums=[len(v) for v in lucky_draw_items]
        prize,_=function_manage.lucky_draw(random.Random(), goods.priceseg, inums)
        #lucky=function_manage.lucky_draw(random.Random())
        if prize!=0:
            prize=1
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
        
        result={'code':0,'msg':'ok','lucky':prize,'user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))

@csrf_exempt
def friends_invitation(request):
    '''invitation friends to add credits
    '''
    return render_to_response('elife.html', {'results': ''})

@csrf_exempt    
def add_oil(request):
    '''friends add oil to user
    '''
    redis_client=function_manage.get_codis_connect()
    username=request.POST.get('username')
    if not username:
        result={'code':600,'msg':'not input parameters'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    username=username.lower()
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, username)
    user=user_manage.User(user_obj)
    '''
    if user.status!=1:
        result={'code':601,'msg':'the user have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    '''
    user.credits+=5
    redis_client.set_one_content(settings.USERS_HASH_NAME,username, user.object_to_json())
    result={'code':0,'msg':'ok'}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
@csrf_exempt   
def sign_in(request):
    '''user sign in 
    '''
    redis_client=function_manage.get_codis_connect()
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':700,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=user_name.lower()
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name not in result.keys():
        result={'code':701,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user=result[user_name]
    user=user_manage.User(user)
    if user.sign_in_day==str(datetime.date.today()):
        result={'code':702,'msg':'the username have sign in','user':user.object_to_dict()}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    add_credits=function_manage.signin_gain(random.Random())
    user.credits+=add_credits
    user.sign_in_num+=1
    user.sign_in_day=str(datetime.date.today())
    redis_client.set_one_content(settings.USERS_HASH_NAME, user_name, user.object_to_json())
    result={'code':0,'msg':'ok','addcredits':add_credits,'user':user.object_to_dict()}
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
    user_name=request.POST.get('username')
    if not request.POST:
        result={'code':800,'msg':'not post username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=user_name.lower()
    if not function_manage.check_login(user_name):
        result={'code':801,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=user_name.lower()
    goodses=function_manage.get_like_goods(user_name)
    if len(goodses)%2!=0:
        goodses=goodses[0:len(goodses)-1]
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
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':900,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    user_name=user_name.lower()
    if not function_manage.check_login(user_name):
        result={'code':901,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    db_result=redis_client.get_all_content(settings.RECORD_HASH_NAME)
    for key in sorted(db_result.keys())[::-1]:
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
    '''get the routette image,lucky draw nad credits exchange goods
    '''
    redis_client=function_manage.get_codis_connect()
    routette_image=redis_client.get_one_content('e_live_logo', 'routette_image')
    tital_image=redis_client.get_one_content('e_live_logo', 'title_image')
    
    #first page need two lucky drawl goods
    lucky_draw_goods=function_manage.get_lucky_draw_goods()[0:2]
    #first page need six credits exchange goods
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
    user_name=request.POST.get('username')
    if not user_name:
        result={'code':1000,'msg':'not input username'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    user_name=user_name.lower()
    if user_name not in result.keys():
        result={'code':1001,'msg':'the username not exist'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    
    user=result[user_name]
    user=user_manage.User(user)
    if user.status!=1:
        result={'code':1002,'msg':'the username have not login'}
        return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))
    result={'code':0,'msg':'ok','user':user.object_to_dict()}
    return HttpResponse(json.dumps(result,ensure_ascii=False,encoding='utf-8'))