import datetime
import pyperclip as pc

def get_user_intention():
    res = input('Do you want to [r]un the program or [c]hange settings?: ')
    if res.strip().lower() == 'r':
        return 'run'
    elif res.strip().lower() == 'c':
        return 'change'
    else:
        print('Invalid input. Please try again.')
        get_user_intention()

        
def get_date():
    # Get current date and time
    now = datetime.datetime.now()
    # Format date and time
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    return date

def write_wishlist_to_file(wishlist, download_folder):
    wishlist_str = wishlist_to_string(wishlist)
    # Open file
    with open(download_folder,f'slsk wishlist - {wishlist.date}.txt', 'w') as f:
        # Write wishlist to file
        f.write("Updated on: " + wishlist.date + "\n\n")

        # Write Discogs items to file
        f.write(wishlist_str)


def query_output_type():
    res = input('[w]rite wishlist to file or [c]opy to clipboard?: ')
    if res.strip().lower() == 'w':
        return 'file'
    elif res.strip().lower() == 'c':
        return 'clipboard'
    else:
        print('Invalid input. Please try again.')
        query_output_type()

def copy_wishlist_to_clipboard(wishlist):
    wishlist_str = wishlist_to_string(wishlist)
    pc.copy(wishlist_str)

def wishlist_to_string(wishlist):
    # Init wishlist string
    wishlist_str = ''
    # Add discogs items to wishlist string
    wishlist_str += 'Discogs items:\n'
    wishlist_str += '--------------------------------------------------------------------- \n'
    for item in wishlist.discogs_items:
        wishlist_str += f"[{item.catno}] {item.artist} - {item.title} ({item.year})\n"
        wishlist_str += f"  {item.url}\n\n"
    # Add bandcamp items to wishlist string
    wishlist_str += '\n\nBandcamp items:\n'
    wishlist_str += '--------------------------------------------------------------------- \n'
    for item in wishlist.bandcamp_items:
        wishlist_str += f"{item.artist} - {item.title}\n"
        wishlist_str += f"  {item.url}\n\n"
    return wishlist_str

def output_wishlist(wishlist, output):
    if output == 'file':
        # Write wishlist to file
        write_wishlist_to_file(wishlist, output)
        print(f'Wishlist written to file: slsk wishlist - {wishlist.date}.txt')

    elif output =='clipboard':
        # Copy wishlist to clipboard
        copy_wishlist_to_clipboard(wishlist)
        print('Wishlist copied to clipboard.')



        
class Wishlist:
    def __init__(self, date, discogs_items, bandcamp_items):
        self.date = date
        self.discogs_items = discogs_items
        self.bandcamp_items = bandcamp_items

    def __str__(self):
        return f'Wishlist created on {self.date}. Contains {len(self.discogs_items)} Discogs items and {len(self.bandcamp_items)} Bandcamp items.'
