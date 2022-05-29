import vk_api
import requests
from config import token
from PIL import Image
import time

user_list = []
true_size = (81, 81)
photos_colors = []
photos_url = []
start_time = time.time()

SAMPLE = '/Users/miketseytlin/PycharmProjects/PhotoMosaic/data/SchoolProject2021Photo'
MAIN_PHOTO = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/Me_test.jpg"
RESULT = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/Me_test1.jpg"
COLOR_DATA = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/SchoolProject2021_ColorsData"
MAIN_COLORS = "/Users/miketseytlin/PycharmProjects/PhotoMosaic/MainPhotoAveColors"
LINES = 150
DATA_SIZE = 40000


# Изменяет размер исходного фото
def make_main_photo():
    p = Image.open(MAIN_PHOTO)
    p = p.resize((LINES * 81, LINES * 81))
    p.save(MAIN_PHOTO)


# Возвращает список айдишников друзей
def users():
    user_list_tmp = vk.friends.get(v='5.52')['items']
    for user in user_list_tmp:
        user_list.append(str(user))
    return user_list


# Возвращает список длины 700 из друзей друзей
def friends_of_friends(friends_list):
    friends_of_friends_set = set()
    while True:
        for friend in friends_list:
            user_list_tmp = vk.friends.get(user_id=friend, v='5.52')['items']
            for user in user_list_tmp:
                friends_of_friends_set.add(str(user))
                if len(friends_of_friends_set) > 700:
                    friends_of_friends_list = list(friends_of_friends_set)
                    return (friends_of_friends_list)


# Возвращает список url фотографий со страниц друзей и друзей друзей
def json_download(user_list_):
    data_tmp = []
    user_list = user_list_
    while len(user_list) < 700:
        for friend in friends_of_friends(user_list):
            user_list.append(friend)
    user_list = list(set(user_list))
    for user in user_list:
        for i in range(10):
            try:
                data_tmp = vk.photos.getAll(owner_id=user, v='5.52', count='200')['items']
            except Exception as e:
                print(e)
                break
        for el in data_tmp:
            try:
                photos_url.append(el['photo_130'])
            except:
                pass
        print("Downloaded " + str(len(photos_url)) + " url")
        if len(photos_url) > DATA_SIZE:
            break
    return photos_url


# Скачивает фотографии по списку url
def data(photos_url):
    i = 0
    sample = SAMPLE
    for url in photos_url:
        if i == DATA_SIZE:
            break
        try:
            i += 1
            name = sample + str(i) + '.jpg'
            out = open(name, 'wb')
            photo = requests.get(url)
            out.write(photo.content)
            out.close()
            img = Image.open(name)
            img = img.resize(true_size)
            img.save(name)
        except Exception as e:
            print(e)
        print("Downloaded " + str(i) + " photos")


# Возвращает список из средних цветов 9 фрагментов фотографии
def photo_ave_colors(photo_url):
    photo = Image.open(photo_url)
    ave_color_list = []

    for k in range(3):
        for i in range(3):
            y_0 = (k - 1) * 27
            r = 0
            g = 0
            b = 0
            for j in range(27):
                x_0 = (i - 1) * 27
                for l in range(27):
                    r1, g1, b1 = photo.getpixel((x_0 + l, y_0))
                    r += r1
                    b += b1
                    g += g1
            r //= 729
            g //= 729
            b //= 729
            ave_color_list.append([r, g, b])
    return ave_color_list


# Возвращает список из средних цветов фрагментов исходной фотографии
def main_photo_color_data(Main_Photo_Color_Data_File):
    for part in main_photo_ave_colors(MAIN_PHOTO):
        r, g, b = part
        Main_Photo_Color_Data_File.write(str(r) + " " + str(g) + " " + str(b) + " ")


# Записывает в файл средние цвета 9 фрагментов фотографий
def Color_Data(Color_Data_File):
    for i in range(DATA_SIZE):
        name = SAMPLE + str(
            i + 1) + ".jpg"
        try:
            tmp_colors = photo_ave_colors(name)
        except Exception as e:
            print(e)
        for part in tmp_colors:
            r, g, b = part
            Color_Data_File.write(str(r) + " " + str(g) + " " + str(b) + " ")
        Color_Data_File.write("\n")
        print("In color data " + str(i) + " photos")


# Записывает в файл средние цвета фрагментов исходной фотографии
def main_photo_ave_colors(main_photo):
    photo = Image.open(main_photo)
    ave_color_list = []
    z = 0

    for k in range(LINES * 3):
        for i in range(LINES * 3):
            y_0 = (k - 1) * 27
            r = 0
            g = 0
            b = 0
            for j in range(27):
                x_0 = (i - 1) * 27
                for l in range(27):
                    r1, g1, b1 = photo.getpixel((x_0 + l, y_0))
                    r += r1
                    b += b1
                    g += g1
            r //= 729
            g //= 729
            b //= 729
            ave_color_list.append([r, g, b])
            print("In MainPhotoColorsData " + str(z) + " parts")
            z += 1
    return ave_color_list


# Возвращает список из средних цветов 9 фрагментов фотографий и список средних цветов фрагментов исходной фотографии
def Colors_File_To_List(ColorsDataFileName, MainPhotoColorsFileName):
    ColorsDataFile = open(ColorsDataFileName, 'r')
    MainPhotoColorsFile = open(MainPhotoColorsFileName, "r")
    ColorsData = []
    tmp = list(map(int, ColorsDataFile.read().split()))
    for i in range(len(tmp) // 27):
        ColorsData.append(tmp[(i * 27):(i * 27 + 27)])
    MainPhotoColors = list(map(int, MainPhotoColorsFile.read().split()))
    ColorsDataFile.close()
    MainPhotoColorsFile.close()
    return ColorsData, MainPhotoColors


# Возвращает порядковый номер фотографии, наиболее схожей с данным фрагментом исходной фотографии
def best_photo(photos_colors_list, main_photo_colors, x, y, numbers):
    sum = 255 + 1
    part_of_main = []
    for i in range(9):
        part_of_main.append(main_photo_colors[x * 3 + y * 9 * LINES + i])
    for i in range(9):
        part_of_main.append(main_photo_colors[x * 3 + (y + 1) * 9 * LINES + i])
    for i in range(9):
        part_of_main.append(main_photo_colors[x * 3 + (y + 2) * 9 * LINES + i])
    for n in numbers:
        tmp_sum = 0
        for j in range(27):
            tmp_sum += abs(photos_colors_list[n][j] - part_of_main[j]) / 27
        if tmp_sum <= sum:
            photo_number = n
            sum = tmp_sum
    return photo_number


# Пробегает по всем фрагментам исходного фото, находя наиболее схожее фото для каждого
def collage(main_photo_url, photos_colors_list, main_photo_colors):
    main_photo = Image.open(main_photo_url)
    numbers = [i for i in range(DATA_SIZE)]
    i = 0
    while True:
        if i == LINES * LINES - 1:
            break
        print(f"Result done at {round((i / (LINES * LINES - 1) * 100), 2)}%")
        x = i % LINES * 3
        y = i // LINES * 3
        photo = best_photo(photos_colors_list, main_photo_colors, x, y, numbers)
        name = SAMPLE + str(photo + 1) + '.jpg'
        try:
            tmp_photo = Image.open(name)
            y0 = y * 27
            for j in range(81):
                x0 = x * 27
                for l in range(81):
                    main_photo.putpixel((x0 + j, y0 + l), tmp_photo.getpixel((j, l)))
            numbers.remove(photo)
            i += 1
        except Exception as e:
            numbers.remove(photo)
            print(e)
    main_photo.show()
    main_photo.save(RESULT)


# Запускать при первом запуске программы. Изменяет размер исходного фото, скачивает фотографии друзей и друзей друзей,
# записывает в файл среднии цвета фрагментов фотографий, записывает в файл цвета фрагментов  исходной фотографии
def start():
    make_main_photo()

    data(json_download(users()))

    MainPhotoAveColorsFile = open('MainPhotoAveColors', "w")
    main_photo_color_data(MainPhotoAveColorsFile)
    MainPhotoAveColorsFile.close()

    Color_Data_File = open(COLOR_DATA, 'w')
    Color_Data(Color_Data_File)
    Color_Data_File.close()


if __name__ == '__main__':
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    make_main_photo()
    MainPhotoAveColorsFile = open('MainPhotoAveColors', "w")
    main_photo_color_data(MainPhotoAveColorsFile)
    MainPhotoAveColorsFile.close()
    collage(MAIN_PHOTO, Colors_File_To_List(COLOR_DATA, MAIN_COLORS)[0],
            Colors_File_To_List(COLOR_DATA, MAIN_COLORS)[1])
    print(f"Lead time: {time.time() - start_time}")
