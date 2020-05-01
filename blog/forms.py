from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from blog.models import Tag

class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(1,20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1,128)])
    remember = BooleanField('记住密码')
    submit = SubmitField('登陆')


class SettingForm(FlaskForm):
    blog_title = StringField('博客名称', validators=[DataRequired(), Length(1,40)])
    phone = StringField('手机', validators=[DataRequired(), Length(11)])
    weixin = StringField('微信', validators=[DataRequired(), Length(1,60)])
    about = CKEditorField('关于作者', validators=[DataRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    tag = StringField('添加标签（多个标签用空格分开）', validators=[Optional(), Length(0, 64)])
    body = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField('发布文章')




