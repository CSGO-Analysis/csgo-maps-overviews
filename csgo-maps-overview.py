#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import requests
import subprocess
import pprint
import time
import urllib
import sys

# https://www.online-convert.com
API_KEY = sys.argv[1]
DIR = "overviews"
URL = "http://api2.online-convert.com/jobs"
TYPE_IN = "dds"
TYPE_OUT = "png"
headers = {
    'x-oc-api-key': API_KEY,
    'content-type': "application/json",
    'cache-control': "no-cache"
}

print API_KEY

print "Starting"

input_dir = DIR + "/"
files = [name for name in os.listdir(input_dir) if os.path.isfile(input_dir + name) and name.endswith("." + TYPE_IN)]

for filename in files:
    payload = "{\"input\":[{\"type\":\"remote\",\"source\":\"https://github.com/CSGO-Analysis/csgo-maps-overviews/raw/master/overviews/" + filename + "\"}],\"conversion\":[{\"category\":\"image\",\"target\":\"" + TYPE_OUT + "\"}]}"

    response = requests.request("POST", URL, data=payload, headers=headers)
    response_json = json.loads(response.text)
    job_id = response_json['id']

    result = False
    while not result:
        print "Waiting",
        for i in range(0, 10):
            print ".",
            time.sleep(1)

        response = requests.request("GET", URL + "/" + job_id, headers=headers)
        response_json = json.loads(response.text)
        if len(response.text):
            if response_json['status']['code'] == 'completed':
                result = True
                download_url = response_json['output'][0]['uri']
                print("Downloading: {}".format(download_url))
                urllib.urlretrieve(download_url, "./overviews/{}.{}".format(os.path.splitext(filename)[0], TYPE_OUT))

print("Done.")
