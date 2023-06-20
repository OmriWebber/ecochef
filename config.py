# config.py
import os
from flask_cdn import CDN

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ecochef'
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    UPLOAD_FOLDER = 'static/img/recipeImages/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    API_URL = 'http://ecochef-api-env.ap-southeast-2.elasticbeanstalk.com'
    # API_URL = 'http://localhost:4000'
    # CDN_DOMAIN = 'd1r3w4d5z5a88i.cloudfront.net'
        
