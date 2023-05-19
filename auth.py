from functools import wraps
import json
import requests
from flask import Blueprint,request,Response,current_app

bp = Blueprint("auth",__name__,url_prefix='/auth')



def middleware(func):
    @wraps(func)
    def wrapper():
        authorization = request.headers.get("Authorization",None)
        if(authorization is None):
            return Response(
                response=json.dumps({
                    "details": "User not authenticate",
                }),
                status=401,
                mimetype="application/json"
            )

        # make a request to keycloak server to get the user information
        headers = {"Authorization": authorization}
        url = f"{current_app.config['KEYCLAOK_URI']}realms/{current_app.config['KEYCLOAK_REALM_NAME']}/protocol/openid-connect/userinfo"
        # http://192.168.2.56:8080/realms/keycloak/protocol/openid-connect/userinfo
        response = requests.get(url,headers=headers)
        if response.status_code != 200:
            return Response(
                response=json.dumps({"details": "user not authenticate"}),
                status=401,
                mimetype='application/json'
            )
        
        user = response.json()

        return func(user['email'])
    return wrapper
