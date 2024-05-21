import random
import socket
import webbrowser
from threading import Thread
from fuzzywuzzy import fuzz
from variable import opts
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import ipinfo

translater = Translator()
SERVER_HOST = '192.168.34.164'
SERVER_PORT = 4578
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options)

client_sockets = {}
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'[*] Listening as {SERVER_HOST}:{SERVER_PORT}')


def first_processing(msg):  # Убрать из сообщения ненужные слова
    for opt in opts['alias']:
        msg = msg.replace(opt, '')
    for opt in opts['tbr']:
        msg = msg.replace(opt, '')
    return msg


def second_processing_full(msg):  # Проверка всей строки
    result = {'cmd': '', 'percent': 0}
    for key, meaning in opts['cmd'].items():
        for keyword in meaning:
            percent = fuzz.ratio(msg, keyword)
            if percent > result['percent']:
                if key == 'off_windows' or key == 'restart_windows' or key == 'off_screen' or key == 'kill_process':
                    if percent >= 81:
                        result['cmd'] = key
                        result['percent'] = percent
                else:
                    result['cmd'] = key
                    result['percent'] = percent
    if result['percent'] <= 56:
        result['cmd'] = 'unclear'
    print(f"{result['cmd']}, {result['percent']}")
    return result


def second_processing_first_word(msg):  # Проверка на первое слово
    msg = ''.join(msg.split(" ")[:1])
    result = {'cmd': '', 'percent': 0}
    for key, meaning in opts['cmd'].items():
        for keyword in meaning:
            percent = fuzz.ratio(msg, keyword)
            if percent > result['percent']:
                if key == 'off_windows' or key == 'restart_windows' or key == 'off_screen' or key == 'kill_process':
                    if percent >= 81:
                        result['cmd'] = key
                        result['percent'] = percent
                else:
                    result['cmd'] = key
                    result['percent'] = percent
    if result['percent'] <= 56:
        result['cmd'] = 'unclear'
    print(f"{result['cmd']}, {result['percent']}")
    return result


def second_processing_last_word(msg):  # Проверка на последнее слово
    msg = ''.join(msg.split(" ")[-1:])
    result = {'cmd': '', 'percent': 0}
    for key, meaning in opts['cmd'].items():
        for keyword in meaning:
            percent = fuzz.ratio(msg, keyword)
            if percent > result['percent']:
                if key == 'off_windows' or key == 'restart_windows' or key == 'off_screen' or key == 'kill_process':
                    if percent >= 81:
                        result['cmd'] = key
                        result['percent'] = percent
                else:
                    result['cmd'] = key
                    result['percent'] = percent
    if result['percent'] <= 56:
        result['cmd'] = 'unclear'
    print(f"{result['cmd']}, {result['percent']}")
    return result


def second_processing(msg):  # Какую функцию выбрать
    result_full = second_processing_full(msg)
    result_first_word = second_processing_first_word(msg)
    result_last_word = second_processing_last_word(msg)
    if result_first_word['percent'] > result_full['percent'] and \
            result_first_word['percent'] > result_last_word['percent']:
        if result_first_word['cmd'] == 'kill_process' or result_first_word['cmd'] == 'youtube' or \
                result_first_word['cmd'] == 'kill_process' or result_first_word['cmd'] == 'write' or \
                result_first_word['cmd'] == 'open' or result_first_word['cmd'] == 'kill_volume' or \
                result_first_word['cmd'] == 'weather' or result_first_word['cmd'] == 'search_browser':
            print(f'[!] cmd: {result_first_word["cmd"]}')
            return result_first_word['cmd']
    if result_last_word['percent'] > result_first_word['percent'] \
            and result_last_word['percent'] > result_full['percent']:
        if result_last_word['cmd'] == 'kill_process' or result_last_word['cmd'] == 'youtube' or \
                result_last_word['cmd'] == 'kill_process' or result_last_word['cmd'] == 'write' or \
                result_last_word['cmd'] == 'open' or result_last_word['cmd'] == 'kill_volume' or \
                result_last_word['cmd'] == 'weather' or result_last_word['cmd'] == 'search_browser':
            print(f'[!] cmd: {result_last_word["cmd"]}')
            return result_last_word['cmd']
    print(f'[!] cmd: {result_full["cmd"]}')
    return result_full['cmd']


def internet_search(msg):
    search_words = str(msg.replace(' ', '+'))
    search = 'https://www.google.com/search?q=' + search_words

    try:
        driver.get(search)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        try:
            name = soup.find('span', class_='LWPArc').text
            word_definition = soup.find('div', style='display:inline').text
            return f'speak, {name + " - " + word_definition}'
        except:
            name__word_definition = soup.find('span', class_='hgKElc').text
            return f'speak, {name__word_definition}'
    except Exception as e:
        print(f'[E] {e}')
        return f'search_browser, {search}'


def get_number_from_str(string):
    nums = '0123456789'
    num = ''
    for i in list(string):
        if i in nums:
            num += i
    if num == '':
        return 'error_level'
    num = int(num)
    if num < 0 or num > 100:
        return 'error_valid_number'
    return num


def processing(msg):  # Функция, которая вызывает другие функции для обработки сообщения
    msg = first_processing(msg)
    cmd = second_processing(msg)
    if cmd == 'open':
        to_open = ''
        for word in msg.split(' '):
            if not (word in opts['filtration_word']['open']['WebSite']) and \
                    not (word in opts['filtration_word']['open']['EXE']):
                to_open += word + ' '
        if to_open == '':
            return f'{cmd}, 0'
        if to_open[-1] == ' ':
            to_open = to_open[:-1]
        return f'{cmd}, {to_open}'
    if cmd == 'search_browser':
        answer = internet_search(msg)
        return answer
    if cmd == 'volume':
        num = get_number_from_str(msg)
        return f'{cmd}, {num}'
    if cmd == 'write':
        to_write = ''
        for word in msg.split(' '):
            if not (word in opts['filtration_word']['write']):
                to_write += ' ' + word
        if to_write == '':
            return f'{cmd}, 0'
        return f'{cmd}, {to_write[1:]}'
    if cmd == 'verse':
        file = open('verses.txt', 'r')
        verses = file.readlines()
        file.close()
        return f'{cmd}, {verses[random.randint(0, len(verses) - 1)].strip()}'
    if cmd == 'joke':
        file = open('jokes.txt', 'r')
        jokes = file.readlines()
        file.close()
        return f'{cmd}, {jokes[random.randint(0, len(jokes) - 1)].strip()}'
    if cmd == 'kill_process':
        to_kill = ''
        for word in msg.split(' '):
            if not(word in opts["filtration_word"]["kill_process"]):
                to_kill += word
        print(to_kill)
        if to_kill == '':
            return f'{cmd}, 0'
        return f'{cmd}, {to_kill}'
    return f'{cmd}, 0'


def listen_for_client(cs, ca, name_ID):  # Функция сервера, которая слушает клиента
    ID = "-".join(name_ID.split("-")[1:])
    if name_ID.split('-')[0] == 'D':
        while True:
            try:
                message = cs.recv(1024).decode()
                print(f'[D]: {message}')
                if message == '':
                    break
                # команды по одной форме NAME, NUM, пример: DHT, 37.7
                if str(message).split(',')[0] == 'DHT':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'K':
                            client_sock.send(f'speak, Температура в доме: {str(message).split(", ")[1]}'.encode())
                print(f'[!] {name_ID}: {message}')
            except WindowsError:
                client_sockets.pop(cs)
                break
            except Exception as e:
                print(f'[!] Error: {e}')
        print(f'[-] {ca} - {name_ID}, disconnected.')
    else:
        while True:
            try:
                message = cs.recv(1024).decode()
                if message == '':
                    break
                print(f'[!] {name_ID}: {message}')
                cmd = processing(message.lower())
                if cmd.split(',')[0] == 'window_open':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('W-0'.encode())
                elif cmd.split(',')[0] == 'window_close':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('W-1'.encode())

                elif cmd.split(',')[0] == 'water_on':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('B-1'.encode())
                elif cmd.split(',')[0] == 'water_off':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('B-0'.encode())

                elif cmd.split(',')[0] == 'light_on':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('L-1'.encode())
                elif cmd.split(',')[0] == 'light_off':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('L-0'.encode())
                elif cmd.split(',')[0] == 'get_temperature':
                    for client_sock in client_sockets:
                        if '-'.join(client_sockets[client_sock].split('-')[1:]) == ID \
                                and client_sockets[client_sock].split('-')[0] == 'D':
                            client_sock.send('DHT'.encode())
                cs.send(cmd.encode())
            except WindowsError:
                client_sockets.pop(cs)
                break
            except Exception as e:
                print(f'[!] Error: {e}')
        print(f'[-] {ca} - {name_ID}, disconnected.')


while True:  # Запуск процесса сервера
    client_socket, client_address = s.accept()
    received_name_ID = str(client_socket.recv(1024).decode())
    print(f'[+] {client_address} - {received_name_ID}, connected.')
    client_sockets[client_socket] = received_name_ID
    t = Thread(target=listen_for_client, args=(client_socket, client_address, received_name_ID))
    t.daemon = True
    t.start()
