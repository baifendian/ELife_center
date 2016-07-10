#coding=utf-8
'''
Created on 2016年7月6日

@author: BFD_389
'''
import random
from django.http import HttpResponseRedirect
from data_manage import goods_manage
from data_manage import user_manage
from codis_manage import codis_manager
from ELife_center import settings

CODIS_CONNECT=None


def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def get_codis_connect():
    global CODIS_CONNECT
    if not CODIS_CONNECT:
        CODIS_CONNECT=codis_manager.RedisClient(settings.CODIS_ADDRESS,settings.CODIS_POET,settings.CODIS_DB)
    return CODIS_CONNECT

def check_login(user_name):
    redis_client=get_codis_connect()
    
    result=redis_client.get_all_content(settings.USERS_HASH_NAME)
    if user_name in result.keys():
        user=user_manage.User(result[user_name])
        if user.status==1:
            return True
        
    return False
        
    
    
def get_exchange_goods():
    '''get the goods participated in exchange
    '''
    codis_client=get_codis_connect()
    exchange_goods_list=[]
    result=codis_client.get_all_content(settings.GOODS_HASH_NAME)
    for one in result.keys():
        one_good=goods_manage.Goods(result[one])
        if one_good.is_credit_exchange==1:
            exchange_goods_list.append(one_good.object_to_dict())
    return exchange_goods_list
    

def get_lucky_draw_goods():
    '''get lucky draw goods
    '''
    codis_client=get_codis_connect()
    lucky_draw_goods_list=[]
    result=codis_client.get_all_content(settings.GOODS_HASH_NAME)
    #print result
    for one in result.keys():
        one_good=goods_manage.Goods(result[one])
        if one_good.is_lucky_goods==1:
            lucky_draw_goods_list.append(one_good.object_to_dict())
    return lucky_draw_goods_list

def get_like_goods(user_name):
    like_goods=[]
    redis_client=get_codis_connect()
    user_obj=redis_client.get_one_content(settings.USERS_HASH_NAME, user_name)
    user=user_manage.User(user_obj)
    for i in user.like_goods:
        goods_obj=redis_client.get_one_content(settings.GOODS_HASH_NAME, i)
        if goods_obj:
            goods=goods_manage.Goods(goods_obj)
            like_goods.append(goods.object_to_dict())
    return like_goods
        
        
def get_lucky_draw_items(orand = None):
    all_lucky_goods=get_lucky_draw_goods()
    three_level=[]
    two_level=[]
    one_level=[]
    for one in all_lucky_goods:
        if one['priceseg']==1 or one['priceseg']==2:
            three_level.append(one['goodsid'])
        elif one['priceseg']==3:
            two_level.append(one['goodsid'])
        elif one['priceseg']==4:
            one_level.append(one['goodsid'])
    luck_items = [three_level, two_level, one_level]
    return luck_items
def signin_gain(orand):
    '''
        get luck number for sign in action, average number is 10, scope is 1-100
    '''

    ratio_seg = [1.0, 0.18, 0.066, 0.006]
    nseg = len(ratio_seg)
    rand_seg = [0, 10, 30, 60, 100]

    xr = orand.uniform(0.0, 1.)
    for j in xrange(nseg-1, -1, -1):
        if xr <= ratio_seg[j]:
            return orand.randint(rand_seg[j]+1, rand_seg[j+1])
        
def lucky_draw(orand=None, luck_items_or_level=None, inums=None):
    '''
        抽奖算法
        输入参数：
            orand：随机数对象, random.Random()
            luck_items_or_level: 轮盘抽奖是传入带抽奖的商品ID列表，形如:[[1,2,3,4], [5,6,7], [8,9]]
                    或者商品的价值等级（对应抽奖等级），1、2、3、4对应于 3、3、2、1
            inums：对应3个等次的奖品的数目
        返回：
            中奖等级：0、1、2、3, 分别对应于 未中奖、1等奖、2等奖、3等奖，对应的概率为：90%、1%、2%、7%
            中奖商品ID：传入luck_items_or_level列表参数时，返回中奖商品ID
    '''
    if not orand:
        orand = random.Random()
    fr = orand.uniform(1.e-8, 1.)
    thresholds = [0, 0.21, 0.27, 0.3]
    if inums:
        isum = sum(inums)
        nthresholds = [0.] * 4
        for i in xrange(len(inums)):
            nthresholds[i+1] = (thresholds[i+1] - thresholds[i]) * isum / inums[i] + nthresholds[i]
        #print nthresholds
        thresholds = nthresholds
    for i in xrange(len(thresholds)-1):
        if fr > thresholds[i] and fr <= thresholds[i+1]:
            if not inums:
                ri = orand.randint(1, len(luck_items_or_level[i]))-1
                return 3-i, luck_items_or_level[i][ri]
            l0 = luck_items_or_level
            if luck_items_or_level < 3 or luck_items_or_level > 4:
                luck_items_or_level = 0     # 0
            else:
                luck_items_or_level -= 2    # 1, 2
            if i == luck_items_or_level:
                #print 3-luck_items_or_level, l0
                return 3-luck_items_or_level, None  # 0, 1, 2 => 3, 2, 1
    # not BINGO
    return 0, None

if __name__=="__main__":
    ord=random.Random()
    luck_items = [[1026, 1044, 1029, 1028, 1022, 1023, 1011, 1031], [1048, 1045, 1037, 1012],
                  [1004, 1002, 1001, 1008, 1009, 1034]]
    print lucky_draw(random.Random())
    print signin_gain(ord)