import requests
import os
import shutil
import os.path
from pprint import pprint
import yadisk

def vkontakte(id_user, count):
    url = ' https://api.vk.com/method/photos.getAll'
    with open('token vk.ini') as f:
        token_vk = f.read().strip()
    headers = {
        'Authorization': token_vk
        # 'Content-Type': 'multipart/form-data'
    }
    params = {
        'v': '5.131',
        # 'album_id': 'wall',
        'owner_id': id_user,
        'count': count,
        # 'no_service_albums': '0',
        'extended':'1',
        'photo_sizes': '1',  
    
    }
    res = requests.get(url=url, headers=headers,params=params)
    photo_final = {}
    n = 0
    os.mkdir('temp/')
    for i in res.json()['response']['items']:
        for photo in i['sizes']:
            if photo['type'] == 'r':
                n += 1
                photo_final[f'photo{n}'] = {'likes': i['likes']['count'], 'date': i['date'], 'url': photo['url']}
                link = photo_final[f'photo{n}']['url']
                file_name = photo_final[f'photo{n}']['likes']
                file_name1 = f"{photo_final[f'photo{n}']['likes']} + {photo_final[f'photo{n}']['date']}"
                if os.path.exists(f'temp/{file_name}.jpg'):
                    with open(f'temp/{file_name1}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        fi.write(response.content)
                else:           
                    with open(f'temp/{file_name}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        fi.write(response.content)  
    return fi



def yandex():    
    with open ('token ya.ini') as file:
        token_ya = file.read().strip()
        y = yadisk.YaDisk(token=token_ya)
        if y.exists('/vk'):
            for address, dirs, files  in os.walk('temp/'):
                for file in files:
                    y.upload(f'temp/{file}', f'vk/{file}', overwrite=True)
        else:
            y.mkdir('/vk')
            for address, dirs, files  in os.walk('temp/'):
                for file in files:
                    y.upload(f'temp/{file}', f'vk/{file}', overwrite=True)
    return print('Copying to yandex disk completed successfully')


id_user = int(input('Please, enter id user: '))
count = int(input('Please enter the number of photos: '))
vkontakte(id_user, count)
yandex()
shutil.rmtree('temp/')      
