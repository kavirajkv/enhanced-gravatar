from flask import Flask
import redis,os

app=Flask(__name__)
app.secret_key ='kavi1234' 

redis_host=os.getenv('REDIS_HOST')
redisconnect=redis.Redis(host=redis_host, port=6379)

from app import views

from app import api

from app import forms