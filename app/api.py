from app import app
from app import redisconnect as r
import hashlib,requests,json
from flask import request,jsonify



##############################
'''APIs for storing and retriving user data'''


#get email from request body and converts it to sha256 digest and retrive data from gravatar api
@app.route('/api/getgravatardata',methods=['GET'])
def get_gravatordata():
    data=request.json
    email=data.get('email')
    
    if not email:
        return jsonify({"message":"Invalid data provided"}),400
    
    encoded_email=email.lower().encode('utf-8')
    email_hash=hashlib.sha256(encoded_email).hexdigest()
    
    response=requests.get(f'https://api.gravatar.com/v3/profiles/{email_hash}')
    if response.status_code==200:
        res=response.json()
        gravatordata={'hash':res['hash'],'url':res['profile_url'],'image_url':res['avatar_url'],'location':res['location'],'bio':res['description']}
        return jsonify(gravatordata),200
    else:
        return jsonify({'message':'profile not found'}),404
    

#API to push data to redis
#it receives json data and stores in redis with email hash as key
@app.route('/api/adduserdata',methods=['GET','POST'])
def add_userdata():
    data=request.json
    userdata=data.get('userdata')
    
    if not userdata:
        return jsonify({"message":"Invalid data provided"}),400
    
    for key,value in userdata.items():
        jsonvalues = json.dumps(value)
        x=r.hset('userdata',key=key,value=jsonvalues)
        if x==1:
            return jsonify({"message":"Data added successfully"}),200
        else:
            return jsonify({"message":"Error while adding data"}),404
    

#gets email hash as json body and get data from redis using that hash which is stored as key
@app.route('/api/getuserdata',methods=['GET'])
def get_userdata():
      data=request.json
      emailhash=data.get('emailhash')
      
      if not emailhash:
          return jsonify({"message":"Invalid data provided"}),400
      
      userdata=r.hget('userdata',emailhash)
      
      if userdata:
          jsondata=json.loads(userdata)
          return jsonify(jsondata),200
      else:
          return jsonify({"message":"Error while retriving data"}),404
        