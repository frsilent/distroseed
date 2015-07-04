#!/usr/bin/env python

import os
import urllib
import requests
from BeautifulSoup import BeautifulSoup

url = "http://distrowatch.com/index.php?distribution=all&release=all&month=all&year=2015"
response = requests.get(url)
page = str(BeautifulSoup(response.content))
start_link = page.find("a href")
list = []
downloadlist = []


# strip the links from the page
def getURL(page):
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

while True:
    url, n = getURL(page)
    page = page[n:]
    if url:
        list.append(url)
    else:
        break

# filter down to only links that endwith .torrent
# TODO: might exclude links that have variables at the end
links = filter(lambda x:x.endswith(".torrent"), list)

# download the torrent link
def download(url):
        print "Downloading %s ..." % url
	webFile = urllib.urlopen(url)
	localFile = open(os.getcwd() + "/torrents/" + url.split('/')[-1], 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()

# make sure we don't already have the torrent file
for url in links:
    if not os.path.isfile(os.getcwd() + "/torrents/" + url.split('/')[-1]):
        downloadlist.append(url)
    else:
        print "Skipping %s ... Already downloaded." % url.split('/')[-1]

# download missing torrent files
for link in downloadlist:
    download(link)
