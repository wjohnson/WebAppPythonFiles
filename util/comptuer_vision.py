import requests
from app import appvar
import json
import uuid
import urllib.parse as urlparse
from urllib.parse import urlencode
import time
from util import common

PATH_LOOKUP = {
    "detect":'/detect',
    "translate":'/translate',
    "alternatives":'/dictionary/lookup',
    "list":"/languages"
}

def ocr_image(img_url, from_lang, mode=None):
    header = common.headers(appvar.config["VISION_KEY"])
    service_url = appvar.config["VISION_URL"]

    params = {"language":from_lang, "detectOrientation":True}

    if mode == "Handwritten":
        params = {"mode":"Handwritten"}
        service_url = service_url + "recognizeText"
    else:
        service_url = service_url + "ocr"

    req = requests.post(
        url = service_url,
        params = params,
        headers = header,
        data = json.dumps({"url":img_url})
    )
    print(req.status_code)
    # If we don't get a 200, blow up
    try:
        req.raise_for_status()
    except Exception:
        print(req.status_code)
        prepared = req.request
        
        common.pretty_print_POST(prepared)

    if mode == "Handwritten":
        results = ocr_parse_handwritten(req, header)
    else:
        results = ocr_parse_printed(req.json())
    
    return results
        

def ocr_parse_printed(json_object):
    line_infos = [region["lines"] for region in json_object["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info["text"])

    return ' '.join(word_infos)

def ocr_parse_handwritten(req,headers):
    print(req.headers)
    operation_url = req.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    while "recognitionResult" not in analysis:
        response_final = requests.get(
            url = operation_url, 
            headers=headers
        )
        analysis = response_final.json()
        print("Looping")
        time.sleep(1)

    # Extract the recognized text
    tokens = [line["text"] for line in analysis["recognitionResult"]["lines"]]

    results = ' '.join(tokens)

    return results