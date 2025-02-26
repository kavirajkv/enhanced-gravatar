from app import app
from flask import  render_template, redirect, url_for, flash,get_flashed_messages
from app.forms import UserForm,SearchForm
import requests,hashlib

##############################
'''views flow'''
'''
1.index page where user can enter his/her email and retrive their profile card 
2.if profile not found redirected to enter details, else data retrived from redis and displayed
3.user given email can be checked with gravatar to fetch gravator details 
4.if gravatar details found, Unavailable fields can be filled with user given data. if gravatar details not found, user entered details are stored.
5.User data stored in redis 

'''


#this route will get user email to search in redis and return user data
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    messages=get_flashed_messages()
    
    if form.validate_on_submit():
        email=form.email.data
        
        payload={"email":email}
        url="http://localhost:5000/api/getuserdata"
        response=requests.get(url=url,json=payload)
        if response.status_code==200:
            details=response.json()
            return render_template('profile.html',details=details)
        else:
            flash('Profile not found! Register your details')
            return redirect(url_for('register'))

    return render_template('index.html', form=form,messages=messages)



##############


#If user not found user email can be checked with gravatar and user details can be added based on response
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email=form.email.data
        
        payload={"email":email}
        url="http://localhost:5000/api/getgravatardata"
        response=requests.get(url=url,json=payload)
        if response.status_code==200:
            res=response.json()
            payload={
               "userdata":{
                   res['hash']:{
                       "profile":res['image_url'],
                       "personal_detail":{"name":res['name'],"location": res['location'] if res['location']!="" else form.location.data,"url":res['url']},
                       "contact":{"email":form.email.data,"phone":form.phone.data},
                       "bio":res['bio'] if res['bio']!="" else form.bio.data,
                       "social_profile":form.personalurl.data
                   }
               } 
            }
            url="http://localhost:5000/api/adduserdata"
            added=requests.post(url=url,json=payload)
            if added.status_code==200:
                return redirect(url_for('index'))
            else:
                flash('Error updatind data')
                return render_template('register.html',form=form)
        else:
            encoded_email=email.lower().encode('utf-8')
            email_hash=hashlib.sha256(encoded_email).hexdigest()  
            
            payload={
               "userdata":{
                   email_hash:{
                       "profile":"https://kavidetails.s3.ap-south-1.amazonaws.com/blank-profile-picture-973460_640.png",
                       "personal_detail":{"name":form.name.data,"location":form.location.data,"url":"gravatar profile not found"},
                       "contact":{"email":form.email.data,"phone":form.phone.data},
                       "bio":form.bio.data,
                       "social_profile":form.personalurl.data
                   }
               } 
            }
            url="http://localhost:5000/api/adduserdata"
            added=requests.post(url=url,json=payload)
            if added.status_code==200:
                return redirect(url_for('index'))
            else:
                flash('Error updatind data')
                return render_template('register.html',form=form)
        
    return render_template('register.html',form=form)