from flask_restful import Resource
from flask import request,jsonify
from database import *
import uuid
from general import *
from auth import auth
from flask_cors import CORS,cross_origin

class Input(Resource):

    @auth
    @cross_origin()
    def post(self):
        
        try:

            data=request.get_json(force=True)
            

            bill_no=data["bill"]
            vendor_name=data["vendor"].strip()
            user_name=data["user"].strip()
            date=data["date"]
            item_details=data["items"]
            totalprice=int(data["price"])
            tax=int(data["tax"])
            grandtotal=int(data["grandtotal"])
            totalitems=int(data["totalitems"])
        except Exception as e:

            return jsonify({"success":False,"error":e.__str__()})

        try:
            inventory.vendors.create_index("name",unique=True)
            vendor_exist = inventory.vendors.find_one({"name":vendor_name})
            
            if vendor_exist:
                vendor_id = vendor_exist["_Id"]
            
            else:
                vendor_id = uuid.uuid4().hex
                new_vendor = {
                    "_Id":vendor_id,
                    "name":vendor_name
                    }
                inventory.vendors.insert_one(new_vendor)

            inventory.users.create_index("name",unique=True)
            user_exist=inventory.users.find_one({"name":user_name})
            if user_exist:
                user_id=user_exist["_Id"]
            
            else:
                
                user_id=uuid.uuid4().hex
                new_user = {
                    "_Id":user_id,
                    "name":user_name
                    }
                inventory.users.insert_one(new_user)
             
            
            
            for item in item_details:
                
                item_name=item["name"].strip()
                item["name"]=item["name"].strip()

                boxes=int(item["boxes"])
                quantity=int(item["quantity"])
                price=int(item["price"])

                inventory.item_details.create_index("name",unique=True)
                item_exist=inventory.item_details.find_one({"name":item_name})
                
                
                if item_exist:
                    boxes_exist=int(item_exist["boxes"])
                    quantity_exist=int(item_exist["total_quantity"])
                    item_id=item_exist["_Id"]
                    item["_Id"]=item_id
                    remaining_exist=int(item_exist["remaining_quantity"])
                    update_item = {"boxes":boxes_exist+boxes,"total_quantity":quantity_exist+quantity,"remaining_quantity":remaining_exist+quantity}
                    
                    inventory.item_details.update_one({"name":item_name},{"$set":update_item})
                    
                else:
                    item_id=uuid.uuid4().hex
                    item["_Id"]=item_id
                    board_details=[]

                    cursor=inventory.boards.find({},{"_id":0})
                    
                    for board in cursor:
                        new_detail={"name":board["name"],
                        "_Id":board["_Id"],
                        "quantity":0}
                        
                        board_details.append(new_detail)

                    
                    new_item = {
                       
                    "_Id":item_id,
                    "name":item_name,
                    "boxes":boxes,
                    "total_quantity":quantity,
                    "remaining_quantity":quantity,
                    "board_details":board_details
                    }

                    inventory.item_details.insert_one(new_item)
                    inventory.item_details.create_index("board_details._Id")
                    
                
                
                    
            new_details={
                "Vendor_Id":vendor_id,
                "User_Id":user_id,
                "Vendor_Name":vendor_name,
                "Bill_No":bill_no,
                "Date_of_Entry":dateToepoch(date),
                "User_Name":user_name,
                "items_details":item_details,
                "price":totalprice,
                "tax":tax,
                "Grand_Total":grandtotal,
                "Total_Items":totalitems

            }
            
            inventory.inputdetails.insert_one(new_details)

            inventory.inputdetails.create_index("items_details._Id")
            inventory.inputdetails.create_index("User_Id")
            inventory.inputdetails.create_index("Vendor_Id")
            
            return jsonify({"success":True,"message":"Item details inserted"})
            
            
        except Exception as e:
            return jsonify({"succees":False,"error":e.__str__()})



