#encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Question
from exts import db
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.all()
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
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        questions = Question(title=title, text=content, time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        db.session.add(questions)
        db.session.commit()
        return '发布成功'

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
