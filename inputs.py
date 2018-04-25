from flask_restful import Resource
from flask import request,jsonify
from database import inventory
import uuid
from general import *


class Input(Resource):


    def post(self):
        
        try:

            data=request.get_json(force=True)
            

            bill_no=data["bill"]
            vendor_name=data["vendor"]
            user_name=data["user"]
            date=data["date"]
            item_details=data["items"]
            totalprice=int(data["price"])
            tax=int(data["tax"])
            grandtotal=int(data["grandtotal"])
            totalitems=int(data["totalitems"])
        except Exception as e:

            return jsonify({"success":False,"error":e.__str__()})

        try:
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
                
                item_name=item["name"]


                boxes=int(item["boxes"])
                quantity=int(item["quantity"])
                price=int(item["price"])
                
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
            
            return jsonify({"success":True,"message":"Item details inserted"})
            
            
        except Exception as e:
            return jsonify({"succees":False,"error":e.__str__()})



