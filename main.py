import vk_api
from config import token, ya_token
from PIL import Image
import requests
import yadisk
import time
import os
import shutil
import zipfile

user_list = []
true_size = (81, 81)
photos_colors = []
photos_url = []

fragments = []
ynd = yadisk.YaDisk(token=ya_token)


class frag():
    def __init__(self, photo, place):
        self.photo = photo
        u_photo = Image.open(self.photo)
        u_photo = u_photo.resize(true_size)
        u_photo.save(self.photo)
        u_photo = Image.open(self.photo)
        r = 0
        g = 0
        b = 0
        for i in range(81):
            for j in range(81):
                r += u_photo.getpixel((i, j))[0]
                g += u_photo.getpixel((i, j))[1]
                b += u_photo.getpixel((i, j))[2]
        r = r // 6561
        g = g // 6561
        b = b // 6561
        self.color = [r, g, b]
        self.place = place


# -----------------------------------------VK-----------------------------------------------------------------------------------

# Возвращает список айдишников друзей
def users(user_id):
    user_list_tmp = vk.friends.get(user_id=user_id, v='5.89')['items']
    for user in user_list_tmp:
        user_list.append(str(user))
    return user_list


# Возвращает список длины 100 из друзей друзей
def friends_of_friends(friends_list):
    friends_of_friends_set = set()
    while True:
        for friend in friends_list:
            try:
                user_list_tmp = vk.friends.get(user_id=friend, v='5.89')['items']
            except Exception as e:
                print(e)
            for user in user_list_tmp:
                friends_of_friends_set.add(str(user))
                if len(friends_of_friends_set) > 1000:
                    friends_of_friends_list = list(friends_of_friends_set)
                    return (friends_of_friends_list)


# Возвращает список url фотографий со страниц друзей и друзей друзей
def json_download(user_list_, data_size):
    data_tmp = []
    photos_url_set = set()

    user_list = user_list_
    while len(user_list) < data_size:
        for friend in friends_of_friends(user_list):
            user_list.append(friend)
    user_list = list(set(user_list))
    for user in user_list:
        for i in range(10):
            try:
                data_tmp = vk.photos.getAll(owner_id=user, v='5.89', count='200')['items']
            except Exception as e:
                print(e)
                break
        for el in data_tmp:
            try:
                for el1 in el['sizes']:
                    if el1['height'] == 130:
                        photos_url_set.add(el1['url'])
            except Exception as e:
                print(e)
                pass
        print("Downloaded " + str(len(photos_url_set)) + " url")
        if len(photos_url_set) > data_size:
            break
    print(list(photos_url_set))
    return list(photos_url_set)


# Скачивает фотографии по списку url
def data(photos_url, data_size, uniq_numb):
    i = 0
    os.mkdir('/Users/miketseytlin/PycharmProjects/PhotoMosaic/data' + str(uniq_numb))
    sample = '/Users/miketseytlin/PycharmProjects/PhotoMosaic/data' + str(uniq_numb) + '/SchoolProject2022Photo' + str(
        uniq_numb)
    while len(fragments) < data_size:
        for url in photos_url:
            try:
                i += 1

                name = sample + str(i) + '.jpg'
                out = open(name, 'wb')
                photo = requests.get(url)
                out.write(photo.content)
                out.close()
                fragment = frag(sample + str(i) + '.jpg', [])
                fragments.append(fragment)
            except Exception as e:
                print(e, 'data')
            print("Downloaded " + str(i) + " photos")


def main_photo_download(main_url, lines, uniq_numb):
    a = ynd.get_public_download_link(main_url)
    MAIN_PHOTO = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/Main_Photo" + str(uniq_numb) + ".jpg"
    out = open(MAIN_PHOTO, 'wb')
    b = requests.get(a)
    out.write(b.content)
    out.close()
    p = Image.open(MAIN_PHOTO)
    p = p.resize((lines * 81, lines * 81))
    p.save(MAIN_PHOTO)


# ------------------------------------------------------------------------------------------------------------------------------

# Скачивание фотографий из диска
def YD_data(link, uniq_numb):
    a = ynd.get_public_download_link(link)
    direct = '/Users/miketseytlin/PycharmProjects/PhotoMosaic/data' + str(uniq_numb) + '.zip'
    out = open(direct, 'wb')
    b = requests.get(a)
    out.write(b.content)
    out.close()
    with zipfile.ZipFile(direct, 'r') as zip_file:
        zip_file.extractall('/Users/miketseytlin/PycharmProjects/PhotoMosaic/')
    os.rename("Photo_Mosaic", "data" + str(uniq_numb))
    d = os.listdir("data" + str(uniq_numb))
    i = 1
    for photo in d:
        try:
            i += 1
            os.rename('/Users/miketseytlin/PycharmProjects/PhotoMosaic/data' + str(uniq_numb) + '/' + photo,
                      '/Users/miketseytlin/PycharmProjects/PhotoMosaic/data/SchoolProject2022Photo' + str(
                          uniq_numb) + str(i) + '.jpg')
            fragment = frag(
                '/Users/miketseytlin/PycharmProjects/PhotoMosaic/data/SchoolProject2022Photo' + str(uniq_numb) + str(
                    i) + '.jpg', [])
            fragments.append(fragment)
        except Exception as e:
            print(e)


# Записывает в файл средние цвета фрагментов исходной фотографии
def main_photo_ave_colors(main_photo, lines, uniq_numb):
    s = '/Users/miketseytlin/PycharmProjects/PhotoMosaic/main_photo' + str(uniq_numb) + '20.jpg'
    os.system(
        'cp ' + main_photo + ' /Users/miketseytlin/PycharmProjects/PhotoMosaic/main_photo' + str(uniq_numb) + '20.jpg')

    photo = Image.open(s)
    ave_color_list = []
    photo = photo.resize((lines, lines))

    for k in range(lines):
        for i in range(lines):
            ave_color_list.append(photo.getpixel((k, i)))
    return ave_color_list


def best_photo(main_photo_colors, x, y, lines, mode):
    sum = 766
    best = -1
    for i in range(len(fragments)):
        f = fragments[i]
        r, g, b = f.color
        if sum > abs(main_photo_colors[x * lines + y][0] - r) + abs(main_photo_colors[x * lines + y][1] - g) + abs(
                main_photo_colors[x * lines + y][2] - b):
            if f.place == [] and mode == 'VK':
                best = i
            if mode == 'Disk':
                is_used = 0
                for p in f.place:
                    if abs(x - p[0]) + abs(y - p[1]) < 3:
                        is_used += 1
                if is_used == 0:
                    best = i
                    sum = abs(main_photo_colors[x * lines + y][0] - r) + abs(
                        main_photo_colors[x * lines + y][1] - g) + abs(main_photo_colors[x * lines + y][2] - b)
    f = fragments[best]
    d = f.place
    d.append([x, y])
    f1 = frag(f.photo, d)
    del fragments[best]
    fragments.append(f1)


def collage(main_photo_url, main_photo_colors, lines, mode, uniq_numb):
    main_photo = Image.open(main_photo_url)
    i = 0
    for x in range(lines):
        for y in range(lines):
            best_photo(main_photo_colors, x, y, lines, mode)
    for f in fragments:
        for p in f.place:
            try:
                img = Image.open(f.photo)
                for j in range(81):
                    x0 = p[0] * 81
                    y0 = p[1] * 81

                    for l in range(81):
                        c = tuple([(3 * img.getpixel((j, l))[0] + (main_photo_colors[p[0] * lines + p[1]][0])) // 4,
                                   (3 * img.getpixel((j, l))[1] + (main_photo_colors[p[0] * lines + p[1]][1])) // 4,
                                   (3 * img.getpixel((j, l))[2] + (main_photo_colors[p[0] * lines + p[1]][2])) // 4])
                        main_photo.putpixel((x0 + j, y0 + l), c)
                i += 1
                print(f"Result done at {round((i / (lines * lines - 1) * 100), 2)}%")
            except Exception as e:
                print(e)

    RESULT = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/Result" + str(uniq_numb) + ".jpg"
    main_photo.save(RESULT)
    u = "/Фотомозаика/main" + str(uniq_numb) + '.jpg'
    ynd.upload(RESULT, u)
    ynd.publish(u)
    l = ynd.get_download_link(u)
    shutil.rmtree('/Users/miketseytlin/PycharmProjects/PhotoMosaic/data' + str(uniq_numb))
    if mode == 'Disk':
        os.remove("/Users/miketseytlin/PycharmProjects/PhotoMosaic/data" + str(uniq_numb) + ".zip")
    os.remove("/Users/miketseytlin/PycharmProjects/PhotoMosaic/Main_Photo" + str(uniq_numb) + ".jpg")
    os.remove('/Users/miketseytlin/PycharmProjects/PhotoMosaic/main_photo' + str(uniq_numb) + '20.jpg')
    os.remove(RESULT)
    return l


def start(user_id, data_size, lines, mode, link, uniq_numb):
    if mode == 'VK':
        data(json_download(friends_of_friends(users(user_id)), data_size), data_size, uniq_numb)
    else:
        YD_data(link, uniq_numb)
    MAIN_PHOTO = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/Main_Photo" + str(uniq_numb) + ".jpg"
    result = collage(MAIN_PHOTO, main_photo_ave_colors(MAIN_PHOTO, lines, uniq_numb), lines, mode, uniq_numb)
    return result


vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
