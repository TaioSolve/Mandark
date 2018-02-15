from flask_admin import AdminIndexView, BaseView
from flask_security import current_user
from flask_admin.contrib.sqla.view import ModelView
from flask import redirect, url_for, flash
from wtforms import PasswordField, validators


class AdminBaseView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash("You don't have permissions to go there", category="warning")
            return redirect(url_for('main.index'))


class AdminIndexView(AdminIndexView, AdminBaseView):
    pass


class AdminModelView(ModelView, AdminBaseView):
    pass


class UserModelView(AdminModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['last_login_at', 'current_login_at',
                             'last_login_ip', 'current_login_ip',
                             'login_count']
    form_overrides = dict(password=PasswordField)
    form_extra_fields = {'password2': PasswordField('Confirm Password',
                                                    [validators.EqualTo(
                                                        'password',
                                                        message='Passwords must match')])}  # noqa
    form_columns = ('roles', 'email', 'password', 'password2', 'active')


class RoleModelView(AdminModelView):
    pass
