#! python 3
# blu-search.py

import requests
import csv
import datetime
from bs4 import BeautifulSoup
import string
import re

def FormatTitle(unformatted):

	# removes all punctuation
	formatted = unformatted.translate(str.maketrans('', '', string.punctuation))
	
	# removes any extra spaces
	formatted = " ".join(formatted.split())
	
	# converts to Title (each work capitalized)
	formatted = formatted.title()

	# Removes "The" from the data file title
	if formatted[0:3] == "The":
		formatted = formatted[4:]
	
	return formatted

def GetTitleFromResult(result):
	
	# Removes the format from the title
	regex = "\[[^\[.\]]*\]"

	title = re.sub(regex, "", str(result))

	return title

def GetMediaFromResult(result):
	return result[result.find(" ["):].title()

def GetSearchPageLink():

	search_page_link = "%s%s%s" % ('https://mobi.ent.sirsi.net/client/en_US/default/search/results?qu=', parameter.replace(' ', '+'), '+' + item_format + '&te=&te=ILS')

	return search_page_link

def GetPubDate(result):
	pubdate = result.find_all('div', {'class': ['displayElementText text-p highlightMe PUBDATE']})
	if pubdate:
		pubdate = " (" + pubdate[0].text.strip() + ")"
	else:
		pubdate = ""
	
	return pubdate

def GetPageContents(response):

	return BeautifulSoup(response.text, 'html.parser')

# --------------------------------------------------------------

now = datetime.datetime.now()
page_response_timeout = 15
tab = "&nbsp;&nbsp;&nbsp;"
search_message = ''
not_found = " not found"
found = False
result_prefix = ''
result_suffix = ''
title_element_multiple = '.detailLink'
title_element_single = 'div.text-p.INITIAL_TITLE_SRCH'
pubdate_element = '.highlightMe.PUBDATE'

file_path = "//192.168.1.101/alan/Coding/Python scripts/"

output_file = open(file_path + "movie-links.htm", "w") # w for write, a for append
#output_file_debug = open(file_path + "debug.txt", "w", encoding="utf-8")

html_header = "<html>\n   <head>\n      <title>Mobile Public Library Python automated Bluray and DVD lookup</title>\n   </head>\n   <body style='line-height: 1.5em'>\n"

output_file.write(html_header + "   " + now.strftime("%m/%d/%Y") + "<br>\n")

input_file = file_path + "movies.csv"
#input_file = file_path + "movies_test.csv"

# Open data files and read in CSV data
data_file = open(input_file)
data_reader = csv.reader(data_file)
data = list(data_reader)
item_formats_list = ['blu','dvd']

# For every user provided data entry from input file
for row in data:

	search_message = ''
	result_prefix = ''
	result_suffix = '<br>'

	# Print separation headers for DVD section
	if str(row).find("DVD--") > 0 :
		output_file.write("----------------------- DVD ----------------------- <br>")
		continue
	
	# skips any title with -- found
	if "---" in str(row):
		continue
	
	# Remove any [], apostrophes, spaces and convert to Uppercase words (via title())
	parameter = FormatTitle(str(row))

	# loop to check for Blu-ray and DVD
	for item_format in item_formats_list:
		
		#Building link to search
		page_link = GetSearchPageLink()

		# getting search response page
		page_response = requests.get(page_link, timeout=page_response_timeout) # 15s timeout

		#building link to display in results
		result_link = "<a href='" + page_link + "' target='_blank'>" + parameter + "</a>"
		item_link = result_link

		#parse HTML
		page_content = GetPageContents(page_response)
		
		# select all elements associated with the title of the movie
		elements = page_content.select('.results_bio') # (title_element_multiple)
		
		# Displays the current title and format being researched to the terminal
		print ("Checking " + parameter + " (" + item_format + ")...")

		# if multiple results are found 
		if (len(elements) > 0) :			
			
			publication_date = ""
			
			for idx, result in enumerate(elements):				
				
				publication_date = GetPubDate(result)

				result_title = result.find('a')['title']
				
				# gets the title part of the HTML tag (part before [])
				web_title = FormatTitle(GetTitleFromResult(result_title))
	
				# compare the title from the web results to the data title
				if web_title.find(parameter) >= 0:
					
					media_type = GetMediaFromResult(result_title)
					
					if media_type.title().find("Blu") > 0 and item_format == "dvd":
						#print ("found bluray, looking for DVD")
						continue

					if media_type.find("Season") > 0:
						print ("------------- TV ------------------ " + parameter)
						continue
					
					# if title is found at the beginning of the web result
					if web_title.find(parameter,0) == 0:
						# print("found")
						# print(str(result.find('a')['href']))
						item_link = "<a href='https://mobi.ent.sirsi.net" + str(result.find('a')['href']) + \
								"' target='_blank'>" + web_title + publication_date + "</a>"
					# if title is found but not at the beginning of the result
					else:
						print("try this")
						item_link = "Try this - <a href='https://mobi.ent.sirsi.net" + str(result.find('a')['href']) + \
								"' target='_blank'>" + web_title + publication_date + "</a>"
					
					# if the result is a DVD and the script is looking for DVD, set item link to search result link
					if media_type=="[Videorecording]" and item_format=="dvd":
						print("DVD")
						item_link = result_link

					search_message =  item_format + ": " + result_link + " - " + item_link
					result_prefix = tab + tab + "<strong>"
					result_suffix = "</strong><br>"
					found = True
					
					# break


			if not found:
				search_message = item_format + ": " + result_link + not_found
				result_prefix = ""
		
		#if there is a single result
		else :
			# if there is a single result, look over the page contents for the title movie tag
			element = page_content.select(title_element_single)

			# if the title movie tag is found 
			if (element) :

				# compare just the title from the web results to the data title after removing any punctionation marks, etc
				if(str(element[0].contents)[0:str(element[0].contents).find(" [")].translate(str.maketrans('', '', string.punctuation)).title().find(parameter) >= 0) :

					if not page_content.select(".text-p.PUBLICATION_INFO"):
						#print("No pub date found")
						publication_date = ""
					else:
						publication_date = " (" + re.search('\d{4}', str(page_content.select(".text-p.PUBLICATION_INFO")))[0] + ")"
					
					search_message = item_format + ": " + result_link + " - <a href='" + page_link + "' target='_blank'>" + parameter + publication_date + "</a>"
					result_prefix = tab + tab + "<strong>"
					result_suffix = "</strong><br>"
				
				#if single result is found but the title is not found
				else :
					search_message = item_format + ": " + result_link + not_found
					result_prefix = ""
			
			#if no results are found
			else :
				search_message = item_format + ": " + result_link + not_found 
				result_prefix = ""
				#result_suffix = "</strong><br>"
		
		output_file.write ("   " + tab + result_prefix + search_message + result_suffix + '\n')
		found = False
		
	output_file.write ("<br>\n")
output_file.write("\n<a href='file:///H:/Coding/Python%20scripts/movie-research.htm'>Movie Research</a><br><br>")
output_file.write("\nEnd of File\n   </body>\n</html>")
output_file.close()

