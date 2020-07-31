# -*- coding: utf-8 -*-


def links(songs):
    base_url='https://www.youtube.com/results?search_query='
    links_list=[]
    for i in songs:
        a='+'.join(i.get('name').split(' '))
        b='+'.join(i.get('artists')[0].split(' '))
        # print(a)
        links_list.append(base_url+a+'+'+b)

    return(links_list)

