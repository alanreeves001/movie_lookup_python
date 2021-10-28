#! python 3
# bluray.py

import requests
import csv
import datetime
from bs4 import BeautifulSoup
import string
import re

def FormatTitle(unformatted):

	# removes all punctuation
	formatted = str(unformatted).translate(str.maketrans('', '', string.punctuation))
	
	# removes any extra spaces
	formatted = " ".join(formatted.split())
	
	# converts to Title (each work capitalized)
	formatted = formatted.title().strip()

	# Removes "The" from the data file title
	if formatted[0:3] == "The":
		formatted = formatted[4:]
	
	return formatted

def GetTitleFromResult(result):
	
	# Removes the format from the title
	regex = "\[[^\[.\]]*\]"

	title = re.sub(regex, "", str(result))

	return title.strip()

def GetMediaFromResult(result):
	# get any characters after [ to the end
	return result[result.find(" ["):].title()

def GetSearchPageLink(parameter, item_format):
	# formats a link to do the initial search for web scraping
	search_page_link = "%s%s%s" % (SEARCH_URL, parameter.replace(' ', '+'), '+' + item_format + SEARCH_URL_SUFFIX)

	return search_page_link

def GetPubDateMultiple(data):
	pubdate = data.find_all('div', {'class': [PUBDATE_ELEMENT_RESULTS]})
	if pubdate:
		pubdate = " (" + pubdate[0].text.strip() + ")"
	else:
		pubdate = ""
	
	return pubdate

def GetPubDateSingle(data):
	
	if not data.select(PUBDATE_ELEMENT_PAGE):
						#print("No pub date found")
		publication_date = ""
	else:
		publication_date = " (" + re.search('\d{4}', str(data.select(PUBDATE_ELEMENT_PAGE)))[0] + ")"
	
	return publication_date

def GetPageContents(response):

	return BeautifulSoup(response.text, 'html.parser')

def GetDataAsList(data):
	# Opens data source. Converts data to list. Returns data list
	
	data_source = GetDataSource(data)
	data_list = list(ReadData(data_source))
	return data_list

def GetDataSource(source):
	return open(source)

def ReadData(data):
	return csv.reader(data)

def DataOutput(data):
	output_file.write(data)

def CheckResultForItemFormat(data, format):
	# print("CheckresultForItemFormat")
	if data.title().find("Blu") > 0 and format == "dvd":
		print("Found blu, looking for dvd")
		return False

	if data.title().find("Season") > 0:
		print ("------------- TV ------------------ " + data)
		return False
	# print("data title: " + data.title())
	return True

# --------------------------------------------------------------

# CONSTANTS
SEARCH_URL = 'https://mobi.ent.sirsi.net/client/en_US/default/search/results?qu='
SEARCH_URL_SUFFIX = '&te=&te=ILS'
FILE_PATH = "./"
TITLE_ELEMENT_MULTIPLE = '.results_bio'
TITLE_ELEMENT_SINGLE = 'div.text-p.INITIAL_TITLE_SRCH'
PUBDATE_ELEMENT_RESULTS ='displayElementText text-p highlightMe PUBDATE'
PUBDATE_ELEMENT_PAGE = '.text-p.PUBLICATION_INFO'
#INPUT_DATA = FILE_PATH + "movies.csv"
INPUT_DATA = FILE_PATH + "movies_test.csv" # Short data file used for testing/debugging

# Variables
now = datetime.datetime.now()
page_response_timeout = 22
tab = "&nbsp;&nbsp;&nbsp;"
search_message = ''
not_found = " not found"
found = False
result_prefix = ''
result_suffix = ''
item_formats_list = ['blu','dvd']
item_link_prefix = ""

output_file = open(FILE_PATH + "movie-links.htm", "w") # w for write, a for append
#output_file_debug = open(FILE_PATH + "debug.txt", "w", encoding="utf-8")

html_header = "<html>\n   <head>\n      <title>Mobile Public Library Python automated Bluray and DVD lookup</title>\n   </head>\n   <body style='line-height: 1.5em'>\n"

DataOutput(html_header + "   " + now.strftime("%m/%d/%Y @ %I:%M %p ") + "<br>\n")

# Open data sources and read in data
data = GetDataAsList(INPUT_DATA)

# For every user provided data entry from input file
for row in data:

	search_message = ''
	result_prefix = ''
	result_suffix = '<br>'
	item_link_prefix = ''

	# Print separation headers for DVD section
	if str(row).find("DVD--") > 0 :
		DataOutput("----------------------- DVD ----------------------- <br>")
		continue
	
	# skips any title with -- found
	if "---" in str(row):
		continue
	
	# Remove any [], apostrophes, spaces and convert to Uppercase words (via title())
	parameter = FormatTitle(row)

	# loop to check for Blu-ray and DVD
	for item_format in item_formats_list:
		publication_date = ""
		#Building link to search - Uses hard coded link, title (parameter), and item format to generate a search link
		page_link = GetSearchPageLink(parameter, item_format)

		# getting search response page
		page_response = requests.get(page_link, timeout=page_response_timeout) # 15s timeout

		#building link to display in results
		search_link = "<a href='" + page_link + "' target='_blank'>" + parameter + "</a>"
		#item_link = search_link

		#parse HTML
		page_content = GetPageContents(page_response)
		
		# select all elements associated with the title of the movie
		elements = page_content.select(TITLE_ELEMENT_MULTIPLE)
		
		# Displays the current title and format being researched to the terminal
		print ("Checking " + parameter + " (" + item_format + ")...")

		# if multiple results are found 
		if elements :			
			
			for item in elements:				

				result = item.find('a')['title']

				# gets the title part of the HTML tag (part before [])
				result_title = FormatTitle(GetTitleFromResult(result))

				# compare the title from the web results to the data title
				if result_title.find(parameter) >= 0:
					
					media_type = GetMediaFromResult(result)
					
					if not CheckResultForItemFormat(result, item_format):
						continue

					# if title is not found at the beginning of the web result
					if result_title.find(parameter,0) != 0 or len(result_title) > len(parameter):
						print("Try this: " + result_title + " for this: " + parameter)
						item_link_prefix = " - Try this"

					publication_date = GetPubDateMultiple(item)

					page_link = "https://mobi.ent.sirsi.net" + str(item.find('a')['href'])

					result_link = " - <a href='" + page_link + "' target='_blank'>" + result_title + publication_date + "</a>"

					# if the result is a DVD and the script is looking for DVD, set item link to search result link
					if media_type=="[Videorecording]" and item_format=="dvd":
						print("DVD")
						result_link = search_link 

					found = True

					search_message = search_link + item_link_prefix + result_link

					result_prefix = tab + tab + "<strong>"
					result_suffix = "</strong><br>"
					break	# breaks after first found close result. Comment out to find last close result

			if not found:
				search_message = search_link + not_found
				result_prefix = ""
		
		#if there is a single result (no elements)
		else :
			# if there is a single result, look over the page contents for the title movie tag
			item = page_content
			result = item.select(TITLE_ELEMENT_SINGLE)
			#print("single")
			if (result) :
				result = str(result[0].contents)
				
				# gets the title part of the HTML tag (part before [])
				result_title = FormatTitle(GetTitleFromResult(result))
				
				# compare the title from the web results to the data title
				if result_title.find(parameter) >= 0:
					
					media_type = GetMediaFromResult(result)
					
					if not CheckResultForItemFormat(result, item_format):
						continue

					if result_title.find(parameter,0) != 0 or len(result_title) > len(parameter):
						print("Try this: " + result_title + " for this: " + parameter)
						item_link_prefix = " - Try this"

					publication_date = GetPubDateSingle(item)

					# page_link = page_link

					result_link = " - <a href='" + page_link + "' target='_blank'>" + result_title + publication_date + "</a>"
					
					found = True

					search_message = search_link + item_link_prefix + result_link

					# exactly the same
					result_prefix = tab + tab + "<strong>"
					result_suffix = "</strong><br>"
					# exactly the same

				#if single result is found but the title is not found
				else :
					search_message = search_link + not_found
					result_prefix = ""
			
			#if no results are found
			else :
				search_message = search_link + not_found 
				result_prefix = ""
				#result_suffix = "</strong><br>"

		DataOutput("   " + tab + result_prefix + item_format + ": " + search_message + result_suffix + '\n')
		found = False
		# end - for item_format in item_formats_list:	

	DataOutput("<br>\n")

DataOutput("\n<a href='file:///H:/Coding/Python%20scripts/Movie%20lookup/movie-research.htm'>Movie Research</a><br><br>")
DataOutput("\nEnd of File\n   </body>\n</html>")
output_file.close()

