#!/usr/bin/env python2
'''
Wallsplash

Usage:
  wallsplash ( [--category=<category>] | [--user=<user>] ) [--query=<query>]
  wallsplash --version
  wallsplash -h | --help

Options:
  --category=<category>  Category to pull from.
  --user=<user>          User to pull from.
  --query=<query>        Comma-separated search terms.
  --version              Show version.
  -h --help              Show this screen.
'''

import subprocess
import urlparse
import os
import re

import requests
import docopt

BASE_URL = 'https://source.unsplash.com'
WALLPAPER_SIZE = '1280x800'
IMAGES_FOLDER = '/tmp'
CATEGORIES = ('buildings', 'food', 'nature', 'people', 'technology', 'objects')


def download_wallpaper(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    url_data = urlparse.urlparse(url)
    image_path = os.path.join(IMAGES_FOLDER, url_data.path.split('/')[-1])
    with open(image_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)
    return image_path


def get_wallpaper_url(resource, query=None):
    params = { '': query } if query else None
    r = requests.get('{}/{}/{}'.format(BASE_URL, resource, WALLPAPER_SIZE),
                     params=params, allow_redirects=False)
    r.raise_for_status()
    if not r.is_redirect:
        print('not a redirect')
        raise SystemExit(1)
    return r.headers.get('location')


def set_wallpaper(fn):
    subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                     'picture-uri', fn])


def switch_wallpaper(category=None, user=None, query=None):
    if category:
        if category not in CATEGORIES:
            print('category should be one of: {}'.format(', '.join(CATEGORIES)))
            raise SystemExit(1)
        resource = 'category/{}'.format(category)
    elif user:
        resource = 'user/{}'.format(user)
    else:
        resource = 'random'
    url = get_wallpaper_url(resource, query=query)
    fn = download_wallpaper(url)
    set_wallpaper(fn)


def main():
    args = docopt.docopt(__doc__, version='0.0.2')
    switch_wallpaper(args.get('--category'), args.get('--user'),
                     args.get('--query'))


if __name__ == '__main__':
    main()
