import requests
from bs4 import BeautifulSoup as scraper
import random
URL='https://explosm.net/comics/'

def get_image_url():
  response=requests.get(url=URL+str(random.randint(39, 5010)))
  if 'Could not find comic' in str(response.content):
    get_image_url()
  
  else:
    soup = scraper(response.content, 'html.parser')
    image_url = soup.find('img', {'id': 'main-comic'}).get('src')
    return 'https:' + str(image_url).split('?')[0]
    
