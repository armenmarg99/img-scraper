from __future__ import annotations
from typing import Set

import os
from os.path import join
from urllib.parse import urlparse
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError


def get_absolute_url(url: str) -> str:
    url_parsed = urlparse(url)
    url = url_parsed.scheme
    url += "://"
    url += url_parsed.netloc
    url += url_parsed.path
    return url


def is_valid_url(url: str) -> bool:
    url_parsed = urlparse(url)
    return bool(url_parsed.scheme) and bool(url_parsed.netloc)


def get_short_url(url: str) -> str:
    return url.split('?')[0]


def get_url_variations(url: str) -> Set[str]:
    url_parsed = urlparse(url)
    ans = {url}
    if 'www.' in url:
        ans.add(url.replace('www.', ''))
    else:
        ans.add(url_parsed.scheme + '://www.' + url_parsed.netloc + url_parsed.path)

    vars_with_slash = set()
    for url in ans:
        if url.endswith('/'):
            vars_with_slash.add(url[:-1])
        else:
            vars_with_slash.add(url + '/')
    ans.update(vars_with_slash)
    return ans


def replace_slashes_with_dashes(string: str):
    string = string.replace('/', '-')
    return string


def download_image_and_check_size(url: str, output_folder: str, min_width: int, min_height: int):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    save_path = join(output_folder, url.split("/")[-1])
    img_data = requests.get(url).content
    try:
        img = Image.open(BytesIO(img_data))
    except UnidentifiedImageError:
        print(f"Could not read image from the following url {url}")
        return
    if img.size[0] >= min_width and img.size[1] >= min_height:
        with open(save_path, "wb") as f:
            f.write(img_data)
