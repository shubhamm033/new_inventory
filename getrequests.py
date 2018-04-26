from flask_restful import Resource
from flask import request,jsonify
from database import inventory
import uuid
from general import *
from flask_cors import CORS,cross_origin
from auth import auth

class Getnames(Resource):
    @auth
    @cross_origin()
    def get(self):
        
        try:
            print("hello")
            cursor = inventory.vendors.find({},{"_id":0})
            vendors=[]
            for vendor in cursor:
                vendors.append(vendor)

            cursor = inventory.receivers.find({},{"_id":0})
            receivers=[]
            for receiver in cursor:
                receivers.append(receiver)
            
            cursor=inventory.item_details.find({},{"_id":0,"board_details":0,"boxes":0,"quantity":0})
            item_names=[]
            for item in cursor:
                item_names.append(item)
            
            cursor=inventory.boards.find({},{"_id":0})
            boards=[]
            for board in cursor:
                boards.append(board)

            cursor=inventory.users.find({},{"_id":0})
            users=[]    
            for user in cursor:
                users.append(user)
            return jsonify({"success":True,"vendors":vendors,"users":users,"item_names":item_names,"boards":boards,"receivers":receivers})   
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})





class Gettabledetails(Resource):
    @auth
    @cross_origin()
    def get(self):

        table_data=[]

        try:
            
            headers=["Serial.No","Item","Qty total","Qty remaining"]
            board_names=[]
            cursor=inventory.item_details.find({},{"_id":0})
            for board in cursor[0]["board_details"]:
                board_names.append(board["name"])
                
            headers+=board_names
            
            cursor=inventory.item_details.find({},{"_id":0})
            
            board_details=[]
            count=1
            for detail in cursor:

                item_by_board=[]
                for board in detail["board_details"]:
                    item_by_board.append(board["quantity"])
                
                new_data=[
                    count,detail["name"],detail["total_quantity"],detail["remaining_quantity"]
                ]
                new_data+=item_by_board
                count= count+1
                board_details.append(new_data)

            return jsonify({"success":True,"headers":headers,"details":board_details})

        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})
        
class Getinputdetails(Resource):
    
    @auth
    @cross_origin()
    def get(self):    
        
        input_details1=[]
        input_details2=[]
        try:
            cursor=inventory.inputdetails.find({},{"_id":0,"User_Id":0,"Vendor_Id":0})
            cursor= sorted(cursor,key=lambda i:i["Date_of_Entry"],reverse=True)


            for index,detail in enumerate(cursor):
                detail["epoch_of_date"]=detail["Date_of_Entry"]
                detail["Date_of_Entry"]=nicetime(detail["Date_of_Entry"])

                for item in detail["items_details"]:
                    
                    item.pop("_Id")
                if index%2==0:
                    input_details1.append(detail)

                else:
                    input_details2.append(detail)
            return jsonify({"success":True,"result1":input_details1,"result2":input_details2})

        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

class Getoutputdetails(Resource):
    @auth
    @cross_origin()
    def get(self):
        output_details1=[]
        output_details2=[]

        try:
            cursor=inventory.outputdetails.find({},{"_id":0,"Receiver_Id":0,"Board_Id":0})
            cursor= sorted(cursor,key=lambda i:i["Date_of_receiving"],reverse=True)
            
            for index,detail in enumerate(cursor):
                detail["epoch_of_date"]=detail["Date_of_receiving"]
                detail["Date_of_receiving"]=nicetime(detail["Date_of_receiving"])
                
                for item in detail["items_details"]:
                    item.pop("_Id")
                if index%2==0:
                    output_details1.append(detail)

                else:
                    output_details2.append(detail)
                 

            return jsonify({"success":True,"result1":output_details1,"result2":output_details2})

        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

