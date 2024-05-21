import requests
import speech_recognition
import pyttsx3
import keyboard
from googletrans import Translator
import os
import datetime

translater = Translator()
list_exe = []
list_paths = []
list_paths2 = []
domens = ['', '.com', '.ru', '.рф', '.net', '.org', '.ru.net']


def addToPath():
    global list_paths, list_paths2, list_exe
    user = os.environ.get("USERNAME")
    path = f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".lnk"):
                path_file = os.path.join(root, file)
                list_paths.append(path_file)
    for i in range(len(list_paths)):
        list_paths2.append(str(list_paths[i]).split("Programs\\")[1])
        try:
            list_exe.append(str(list_paths2[i]).split("\\")[1])
        except:
            list_exe.append(str(list_paths2[i]))
    list_paths2 = []
    path = "C:\\Program Files"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe"):
                path_file = os.path.join(root, file)
                list_paths2.append(path_file.split("\\"))
    print(1)
    path = 'C:\\Program Files (x86)'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe"):
                path_file = os.path.join(root, file)
                list_paths2.append(path_file.split("\\"))
    path = "C:\\Windows\\System32"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe"):
                path_file = os.path.join(root, file)
                list_paths2.append(path_file.split("\\"))
    for i in range(0, len(list_paths2) - 1):
        list_exe.append(str(list_paths2[i][len(list_paths2[i]) - 1]))
        list_paths.append("\\".join(list_paths2[i]))
    for i in range(len(list_paths)):
        list_paths[i] = list_paths[i].lower()
    for i in range(len(list_exe)):
        list_exe[i] = list_exe[i].lower()
    print(list_exe)


def set_volume(volume):
    for _ in range(0, 50):
        keyboard.press_and_release("volume down")
    for _ in range(int(volume) // 2):
        keyboard.press_and_release("volume up")


def take_command():
    with speech_recognition.Microphone() as mic:
        sr = speech_recognition.Recognizer()
        sr.pause_threshold = 0.5
        sr.adjust_for_ambient_noise(mic, duration=0.5)
        print('слушаю')
        audio = sr.listen(mic)
        print('Расшифровываю')
        try:
            query = sr.recognize_google(audio, language="ru-RU").lower()
            return query
        except speech_recognition.UnknownValueError:
            pass
        except Exception as e:
            print(f'[!] Error: {e}')


def get_day():
    now = datetime.datetime.today()
    dow = str(now.weekday())
    if dow == "0":
        dow = "понедельник"
    elif dow == "1":
        dow = "вторник"
    elif dow == "2":
        dow = "среда"
    elif dow == "3":
        dow = "четверг"
    elif dow == "4":
        dow = "пятница"
    elif dow == "5":
        dow = "суббота"
    else:
        dow = "воскресенье"

    month = ''
    month_date = now.strftime("%m")
    print(month_date)
    if month_date == '01':
        month = "Января"
    elif month_date == '02':
        month = "Февраля"
    elif month_date == '03':
        month = "Марта"
    elif month_date == '04':
        month = "Апреля"
    elif month_date == '05':
        month = "Мая"
    elif month_date == '06':
        month = "Июня"
    elif month_date == '07':
        month = "Июля"
    elif month_date == '08':
        month = "Августа"
    elif month_date == '09':
        month = "Сентября"
    elif month_date == '10':
        month = "Октября"
    elif month_date == '11':
        month = "Ноября"
    elif month_date == '12':
        month = "Декабря"

    numberOfMonth = str(now.strftime("%d"))
    if numberOfMonth[0] == '0':
        numberOfMonth = numberOfMonth[1]

    answer = dow + ", " + numberOfMonth + " " + month

    return answer


def kill_process(process_name):
    if process_name == "гугл":
        process_name = "google"
    if process_name == "калькулятор":
        process_name = "calc"
    if process_name == "яндекс":
        process_name = "yandex"
    if process_name == "блокнот":
        process_name = "notepad"
    if process_name == "дискорд":
        process_name = "discord"
    try:
        process_name = translater.translate(process_name, dest="en").text
    except:
        pass

    print(process_name)
    try:
        os.system('tskill ' + process_name)
        return True
    except:
        return False


def open_exe(file_name):
    global list_paths, list_exe
    if file_name == "гугл":
        file_name = "google"
    if file_name == "калькулятор":
        file_name = "calc"
    if file_name == "яндекс":
        file_name = "yandex"
    if file_name == "блокнот":
        file_name = "notepad"
    try:
        file_name = translater.translate(file_name, dest="en").text
    except:
        pass

    if file_name.lower()+".lnk" in list_exe:
        print(list_paths[(list_exe.index(file_name.lower()+'.lnk'))])
        os.startfile(list_paths[(list_exe.index(file_name.lower()+'.lnk'))])
        return True
    if file_name.lower()+".exe" in list_exe:
        print(list_paths[(list_exe.index(file_name.lower() + '.exe'))])
        os.startfile(list_paths[(list_exe.index(file_name.lower() + '.exe'))])
        return True
    return False


def check_site(site_name):
    try:
        site_name = translater.translate(site_name, dest="en").text
    except:
        pass
    for domen in domens:
        site = f'https://www.{site_name}{domen}'
        try:
            requests.get(site)
            print('123')
            return f'http://www.{site_name}{domen}'
        except:
            continue
    return None
