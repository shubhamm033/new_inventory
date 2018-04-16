from flask_restful import Resource
from flask import request,jsonify
from database import inventory
import uuid
from general import *
from flask_cors import CORS,cross_origin




class Edit(Resource):
    
    @cross_origin()
    def post(self):

        try:
            data=request.get_json(force=True)
            type_edit=data["type"]
            type_id=data["element"]["_Id"]
            type_name=data["element"]["name"]

            if type_edit=="users":
                
                update_name={"name":type_name}
                update_input_details={"User_Name":type_name}
                
                inventory.users.update_one({"_Id":type_id},{"$set":update_name})
                inventory.inputdetails.update({"User_Id":type_id},{"$set":update_input_details})
  
                return jsonify({"success":True,"message":"user updated"})
            
            elif type_edit=="vendors":
                
                update_name={"name":type_name}
                update_input_details={"Vendor_Name":type_name}
                inventory.vendors.update_one({"_Id":type_id},{"$set":update_name})
                inventory.inputdetails.update({"Vendor_Id":type_id},{"$set":update_input_details})
                return jsonify({"success":True,"message":"vendor updated"})
            
            elif type_edit=="receivers":
                
                update_name={"name":type_name}
                update_output_details={"Receiver_Name":type_name}
                inventory.receivers.update_one({"_Id":type_id},{"$set":update_name})
                inventory.outputdetails.update({"Receiver_Id":type_id},{"$set":update_output_details})
                return jsonify({"success":True,"message":"receiver updated"})

            elif type_edit=="boards":
                
                update_name={"name":type_name}
                update_output_details={"Board_Name":type_name}
                inventory.boards.update_one({"_Id":type_id},{"$set":update_name})
                inventory.outputdetails.update_one({"Board_Id":type_id},{"$set":update_output_details})
                
                # cursor=inventory.item_details.find({},{"name":0,"total_quantity":0,"boxes":0,"remaining_quantity":0,"_Id":0})
                
                # for detail in cursor:
                #     _id=detail["_id"]
                    




                return jsonify({"success":True,"message":"board updated"})

            elif type_edit=="itemnames":
                
                update_name={"name":type_name}
                inventory.item_details.update_one({"_Id":type_id},{"$set":update_name})
                
                cursor=inventory.inputdetails.find({},{"Vendor_Name":0,"User_Id":0,"Vendor_Id":0,"Bill_No":0,"price":0,"Date_of_Entry":0})
                
                for detail in cursor:
                    Id=detail["_id"]
                    
                    match=False
                    while match==False:
                        count=0
                        for item in detail["items_details"]:
                            if item["_Id"] != type_id:
                                count+=1
                            else:
                                match=True
                                break
                        
                        update_input_items={"items_details."+str(count)+".name":type_name}

                        inventory.inputdetails.update_one({"_id":Id},{"$set":update_input_items})
                
                cursor=inventory.outputdetails.find({},{"Board_Name":0,"Board_Id":0,"Receiver_Id":0,"Receiver_Name":0,"Date_of_receiving":0})
                
                for detail in cursor:
                    Id=detail["_id"]
                    
                    match=False
                    while match==False:
                        count=0
                        for item in detail["items_details"]:
                            if item["_Id"] != type_id:
                                count+=1
                            else:
                                match=True
                                break
                        
                        update_input_items={"items_details."+str(count)+".name":type_name}

                        inventory.outputdetails.update_one({"_id":Id},{"$set":update_input_items})
                


                return jsonify({"success":True,"message":"itemname updated"})
        
        except Exception as e:
            return jsonify({"success":False,"error":e.__str__()})




