import requests
import os
import shutil
import os.path
from pprint import pprint
import yadisk
from tqdm import tqdm
import json

def vkontakte(id_user, count):
    
    url = ' https://api.vk.com/method/photos.getAll'
    with open('token vk.ini') as f:
        token_vk = f.read().strip()
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    params = {
        'access_token': token_vk,
        'v': '5.131',
        'owner_id': id_user,
        'count': count,
        'extended':'1',
        'photo_sizes': '1',  
    
    }
    res = requests.get(url=url, headers=headers,params=params)
    os.mkdir('temp/')
    
    photo_final = {}
    n = 0
    print('Copying the photos to the HDD') 
    
    for i in res.json()['response']['items']:
        for photo in i['sizes']:   
            if photo['type'] == 'r':
                n += 1
                photo_final[f'photo{n}'] = {'likes': i['likes']['count'], 'date': i['date'], 'url': photo['url']}
                with open('info_photo.json', 'w') as file:
                    json_string = json.dumps(photo_final)
                    file.writelines(json_string  + '\n')
                link = photo_final[f'photo{n}']['url']
                file_name = photo_final[f'photo{n}']['likes']
                file_name1 = f"{photo_final[f'photo{n}']['likes']} + {photo_final[f'photo{n}']['date']}"
                if os.path.exists(f'temp/{file_name}.jpg'):
                    with open(f'temp/{file_name1}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        for z in tqdm(range(1)):
                            fi.write(response.content)
                else:           
                    with open(f'temp/{file_name}.jpg', 'wb+') as fi:
                        response = requests.get(link)
                        for z in tqdm(range(1)):
                            fi.write(response.content)  
       
    return fi



def yandex():  
    print('Copying the photos to the Yandex Disk') 
    
    with open ('token ya.ini') as file:
        token_ya = file.read().strip()
        y = yadisk.YaDisk(token=token_ya)
        
           
        if y.exists('/vk'):
            for address, dirs, files  in os.walk('temp/'):
                for file in files:
                    for z in tqdm(range(1)):
                         y.upload(f'temp/{file}', f'vk/{file}', overwrite=True)
        else:
            y.mkdir('/vk')
            for address, dirs, files  in os.walk('temp/'):
                for file in files:
                    for z in tqdm(range(1)):
                        y.upload(f'temp/{file}', f'vk/{file}', overwrite=True)
        
    return print('Copying to yandex disk completed successfully')

if __name__== '__main__':
    id_user = int(input('Please, enter id user: '))
    count = int(input('Please enter the number of photos: '))
    vkontakte(id_user, count)
    yandex()
    shutil.rmtree('temp/') 
    
        
