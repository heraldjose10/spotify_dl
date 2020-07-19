import requests
import webbrowser
from spotify_app import client_id

def open_browser():
    url='https://accounts.spotify.com/authorize'
    para={
        'client_id' : client_id,
        'response_type' : 'code',
        'redirect_uri' : 'https://github.com/',
        'scope' : 'playlist-modify-public playlist-modify-private'
    }
    res=requests.get(url,params=para)
    webbrowser.open(res.url,new=1)