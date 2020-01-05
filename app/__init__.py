from flask import Flask


#initialize app
app = Flask(__name__)


#importing configuration
app.config.from_pyfile('conf.py')


#importing views
from app import views



def getApp():

    #db.create_all()
    return app