import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#es el path de nuestro archivo de bbdd
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
#carpeta donde guardaremos los archivos de datos de sqlAlchemy

WTF_CSRF_ENABLED = True
SECRET_KEY = 'hardpwd'

#definimos la lista de proveedores OpenID que queremos presentar
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]