import json
from haralyzer import HarParser
from haralyzer import HarPage

with open('www.nytimes.com.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))


for page in har_parser.pages:
	# entries = page.filter_entries(content_type='image*')
	print len(page.entries)

no_of_objects = 0

domain = dict()
size_domain = dict()
type_file = dict()
dependencies = dict()

shit = 0
	
print len(har_parser.pages)

for page in har_parser.pages:
  	# print len(page.css_files)
  	# print page.css_files[1]
    # for entry in page.entries:
  	# entries = page.filter_entries(content_type='css.*', status_code='2.*')
  	entries = page.filter_entries(request_type='GET', status_code='200')
  	

  	for entry in entries:
  		diff = page.get_total_size([entry])
  		child = entry['request']['url']
  		parent = entry['request']['headers'][5]['value']

  		IP_server = entry['serverIPAddress']
  		IP_server += " : "
	 	IP_server += (child.split("/"))[2]

  		if(IP_server in size_domain):
  			size_domain[IP_server] += diff
  		else:
  			size_domain[IP_server] = diff

  		# print "Size is  " + str(diff)

  		if(IP_server in domain):
  			domain[IP_server] += 1
  		else:
  			domain[IP_server] = 1

  		if(parent in dependencies):
  			dependencies[parent].append(child)
  		else:
  			dependencies[parent] = [child]
	  	



  	# Calculating the number of css, js etc. files and their total size.
	js = page.js_files
  	css = page.css_files
  	img = page.image_files
  	txt = page.text_files
  	aud = page.audio_files
  	vid = page.video_files
  	# misc = page.misc_files

  	type_file['js'] = len(page.js_files)
  	type_file['css'] = len(page.css_files)
  	type_file['image'] = len(page.image_files)
  	type_file['txt'] = len(page.text_files)
  	type_file['audio'] = len(page.audio_files)
  	type_file['video'] = len(page.video_files)
  	# type_file['misc'] = len(page.misc_files)
  	


# Printing the number of objects corresponding to each domain.
for key, value in dependencies.items():
	print key
	print value



# # Printing the number of objects corresponding to each domain.
# for key, value in size_domain.items():
# 	print key, value

# # Printing the size of objects corresponding to each domain.
# for key, value in domain.items():
# 	print key, value

# # Printing the number of files corresponding to each type.
# for key, value in type_file.items():
# 	print key, value

# print len(entries)
