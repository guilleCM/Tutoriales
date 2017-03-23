from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref="autor", lazy='dynamic')

    @property
    def is_authenticated(self):
        '''devuelve True a menos que el objeto represente un usuario que no esta autorizado por alguna razon'''
        return True

    @property
    def is_active(self):
        '''devuelve True a menos que el usuario este inactivo, por ejemplo baneado'''
        return True

    @property
    def is_anonymous(self):
        '''devuelve true si el usuario no tendria que estar logeado'''
        return False

    def get_id(self):
        '''devuelve el id que le corresponde en la bbdd'''
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r' % self.nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body
