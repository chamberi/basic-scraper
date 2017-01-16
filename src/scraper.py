"""Basic scraper to scrape king county's restaurant inspection results."""
import requests
import io
from bs4 import BeautifulSoup
import sys


DOMAIN_PATH = "http://info.kingcounty.gov"
RESULTS_PAGE = "/health/ehs/foodsafety/inspections/Results.aspx"
SEARCH_CRITERIA = {
    "Output": "W",
    "Business_Name": "",
    "Business_Address": "",
    "Longitude": "",
    "Latitude": "",
    "City": "",
    "Zip_Code": "",
    "Inspection_Type": "All",
    "Inspection_Start": "",
    "Inspection_End": "",
    "Inspection_Closed_Business": "A",
    "Violation_Points": "",
    "Violation_Red_Points": "",
    "Violation_Descr": "",
    "Fuzzy_Search": "N",
    "Sort": "B",
}


def get_inspection_page(**kwargs):
    """Submits get request for king co page with kwargs as params."""
    target_url = DOMAIN_PATH + RESULTS_PAGE
    for key, val in kwargs:
        if key in SEARCH_CRITERIA:
            key[SEARCH_CRITERIA] = val
    try:
        import pdb; pdb.set_trace()
        results = requests.get(target_url, SEARCH_CRITERIA)
    except:
        pass
    return results


def load_inspection_page(results):
    """Load the inspection page."""
    with open(results, 'r') as f:
        read_data = f.read()
    return read_data


def parse_source(read_data, encoding='utf-8'):
    "parse"
    parsed = BeautifulSoup(read_data, 'html5lib', from_encoding=encoding)
    
    return parsed
