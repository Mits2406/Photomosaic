import os
import yadisk
from config import token, ya_token
import vk_api
import zipfile

import requests

out = open('/Users/miketseytlin/PycharmProjects/PhotoMosaic/data1652901739.620854/SchoolProject2022Photo1652901739.620854320873.jpg', 'wb')
photo = requests.get('https://img.freepik.com/free-photo/a-beautiful-bright-red-kitten-on-a-white-background-looks-to-the-side-young-cute-little-red-kitty-long-haired-ginger-kitten-play-at-home-cute-funny-home-pets-space-for-text_332694-193.jpg')
out.write(photo.content)
out.close()
