# -*-codeing = utf-8 -*-
# @Time : 2022-04-02 10:06
# @Author : 齐物逍遥游
# @File : forms.py
# @Software : PyCharm

import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import EmailCapathaModel,UserModel

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6,max=20)])

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3,max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4,max=4)])
    password = wtforms.StringField(validators=[length(min=6,max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self,field):    #重写captcha的validator?
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCapathaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError('邮箱验证码错误')

    def validate_email(self,field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经存在！')

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])