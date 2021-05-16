import os
import re
from pathlib import Path
import yaml

class ConfigUtil:
    """
    Utilities for reading Application config file
    """
    conf = None

    def __init__(self):
        """
        Constructor method
        """
        if ConfigUtil.conf is None:
            pattern = re.compile(r'^(.*)\<%= ENV\[\'(.*)\'\] %\>(.*)$')
            yaml.add_implicit_resolver("!pathex", pattern)

            def pathex_constructor(loader, node):
                value = loader.construct_scalar(node)
                groups = pattern.match(value).groups()
                if groups[1] in os.environ:
                    return groups[0] + os.environ[groups[1]] + groups[2]
                else:
                    print(
                        'Please set APP_HOME environment variable.')
                    exit(0)

            yaml.add_constructor('!pathex', pathex_constructor)
            with open(os.path.join(os.getenv("APP_HOME", Path.home()), 'application_properties.yaml'),
                      'r') as f:
                ConfigUtil.conf = yaml.load(f, Loader=yaml.FullLoader)
        self.conf = ConfigUtil.conf

    def get_database_config(self):
        """
        Function to get the database properties

        :return: A dict containing the database configuration
        :rtype: dict
        """
        return self.conf['database']

class MiscUtil:

    def getISODate(self, date):
        if date:
            try:
                return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            except AttributeError:
                return date
        return date

class Validate:
    
    def validate_form(self, dict_items, required):
        """
        Check that all fields in required are present
        in the form with a non-empty value. Return a 
        list of error messages, if there are no errors
        this will be the empty list
        """
        messages = []
        for field in required:
            value = dict_items.get(field)
        if value=="" or value==None:
            messages.append("You must enter a value for %s in body" % field)
        return messages