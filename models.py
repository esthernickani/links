"""SQLAlchemy models for links"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """users in the system"""
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(200),
        nullable = False
    )

    last_name = db.Column(
        db.String(200),
        nullable = False
    )

    email = db.Column(
        db.String(50),
        nullable = False,
        unique = True
    )

    password = db.Column(
        db.String,
        nullable = False
    )

    def __repr__(self):
        return '<User %r>' % self.username
    
    @classmethod
    def signup(cls, first_name, last_name, email, password):
        """sign up user, hashes password and adds user to system"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            first_name=first_name,
            last_name = last_name,
            email = email,
            password = hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """find user with username and password"""
        user = cls.query.filter_by(email = email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)

            if is_auth:
                return user
            else:
                return False

    link = db.relationship('Link', backref="user", cascade="all, delete-orphan")


class Link(db.Model):
    """customer to join queue that are not authenticated"""
    __tablename__ = "link"
    id = db.Column(
        db.Integer,
        primary_key = True
    )

    link = db.Column(
        db.String(300),
        nullable = False,
        unique = True
    )

    platform = db.Column(
        db.String(50),
        nullable = False,
        default = "Unknown"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)


