from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref="autor", lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    @staticmethod
    def make_unique_nickname(nickname):
        '''Coge el nickname y le anade un numero incrementativo si ya existiese hasta
         que encuentre uno que no exista en la bd'''
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

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
