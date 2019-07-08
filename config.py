import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SEARCH_NAME = os.environ.get('SEARCH_SERVICE_NAME')
    SEARCH_API = os.environ.get('SEARCH_API_VERSION')
    SEARCH_QUERY_KEY = os.environ.get('SEARCH_QUERY_KEY')
    SEARCH_INDEX_NAME = os.environ.get('SEARCH_INDEX_NAME')
        
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET-KEY'