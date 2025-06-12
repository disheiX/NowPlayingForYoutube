from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from get_data import get_data, get_wrapper
import re
from requests_html import HTMLSession


# handle, pid = 1247884, 4652
# wrapper = get_wrapper(handle, pid)
# data = get_data(wrapper)

def get_img(data):
    if data == None:
        return None
    url = f'https://img.youtube.com/vi/{data[1]}/mqdefault.jpg'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # Resizing and cropping img
    new_width = int(128 * (img.width / img.height))
    left = (new_width - 128)/2
    right = (new_width + 128)/2 -1
    img = img.resize((new_width, 128), Image.ANTIALIAS)
    img = img.crop((left, 0, right, 128))
    return img


def get_metadata(data):
    url = f'https://www.youtube.com/watch?v={data[1]}'
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "lxml")
    text_soup = str(soup)
            
    try: 
        pattern = re.compile('(?<=videoAttributeViewModel).*(?=,"orientation)')
        metadata = pattern.findall(text_soup)[0]
        song = re.search('"title":"(.+?)","subtitle"', metadata).group(1)
        artist = re.search('"subtitle":"(.+?)","secondarySubtitle"', metadata).group(1)
        return [song, artist]
    except:
        return None
