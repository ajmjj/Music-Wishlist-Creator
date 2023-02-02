import datetime

def get_date():
    # Get current date and time
    now = datetime.datetime.now()
    # Format date and time
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    return date

def write_wishlist_to_file(wishlist):
    # Open file
    with open(f'slsk wishlist - {wishlist.date}.txt', 'w') as f:
        # Write wishlist to file
        f.write("Updated on: " + wishlist.date)

        # Write Discogs items to file
        f.write("\n\nDiscogs items:\n")
        for item in wishlist.discogs_items:
            f.write(f"[{item.catno}] {item.artist} - {item.title} ({item.year})\n")
        
        # Write Bandcamp items to file
        f.write("\n\nBandcamp items:\n")
        for item in wishlist.bandcamp_items:
            f.write(f"{item.artist} - {item.title}\n")





class Wishlist:
    def __init__(self, date, discogs_items, bandcamp_items):
        self.date = date
        self.discogs_items = discogs_items
        self.bandcamp_items = bandcamp_items

    def __str__(self):
        return f'Wishlist created on {self.date}. Contains {len(self.discogs_items)} Discogs items and {len(self.bandcamp_items)} Bandcamp items.'
