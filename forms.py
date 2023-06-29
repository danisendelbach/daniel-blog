from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Create Account")





class CommentForm(FlaskForm):
    text = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Comment")
    '''
    def __init__(self, current_user):
        
        self.current_user = current_user
        if current_user.is_authenticated:
            self.submit = SubmitField("Comment")
        else:
            self.submit = SubmitField("Login to Comment")
    '''