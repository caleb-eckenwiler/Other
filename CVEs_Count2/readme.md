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

```pip3 install -r requirements.txt```

Run the scipt.

```python3 count.py```
