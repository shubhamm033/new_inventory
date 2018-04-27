from flask_restful import Resource
from database import *
from flask import request,jsonify
import uuid
import hashlib
import jwt
from general import *
from auth import auth
from flask_cors import CORS,cross_origin

class Login(Resource):
    

    @cross_origin()
    def post(self):
        
        try:
            data=request.get_json(force=True)
            print(data)
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

        try:
            if not data:
                return jsonify({"success":False,"message":"please enter details"})
        
            admin_email = data["email"]
            admin_password=data["password"]            
            if not admin_email or not admin_password:

                return jsonify({"success":False,"message":"please enter proper details"})
            
            password = hashlib.sha256(admin_password.encode("utf-8")).hexdigest()
            admin = inventory.admin.find_one({"email":admin_email})
            
            
            if not admin:
                return jsonify({"success":False,"message":"Admin is not registerd"})
            
            else:
                if admin['password'] != password:
                    return jsonify({"success":False,"message":"incorrect password"})
            
                else:
                

                    token_json = {
                        "_id": admin["admin_id"]
                        }
                
                token =  jwt.encode(token_json, jwt_secret, algorithm="HS256")
                return jsonify({"success":True,"token": str(token.decode("utf-8")),"username":admin_email})
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})