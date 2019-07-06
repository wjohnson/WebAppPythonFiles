import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    TEXTANALYTICS_KEY = os.environ.get('TEXTANALYTICS_KEY')
    TEXTANALYTICS_URL = os.environ.get('TEXTANALYTICS_URL')

    SEARCH_NAME = os.environ.get('SEARCH_NAME')
    SEARCH_KEY = os.environ.get('SEARCH_KEY')
    SEARCH_API = os.environ.get('SEARCH_API')
    SEARCH_QUERY_KEY = os.environ.get('SEARCH_QUERY_KEY')
    SEARCH_INDEX_NAME = os.environ.get('SEARCH_INDEX_NAME')

    VISION_KEY = os.environ.get('VISION_KEY')
    VISION_URL = os.environ.get('VISION_URL')

    
    BLOB_ACCT_NAME = os.environ.get("BLOB_ACCT_NAME")
    BLOB_KEY = os.environ.get("BLOB_KEY")
    BLOB_URL = os.environ.get("BLOB_URL")
    BLOB_DISPLAY_CONTAINER = os.environ.get("BLOB_DISPLAY_CONTAINER")
    BLOB_OCR_RAW_CONTAINER = os.environ.get("BLOB_OCR_RAW_CONTAINER")
    BLOB_SAS = os.environ.get("BLOB_SAS")
    
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'uploads')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET-KEY'