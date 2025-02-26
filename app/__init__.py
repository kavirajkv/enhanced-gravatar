from flask import Flask
import redis

app=Flask(__name__)
app.secret_key ='kavi1234' 

redisconnect=redis.Redis(host='localhost', port=6379)

from app import views

from app import api

from app import forms