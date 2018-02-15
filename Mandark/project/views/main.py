# -*- coding: utf-8 -*-
from flask import render_template, g, Blueprint
from flask_security import current_user, login_required


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
