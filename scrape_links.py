import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from genius import access


PATH='C:\Program Files (x86)\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=PATH,chrome_options=options)


def metadata(ID):
    url='http://api.genius.com/songs/'+str(ID)
    head={
        # 'Accept': 'application/json',
        'Authorization':'Bearer '+access
        }
    r=requests.get(url,headers=head)
    res=r.json()
    # print(res)
    if res.get('response').get('song').get('album'):
        return({
            'Title':res.get('response').get('song').get('title'),
            'Album':res.get('response').get('song').get('album').get('name'),
            'Artist':res.get('response').get('song').get('primary_artist').get('name'),
            'Album Art':res.get('response').get('song').get('header_image_url')
        })
    else:
        return({
            'Title':res.get('response').get('song').get('title'),
            'Artist':res.get('response').get('song').get('primary_artist').get('name'),
            'Album Art':res.get('response').get('song').get('song_art_image_thumbnail_url')
        })


def scrape(li):
    print('Scraping Music Links--This will take few minutes')
    # songs=[]
    for vid in li:
        # print(vid)
        if vid.get('song_id'):
            meta=metadata(vid.get('song_id'))
            vid['metadata']=meta
        else:
            vid['metadata']=None
        driver.get(vid.get('url'))
        link=driver.find_element_by_id('thumbnail')
        vid['youtube']=(link.get_attribute('href'))
    return(li)
    driver.close()

# output=[{'url': 'https://www.youtube.com/results?search_query=Phoenix+League+of+Legends', 'song_id': 4929997}, {'url': 'https://www.youtube.com/results?search_query=Roses+-+Imanbek+Remix+SAINt+JHN', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Lily+Alan+Walker', 'song_id': 4148291}, {'url': 'https://www.youtube.com/results?search_query=End+of+Time+K-391', 'song_id': 5308669}, {'url': 'https://www.youtube.com/results?search_query=On+&+On+Cartoon', 'song_id': 2496852}, {'url': 'https://www.youtube.com/results?search_query=Blueberry+Faygo+Lil+Mosey', 'song_id': 4606781}, {'url': 'https://www.youtube.com/results?search_query=Legends+Never+Die+League+of+Legends', 'song_id': 3236132}, {'url': 'https://www.youtube.com/results?search_query=The+Box+Roddy+Ricch', 'song_id': 5068155}, {'url': 'https://www.youtube.com/results?search_query=Everything+Black+Unlike+Pluto', 'song_id': 3016408}, {'url': 'https://www.youtube.com/results?search_query=Play+K-391', 'song_id': 4812810}, {'url': 'https://www.youtube.com/results?search_query=Fly+Away+TheFatRat', 'song_id': 3110086}, {'url': 'https://www.youtube.com/results?search_query=Fearless+Pt.+II+Lost+Sky', 'song_id': 3807302}, {'url': 'https://www.youtube.com/results?search_query=Warriors+League+of+Legends', 'song_id': 5160726}, {'url': 'https://www.youtube.com/results?search_query=HIGHEST+IN+THE+ROOM+Travis+Scott', 'song_id': 4497172}, {'url': 'https://www.youtube.com/results?search_query=Bandit+(with+YoungBoy+Never+Broke+Again)+Juice+WRLD', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Ignite+Alan+Walker', 'song_id': 5120556}, {'url': 'https://www.youtube.com/results?search_query=Heroes+Tonight+Janji', 'song_id': 2944226}, {'url': 'https://www.youtube.com/results?search_query=Fearless+Lost+Sky', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Awaken+League+of+Legends', 'song_id': 4247165}, {'url': 'https://www.youtube.com/results?search_query=Ludens+Bring+Me+The+Horizon', 'song_id': 4912244}, {'url': 'https://www.youtube.com/results?search_query=Superhero+Unknown+Brain', 'song_id': 2871267}, {'url': 'https://www.youtube.com/results?search_query=Nevada+Vicetone', 'song_id': 2688321}, {'url': 'https://www.youtube.com/results?search_query=SICKO+MODE+Travis+Scott', 'song_id': 3876994}, {'url': 'https://www.youtube.com/results?search_query=MEGALOVANIA+Toby+Fox', 'song_id': 2807485}, {'url': 'https://www.youtube.com/results?search_query=RISE+League+of+Legends', 'song_id': 3982228}, {'url': 'https://www.youtube.com/results?search_query=All+Girls+Are+The+Same+Juice+WRLD', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=ROCKSTAR+(feat.+Roddy+Ricch)+DaBaby', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Astronomia+Vicetone', 'song_id': 2881434}, {'url': 'https://www.youtube.com/results?search_query=goosebumps+Travis+Scott', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Unity+TheFatRat', 'song_id': 2079004}, {'url': 'https://www.youtube.com/results?search_query=After+Party+Don+Toliver', 'song_id': 4822192}, {'url': 'https://www.youtube.com/results?search_query=BOP+DaBaby', 'song_id': 4895345}, {'url': 'https://www.youtube.com/results?search_query=THE+SCOTTS+THE+SCOTTS', 'song_id': 5493340}, {'url': 'https://www.youtube.com/results?search_query=Party+Girl+StaySolidRocky', 'song_id': 5233319},
# {'url': 'https://www.youtube.com/results?search_query=GOOBA+6ix9ine', 'song_id': 5545285}, {'url': 'https://www.youtube.com/results?search_query=WHATS+POPPIN+(feat.+DaBaby,+Tory+Lanez+&+Lil+Wayne)+-+Remix+Jack+Harlow', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=La+Jeepeta+-+Remix+Nio+Garcia', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Savage+Love+(Laxed+-+Siren+Beat)+Jawsh+685', 'song_id': 5556181}, {'url': 'https://www.youtube.com/results?search_query=21+Polo+G', 'song_id': 5171419}, {'url': 'https://www.youtube.com/results?search_query=Bad+Energy+Juice+WRLD', 'song_id': 4674927}, {'url': 'https://www.youtube.com/results?search_query=Only+A+Fool+(with+Pink+Sweat$)+Galantis', 'song_id': None}, {'url': 'https://www.youtube.com/results?search_query=Time+-+Alan+Walker+Remix+Alan+Walker', 'song_id': None}]
# data=scrape(output)
# print(data)