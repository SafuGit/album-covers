from django.shortcuts import render
import internetarchive
import random
import requests
from django.http import HttpResponseRedirect

reload_alert = 'False'
items = [] # type: ignore
def search_items():
    search = internetarchive.search_items('collection:album_covers')
    for result in search:
        items.append(result)


def get_random_item(items):
    random_item = random.choice(items)
    return random_item


def get_item_data(identifier):
    try:
        unique_id = identifier['identifier']
        dir = f'https://archive.org/metadata/{unique_id}'
        response = requests.get(dir)
        data = response.json()
        print(response.status_code)
        return data
    except:
        reload_alert = 'True'


def get_item_image(data):
    try:
        d1 = data['d1']
        dir = data['dir']
        for file in data['files']:
            if file['format'] == 'JPEG' or file['format'] == 'PNG' or file['format'] == 'JPG':
                img_file = file['name']
        url = f'https://{d1}{dir}/{img_file}'
        return url
    except:
        reload_alert = 'True'


# Create your views here.
def index(request):
    search_items()
    id = get_random_item(items)
    data = get_item_data(id)
    image_url = get_item_image(data)
    print(image_url)
    print(id)
    if image_url == None:
        reload_alert = 'True'
    else:
        reload_alert = 'False'
    return render(request, 'backend/index.html', context={
        'img': image_url,
        'reload': reload_alert
    })