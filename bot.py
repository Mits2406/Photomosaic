from main import main_photo_download
from main import start
import vk_api
import threading
import time
from config import key

start_var = 0
USERS = {}  # mode, data size, lines, main photo, YD link
READY_USER_IDS = []
vk_session = vk_api.VkApi(token=key)
file = open('project_sub_file', 'w')
file.write('0')
file.close()
from vk_api.longpoll import VkLongPoll, VkEventType


def main_p(user_id, user_size, user_main, user_lines, user_mode, user_link):
    uniq_numb = time.time()
    main_photo_download(user_main, user_lines, uniq_numb)
    result = start(user_id, user_size, user_lines, user_mode, user_link, uniq_numb)
    vk.messages.send(user_id=event.user_id, random_id='',
                     message='Ваше фото готово. Ссылка:')
    vk.messages.send(user_id=event.user_id, random_id='',
                     message=result)
    file = open('project_sub_file', 'w')
    file.write('0')
    file.close()


user_number = 0

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text == 'Привет' or event.text == 'привет':
                if event.from_user:
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Здравствуйте!\nПожалуйста напишите "Начать", если желаете приступить к обработке')
            elif event.text == 'Начать' or event.text == 'начать':
                if event.from_user:
                    start_var = 1
                    user_id = event.user_id
                    USERS[user_id] = []
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Пожалуйста напишите:\n1) "ВК" для использования фотографий со своей страницы и страниц '
                                             'своих друзей Вконтакте. ВНИМАНИЕ! для работы Вам будет необходимо на время выполнения обработки сделать профиль НЕ приватным\n2) "Диск" для использования фотографий с вашего яндекс диска')
            elif event.text == 'ВК' or event.text == 'вк' or event.text == 'Вк':
                if event.from_user:
                    user_id = event.user_id
                    USERS[user_id].append("VK")
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Итоговое фото будет иметь отношение сторон 1:1. Пожалуйста укажите размер одной из сторон в количестве фрагментов (10-150). Рекомендовано: 50-100 фрагментов. Чем больше это значение, тем полученное изображение получится более четким, но обработка займет больше времени, и будет необходимо больше фотографий.')
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Чтобы начать заново, напишите "Отмена"')


            elif event.text == 'Диск':
                if event.from_user:
                    user_id = event.user_id
                    USERS[user_id].append("Disk")
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Итоговое фото будет иметь отношение сторон 1:1. Пожалуйста укажите размер одной из сторон в количестве фрагментов (10-150). Рекомендовано: 50-100 фрагментов. Чем больше это значение, тем полученное изображение получится более четким, но обработка займет больше времени, и будет необходимо больше фотографий.')
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Чтобы начать заново, напишите "Отмена"')


            elif event.text == 'Подтвердить' or event.text == 'подтвердить':
                if event.from_user:
                    user_id = event.user_id
                    READY_USER_IDS.append(user_id)
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Заявка принята!\nВаше место в очереди: ' + str(len(READY_USER_IDS)))
            elif event.text == 'Отмена' or event.text == 'отмена':
                if event.from_user:
                    start_var = 1
                    user_id = event.user_id
                    USERS[user_id] = []
                    vk.messages.send(user_id=event.user_id, random_id='',
                                     message='Пожалуйста напишите:\n1) "ВК" для использования фотографий со своей страницы и страниц '
                                             'своих друзей Вконтакте. ВНИМАНИЕ! для работы Вам будет необходимо на время выполнения обработки сделать профиль НЕ приватным\n2) "Диск" для использования фотографий с вашего яндекс диска')

            else:
                try:
                    a = int(event.text)
                    if event.from_user and len(USERS[user_id]) == 1:
                        if int(event.text) < 10:
                            vk.messages.send(user_id=event.user_id, random_id='',
                                             message='Слишком мало!')
                        elif int(event.text) > 150:
                            vk.messages.send(user_id=event.user_id, random_id='',
                                             message='Слишком много!')
                        else:
                            USERS[user_id].append(2 * (int(event.text)) ** 2)
                            USERS[user_id].append(int(event.text))
                            vk.messages.send(user_id=event.user_id, random_id='',
                                             message='Пришлите ссылку на скачивание фотографии с Яндекс Диска, которую хотите составить\n ВНИМАНИЕ! При отправке с конмпьютера ВК может предложить вместо текстовой ссылки отправить кнопку с ссылкой, пожалуйста, НАЖИМАЙТЕ КРЕСТИК и отправляйте ссылку текством!')
                            vk.messages.send(user_id=event.user_id, random_id='',
                                             message='Чтобы начать заново, напишите "Отмена"')

                except Exception:
                    if event.from_user and len(USERS[user_id]) == 3 and USERS[user_id][0] == "VK":
                        user_id = event.user_id
                        USERS[user_id].append(event.text)
                        USERS[user_id].append('')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Ссылка получена')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Напишите "Подтвердить" для начала работы')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Чтобы начать заново, напишите "Отмена"')
                    elif event.from_user and len(USERS[user_id]) == 3 and USERS[user_id][0] == "Disk":
                        user_id = event.user_id
                        USERS[user_id].append(event.text)
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Ссылка получена')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Пришлите ссылку на папку с фотографиями, из которых будет составлена мозаика, на вашем Яндекс Диске.\n ВНИМАНИЕ! На самом Яндекс Диске папку необходимо назвать "Photo_Mosaic"\n ВНИМАНИЕ! При отправке с конмпьютера ВК может предложить вместо текстовой ссылки отправить кнопку с ссылкой, пожалуйста, НАЖИМАЙТЕ КРЕСТИК и отправляйте ссылку текством!')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Чтобы начать заново, напишите "Отмена"')
                    elif event.from_user and len(USERS[user_id]) == 4:
                        user_id = event.user_id
                        USERS[user_id].append(event.text)
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Ссылка получена')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Напишите "Подтвердить" для начала работы')
                        vk.messages.send(user_id=event.user_id, random_id='',
                                         message='Чтобы начать заново, напишите "Отмена"')
        file = open('project_sub_file', 'r')
        working_rn = file.read()
        file.close()
        if len(READY_USER_IDS) > 0 and working_rn == '0':
            file = open('project_sub_file', 'w')
            file.write('1')
            file.close()
            user_id = READY_USER_IDS[0]
            del READY_USER_IDS[0]
            user_mode = USERS[user_id][0]
            user_lines = USERS[user_id][2]
            user_size = USERS[user_id][1]
            user_main = USERS[user_id][3]
            user_link = USERS[user_id][4]
            USERS.pop(user_id)
            working_rn = 1
            p = threading.Thread(target=main_p, args=(user_id, user_size, user_main, user_lines, user_mode, user_link))
            p.start()
    except Exception as e:
        vk.messages.send(user_id=event.user_id, random_id='',
                         message="Упс, возникла неведомая ошибка, попробуйте заново!")
        vk.messages.send(user_id=event.user_id, random_id='',
                         message="Ошибка: " + str(e))
