import requests
import json
 

def get_playlists(id,token):
    url='https://api.spotify.com/v1/playlists/{}/tracks?limit=10'.format(id)
    head={
        'Content-Type' :'application/json',
        'Authorization' :'Bearer {}'.format(token)
    }
    r=requests.get(url,headers=head)
    res=r.json()
    songs=[]
    for i in range(len(res.get('items'))):
        name=res.get('items')[i].get('track').get('name')
        artists=[]
        for j in range(len(res.get('items')[i].get('track').get('artists'))):
            artists.append(res.get('items')[i].get('track').get('artists')[j].get('name'))
        songs.append({
            'name':name,
            'artists':artists
        })
        
    return(songs)
    # with open("sample.json", "w") as outfile: 
    #     outfile.write(json.dumps(res))

# def main():
    # get_playlists('37i9dQZF1CAqIft9opEgvG','BQD00EWLAQHaNeLcMhqMOLejKfwFXtulGINjaU0AHjOUXtudP-sscyyMffq9lL06fZ6yfh6TEuWQhBlnOu619LB1oLkfjsRSVLgvT2JOCjtSu3pvvN4KZ0Dl2iqMu-J3z6uFCtbaK96qfqgOy36MS4PHCrd3tfemaUEfbKGCyrBORYUgcIkfU0Bdd33VklFc7BmSycm3bpt2Zsn5aAUWRmsGhTP_wic') 

# if __name__=='__main__':
#     main()