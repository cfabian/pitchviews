import requests as req
import json
import sys

import genres

def getReview(reviewLink):
    url = "https://pitchfork.com/api/v2" + reviewLink
    res = req.get(url)
    if (res.ok):
        data = json.loads(res.text)
        rating = data["results"][0]["tombstone"]["albums"][0]["rating"]["rating"]
        print(rating)

def getReviews(artistLink):
    url = "https://pitchfork.com/api/v2/entities" + artistLink
    res = req.get(url)
    if (res.ok):
        data = json.loads(res.text)
        count = data["content"]["albumreviews"]["count"]
        print(count)
        if count > 0:
            for i in range(0, count):
                reviewLink = data["content"]["albumreviews"]["items"][i]["url"]
                print(reviewLink)
                getReview(reviewLink)

def getArtistLinks(genre, count):
    print(count)
    for i in range(0, count):
        url = "https://pitchfork.com/api/v2/search/?sort=name%20asc&types=musicgroups&status=published&hierarchy=genres%2F" + genre + "&size=1&start=" + str(i)
        res = req.get(url)
        if (res.ok):
            data = json.loads(res.text)
            # print(json.dumps(data, indent=4, separators=(',', ': ')))
            artistLink = data["results"]["list"][0]["url"]
            print(artistLink)
            getReviews(artistLink)

def getHtml():
    for genre in  genres.genres:
        url = "https://pitchfork.com/api/v2/search/?sort=name%20asc&types=musicgroups&status=published&hierarchy=genres%2F" + genre + "&size=1&start=0"
        res = req.get(url)
        if (res.ok):
            data = json.loads(res.text)
            # print(json.dumps(data, indent=4, separators=(',', ': ')))
            # print(data["count"])
            getArtistLinks(genre, data["count"])
            
        else:
            print("error getting html")
            
getHtml()
    