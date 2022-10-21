# Counts of each Unique Open Vulnerability

This POC python script will generate a CSV (count2.csv) with the Counts of each Unique Open Vulnerability in your Kenna Environment.

# How It Does It
- Starts A Full Data Export Of All Open Vulnerabilities (Data Export)
- Waits For Data Export To Be Complete & Downloads Zipped file.
- Coverts JSON File to Pandas DataFrame.

# How to Use It
Update this line to point to your Kenna API URL:

```base_url = "https://api.kennasecurity.com/"```

Update this line to include your Kenna API key:

```RiskToken = "PasteKennaAPIKEyHere"```

Install the needed python requirements.

```pip -r requirements.txt```

Run the scipt.

```python3 count2.py```


# List Unique CVEs and Counts

Code example that builds a CSV containing unique CVEs and the number of each individual unique CVE found in the environment.


## Directions

1. Install the program the program by doing: `pip -r requirements.txt`.
1. Set the environent variable $KENNA_API_KEY
   * In Windows: https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html
   * In DOS: `set KENNA_API_KEY=<your API key>`
   * In Linux: `export KENNA_API_KEY="<your API key>"`
1. Run the program: `python count2.py`

### Options
You can also run the script with a previous search ID. This will first look for `asset_<search ID>.jsonl` and then `asset_<search ID>.gz`. If neither is found, the script will check the export status.

`python count2.py -h` prints help.

## Sample Output
```
Get Unique CVEs
New search ID: 1441359 with XXXXXX Vulnerabilities
Sleeping for 10 seconds. (60)
Unzipping file vulns_1441359.gz to vulns_1441359.jsonl
File vulns_1441359.gz unzipped to vulns_1441359.jsonl
Counting lines in vulns_1441359.jsonl
File: vulns_1441359.jsonl with XXXXX vulns.

XXXX unique vulns discovered.
uniq_vulns.csv is now available.
```
