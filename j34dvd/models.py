__author__ = 'carljame'

from datetime import datetime

from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import desc

from j34dvd import db

#junction low-level table does not need to be a Model class
tags = db.Table('dvd_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('dvd_id', db.Integer, db.ForeignKey('dvds.id'))
                )

class Dvds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    binder = db.Column(db.String(50))
    page = db.Column(db.Integer)
    sleeve = db.Column(db.Integer)
    imdb_page = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, lazy='joined',
                           backref=db.backref('dvds', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Dvds.query.order_by(desc(Dvds.date)).filter(Dvds.user_id == current_user.id).limit(num)

    @staticmethod
    def alpha():
        try:
            return Dvds.query.order_by(Dvds.title).filter(Dvds.user_id == current_user.id)
        except:
            return Dvds.query.order_by(desc(Dvds.date)).limit(0)


    @property
    def tags(self):
        return ','.join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]
        else:
            self._tags = []

    def __repr__(self):
        return self.title

'''
For future functionality
class Binder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    binder = db.Column(db.String(50))
    binder_short = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    dvds = db.relationship('Dvds', backref='user', lazy='dynamic')

    #For future functionality
    #binders = db.relationship('Binder', backref='user', lazy='dynamic')

    password_hash = db.Column(db.String(80))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name