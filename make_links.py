# -*- coding: utf-8 -*-
import json
import requests
from genius import access
# from genius import c_id
# from genius import c_s


def search(name,artist):
    url='http://api.genius.com/search?'
    data={
        'q':name+' '+artist,
    }
    head={
        # 'Accept': 'application/json',
        'Authorization':'Bearer '+access
        }
    r=requests.get(url,headers=head,params=data)
    res=(r.json())
    if (res.get('response').get('hits')[0].get('result').get('title'))==name:
        return(res.get('response').get('hits')[0].get('result').get('id'))
    else:
        return(None)

def links(songs):
    base_url='https://www.youtube.com/results?search_query='
    links_list=[]
    for i in songs:
        a='+'.join(i.get('name').split(' '))
        b='+'.join(i.get('artists')[0].split(' '))
        # print(a)
        s_id=search(i.get('name'),i.get('artists')[0])
        links_list.append(
            {
                'url':base_url+a+'+'+b,
                'song_id' : s_id
            })

    return(links_list)

# text={'name': 'Memories', 'artists': ['Maroon 5']}, {'name': 'Blinding Lights', 'artists': ['The Weeknd']}, {'name': 'Darling', 'artists': ['Chiiild']}, {'name': 'Permanent Way', 'artists': ['Charlie Cunningham']}, {'name': 'Between Moments', 'artists': ['Rand Aldo']}
# links(text)



