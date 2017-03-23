from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Creamos un objeto de Flask y lo asignamos a la variable app
app.config.from_object('config') #una vez creado el archivo de config,  necesitamos decirle a
                                 #flask que lo lea y lo use

db = SQLAlchemy(app)

from app import views, models
#importamos las vistas, lo hacemos al final para evitar referencias circulares