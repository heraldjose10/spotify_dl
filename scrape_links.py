
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

PATH='C:\Program Files (x86)\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=PATH,chrome_options=options)


def scrape(li):
    songs=[]
    for vid in li:
        driver.get(vid)
        link=driver.find_element_by_id('thumbnail')
        songs.append(link.get_attribute('href'))
    return(songs)
    driver.close()


    


# if __name__=='__main__':
#     main()