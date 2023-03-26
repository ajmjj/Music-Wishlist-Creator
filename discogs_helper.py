import discogs_client
import webbrowser
import configparser
from alive_progress import alive_bar
import re

config = configparser.ConfigParser()

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['Discogs']['consumer_key'] 
consumer_secret = config['Discogs']['consumer_secret']
access_token = config['Discogs']['access_token']
access_secret = config['Discogs']['access_secret']

# Discogs user agent
user_agent = 'Telespoks/1.0'

# Static Oauth endpoints
authorize_url = 'https://www.discogs.com/oauth/authorize'
access_token_url = 'https://api.discogs.com/oauth/access_token'

def auth():
    global access_token
    global access_secret
    
    if access_token == '' or access_secret == '':
        print('\nNo access token or secret found, authorizing...')
    # Get auth Url
        client = discogs_client.Client(user_agent,consumer_key,consumer_secret)
        req_token,req_secret,auth_url = client.get_authorize_url()

        # Open authorization URL in browser
        webbrowser.open(auth_url)

        # Get verifier pin from user
        oauth_verifier = input('\nEnter the code shown in the browser: ')

        # Get access token
        access_token,access_secret = client.get_access_token(oauth_verifier)

        # Save access token and secret
        config['Discogs']['access_token'] = access_token
        config['Discogs']['access_secret'] = access_secret

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        greet_user(client)

        return client

    else:
        print('Access token and secret found')
        # Create Client Object
        client = discogs_client.Client(user_agent,consumer_key,consumer_secret,access_token,access_secret)
        
        greet_user(client)
        return client


def greet_user(client):
    me = client.identity()
    print('Logged in to Discogs as: ' + me.username)

def get_wantlist(client):
    print('\nGetting wantlist from Discogs...')
    wantlist_res = client.identity().wantlist
    wantlist = []
    print('Found ' + str(wantlist_res.count) + ' items in your wantlist')
    print('\nProcessing wantlist data...')
    with alive_bar(len(wantlist_res)) as bar:
        regex = r"\(\d+\)"
        for wantlistItem in wantlist_res: # todo -> waste of time? could be skipped and used later
            id = wantlistItem.release.id # necessary?
            # Set title, artist, label, catno, year, url
            # title = wantlistItem.release.title.strip()
            title = wantlistItem.data['basic_information']['title'].strip()
            # artist = wantlistItem.release.artists[0].name.strip()
            artist = wantlistItem.data['basic_information']['artists'][0]['name'].strip()
            # Check if artist name ends with (number) and remove it
            if artist.endswith(')') and re.search(regex,artist): 
                artist = re.sub(regex, "", artist).strip() # remove (x) from artist name
            # label = wantlistItem.release.labels[0].name.strip()
            label = wantlistItem.data['basic_information']['labels'][0]['name'].strip()
            # Check if label name ends with (number) and remove it
            if label.endswith(')') and re.search(regex,label):
                 label = re.sub(regex, "", label).strip() # remove (x) from label name
            # catno = wantlistItem.release.data['labels'][0]['catno'].strip()
            catno = wantlistItem.data['basic_information']['labels'][0]['catno'].strip()
            # year = wantlistItem.release.data['year']
            year = wantlistItem.data['basic_information']['year']
            # url = wantlistItem.release.url
            url = f'https://www.discogs.com/release/{id}'
            wantlist.append(DiscogsItem(id, title, artist, label, catno, year, url))
            bar()
    return(wantlist)

def sort_by_label(wantlist):
    wantlist = sorted(wantlist, key=lambda item: item.label)
    return wantlist



class DiscogsItem:
    def __init__(self, id, title, artist, label, catno, year, url):
        self.id = id
        self.title = title
        self.artist = artist
        self.label = label
        self.catno = catno
        self.year = year
        self.url = url