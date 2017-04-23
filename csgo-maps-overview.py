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
API_URL = "http://api2.online-convert.com/jobs"
TYPE_IN = "dds"
TYPE_OUT = sys.argv[2]
HEADER = {
    'x-oc-api-key': API_KEY,
    'content-type': "application/json",
    'cache-control': "no-cache"
}
API_REQUEST_WAIT = 10
REMOTE_URL = "http://www.tafelrunde.net/csgods/resource/overviews/"  # contains updated game files
LOCAL_DIR = "overviews"
FILES = [
    'de_cache_radar',
    'de_cache_radar_spectate',
    'de_cbble_radar',
    'de_dust2_radar',
    'de_dust2_radar_spectate',
    'de_inferno_radar',
    'de_mirage_radar',
    'de_mirage_radar_spectate',
    'de_nuke_radar',
    'de_nuke_radar_spectate',
    'de_overpass_radar',
    'de_train_radar',
    'de_train_radar_spectate'
]

print "Starting..."

for filename in FILES:
    payload = "{\"input\":[{\"type\":\"remote\",\"source\":\"" + REMOTE_URL + filename + "." + TYPE_IN + "\"}],\"conversion\":[{\"category\":\"image\",\"target\":\"" + TYPE_OUT + "\"}]}"

    response = requests.request("POST", API_URL, data=payload, headers=HEADER)
    response_json = json.loads(response.text)
    job_id = response_json['id']

    result = False
    while not result:
        print "Waiting",
        for i in range(0, API_REQUEST_WAIT):
            print ".",
            time.sleep(1)

        response = requests.request("GET", API_URL + "/" + job_id, headers=HEADER)
        response_json = json.loads(response.text)
        if len(response.text):
            if response_json['status']['code'] == 'completed':
                result = True
                download_url = response_json['output'][0]['uri']
                print("Downloading: {}".format(download_url))
                urllib.urlretrieve(download_url, "./overviews/{}.{}".format(os.path.splitext(filename)[0], TYPE_OUT))

print("Done.")
