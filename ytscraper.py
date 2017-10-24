import requests as req
import json
import sys
import re

def getViews(playlist):
    url = "https://www.youtube.com" + playlist
    print(url)
    res = req.get(url)
    if (res.ok):
        viewCount = res.text[res.text.find("views")-20:res.text.find(" views")]
        n = re.search("\d", viewCount)
        if n:
            viewCount = viewCount[n.start():]
            print(viewCount)
            
        else:
            print("Couldn't find view count")

def makeUrl(title):
    url = "https://www.youtube.com/results?search_query="
    playlistTag = "&sp=EgIQA1AU"
    newTitle = "+".join(title.split())
    return url + newTitle + playlistTag

def search(title):
    print(makeUrl(title))
    res = req.get(makeUrl(title))
    if (res.ok):
        playlist = res.text[res.text.find("/playlist?list="):res.text.find("View full playlist") + 50]
        playlist = playlist[:playlist.find('"')]
        # print (playlist)
        getViews(playlist)
        
def readReviews():
    fname = "reviews.json"
    with open(fname, 'r') as f:
        reviews = json.load(f)
        print(reviews[0])
        
readReviews()
    
# title = "sun ra and his arkestra the magic city"
# search(title)