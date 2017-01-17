"""Basic scraper to scrape king county's restaurant inspection results."""
import requests
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

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

headers = {'User-Agent': UA}

def get_inspection_page(**kwargs):
    """Submits get request for king co page with kwargs as params."""
    url = DOMAIN_PATH + RESULTS_PAGE
    params = SEARCH_CRITERIA.copy()
    for key, val in kwargs.items():
        if key in SEARCH_CRITERIA:
            params[key] = val
        resp = requests.get(url, params=params, headers=headers)
    return resp.content, resp.encoding


def load_inspection_page(results):
    """Load the inspection page."""
    with open(results, 'r') as f:
        content = f.read()
        encoding = 'utf-8'
    return content, encoding

def copy_results_to_local(content)
    """Make local copy so we don't hammer the king co server."""
    with open('page.html', 'w') as outfile:
        outfile.write(bytes)


def parse_source(page.html, encoding='utf-8'):
    """Parse content."""
    parsed = BeautifulSoup(page.html, 'html5lib', from_encoding=encoding)
    return parsed


def extract_data_listings(parsed):
    """Extract the divs from the parsed doc."""
    pr_id = re.compile(r'PR[\d]+~')
    return parsed.find_all('div', id=pr_id)


def has_two_tds(elem):
    """Finds two table tds."""
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    """Remove white spaces."""
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(elem):
    """Use restaurant data and convert to a dictionary."""
    metadata_rows = elem.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata
   

def is_inspection_row(elem):
    """Finds the correct row with inspection data."""
    is_tr = elem.name == 'tr'
    if not is_tr:
        return False
    td_children = elem.find_all('td', recursive=False)
    has_four = len(td_children) == 4
    this_text = clean_data(td_children[0]).lower()
    contains_word = 'inspection' in this_text
    does_not_start = not this_text.startswith('inspection')
    return is_tr and has_four and contains_word and does_not_start


def extract_score_data(elem):
    """Get the score for each restaurant."""
    inspection_rows = elem.find_all(is_inspection_row)
    samples = len(inspection_rows)
    total = high_score = average = 0
    for row in inspection_rows:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total/float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples
    }
    return data


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '1/1/2013',
        'Inspection_End': '12/31/2016',
        'Zip_Code': '98133'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    print(len(listings)) 
    print(listings[0].prettify())
