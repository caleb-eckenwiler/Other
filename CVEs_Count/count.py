import requests
import pandas as pd 
import json
import gzip
import time
import re
from tqdm.auto import tqdm

# Base URL of API Endpoint. 
base_url = "https://api.kennasecurity.com/"

# Key
RiskToken = "PasteAPIKeyHere"

# Setup Data Export
headers = {
    'X-Risk-Token':  RiskToken,
    'Content-type': 'application/json',
}

data = '{ "status" : ["open"], "export_settings" : { "format": "json", "model": "vulnerability" } }'

base_uri = '/data_exports'
url = ''.join([base_url, base_uri])
response = requests.post(url, headers=headers, data=data)
data = json.loads(response.content)
search_id = data['search_id']

# Pull Data Export
headers = {
    'X-Risk-Token': RiskToken ,
}

params = (
    ('search_id', search_id),
)

response = requests.get(url, headers=headers, params=params)
while True:
    if (response.status_code != 200):
        print("Waiting 15 Seconds For Data Export.")
        time.sleep(15)
        response = requests.get(url, headers=headers, params=params)
    if (response.status_code == 200):
            break

with open("kenna_asset_export.gzip", mode='wb') as localfile: 
    localfile.write(response.content)

with gzip.open('kenna_asset_export.gzip', 'rb') as f:
    file_content = f.read()

data = json.loads(file_content)
data = data['vulnerabilities']
df = pd.json_normalize(data)
df_cve = df[df['cve_id'].str.contains("CVE-")]
df_cve = df_cve['cve_id']
df_cve = df_cve.value_counts(dropna=False).reset_index(name='count')

df.to_csv("opencves.csv", index=False)
print(df)
