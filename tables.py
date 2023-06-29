from app import Settings
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.ext.declarative import declarative_base


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
Base = declarative_base()
db = SQLAlchemy()

class User(db.Model, UserMixin, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship("BlogPost", backref="poster")
    comments = db.relationship("Comment", backref="author", foreign_keys="Comment.author_id")
    received_comments = db.relationship("Comment", backref="receiver", foreign_keys="Comment.receiver_id")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class BlogPost(db.Model, Base):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship("Comment", backref="blog_site")
    def __init__(self,author, title, subtitle, date, body, img_url, author_id):
        self.author = author
        self.title = title
        self.body = body
        self.img_url = img_url
        self.subtitle = subtitle
        self.date = date
        self.author_id = author_id

class Comment(db.Model, Base):
    __tablename__="comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))

    def __init__(self, text, author_id, blog_id, receiver_id):
        self.text = text
        self.author_id = author_id
        self.blog_id = blog_id
        self.receiver_id = receiver_id