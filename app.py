from flask import Flask,session,g   #g是flask中独有的，为全局变量
import config
from exts import db,mail
from blueprints import qa_bp,user_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

@app.before_request   #钩子函数的装饰器，在每次请求之前对账号进行处理
def before_requeset():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量也，也可以用setattr(g,"user",user)表示：
            g.user = user  #任何一个当方，拿到这个g.user都可以使用
        except:
            g.user = None

#请求顺序：用户发出请求 -> 执行before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor

@app.context_processor  #上下文处理函数的装饰器
def context_processor():
    if hasattr(g,"user"):
        return {"user":g.user}
    else:
        return {}

if __name__ == '__main__':
    app.run()
