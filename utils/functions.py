from functools import wraps

from flask import session, render_template, redirect


def login_required(func):
    @wraps(func)
    def check(*args,**kwargs):
        user_id = session.get("user_id")
        if user_id:
            return func(*args,**kwargs)
        else:
            return redirect('/back/login/')
            # return render_template('back/login.html')
    return check


