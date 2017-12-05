import boto3
from boto3.dynamodb.conditions import Key, Attr
import os.path
from bs4 import BeautifulSoup

dynamodb = boto3.resource('dynamodb')

def writeToFile(obj, fname):
    line = '"' + str(obj['artistNameAlbumName']) + '","' \
               + str(obj['artistName']) + '","' \
               + str(obj['albumName']) + '","' \
               + str(obj['albumReleaseYear']) + '","' \
               + str(obj['genre']) + '","' \
               + str(obj['authorName']) + '","' \
               + str(obj['publishDate']) + '","' \
               + str(obj['title']) + '","' \
               + str(obj['rating']) + '","' \
               + str(BeautifulSoup(obj['body'], 'html.parser').get_text().replace('\n', '').replace('"', '""')) + '","' \
               + str(obj['url']) + '","' \
               + str(obj['viewCount']) + '","' \
               + str(obj['ytUrl']) + '"\n'
               
    with open(fname, 'a') as f:
        f.write(line)

def getTableData(tableName):
    numComplete = 0
    table = dynamodb.Table(tableName)
    
    res = table.scan()
    data = res['Items']
    for obj in data:
        writeToFile(obj, 'pitchforkReviews.csv')
        
    numComplete += len(data)
    print(numComplete)
    
    while res.get('LastEvaluatedKey'):
        res = table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
        data = res['Items']
        for obj in data:
            writeToFile(obj, 'pitchforkReviews.csv')
            
        numComplete += len(data)
        print(numComplete)
                
def createCSV():
    
    if not os.path.isfile('pitchforkReviews.csv'):
        with open('pitchforkReviews.csv', 'w+') as f:
            f.write('artistNameAlbumName,artistName,albumName,albumReleaseYear,genre,reviewAuthor,reviewPublishDate,reviewTitle,reviewRating,reviewBody,reviewUrl,YouTubeViewCount,YouTubeUrl\n')
        
    getTableData('pitchfork_reviews')
    
createCSV()