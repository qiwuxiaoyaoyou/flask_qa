# -*-codeing = utf-8 -*-
# @Time : 2022-04-02 9:13
# @Author : 齐物逍遥游
# @File : models.py
# @Software : PyCharm
from exts import db
from datetime  import datetime

class EmailCapathaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    captcha = db.Column(db.String(10),nullable=False)   #验证码
    # datetime.now不加括号则为调用的时间，加括号为项目运行时间
    create_time = db.Column(db.DateTime,default=datetime.now)

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime,default=datetime.now)

class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    author = db.relationship("UserModel",backref="questions")

class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel", backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship("UserModel", backref="answers")
