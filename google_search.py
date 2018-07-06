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

res = google_search("Elektabilitas Ridwan Kamil Turun")

print(len(res))
print(res['items'][0]['title'])

for i in range(len(res)):
    d = jellyfish.jaro_distance(u'Elektabilitas Ridwan Kamil Turun',res['items'][i]['title'])
    print(d)
    print(res['items'][i]['title'])