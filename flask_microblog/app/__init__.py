import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

app = Flask(__name__) #Creamos un objeto de Flask y lo asignamos a la variable app
app.config.from_object('config') #una vez creado el archivo de config,  necesitamos decirle a
                                 #flask que lo lea y lo use
#Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp')) #path donde guardaremos los archivos



#conexion BDD
db = SQLAlchemy(app)

from app import views, models
#importamos las vistas, lo hacemos al final para evitar referencias circulares