from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm #importamos la clase LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Guille'} #usuario de prueba
    posts = [ #posts de prueba
        {
            'autor' : {'nickname' : 'C3PO'},
            'body' : 'bip bip bip'
        },
        {
            'autor' : {'nickname' : 'R2D2'},
            'body' : '01111011010111'
        },
    ]

    return render_template('index.html',
                           title='Inicio',
                           user=user,
                           posts=posts)
#Esta vista es simple, solo devuelve un String que sera visualziado en el navegador cliente.
#Cada decorador de ruta mapea las URL a la funcion index():

@app.route('/login', methods=['GET', 'POST'])
#el argumento methods le dice que esta vista acepta peticiones GET y POST
#que recogeran los datos introducidos por el usuario
def login():
    form = LoginForm()
    #manejar los datos introducidos por el usuario
    if form.validate_on_submit():
        #Hace el trabajo de procesar el formulario. Si ha ido bien, devuelve True
        #y entonces los datos son seguros para anadir a la app. Si falla algun campo
        #entonces nos saltara False
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        #flash devuelve un mensaje en la siguiente pagina peresentada al usuario
        return redirect('/index')

    return render_template('login.html',
                           title='Inscribirse',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'] #anadimos los proveedores
                           )
#Importamos la clase LoginForm, hacemos un objeto de ella y se la enviamos al template.

