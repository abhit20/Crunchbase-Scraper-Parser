# Crunchbase Scraper and Parser

### About the software

Python 3 tool to scrape Crunchbase profiles (organization or person), and parse the profiles

### Prerequisites
* Python 3.7
* pip
* selenium
* webdriver_manager
* beautifulsoup4

### Installation

Install the required packages 
```bash
pip install -r requirements.txt
```

Or use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries individually
```bash
pip install selenium
pip install webdriver_manager
pip install beautifulsoup4
```

### Usage
```python
from crunchbase.crunchbase import Crunchbase

# Some Crunchbase profiles (both organization and person) to scrape 
crunchbase_urls = {"Google": "https://www.crunchbase.com/organization/google", "Larry Page": "https://www.crunchbase.com/person/larry-page"}

crunchbase = Crunchbase()

# Login into Crunchbase Pro, if Pro information needs to be scraped and parsed
'''
email = 'XXXXXX'
password = 'XXXXXX'
crunchbase.login(email=email, password=password)
'''

# List to store to the parsed data
crunchbase_data = list()

# Iterates through the Crunchbase urls to scrape the data
for name, url in crunchbase_urls.items():
    # Set Pro parameter to true if logged into Crunchbase Pro
    data = crunchbase.process_profile(pro=False, name=name, url=url)
    if data is not None:
        crunchbase_data.append(data)

    # Writes the scraped data to the JSON file
    with open('data/crunchbase/demo_crunchbase_data.json', 'w', newline='') as json_file:
        json.dump(crunchbase_data, fp=json_file, indent=3, ensure_ascii=False)
```
