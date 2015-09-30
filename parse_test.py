import json
from pprint import pprint
def main():
	with open("www.nytimes.com.har") as DataFile:
		data = json.load(DataFile)

	pprint(data)


if __name__ == '__main__':
	main()