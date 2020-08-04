import youtube_dl
import os
import requests
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TCOM, TCON, TDRC ,TRCK 
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_file(url,name):
    # local_filename = url.split('/')[-1]
    #  the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return name


def d_l(li,folder):
    c=1
    for i in li:
        
        if i.get('metadata'):
            ydl_opts = {
                # 'outtmpl': os.path.join('{}'.format(folder), '%(title)s.%(ext)s'),
                'outtmpl': os.path.join('{}'.format(folder), '{}.%(ext)s'.format(i.get('metadata').get('Title'))),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
        else:
            ydl_opts = {
                'outtmpl': os.path.join('{}'.format(folder), '%(title)s.%(ext)s'),
                # 'outtmpl': os.path.join('{}'.format(folder), '{}.%(ext)s'.format(li.get('metadata').get('Title'))),
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
        # print('Downloading Music Number {}'.format(c))
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([i.get('youtube')])
    
        
        if i.get('metadata'):
            print('Adding Metadata')
            fname=folder+'\{}.mp3'.format(i.get('metadata').get('Title'))
            try: 
                tags = ID3(fname)
            except ID3NoHeaderError:
                print("Adding ID3 header")
                tags = ID3()
            tags["TIT2"] = TIT2(encoding=3, text='{}'.format(i.get('metadata').get('Title')))
            tags["TALB"] = TALB(encoding=3, text=u'{}'.format(i.get('metadata').get('Album')))
            tags["TPE1"] = TPE1(encoding=3, text=u'{}'.format(i.get('metadata').get('Artist')))
            tags['TPE2'] = TPE2(encoding=3, text=u'{}'.format(i.get('metadata').get('Artist')))
            # audio.add(TPE2(encoding=3, text=u"aa"))   #ALBUMARTIST
            # tags["TCON"] = TCON(encoding=3, text=u'mutagen Genre')
            # tags["TDRC"] = TDRC(encoding=3, text=u'2010')
            tags["TRCK"] = TRCK(encoding=3, text=u'{}'.format(c))

            tags.save(fname)
            
            download_file(i.get('metadata').get('Album Art'),folder+'\pic'+str(c)+'.png')
            pic=(folder+'\pic'+str(c)+'.png')
            imagedata = open(pic, 'rb').read()
            id3 = ID3(fname)
            id3.add(APIC(3, 'image/png', 3, 'Front cover', imagedata))
            id3.add(TIT2(encoding=3, text='{}'.format(i.get('metadata').get('Title'))))

            id3.save(v2_version=3)

            os.remove(pic)

            c+=1


# path='E:\program files'
# data=[{'url': 'https://www.youtube.com/results?search_query=Memories+Maroon+5', 'song_id': 4881650, 'metadata': {'Title': 'Memories', 'Album': 'M57*', 'Artist': 'Maroon 5', 'Album Art': 'https://images.genius.com/ba9cad490f43f0688c43025d9f64955f.300x300x1.png'}, 'youtube': 'https://www.youtube.com/watch?v=SlPhMPnQ58k'}, {'url': 'https://www.youtube.com/results?search_query=Blinding+Lights+The+Weeknd', 'song_id': 5049949, 'metadata': {'Title': 'Blinding Lights', 'Album': 'After Hours', 'Artist': 'The Weeknd', 'Album Art': 'https://images.genius.com/22ca9d47b12db20bbfc88da431fba87b.300x300x1.png'}, 'youtube': 'https://www.youtube.com/watch?v=4NRXx6U8ABQ'}, {'url': 'https://www.youtube.com/results?search_query=Darling+Chiiild', 'song_id': 5027518, 'metadata': {'Title': 'Darling', 'Album': 'Synthetic Soul', 'Artist': 'Chiiild', 'Album Art': 'https://images.genius.com/1090a2e8201ea153aab11a18542536f8.300x300x1.jpg'}, 'youtube': 'https://www.youtube.com/watch?v=vJm4csJdNNE'}, {'url': 'https://www.youtube.com/results?search_query=Permanent+Way+Charlie+Cunningham', 'song_id': 4314503, 'metadata': {'Title': 'Permanent Way', 'Album': 'Permanent Way', 'Artist': 'Charlie Cunningham', 'Album Art': 'https://images.genius.com/b9ab7f960b28a2d19d2d614d0bb4d491.300x300x1.jpg'}, 'youtube': 'https://www.youtube.com/watch?v=Gn0NUodkwJM'}, {'url': 'https://www.youtube.com/results?search_query=Between+Moments+Rand+Aldo', 'song_id': None, 'youtube': 'https://www.youtube.com/watch?v=Sdca6VLP-lY'}]
# d_l(data,path)




