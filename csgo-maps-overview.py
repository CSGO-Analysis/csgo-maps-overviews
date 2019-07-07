#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import time
import urllib

import requests

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
FILE_URLS = sys.argv[3]  # file with urls containing updated game files
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
    'de_nuke_lower_radar',
    'de_overpass_radar',
    'de_train_radar',
    'de_biome_radar',
    'de_biome_radar_spectate',
    'de_austria_radar',
    'de_austria_radar_spectate',
    'de_castle_radar',
    'de_castle_radar_spectate',
    'de_subzero_radar',
    'de_vertigo_radar',
    'de_vertigo_lower_radar',
    'de_zoo_radar',
    'de_zoo_radar_spectate',
    'dz_blacksite_radar',
    'dz_sirocco',
    'dz_sirocco_radar',
    'de_season_radar',
    'de_season_radar_spectate'
]

print("Starting...")

remote_url = None

f = open(FILE_URLS, "r")
for url in f:
    if requests.get(url + "de_dust2.dds").status_code == 200:
        remote_url = url
        break

for filename in FILES:
    payload = '{"input":[{"type":"remote","source":"' + remote_url + filename + '.' + TYPE_IN + '"}],"conversion":[{"category":"image","target":"' + TYPE_OUT + '"}]}'

    response = requests.request("POST", API_URL, data=payload, headers=HEADER)
    response_json = json.loads(response.text)
    job_id = response_json['id']

    result = False
    while not result:
        print("Waiting",)
        for i in range(0, API_REQUEST_WAIT):
            print(".",)
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
