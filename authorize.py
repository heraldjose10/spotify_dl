import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from app import client_id

PATH='C:\Program Files (x86)\chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=PATH,chrome_options=options)


def open_browser():
    url='https://accounts.spotify.com/authorize'
    para={
        'client_id' : client_id,
        'response_type' : 'code',
        'redirect_uri' : 'https://github.com/',
        'scope' : 'playlist-modify-public playlist-modify-private'
    }
    res=requests.get(url,params=para)
    driver.get(res.url)
    print('WE DO NOT SAvE CREDs')
    user=input('---spotify username---')
    password=input('---spotify password---')
    print('LOgginG IN Spotify')
    inputElement=driver.find_element_by_id("login-username")
    inputElement.send_keys(user)
    inp=driver.find_element_by_id("login-password")
    inp.send_keys(password)
    but=driver.find_element_by_id('login-button')
    but.send_keys("\n")
    time.sleep(5)
    u=driver.current_url
    driver.close()

    return(u[25:])