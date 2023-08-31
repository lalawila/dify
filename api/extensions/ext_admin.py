from extensions.ext_database import db
from models.account import Account, Tenant

from flask import Flask, url_for, redirect, render_template, request

import flask_login as login
from wtforms import form, fields, validators

from flask_admin import Admin, AdminIndexView, helpers, expose
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from flask_admin.babel import gettext


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        if self.login.data != 'admin' or self.password.data != '123456':
            raise validators.ValidationError('Invalid password')
        
class User:
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return 1

    # Required for administrative interface
    def __unicode__(self):
        return 'admin'

# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        print('index')
        print(login.current_user.is_active)
        if not login.current_user.is_active:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()
            login.login_user(user)
        print('login_view')
        print(login.current_user.is_active)
        if login.current_user.is_active:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        print(login.current_user)
        return login.current_user.is_authenticated

class AccountAdmin(MyModelView):
    pass

def ini_admin_user(user_id):
    if user_id == 1:
        return User()

def init_app(app):

    # Create admin
    admin = Admin(app, name='Admin',index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap4')

    # Add views
    admin.add_view(AccountAdmin(Account, db.session))
    admin.add_view(MyModelView(Tenant, db.session))
