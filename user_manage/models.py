from django.db import models

# Create your models here.

class User(models.Model):
    '''the class use to generate database table User.
    
    id:
        the django auto generate
    name:
        user name
    password:
        password of user
    credit:
        credit of user   
    '''
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    credit=models.IntegerField()
    
class Goods(models.Model):
    '''the class use to generate database table Goods
    
    id:
        the django auto generate
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
    name=models.CharField(max_length=50)
    material=models.CharField(max_length=150)
    usage=models.CharField(max_length=150)
    url=models.CharField(max_length=150)
    use_range=models.CharField(max_length=150)
    time_range=models.DateField()
    is_routette=models.IntegerField()
    is_credit_exchange=models.IntegerField()
    credit_exchange=models.IntegerField()
    probability=models.FloatField()
    