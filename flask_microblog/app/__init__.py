from flask import Flask
#importamos Flask

app = Flask(__name__) #Creamos un objeto de Flask y lo asignamos a la variable app
app.config.from_object('config') #una vez creado el archivo de config,  necesitamos decirle a
                                 #flask que lo lea y lo use

from app import views #importamos las vistas, lo hacemos al final para evitar referencias circulares