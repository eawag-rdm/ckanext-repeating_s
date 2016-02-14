import re
import ckan.plugins as p
from ckan.plugins.toolkit import add_template_directory

from ckanext.repeating import validators


def repeating_get_values(field_name, form_blanks, data):
    '''
    Template helper function.
    Get data from repeating_text-field from either field_name (if the
    field comes from the database) or construct from several field-N -
    entries in case data wasn't saved yet, i.e. a validation error occurred.
    In the first case, show additional <form_blanks> empty fields. In the
    latter, don't change the form.
    '''
    def mk_value():
        fields = [re.match(field_name + "-\d+", key) for key in data.keys()]
        fields = sorted([r.string for r in fields if r])
        values = [data[f] for f in fields if data[f]]
        values = values + [''] * max(form_blanks - len(values), 0)
        return values
        
    value = data.get(field_name)
    if value:
        value = value if isinstance(value, list) else [value]
        value = value + [''] * form_blanks if value else mk_value()
    else:
        value = mk_value()
    return value

class RepeatingPlugin(p.SingletonPlugin):
    p.implements(p.IValidators)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        """
        We have some form snippets that support ckanext-scheming
        """
        add_template_directory(config, 'templates')

    def get_validators(self):
        return {
            'repeating_text': validators.repeating_text,
            'repeating_text_output':
                validators.repeating_text_output,
            }
    # ITemplateHelpers
    def get_helpers(self):
        return {'repeating_get_values': repeating_get_values}
    
