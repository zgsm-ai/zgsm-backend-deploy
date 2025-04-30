from wtforms import Form, StringField, SelectField, validators
from flask_admin import expose
from flask import request, redirect, url_for, flash

from models.configuration import Configuration
from ..base import BaseView, ActionView

class ConfigurationAdmin(BaseView):
    column_labels = dict(
        id='ID',
        name='Name',
        type='Type',
        value='Value',
        description='Description',
        status='Status',
        date_created='Created At',
        date_updated='Updated At'
    )
    column_list = ('id', 'name', 'type', 'value', 'description', 'status', 'date_created', 'date_updated')
    column_filters = ('id', 'name', 'type', 'status')
    column_searchable_list = ('name', 'value', 'description')
    column_formatters = {}
    column_sortable_list = ('id', 'date_created', 'date_updated')
    form_excluded_columns = ('date_created', 'date_updated')
    form_choices = {
        'type': [
            ('text', 'Text'),
            ('json', 'JSON'),
            ('int', 'Integer'),
            ('float', 'Float'),
            ('bool', 'Boolean'),
        ],
        'status': [
            ('0', 'Disabled'),
            ('1', 'Enabled'),
        ],
    }

    def on_model_change(self, form, model, is_created):
        # Validate model data before saving
        self.validate_config(model)

    def validate_config(self, model):
        # Convert value according to type
        if model.type == 'int':
            try:
                int(model.value)
            except ValueError:
                flash('Value must be an integer', 'error')
        elif model.type == 'float':
            try:
                float(model.value)
            except ValueError:
                flash('Value must be a float', 'error')
        elif model.type == 'bool':
            if model.value.lower() not in ('true', 'false', '0', '1'):
                flash('Value must be a boolean (true/false/0/1)', 'error')


class ConfigForm(Form):
    name = StringField('Name', [validators.DataRequired(), validators.Length(max=255)])
    type = SelectField('Type', choices=[
        ('text', 'Text'),
        ('json', 'JSON'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('bool', 'Boolean'),
    ])
    value = StringField('Value', [validators.DataRequired()])
    description = StringField('Description', [validators.Length(max=255)])
    status = SelectField('Status', choices=[
        ('1', 'Enabled'),
        ('0', 'Disabled'),
    ])


class ConfigUpdateView(ActionView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = ConfigForm(request.form)
        if request.method == 'POST' and form.validate():
            # Save data to database
            configuration = Configuration.get_or_none(Configuration.name == form.name.data)
            if configuration:
                configuration.type = form.type.data
                configuration.value = form.value.data
                configuration.description = form.description.data
                configuration.status = int(form.status.data)
                configuration.save()
                flash('Configuration updated successfully', 'success')
            else:
                Configuration.create(
                    name=form.name.data,
                    type=form.type.data,
                    value=form.value.data,
                    description=form.description.data,
                    status=int(form.status.data)
                )
                flash('Configuration created successfully', 'success')
            return redirect(url_for('configuration.index_view'))

        return self.render(self.SUCCESS_PAGE)