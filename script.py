import json
from haralyzer import HarParser

with open('www.nytimes.com.har', 'r') as f:
	har_parser = HarParser(json.loads(f.read()))

no_of_objects = 0

print "Total number of pages is " + str(len(har_parser.pages))

for page in har_parser.pages:
    print "Number of get requests sent was " + str(len(page.get_requests))
    print "Number of requests with status code 200 is " + str(len(page.filter_entries(request_type='GET', status_code='200')))
    print "Number of requests having no content (status code = 204) is " + str(len(page.filter_entries(request_type='GET', status_code='204*')))
    print "Total size of the page is " + str(page.page_size) + " bytes" 
    
    #for entry in entries:
        # Finding the URL
        # print entry.url
