from flask import Flask
from flask_cors import CORS





def create_app(config_filename):
    app=Flask(__name__)
    CORS(app,support_credentials=True)
    app.config["CORS_HEADERS"]='Authorization'
    

    
    
    
    from app import api_bp
    app.register_blueprint(api_bp,url_prefix="/inventory")

    
    
    return app

if __name__== "__main__":
    app=create_app("config")
    app.run(host="0.0.0.0",debug=True)