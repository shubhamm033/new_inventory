from flask_restful import Resource
from flask import request,jsonify
from database import inventory
import uuid
from general import *


class Output(Resource):

    def post(self):

        try:
            data=request.get_json(force=True)
            
            receiver_name=data["collector"]
            board_name=data["board"]
            item_details=data["items"]
            date=data["date"]
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})

        try:
            board_exist = inventory.boards.find_one({"name":board_name})
            if board_exist:

                board_id=board_exist["_Id"]
                
            else:
                board_id = uuid.uuid4().hex
                new_board = {
                    "_Id":board_id,
                    "name":board_name
                    }
                inventory.boards.insert_one(new_board)            

                update_board_details={"board_details."  +  board_name : 0}

                
                inventory.item_details.update_many({},{"$set":update_board_details})
           
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
                item_name=item["name"]
                quantity=int(item["quantity"])
                
                item_exist=inventory.item_details.find_one({"name":item_name})
                
                if item_exist:
                    item_id=item_exist["_Id"]
                    item["_Id"]=item_id
                    quantity_exist=int(item_exist["remaining_quantity"])
                    if quantity_exist<quantity:
                        return jsonify({"success":False,"message":" Entered Quantity does not exist" })
                    
                    quantity_in_board=item_exist["board_details"][board_name]    
                    
                    update_item={"remaining_quantity":quantity_exist-quantity,"board_details."+board_name:quantity_in_board+quantity }
                    inventory.item_details.update_one({"name":item_name},{"$set":update_item})




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
            return jsonify({"success":True,"message":"Item details inserted"})
            
            
        except Exception as e:
            return jsonify({"succees":False,"error":e.__str__()})
