# -*-codeing = utf-8 -*-
# @Time : 2022-04-01 16:08
# @Author : 齐物逍遥游
# @File : user.py
# @Software : PyCharm

from flask import Blueprint, render_template, request,redirect,url_for,jsonify,session,flash
from exts import mail,db
from flask_mail import Message
# 若不导入，flask db migrate 将无法生成迁移脚本，因为无法识别增加的数据模型
from models import EmailCapathaModel,UserModel
import string
import random
from datetime import datetime
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash  #对密码生成哈希值
from werkzeug.security import check_password_hash   #对密码检测哈希值

bp = Blueprint('user',__name__,url_prefix='/user')

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password,password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash('邮箱和密码不匹配！')
                return redirect(url_for('user.login'))
        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for('user.login'))

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)  # request.form将存储通过前端form表单传递进来的数据
        if form.validate():  # 如果验证通过
            email = form.email.data
            username = form.username.data
            password = form.password.data

            hash_password = generate_password_hash(password)  #将用户传入的密码进行哈希处理
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:  # 如果没有验证通过
            return redirect(url_for('user.register'))

# @bp.route('/mail')
# def my_mail():
#     '''
#     邮箱的验证码可以存储在 memcached/redis/数据库  中
#     '''
#     message = Message(
#         subject='邮箱测试',
#         recipients=['songwenhaochn@163.com'],  #邮件的接收者
#         body='这是一篇测试邮件',
#     )
#     mail.send(message)
#     return 'success'

@bp.route("logout")
def logout():
    session.clear()     #清楚session中所有的数据
    return  redirect(url_for('user.login'))

@bp.route('/captcha',methods=['POST'])
def get_captcha():
    '''
    邮箱的验证码可以存储在 memcached/redis/数据库  中
    '''
    email = request.form.get('email')  #POST使用request.form方法获取，GET使用request.agrs方法获取
    letters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(letters,4))
    if email:
        message = Message(
            subject='邮箱测试',
            recipients=[email],  #邮件的接收者
            body=f'【知了问答】您的注册邮箱验证码是:{captcha}，请勿泄露',
        )
        mail.send(message)
        captcha_model = EmailCapathaModel.query.filter_by(email=email).first() #查询数据库是否已存在该邮箱
        if captcha_model:       #如果已存在该邮箱
            captcha_model.captcha = captcha     #则修改该邮箱的验证码为新的验证码
            captcha_model.create_time = datetime.now()    #并更新时间的默认值
            db.session.commit()
        else:                       #如果不存在该邮箱
            captcha_model = EmailCapathaModel(email=email,captcha=captcha)   #调用该数据模型，并传入参数
            db.session.add(captcha_model)
            db.session.commit()
        print('验证码：',captcha)  #收到验证码时顺便打印，增加开发效率
        return jsonify({'code':200})  #200 成功请求
    else:
        return jsonify({'code':400,'message':'请先传递邮箱'})  #400 客户端错误

