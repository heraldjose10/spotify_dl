import requests
import json
 

def get_playlists(id,token):
    url='https://api.spotify.com/v1/playlists/{}/tracks?limit=50'.format(id)
    head={
        'Content-Type' :'application/json',
        'Authorization' :'Bearer {}'.format(token)
    }
    r=requests.get(url,headers=head)
    res=r.json()
    songs=[]
    for i in range(len(res.get('items'))):
        # print('Finding Song Info of Song {} of {}'.format(i+1,len(res.get('items'))))
        name=res.get('items')[i].get('track').get('name')
        artists=[]
        for j in range(len(res.get('items')[i].get('track').get('artists'))):
            artists.append(res.get('items')[i].get('track').get('artists')[j].get('name'))
        songs.append({
            'name':name,
            'artists':artists
        })
        
    return(songs)
    