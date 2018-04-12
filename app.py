from flask import Blueprint
from flask_restful import Api
from inputs import Input
from outputs import Output
from getrequests import * 
from actionrequests import *
from login import Login 
from admin import Admin




api_bp= Blueprint("api",__name__)
api=Api(api_bp)

api.add_resource(Input,"/input")
api.add_resource(Output,"/output")
api.add_resource(Getnames,"/getnames")
api.add_resource(Gettabledetails,"/tabledetails")
api.add_resource(Getinputdetails,"/inputdetails")
api.add_resource(Getoutputdetails,"/outputdetails")
api.add_resource(Edit,"/edit")
api.add_resource(Login,"/login")
api.add_resource(Admin,"/admin")