# -*- coding: utf-8 -*-
import webbrowser


def links(songs):
    base_url='https://www.youtube.com/results?search_query='
    links_list=[]
    for i in songs:
        a='+'.join(i.get('name').split(' '))
        b='+'.join(i.get('artists')[0].split(' '))
        # print(a)
        links_list.append(base_url+a+'+'+b)

    return(links_list)


# def main():
#     li=[{'name': 'Kaise Hua', 'artists': ['Vishal Mishra']}, {'name': 'Bloodshot', 'artists': ['Mike Perry', 'Charlotte Haining']}, {'name': 'Bekhayali (Arijit Singh Version)', 'artists': ['Arijit Singh']}, {'name': 'Crashing (feat. Bahari)', 'artists': ['ILLENIUM', 'Bahari']},
# {'name': 'Without Me - ILLENIUM Remix', 'artists': ['Halsey', 'ILLENIUM']}, {'name': 'Pehla Pyaar', 'artists': ['Armaan Malik']}, {'name': 'Señorita', 'artists': ['Shawn Mendes', 'Camila Cabello']}, {'name': 'Feel Good (feat. Daya)', 'artists': ['Gryffin', 'ILLENIUM', 'Daya']}, {'name': 'Lighthouse', 'artists': ['Mike Perry', 'Hot Shade', 'René Miller']}, {'name': 'Bekhayali (From "Kabir Singh")', 'artists': ['Sachet Tandon', 'Sachet-Parampara']}]
#     s=links(li)
#     webbrowser.open(s[-4])
# if __name__=='__main__':
#     main()