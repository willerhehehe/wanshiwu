#encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Question,Comment
from exts import db
import time
from ziroom import main

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 检测登录的装饰器
def check_login(func):
    def check(*args,**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return check

# @app.route('/test',endpoint='test')
# @check_login
# def test():
#     return 'test pass'

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-time').all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 31天内不需要重复登陆
            session.permanent=True
            return  redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后再登陆！'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 账号验证，如果被注册就不能在注册
        user=User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该账号已被注册！'
        else:
            # password1==password2
            if password1 != password2:
                return u'两次密码不相同，请核对后再填写！'
            else:
                user = User(telephone = telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功则跳转登陆页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
def question():
    if session.get('user_id'):
        if request.method == 'GET':
            return render_template('question.html')
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            if title !='' and content !='':
                questions = Question(title=title, text=content,use_id=session['user_id'],time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                db.session.add(questions)
                db.session.commit()
                return '发布成功'
            else:
                return render_template('question.html',title=title,content=content)
    else:
        return redirect(url_for('login'))


@app.route('/ziroom/',methods=['GET','POST'])
def ziroom():
    if request.method == 'GET':
        return render_template('ziroom.html')
    else:
        return request.form.get('demo1')


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_info = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question_info)


@app.route('/add_comment/',methods=['GET','POST'],endpoint='add_comment')
@check_login
def add_comment():
    content = request.form.get('comment_content')
    question_id = request.form.get('question_id')
    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question=question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))


@app.route('/demo/')
def demo():
    return render_template('demo.html')


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
