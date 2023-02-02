import os
import configparser

from bs4 import BeautifulSoup
import discogs_helper as discogs
import bandcamp_helper as bandcamp
import main_helper as main

# Clear console
os.system('cls' if os.name == 'nt' else 'clear')


print('================================================================================')
print('                                Discogs Init')
print('================================================================================')
# Create discogs client
discogs_client = discogs.auth()

discogs_wantlist = discogs.get_wantlist(discogs_client)
discogs_wantlist = discogs.sort_by_label(discogs_wantlist)

print()
print('================================================================================')
print('                                Bandcamp Init')
print('================================================================================')

# Set bandcamp username
bandcamp_username = bandcamp.auth()

# Print bandcamp username
bandcamp.greet_user(bandcamp_username)

# Create soup object of wishlist page
soup = bandcamp.get_soup(bandcamp_username)

# Get number of wishlist items from soup object
num_wishlist_items = bandcamp.get_num_wishlist_items(soup)

# Get fan id from soup object
fan_id = bandcamp.get_fan_id(soup)

# Get all wishlist items (as json) from bandcamp GET request
wishlist_json = bandcamp.get_wishlist_items(fan_id, num_wishlist_items)
bandcamp_wishlist_items = bandcamp.get_items_from_json(wishlist_json)


# Check number of scraped wishlist items is equal to number of items indicated
assert len(bandcamp_wishlist_items) == int(num_wishlist_items)


print()
print('================================================================================')
print('                               Creating Wishlist')
print('================================================================================')
# Get current date 
date = main.get_date()

# Create wishlist object
wishlist = main.Wishlist(date, discogs_wantlist, bandcamp_wishlist_items)

# Write wishlist to file
main.write_wishlist_to_file(wishlist)

print("wishlist created")