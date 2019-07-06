import requests
from app import appvar
import json
from util.common import pretty_print_POST

def search_header():
    headers = {'content-type': 'application/json', 'api-key': appvar.config["SEARCH_KEY"]}
    return headers

def search_url(action=None):
    INDEX_NAME = appvar.config["SEARCH_INDEX_NAME"]
    URL = 'https://{}.search.windows.net'.format(appvar.config["SEARCH_NAME"])
    API = appvar.config["SEARCH_API"]

    if action is None:
        output_url = ''.join([URL, '/indexes/',INDEX_NAME,'?api-version=',API])
    else:
        output_url = ''.join([URL, '/indexes/',INDEX_NAME, action,'?api-version=',API])
    print(output_url)
    return output_url

def query_index(params):
    
    query_url = search_url(action='/docs')

    search_results = requests.get(query_url, params=params, headers=search_header())

    output={}
    try:
        search_results.raise_for_status()
    except requests.exceptions.HTTPError:
        pretty_print_POST(search_results.request)
        search_results.json()
        raise
    
    try:
        output = search_results.json()["value"]
    except KeyError:
        output = []

    return output
