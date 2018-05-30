from flask_restful import Resource
from flask import request,jsonify
from database import *
import uuid
from general import *
from auth import auth
from flask_cors import CORS,cross_origin


class Output(Resource):
    
    # @auth
    @cross_origin()
    def post(self):

        try:
            data=request.get_json(force=True)
            
            receiver_name=data["collector"].strip()
            board_name=data["board"].strip()
            item_details=data["items"]
            date=data["date"]
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

        try:
            inventory.boards.create_index("name",unique=True)
            board_exist = inventory.boards.find_one({"name":board_name})
            if board_exist:

                board_id=board_exist["_Id"]
                board_name=board_exist["name"]
            else:
                board_id = uuid.uuid4().hex
                new_board = {
                    "_Id":board_id,
                    "name":board_name
                    }
                
                inventory.boards.insert_one(new_board)            

                update_board_details={"name":board_name,"_Id":board_id,"quantity":0}
                inventory.item_details.update_many({},{"$push":{"board_details":update_board_details}})
           
            inventory.receivers.create_index("name",unique=True)
            receiver_exist=inventory.receivers.find_one({"name":receiver_name})
            
            if receiver_exist:
                receiver_id=receiver_exist["_Id"]
            else:
                receiver_id=uuid.uuid4().hex
                new_receiver = {
                    "_Id":receiver_id,
                    "name":receiver_name
                    }
                inventory.receivers.insert_one(new_receiver)
            
            
            for item in item_details:
                item_name=item["name"].strip()
                item["name"]=item["name"].strip()
                quantity=int(item["quantity"])
                
                item_exist=inventory.item_details.find_one({"name":item_name})
                
                if item_exist:
                    item_id=item_exist["_Id"]
                    item["_Id"]=item_id
                    quantity_exist=int(item_exist["remaining_quantity"])
                    if quantity_exist<quantity:
                        return jsonify({"success":False,"message":" Entered Quantity does not exist" })
                    
                    else:
                        count=0
                        for board in item_exist["board_details"]:

                            if board_id!=board["_Id"]:
                                count+=1
                            else:
                                quantity_in_board=board["quantity"]
                                update_item_details={"board_details."+str(count)+".quantity": quantity_in_board+quantity,"remaining_quantity":quantity_exist-quantity}
                                inventory.item_details.update_one({"name":item_name},{"$set":update_item_details})

                else:

                    return jsonify({"success":False,"message":"item does not exist" })






            new_details={
                "Board_Id":board_id,
                "Receiver_Id":receiver_id,
                "Board_Name":board_name,
                "Receiver_Name":receiver_name,
                "items_details":item_details,
                "Date_of_receiving":dateToepoch(date)
            }
            
            inventory.outputdetails.insert_one(new_details)
            
            
            # inventory.outputdetails.create_index([("items_details._Id",ASCENDING),("Board_Id",DESCENDING)])
            inventory.outputdetails.create_index("items_details._Id")
            inventory.outputdetails.create_index("Board_Id")
            inventory.outputdetails.create_index("Receiver_Id")
            return jsonify({"success":True,"message":"Item details inserted"})
            
            
        except Exception as e:
            return jsonify({"succees":False,"error":e.__str__()})
