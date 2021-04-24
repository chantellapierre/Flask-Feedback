"""Models for Flask Feedback app"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Model for user information"""
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.Text(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """Register user with hashed password and return user"""
        hashed= bcrypt.generate_password_hash(pwd)
        #turn bytestring into normal unicode utf8 string
        hashed_utf8 = hashed.decode("utf8")

        #return instance of user with username and hashed password
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate username and password, return if valid"""
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            #return user instancee
            return u
        else:
            return False

    
class Feedback(db.Model):
    """Model for feedback information"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text(100),nullable=False)
    content = db.Column(db.Text, nullable=False)
    username= db.Column(db.Text, db.ForeignKey('users.username'))
    
    user = db.relationship('User', backref="feedback")  


