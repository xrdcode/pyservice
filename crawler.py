import json
from googleapiclient.discovery import build
import jellyfish

GOOGLE_API_URL = 'www.googleapis.com'
EP_CUSTOM_SEARCH = '/customsearch/v1'
API_KEY = 'AIzaSyCdJFglC79BvNr1XS86MaumesQxeQC45_k'
CX_ID = '014928072251006124045:dp7g_kwwlag'

def google_search(q="", **kwargs):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=q, cx=CX_ID, **kwargs).execute()
    return res

##This func will crawl the image title
def crawler(text_to_search="", depth=1):
    result = []
    for i in range(depth):
        start = 1
        tmp = google_search('intitle:"'+text_to_search+'"', num=10, start=start)
        for j in range(len(tmp['items'])):
            tmpDict = {}
            d = jellyfish.jaro_distance(text_to_search,tmp['items'][j]['title'])
            tmpDict['score'] = d
            tmpDict['compared_text'] = tmp['items'][j]['title']
            result.append(tmpDict)
        start += 10
        if(tmp['queries']['request'][0]['count'] < 10):
            break
    return result

# example uncomment below
# res = crawler(text_to_search="Jokowi")
# print((res))
