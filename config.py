# config.py
import os
from flask_cdn import CDN

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ecochef-api'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    UPLOAD_FOLDER = 'static/img/recipeImages/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    API_URL = 'http://127.0.0.1:4000'
    
    if 'RDS_HOSTNAME' in os.environ:
        print('AWS ELB ENV DETECTED')
        RDS_Connection_String = 'mysql+pymysql://' + os.environ['RDS_USERNAME'] + ':' + os.environ['RDS_PASSWORD'] + '@' + os.environ['RDS_HOSTNAME'] + ':' + os.environ['RDS_PORT'] + '/' + os.environ['RDS_DB_NAME']
        SQLALCHEMY_DATABASE_URI = RDS_Connection_String
    else:
        print('LOCAL ENV DETECTED')
        SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/ecochef-api'
        
