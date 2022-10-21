from json.tool import main
import os
import sys
import csv
import time
import json
import logging
import requests
import gzip
import shutil
import math

# Class to store vulnerability information.
# (This is class is small, but will be enlarged in part 2.)
class Vulnerability_Info:
    def __init__(self):
        self.count = 1

    def incr(self):
        self.count += 1

    def get_count(self):
        return self.count

# Print help.
def print_help():
    prog_name = sys.argv[0]
    print("Gets unique CVEs and puts them in a CSV file.")
    print("")

    print("There are 2 formats:")
    print(f"    {prog_name}")
    print(f"    {prog_name} <search_id>")
    print("Where <search_id> is search ID from a vuln export.")
    print("If <search_id> is not present, a new export is created and retrieved.")
    print("")
    
    print("To obtain this output:")
    print(f"    {prog_name} -h")
    print("")

    sys.exit(1)

# Print and log information.
def print_info(msg):
    print(msg)
    logging.info(msg)

# Print and error information.
def print_error(msg):
    print(msg)
    logging.error(msg)

# Process an HTTP error by printing and log.error
def process_http_error(msg, response, url):
    print(f"{msg} HTTP Error: {response.status_code} with {url}")
    if response.text is None:
        logging.error(f"{msg}, {url} status_code: {response.status_code}")
    else:
        logging.error(f"{msg}, {url} status_code: {response.status_code} info: {response.text}")

# Invoke the data_exports API to request a vuln export.
def request_vuln_exports(base_url, headers):
    request_export_url = f"{base_url}data_exports"

    filter_params = {
        'status' : ['open'],
        'export_settings': {
            'format': 'jsonl',
            'model': 'vulnerability'
        }
    }
    
      response = requests.post(request_export_url, headers=headers, data=json.dumps(filter_params))
    if response.status_code != 200:
        process_http_error(f"Request Data Export API Error", response, request_export_url)
        sys.exit(1)

    resp = response.json()
    search_id = str(resp['search_id'])
    num_vulns = resp['record_count']
    print_info(f"New search ID: {search_id} with {num_vulns} vulns")
    return (search_id, num_vulns)
  
  def get_export_status(base_url, headers, search_id):
    check_status_url = f"{base_url}data_exports/status?search_id={search_id}"

    response = requests.get(check_status_url, headers=headers)
    if response.status_code == 206:
        return False
    if response.status_code != 200:
        process_http_error(f"Get Export Status API Error", response, check_status_url)
        sys.exit(1)
    
    resp_json = response.json()
    return resp_json['message'] == "Export ready for download"

# Check to see if the export file is ready to download.
def check_export_status(base_url, headers, search_id, num_vulns):

    # Check if the export is ready already.
    ready = get_export_status(base_url, headers, search_id)
    if ready:
        return
      
    # Estimate export time for if we're waiting.
    # Calculate wait interval between checking if the export file is ready.
    wait_interval_secs = 5 if num_vulns < 2718 else 10
    wait_limit_secs = math.ceil(num_vulns / 16)

    # Loop to check status for wait_limit_secs seconds.
    secs = 0
    ready = False
    while not ready and secs < wait_limit_secs:
        print(f"Sleeping for {wait_interval_secs} seconds. ({secs})\r", end='')
        time.sleep(wait_interval_secs)
        ready = get_export_status(base_url, headers, search_id)
        secs += wait_interval_secs 

    print("")
    if secs >= wait_limit_secs:
        print_info(f"Waited for {wait_limit_secs} seconds.")
        print(f"Consider re-running with search ID")
        sys.exit(1)
 
# Obtain the exported vuln data and ungzip it.
