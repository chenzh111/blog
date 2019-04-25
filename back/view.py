from datetime import datetime

from flask import render_template, request, redirect, session

from werkzeug.security import generate_password_hash, check_password_hash


from flask import Blueprint

from back.model import Article, db, User, Articletype
from utils.functions import login_required

blue = Blueprint('app',__name__)


# 跳转到注册页面
@blue.route('/',methods=['GET'])
def aa():
    return redirect('/register/')


# 注册
@blue.route('/register/',methods=["GET","POST"])
def register():
    if request.method =="GET":
        return render_template('back/register.html')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = "该账号已经被注册了"
                return render_template('back/register.html',error = error)
            else:
                if password2 == password:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect('/login/')
                else:
                    error = '您两次输入的密码不一样，注册失败'
                    return render_template('back/register.html',error = error)
        else:
            error = '请填写完整的信息进行注册'
            return render_template('back/register.html',error = error)


# 登录
@blue.route('/login/',methods=["GET","POST"])
def login():
    if request.method =="GET":
        return render_template('back/login.html')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '账号不存在，请注册后登陆'
                return render_template('back/login.html',error=error)
            if not check_password_hash(user.password,password):
                error = '密码错误，请重新输入'
                return render_template('back/login.html',error=error)
            session['user_id'] = user.id
            return redirect('/index/')
        else:
            error = '请输入完整信息'
            return render_template('back/login.html',error=error)


# 后台主页
@blue.route('/index/',methods=['GET'])
@login_required
def index():
    sum = Article.query.count()
    return render_template('back/index.html', sum=sum)


@blue.route('/add-article/',methods=['GET'])
def add_article():
    name = Articletype.query.order_by(Articletype.id).all()
    time = datetime.now()
    return render_template('back/add-article.html',time=time,name=name)


@blue.route('/add-category/',methods=['GET'])
def add_category():
    return render_template('back/add-category.html')


@blue.route('/article/',methods=['GET'])
def article():
    title = Article.query.all()
    sum = Article.query.count()
    return render_template('back/article.html',title = title, Articletype=Articletype, sum=sum )


@blue.route('/category/',methods=['GET'])
def category():
    name = Articletype.query.order_by(Articletype.id).all()
    sum = Articletype.query.count()
    return render_template('back/category.html',name=name, sum=sum)


@blue.route('/update-article/',methods=['GET'])
def update_article():
    name  = request.args.to_dict().keys()
    for name3 in name:
        name2 = Article.query.filter_by(title=name3).first()
        content = name2.content
        desc = name2.desc
        type = name2.type
        id = name2.id
    name1 = Articletype.query.order_by(Articletype.id).all()
    Id = Articletype.query.filter(Articletype.id ==type).first().t_name
    return render_template('back/update-article.html',name=name,name1=name1,content=content,desc=desc,type=type,id=id,Article=Article,Id=Id)


@blue.route('/update-category/',methods=['GET'])
def update_category():
    name = request.args.to_dict().keys()
    return render_template('back/update-category.html',name=name)


@blue.route('/Category/update/',methods=['GET', 'POST'])
def category_update():
    name = request.args.to_dict().keys()
    for x in name:
        name1 = x
    name = request.form.get('name')
    name2 = Articletype.query.filter_by(t_name = name1).first()
    name2.t_name = name
    db.session.commit()
    return redirect('/category/')


@blue.route('/Article/update/',methods=['GET', 'POST'])
def article_update():
    titles = request.args.to_dict().keys()
    for x in titles:
        name1 = x
    title = request.form.get('title')
    content = request.form.get('content')
    desc = request.form.get('describe')
    type = request.form.get('category')
    name2 = Article.query.filter_by(title = name1).first()
    name2.title = title
    name2.content = content
    name2.desc = desc
    name2.type = type
    db.session.commit()
    return redirect('/article/')


@blue.route('/delete-category/',methods=['GET','POST'])
def delete_category():
    name = request.args.to_dict().keys()
    for x in name:
        name1 = x
    name2 = Articletype.query.filter_by(t_name=name1).first()
    db.session.delete(name2)
    db.session.commit()
    return redirect('/category/')


@blue.route('/delete-article/',methods=['GET','POST'])
def delete_article():
    name = request.args.to_dict().keys()
    for x in name:
        # name1 = x
        name2 = Article.query.filter_by(title=x).first()
        db.session.delete(name2)
        db.session.commit()
    return redirect('/article/')


# 删除
@blue.route('/article/checkall/',methods=['GET', 'POST'])
def article_chenkall():
    title = request.form.getlist('checkbox[]')
    if title is not None:
        for title in title:
            name2 = Article.query.filter_by(title=title).first()
            db.session.delete(name2)
            db.session.commit()
    else:
        pass
    return redirect('/article/')


# 创建数据库
@blue.route('/create/')
def create():
    db.create_all()
    return "xinjian"


@blue.route('/article/add/',methods=['GET','POST'])
def article_add():
    category = request.form.get("category")
    art = Article()
    art.type = category
    art.title = request.form.get('title')
    art.content = request.form.get('content')
    art.desc = request.form.get("describe")
    if art.title and art.content and art.desc:
        art.save()
    else:
        return render_template('back/add-article.html')
    return redirect('/article/')


@blue.route('/category/add/',methods=['GET','POST'])
def category_add():
    type = Articletype()
    type.t_name = request.form.get('name')
    type.save()
    return redirect('/category/')




