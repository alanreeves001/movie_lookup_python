#! python 3
# movies.py
# Script to search for movies being released to DVD (via DVDReleaseDates.com)
# and eventually combining them into a CSV to lookup at the library

import requests
import csv
import datetime
from bs4 import BeautifulSoup
import string
import json

from db import db


outputFileName = 'movie-research.htm'
movieListFileName = 'movies.csv'

# --------------------------------------------------------------------------
# take in URL, returns BeautifulSoup HTML object
def getPage (url) :
    page = requests.get(url, timeout=10)

    pageContent = BeautifulSoup(page.text, 'html.parser')
    return pageContent

# --------------------------------------------------------------------------
# # Takes in movie name (formatted, spaces replaced with underscore) and searches Rotten Tomatoes
# Should return rating, number of results, link, etc
def getRT (movieInput):
    pageRT = getPage("https://www.rottentomatoes.com/search?search=" + movieInput.lower())
    print( movieInput.lower())
    movieList = pageRT.find_all('search-page-media-row') #, id='movies-json')
    print (movieList)
    json_movieList = json.loads(movieList)

    if (len(json_movieList['items']) < 1):
        return False

    # print(json.dumps(json_movieList, indent=4))

    for movie in json_movieList['items']:
        try:
            movieName = movie['name']
            movieYear = movie['releaseYear'] 
            movieScore = movie['tomatometerScore']['score']
            movieAudienceScore = movie['audienceScore']['score']
            movieURL = movie['url']

            if (int(movieYear) < currentYear):
                continue
            
            if (movieInput != movieName):
                continue

            # return (f'{movieName} ({movieYear}) - <a href=\"{movieURL}\">RT: {movieScore}</a>')
            return (f'<a href=\"{movieURL}\" target=\"_new\">RT: {movieScore} - Audience: {movieAudienceScore}</a>')
        except:
            continue
        
    # return movie_list

def openOutputFile(filename):
    output_file = open(filename, "w") # w for write, a for append

    html_header = "<html>\n   <head>\n      <title>DVD Releases</title>\n   </head>\n   <body style='line-height: 1.5em'>\n"

    output_file.write(html_header + "   " + now.strftime("%m/%d/%Y") + "<br>\n")

    return output_file

# def openMovieListFile(filename):
#     dataFile = open(filename)
#     # dataReader = csv.reader(dataFile)
#     # data = list(data_reader)    

#     return dataFile

def checkMovieListFile(movieDataObject, movie):
    with open(movieDataObject) as f:
        if movie in f.read():
            return True
        else:
            return False

# ======================================================================================================
now = datetime.datetime.now()

URL = 'https://www.dvdsreleasedates.com/releases/'
urlBase = 'https://www.dvdsreleasedates.com'

currentYear = now.year
currentMonth = now.month

year = currentYear
month = currentMonth

pageLimit = 4

output_file = openOutputFile(outputFileName)
# movieDataObj = openMovieListFile(movieListFileName)

# loop through each month for movies
for pageCount in range(0, pageLimit):
    
    # formats URL for movie list lookup by month
    movieListURL = URL + str(currentYear) + '/' + str(currentMonth) + '/'

    pageContent = getPage(movieListURL)

    # filters the page contents to get to the movie lists by date/week
    movieList = pageContent.find_all('table', class_="fieldtable-inner")

    # Check to see if there are no results for the current month/week
    if (len(movieList) <= 0):
        print ('No results')

    # Each release date is represented by a row/result
    for row in movieList:
        date = row.find('td', class_='reldate').text
        
        # print the date for the relase week
        # print("\n" + date.split(', ')[0].split(' ')[1] + ' ' + date.split(', ')[0].split(' ')[2] + '\n')
        output_file.write('<br>\n' + date.split(', ')[0].split(' ')[1] + ' ' + date.split(', ')[0].split(' ')[2] + '<br>\n')


        # within the row result, iterate through various movie cells
        for movie in row.find_all('td', {"class": "dvdcell"}):

            movieName = movie.find('a',{"style": "color:#000;"}).text.title()

            # pulls RottenTomatoes search for that movie
            #movieListRT = getRT(movieName)
            movieListRT = ""

            # formats individual movie URL for research
            movieURL = urlBase + movie.find('a',{"style": "color:#000;"}).get('href')
            imdb = movie.find('td', class_='imdblink').text

            if (checkMovieListFile(movieListFileName, movieName)):
                movieMarkupPrefix = "<strong>"
                movieMarkupSuffix = "</strong>"
            else:
                movieMarkupPrefix = ""
                movieMarkupSuffix = ""

            if (movieListRT != False):
                
                print('Researching ' + movieName)
                output_file.write("   " + movieMarkupPrefix + movieName + movieMarkupSuffix + ' - <a href=\"' + movieURL + '\" target=\"_new\">imdb: ' + imdb.split(' ')[1] + '</a> ' + str(movieListRT) + '<br>\n')
                # print()

    
    currentMonth = currentMonth + 1

    if (currentMonth >12):
        currentMonth = 1
        currentYear = currentYear + 1
    
output_file.write("\nEnd of File\n   </body>\n</html>")
output_file.close()
