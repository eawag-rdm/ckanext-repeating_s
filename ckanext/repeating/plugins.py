import re
import ckan.plugins as p
from ckan.plugins.toolkit import add_template_directory

from ckanext.repeating import validators


def repeating_get_values(field_name, data):
    '''
    Template helper function.
    Get data from repeating_text field from either field_name (if the
    field comes from the database) or construct from several field-n -
    entries in case data wasn't saved yet).
    '''
    def mk_value():
        fields = [re.match(field_name + "-\d+", key) for key in data.keys()]
        fields = sorted([r.string for r in fields if r])
        return [data[f] for f in fields]
        
    value = data.get(field_name, mk_value())
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
    
