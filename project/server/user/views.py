# project/server/user/views.py


#############
#  imports  #
#############

import sqlalchemy
from flask import render_template, Blueprint, url_for, \
    redirect, request
from flask.ext.login import login_user

from project.server import db
from project.server.models import User
from project.server.user.forms import RegisterForm


############
#  config  #
############

user_blueprint = Blueprint('user', __name__,)


############
#  routes  #
############

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(
            username=form.username.data).first()
        if email is None and username is None:
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )
            try:
                db.session.add(user)
                db.session.commit()
                login_user(user)
            except sqlalchemy.exc.IntegrityError as err:
                print('Handle Error:{0}'.format(err))
            return redirect(url_for("user.register"))
        else:
            print('Handle Error')
    return render_template('user/register.html', form=form)
