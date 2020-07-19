from authorize import open_browser
from refresh_tokens import refresh
from get_playlists import get_playlists
from make_links import links
from scrape_links import scrape
from download import d_l


open_browser()

user_code=input('input code:')
playlist_id=input('give playlisy id:')
acc_token,ref_token=refresh(user_code)
songs=get_playlists(playlist_id,acc_token)
song_li=links(songs)
to_download=scrape(song_li)
d_l(to_download)



