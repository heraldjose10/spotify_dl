import youtube_dl
import os
import requests
import json
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC, TRCK
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

from app import client_id, client_secret

from genius import access


# PATH = 'C:\Program Files (x86)\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--log-level=3")
# driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)


def login_spotify():
    url = 'https://accounts.spotify.com/authorize'
    para = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'https://github.com/',
        'scope': 'playlist-modify-public playlist-modify-private'
    }
    res = requests.get(url, params=para)
    driver.get(res.url)
    inputElement = driver.find_element_by_id("login-username")
    inputElement.send_keys(user)
    inp = driver.find_element_by_id("login-password")
    inp.send_keys(password)
    but = driver.find_element_by_id('login-button')
    but.send_keys("\n")
    time.sleep(5)
    u = driver.current_url

    return(u[25:])


def open_browser(user, password):
    if not os.path.exists("creds.json"):
        return(login_spotify())
    else:
        with open('creds.json', 'r') as openfile:
            logs = json.load(openfile)
        openfile.close()

        if user == logs.get('username'):
            return('exists')
        else:
            return(login_spotify())


def refresh(code):
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://github.com/'
    }
    res = requests.post(url=url, data=data, auth=(client_id, client_secret))
    res = res.json()
    print(res)
    return(res.get('access_token'), res.get('refresh_token'))


def save_refresh(r_token, username):
    user = {
        'username': username,
        'refresh_token': r_token
    }
    # tokens.append(user)
    with open("creds.json", "w") as outfile:
        json.dump(user, outfile)


def get_playlists(id, token):
    url = 'https://api.spotify.com/v1/playlists/{}/tracks?limit=50'.format(id)
    head = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }
    r = requests.get(url, headers=head)
    res = r.json()
    print(res)
    songs = []
    for i in range(len(res.get('items'))):
        print('Finding Song Info of Song {} of {}'.format(
            i+1, len(res.get('items'))))
        name = res.get('items')[i].get('track').get('name')
        artists = []
        for j in range(len(res.get('items')[i].get('track').get('artists'))):
            artists.append(res.get('items')[i].get(
                'track').get('artists')[j].get('name'))
        songs.append({
            'name': name,
            'artists': artists
        })
    print(songs)
    return(songs)


def search(name, artist):
    url = 'http://api.genius.com/search?'
    data = {
        'q': name+' '+artist,
    }
    head = {
        # 'Accept': 'application/json',
        'Authorization': 'Bearer '+access
    }
    r = requests.get(url, headers=head, params=data)
    res = (r.json())
    if res.get('response').get('hits'):
        if (res.get('response').get('hits')[0].get('result').get('title')) == name:
            return(res.get('response').get('hits')[0].get('result').get('id'))
        else:
            return(None)
    else:
        return(None)


def links(songs):
    base_url = 'https://www.youtube.com/results?search_query='
    links_list = []
    for i in songs:
        print('finding song info')
        a = '+'.join(i.get('name').split(' '))
        b = '+'.join(i.get('artists')[0].split(' '))
        # print(a)
        s_id = search(i.get('name'), i.get('artists')[0])
        links_list.append(
            {
                'url': base_url+a+'+'+b,
                'song_id': s_id
            })

    return(links_list)


def metadata(ID):
    url = 'http://api.genius.com/songs/'+str(ID)
    head = {
        'Authorization': 'Bearer '+access
    }
    r = requests.get(url, headers=head)
    res = r.json()
    if res.get('response').get('song').get('album'):
        return({
            'Title': res.get('response').get('song').get('title'),
            'Album': res.get('response').get('song').get('album').get('name'),
            'Artist': res.get('response').get('song').get('primary_artist').get('name'),
            'Album Art': res.get('response').get('song').get('header_image_url')
        })
    else:
        return({
            'Title': res.get('response').get('song').get('title'),
            'Artist': res.get('response').get('song').get('primary_artist').get('name'),
            'Album Art': res.get('response').get('song').get('song_art_image_thumbnail_url')
        })


def scrape(li):
    print('Scraping Music Links--This will take few minutes')
    # print(li)
    for vid in li:
        # print(vid)
        if vid.get('song_id'):
            meta = metadata(vid.get('song_id'))
            vid['metadata'] = meta
        else:
            vid['metadata'] = None
        driver.get(vid.get('url'))
        link = driver.find_element_by_id('thumbnail')
        vid['youtube'] = (link.get_attribute('href'))
    return(li)
    driver.close()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_file(url, name):
    # local_filename = url.split('/')[-1]
    #  the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return name


def d_l(li, folder):
    c = 1
    for i in li:

        if i.get('metadata'):
            ydl_opts = {
                'outtmpl': os.path.join('{}'.format(folder), '{}.%(ext)s'.format(i.get('metadata').get('Title'))),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join('{}'.format(folder), '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
        # print('Downloading Music Number {}'.format(c))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([i.get('youtube')])

        if i.get('metadata'):
            print('Adding Metadata')
            fname = folder+'\{}.mp3'.format(i.get('metadata').get('Title'))
            try:
                tags = ID3(fname)
            except ID3NoHeaderError:
                print("Adding ID3 header")
                tags = ID3()
            tags["TIT2"] = TIT2(encoding=3, text='{}'.format(
                i.get('metadata').get('Title')))
            tags["TALB"] = TALB(encoding=3, text=u'{}'.format(
                i.get('metadata').get('Album')))
            tags["TPE1"] = TPE1(encoding=3, text=u'{}'.format(
                i.get('metadata').get('Artist')))
            tags['TPE2'] = TPE2(encoding=3, text=u'{}'.format(
                i.get('metadata').get('Artist')))
            # audio.add(TPE2(encoding=3, text=u"aa"))   #ALBUMARTIST
            # tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
            # tags["TDRC"] = TDRC(encoding=3, text=u'2010')
            tags["TRCK"] = TRCK(encoding=3, text=u'{}'.format(c))

            tags.save(fname)

            download_file(i.get('metadata').get('Album Art'),
                          folder+'\pic'+str(c)+'.png')
            pic = (folder+'\pic'+str(c)+'.png')
            imagedata = open(pic, 'rb').read()
            id3 = ID3(fname)
            id3.add(APIC(3, 'image/png', 3, 'Front cover', imagedata))
            id3.add(TIT2(encoding=3, text='{}'.format(
                i.get('metadata').get('Title'))))

            id3.save(v2_version=3)

            os.remove(pic)

            c += 1


def a_token_from_r_token():
    with open('creds.json', 'r') as openfile:
        logs = json.load(openfile)
    ref_token = logs.get('refresh_token')
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': ref_token,
        'redirect_uri': 'https://github.com/'
    }
    res = requests.post(url=url, data=data, auth=(client_id, client_secret))
    res = res.json()
    print('ACCESS TOKEN : {}'.format(res.get('access_token')))
    return(res.get('access_token'))


print('WE DO NOT SAvE CREDs')
user = input('---spotify username---')
password = input('---spotify password---')
print('LOgginG IN Spotify')

user_code = open_browser(user, password)
print(user_code)
if user_code == 'exists':
    playlist_id = input('give playlist id:')
    path = input('download path:')
    acc_token = a_token_from_r_token()
    songs = get_playlists(playlist_id, acc_token)
    song_li = links(songs)
    to_download = scrape(song_li)
    d_l(to_download, path)
else:
    playlist_id = input('give playlist id:')
    path = input('download path:')
    acc_token, ref_token = refresh(user_code)
    print(acc_token, ref_token)
    save_refresh(ref_token, user)
    songs = get_playlists(playlist_id, acc_token)
    song_li = links(songs)
    to_download = scrape(song_li)
    d_l(to_download, path)
