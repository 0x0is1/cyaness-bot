import requests
from bs4 import BeautifulSoup as scraper
URL='https://explosm.net/comics/'

def get_image_url(comic_index):
  response=requests.get(url=URL+str(comic_index))
  if 'Could not find comic' in str(response.content):
    get_image_url(comic_index+1)
  else:
    soup = scraper(response.content, 'html.parser')
    image_url = soup.find('img', {'id': 'main-comic'}).get('src')
    return 'https:' + str(image_url).split('?')[0]
    
