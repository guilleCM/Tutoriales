from datetime import datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app.models import User
from .forms import LoginForm, EditForm  # importamos la clase LoginForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
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

#para determinar si un usuario esta logeado implementamos un evento before_request que correra
#antes que la vista y cada vez que recibe una peticion
@app.before_request
def before_request():
    g.user = current_user #current_user nos lo proporciona Flask-login y lo recogemos en la variable g
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
#el argumento methods le dice que esta vista acepta peticiones GET y POST
#que recogeran los datos introducidos por el usuario
@oid.loginhandler #openID manejo de login. Le dice a openID que esta es nuestra funcion de vista del login
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #manejar los datos introducidos por el usuario
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
        #llamada que desencadena la autenticacion de usuario a traves de f-openID.
        #dos argumenos (La clase User incluye nickname y email. son por los que preguntara
    return render_template('login.html',
                           title='Inscribirse',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'] #anadimos los proveedores
                           )
#Importamos la clase LoginForm, hacemos un objeto de ella y se la enviamos al template.
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":  #El argumento resp contiene informacion que le devuelve OpenID
        #si el email es incorrecto redirige al login de nuevo
        flash('Login incorrecto. Por favor prueba otra vez')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first() #buscamos en la bbdd el email que nos han pasado.
    if user is None: #si el email no esta, se considera un nuevo usuario
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname) #Que la clase User solo coja un UNICO nombre
        user = User(nickname=nickname, email=resp.email)  #creamos un objeto Usuario para enchufar a nuestra tabla User
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index')) #redirigimos a la siguiente pagina o sino a index.
    #Protegemos vistas de usuarios no logeados con el decorador login_required y una vez superado el log cargara
    #la pagina a la que intentaba acceder.

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>') #<nickname> lo buscara en la funcion de la vista
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first() #si el usuario no esta en la bbdd te devuelve a index
    if user == None:
        flash('Usuario %s no encontrado.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'autor' : user, 'body' : 'Post de prueba 1'},
        {'autor' : user, 'body' : 'Post de prueba 2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname) #le pasamos el parametro nickname del usuario
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Tus cambios ha sido guardados')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() #al producirse un error en la bbdd, la devolvemos al estado inicial de la sesion
    return render_template('500.html'), 500
