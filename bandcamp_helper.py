import requests
from bs4 import BeautifulSoup
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')

def auth():
    bandcamp_username = config['Bandcamp']['username'] 

    # If no username is found, ask for one
    if bandcamp_username == '':
        bandcamp_username = input('Enter your Bandcamp username: ')
        config['Bandcamp']['username'] = bandcamp_username

        with open('config.ini', 'w') as configfile:
                config.write(configfile)

    return bandcamp_username


def greet_user(username):
    print(f"Bandcamp username: {username}")

def get_soup(username):
    bandcamp_url = f"https://bandcamp.com/{username}/wishlist"
    res = requests.get(bandcamp_url)
    soup = BeautifulSoup(res._content, "html.parser")
    return soup

def get_num_wishlist_items(soup):
    li = soup.find("li", {"data-tab": "wishlist"})
    num_items = li.find("span", {"class": "count"}).text
    return num_items

def get_fan_id(soup):
    fan_id = soup.find("button", {"class": "follow-unfollow"})['id'].replace('follow-unfollow_', '')
    return fan_id

def get_wishlist_items(fan_id, num_items):
    url = "https://bandcamp.com/api/fancollection/1/wishlist_items"
    current_time = int(time.time())
    body = {
        "fan_id": fan_id,
        "older_than_token": f"{current_time}::a::",
        "count": num_items
    }
    res = requests.post(url, json=body)
    return res.json()

def get_items_from_json(wishlist_dict):
    wishlist_items = []
    for item in wishlist_dict["items"]:
        # print(item)
        item_title = item.get("item_title")
        item_artist = item.get("band_name")
        item_url = item.get("item_url")
        wishlist_items.append(BandcampItem(item_title, item_artist, item_url))
    return wishlist_items

def get_list_items(soup):
    # Filter to wishlist-grid
    wishlist_grid = soup.find("div", {"id": "wishlist-grid"})
    # Get collection grid
    collection_grid = wishlist_grid.find("ol", {"class": "collection-grid"})
    # Get list items
    list_items_raw = collection_grid.find_all("li", {"class": "collection-item-container"})
    return list_items_raw

# def get_first_20(soup):
#     # Filter to wishlist-grid
#     wishlist_grid = soup.find("div", {"id": "wishlist-grid"})
#     # Get collection grid
#     collection_grid = wishlist_grid.find("ol", {"class": "collection-grid"})
#     # Get list items
#     list_items_raw = collection_grid.find_all("li", {"class": "collection-item-container"})
    
#     list_items = []
#     for item in list_items_raw:
#         collection_title_details = item.find("div", {"class": "collection-title-details"})
#         item_url = collection_title_details.find("a", {"class": "item-link"})['href']
#         item_title = collection_title_details.find("div", {"class": "collection-item-title"}).text
#         item_artist = collection_title_details.find("div", {"class": "collection-item-artist"}).text.replace('by ', '')
#         list_items.append(BandcampItem(item_title, item_artist, item_url))

#     return list_items


# Classes:
class BandcampItem:
    def __init__(self, title, artist, url):
        self.title = title
        self.artist = artist
        self.url = url

    def __str__(self):
        return f"BandcampItem(title={self.title}, artist={self.artist}, url={self.url})"