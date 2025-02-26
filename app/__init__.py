from flask import Flask

app = Flask(__name__)
app.secret_key = 'kavi1234' 

from app import views