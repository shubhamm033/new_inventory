from flask_restful import Resource
from database import inventory
from flask import request,jsonify
import uuid
import hashlib
from auth import auth
from flask_cors import CORS,cross_origin 

class Admin(Resource):
    
    
    
    
    @cross_origin()
    # @auth
    def post(self):

        try:    
            data=request.get_json(force=True)
            admin_email = data["email"]
            name=data["name"]
            password=data["password"]
        except Exception as e:
            return jsonify({"success": False,"error":e.__str__()})

        try:
            
            if not admin_email:
                return jsonify({"success":False,"message":"Please provide email"})

            admin_exist=  inventory.admin.find_one({"email":admin_email})
        
            if admin_exist:
                return jsonify({"success":False,"message":"admin already exists"})
        
            else:
                uid = uuid.uuid4().hex
                password = hashlib.sha256(password.encode("utf-8")).hexdigest()
                
                new_admin={
                    
                    "name":name,    
                    "email":admin_email,
                    "password":password,
                    "admin_id":uid
                }
                
                inventory.admin.insert(new_admin)            
                return jsonify({"success":True,"message":"admin added"})
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})



