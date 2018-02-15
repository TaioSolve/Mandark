# -*- coding: utf-8 -*-
from Mandark.project import create_app
from flask import render_template, g
from flask_security import current_user

app = create_app()


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error():
    return render_template('404.html', title='FourOhFour')


@app.errorhandler(500)
def internal_error():
    return render_template('500.html', title='A server oops happened')

