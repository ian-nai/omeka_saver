import requests
import subprocess
from bs4 import BeautifulSoup
from collections import OrderedDict

# Setting up empty lists that will later be populated by links
initial_links_list = []

exhibit_links_list = []

capture_links = []

# Your base URL
base_url = 'example.omeka.net'

# A list of the pages in the exhibit(s) you want to capture
exhibit_urls = ['https://utlibrariescollectionhighlights.omeka.net/exhibits/show/example-exhibit',
'https://utlibrariescollectionhighlights.omeka.net/exhibits/show/example-exhibit/example_page_1',
'https://utlibrariescollectionhighlights.omeka.net/exhibits/show/example-exhibit/example_page_2']

# Find all of the links from the pages in your exhibit_urls list and append them to initial_links_list
for x in exhibit_urls:
    r = requests.get(x)
    html_content = r.text
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a') 
    for x in links:
        if x.has_attr('href'):
             initial_links_list.append(x['href'])
       
# Check the complete list of links for any that contain your exhibit's slug (in this case, 'example-exhibit')
for x in initial_links_list:
    if 'example-exhibit' in x:
        exhibit_links_list.append(x)

print(exhibit_links_list)
# Construct the complete URLs for the links by concatenating your base URL and the links in your exhibit_links_list,
# then append them to the capture_links list
for x in exhibit_links_list:
    y = (base_url + x)
    capture_links.append(y)

# The first link in the list has always been incorrect for me, so I pop it out of the list here
capture_links.pop(0)

# Get the final list of links to capture
final_final = OrderedDict((x, True) for x in capture_links).keys()

# Iterate through the final list and use wget to download the pages as WARCs
for x in final_final:
    r = requests.get(x, allow_redirects=True)
    if x.startswith('http'):
            a = x.replace('http', '')
    if x.startswith('https'):
            a = x.replace('https', '')
            c = a.strip(':')
            d = c.replace('/','_')   
    if len(d) > 240:
            d[:240]
    subprocess.run(['wget', '-p', '-H', x, ('--warc-file=' + d)])
