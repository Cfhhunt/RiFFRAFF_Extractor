import requests
import os
import re
from bs4 import BeautifulSoup
from csv import writer


# Take in song link, save to folder
def save_song(song_link):
    songResponse = requests.get(song_link)
    songSoup = BeautifulSoup(songResponse.text, 'html.parser')
    songTitle = songSoup.find("div", {"class": "ringtone"}).find_next('b').contents[0]
    print(songTitle.text)


artistHTML = 'https://www.azlyrics.com/r/riffraff.html'
response = requests.get(artistHTML)
soup = BeautifulSoup(response.text, 'html.parser')

# Get artist name
artistName = re.sub('.html', '', artistHTML)
artistName = re.sub('https://www.azlyrics.com/r/', '', artistName)

# Make directory for files if it doesn't already exist
if not os.path.exists(artistName):
    os.mkdir(artistName)

# Get the div that contains all albums and songs
albums = soup.find(id="listAlbum")

# Get rid of script tags, they aren't needed
[s.extract() for s in albums('script')]

save_song('https://www.azlyrics.com/lyrics/riffraff/dontwait.html')

for song in albums.find_all('a', href=True):
    song_link = song['href']
    # Fix the url
    song_link = 'http://www.azlyrics.com/lyrics' + song_link.split('lyrics')[-1]
    save_song(song_link)
