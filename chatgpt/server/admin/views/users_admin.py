from flask_admin import expose
from flask import flash, redirect, request, url_for
from wtforms import Form, StringField, BooleanField, validators

from models.user import User
from ..base import BaseView, ActionView

class UsersAdmin(BaseView):
    column_labels = dict(
        id='ID',
        username='Username',
        name='Name',
        email='Email',
        is_admin='Admin',
        is_active='Active',
        date_created='Created At',
        date_updated='Updated At'
    )
    column_list = ('id', 'username', 'name', 'email', 'is_admin', 'is_active', 'date_created', 'date_updated')
    column_filters = ('id', 'username', 'name', 'email', 'is_admin', 'is_active')
    column_searchable_list = ('username', 'name', 'email')
    column_formatters = {}
    column_sortable_list = ('id', 'date_created', 'date_updated')
    form_excluded_columns = ('date_created', 'date_updated', 'password')
    can_create = True
    can_edit = True
    can_delete = False

    @action('toggle_admin', 'Toggle Admin Status', 'Are you sure you want to toggle admin status?')
    def action_toggle_admin(self, ids):
        try:
            for user_id in ids:
                user = User.get_by_id(user_id)
                user.is_admin = not user.is_admin
                user.save()
            flash(f'Successfully changed admin status for {len(ids)} users', 'success')
        except Exception as e:
            flash(f'Failed to change admin status: {str(e)}', 'error')

    @action('toggle_active', 'Toggle Active Status', 'Are you sure you want to toggle active status?')
    def action_toggle_active(self, ids):
        try:
            for user_id in ids:
                user = User.get_by_id(user_id)
                user.is_active = not user.is_active
                user.save()
            flash(f'Successfully changed active status for {len(ids)} users', 'success')
        except Exception as e:
            flash(f'Failed to change active status: {str(e)}', 'error')


class UserForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=3, max=50)])
    name = StringField('Name', [validators.DataRequired(), validators.Length(max=100)])
    email = StringField('Email', [validators.Email(), validators.Length(max=120)])
    is_admin = BooleanField('Admin')
    is_active = BooleanField('Active', default=True)


class UserCreateView(ActionView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = UserForm(request.form)
        if request.method == 'POST' and form.validate():
            # Check if username exists
            if User.get_or_none(User.username == form.username.data):
                flash('Username already exists', 'error')
                return self.render(self.SUCCESS_PAGE)

            # Create new user
            User.create(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                is_admin=form.is_admin.data,
                is_active=form.is_active.data
            )
            flash('User created successfully', 'success')
            return redirect(url_for('users.index_view'))

        return self.render(self.SUCCESS_PAGE)