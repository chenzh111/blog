from flask import Flask, render_template, request, redirect

from flask import Blueprint

from back.model import Article

blue = Blueprint('app',__name__)


@blue.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('web/login.html')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "chen" and password == "123456":
            return redirect('/home/')
        return render_template("web/login.html")


@blue.route('/home/', methods=['GET'])
def home():
    art = Article.query.all()
    return render_template('web/index.html', art=art)


@blue.route('/about/', methods=['GET'])
def about():
    return render_template('web/about.html')


@blue.route('/single/', methods=['GET'])
def post():
    art = request.args.to_dict().keys()
    for art in art:
        article = Article.query.filter_by(title=art).all()
        for article in article:
            content = article.content
    return render_template('web/single.html', article=article, content=content)


@blue.route('/contact/', methods=['GET'])
def contact():
    return render_template('web/contact.html')
