import requests
from app import client_id,client_secret


def refresh(code):
    url='https://accounts.spotify.com/api/token'
    data={
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : 'https://github.com/'
    }
    res=requests.post(url=url,data=data,auth = (client_id, client_secret))
    res=res.json()
    return(res.get('access_token'),res.get('refresh_token'))
