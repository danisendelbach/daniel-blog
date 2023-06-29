from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from forms import RegisterForm, LoginForm, CreatePostForm, CommentForm
from sqlalchemy import Table, Column, Integer, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from tables import User, BlogPost, Comment, db

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Base = declarative_base()
Bootstrap(app)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    user = User.query.filter_by(id=user_id).first()
    print(user_id)
    return user
##CONFIGURE TABLES
with app.app_context():
    db.create_all()



@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    print(type(current_user.get_id()))
    admin_id = current_user.get_id()
    return render_template("index.html", all_posts=posts, admin=admin_id)


@app.route('/register', methods=["POST","GET"])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        print("got here")
        email = request.form.get("email")
        user_exists = User.query.filter_by(email=email).first() is not None
        if not user_exists:
            hashed_password = generate_password_hash(request.form.get("password"),method="pbkdf2:sha256", salt_length=8)
            new_user = User(name=request.form.get("name"), email=email, password=hashed_password)
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
            cur_user = User.query.filter_by(email=email).first()
            login_user(cur_user)
            return redirect(url_for('get_all_posts'))
        else:
            error = "There already exists an account with your email-address"
            return render_template("register.html", form=form, error=error)

    if request.method=="GET":
        return render_template("register.html", form=form, error=error)
    else:
        return "Something went wrong"


@app.route('/login',methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if check_password_hash(user.password,request.form.get("password")):
                login_user(user)
                return redirect(url_for("get_all_posts"))
        else:
            error = "Your input was wrong"
            return render_template("login.html", error=error, form=form)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["POST","GET"])
def show_post(post_id):
    form = CommentForm(current_user=current_user)
    if form.validate_on_submit():
        blog = BlogPost.query.filter_by(id=post_id).first()
        with app.app_context():
            new_comment = Comment(
                text=request.form.get("text"),
                author_id=current_user.get_id(),
                receiver_id=blog.author_id,
                blog_id=post_id
            )
            db.session.add(new_comment)
            db.session.commit()

    requested_post = BlogPost.query.get(post_id)
    admin_id = current_user.get_id()
    return render_template("post.html", post=requested_post, admin=admin_id, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["POST","GET"])
def add_new_post():
    post_form = CreatePostForm()
    if post_form.validate_on_submit():
        with app.app_context():
            new_post = BlogPost(
                title=post_form.title.data,
                subtitle=post_form.subtitle.data,
                body=post_form.body.data,
                img_url=post_form.img_url.data,
                author=current_user.name,
                date=date.today().strftime("%B %d, %Y"),
                author_id=current_user.get_id()
            )
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=post_form)


@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/comments")
def show_comments():
   comments_to_cur_user = current_user.received_comments
   return render_template("comments.html", comments=comments_to_cur_user, current_user=current_user)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
