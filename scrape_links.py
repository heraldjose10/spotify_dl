
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PATH='C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

def scrape(li):
    songs=[]
    for vid in li:
        driver.get(vid)
        link=driver.find_element_by_id('thumbnail')
        songs.append(link.get_attribute('href'))
    return(songs)

# def main():
#     li=['https://www.youtube.com/results?search_query=Kaise+Hua', 'https://www.youtube.com/results?search_query=Bloodshot', 'https://www.youtube.com/results?search_query=Bekhayali+(Arijit+Singh+Version)', 'https://www.youtube.com/results?search_query=Crashing+(feat.+Bahari)', 'https://www.youtube.com/results?search_query=Without+Me+-+ILLENIUM+Remix', 'https://www.youtube.com/results?search_query=Pehla+Pyaar', 'https://www.youtube.com/results?search_query=Señorita', 'https://www.youtube.com/results?search_query=Feel+Good+(feat.+Daya)', 'https://www.youtube.com/results?search_query=Lighthouse', 'https://www.youtube.com/results?search_query=Bekhayali+(From+"Kabir+Singh")']
#     scrape(li)
    


# if __name__=='__main__':
#     main()