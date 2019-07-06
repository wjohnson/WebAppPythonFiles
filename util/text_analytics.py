if __name__ == "__main__":
    import sys, os
    sys.path.append(os.getcwd())

from util import common
from app import appvar
import requests
import json

def extract_keyphrases(content_list_dict):
    header = common.headers(appvar.config["TEXTANALYTICS_KEY"])
    contents_json = {"documents":content_list_dict}

    base_url = appvar.config["TEXTANALYTICS_URL"]+"keyPhrases"

    req = requests.post(
        url = base_url,
        headers = header, 
        data = json.dumps(contents_json)
    )

    try:
        req.raise_for_status()
    except Exception:
        common.pretty_print_POST(req.request)

    try:
        results_list = req.json()["documents"]
    except KeyError:
        results_list = []
    
    return results_list


if __name__ == "__main__":
    content = [
        {"id":"1", "language":"en", "text":"Thomas, Jason was the person in charge of the elevator."},
        {"id":"100", "language":"en", "text":"It was the best of times.  It was the worst of times.  All the world's a stage."},
        {"id":"2", "language":"en", "text":"This is a far better thing I do for my country.  I walk on the moon and I dance on mars."},
    ]
    extract_keyphrases(content)