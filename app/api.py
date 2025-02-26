from app import app
from app import redisconnect as r
import hashlib,requests
from flask import request,jsonify



##############################
'''APIs for storing and retriving user data'''


#get email from request body and converts it to sha256 digest and retrive data from gravatar api
@app.route('/api/getgravatardata',methods=['GET'])
def get_gravatordata():
    data=request.json
    email=data.get('email')
    
    encoded_email=email.lower().encode('utf-8')
    email_hash=hashlib.sha256(encoded_email).hexdigest()
    
    response=requests.get(f'https://api.gravatar.com/v3/profiles/{email_hash}')
    if response.status_code==200:
        res=response.json()
        gravatordata={'hash':res['hash'],'url':res['profile_url'],'image_url':res['avatar_url'],'location':res['location'],'bio':res['description']}
        return jsonify(gravatordata)
    else:
        return jsonify({'message':'profile not found'}),404
        