import socket
from threading import Thread
from threading import Condition
import requests
import keyboard
import pyttsx3
from functions import *
from variable import opts
import random
import webbrowser
import time
import datetime
import win32gui
import win32con

SERVER_HOST = "192.168.34.164"
SERVER_PORT = 4578
cond_var = Condition(lock=None)
ID = "K-280823-111111"
windows_command = False

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
s.send(ID.encode())


def speak(msg):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice = {}

    for i in range(len(voices)):
        voice[voices[i].name] = voices[i]

    if "Aleksandr" in voice.keys():
        engine.setProperty("voice", voice.get('Aleksandr').id)
    engine.say(msg)
    engine.runAndWait()


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print(message)
        cmd = message.split(', ')[0]
        argument = ', '.join(message.split(', ')[1:])
        if cmd == 'hello':
            rand = random.randint(0, len(opts['answer']['hello']) - 1)
            print(opts['answer']['hello'][rand])
            speak(opts['answer']['hello'][rand])
        elif cmd == 'speak':
            print(argument)
            speak(argument)
        elif cmd == 'search_browser':
            webbrowser.open(argument)
            rand = random.randint(0, len(opts['answer']['open']['accept']) - 1)
            print(opts['answer']['open']['accept'][rand])
            speak(opts['answer']['open']['accept'][rand])
        elif cmd == 'volume':
            if argument == 'error_valid_number':
                print(opts['answer']['volume']['error_valid_number'])
                speak(opts['answer']['volume']['error_valid_number'])
            elif argument == 'error_level':
                print(opts['answer']['volume']['error_level'])
                speak(opts['answer']['volume']['error_level'])
            else:
                set_volume(argument)
                time.sleep(0.3)
                print(opts['answer']['volume']['accept'])
                speak(opts['answer']['volume']['accept'])
        elif cmd == 'time':
            str_time = datetime.datetime.now().strftime("%H: %M")
            rand = random.randint(0, len(opts['answer']['time']) - 1)
            str_time = opts['answer']['time'][rand] + str_time
            print(str_time)
            speak(str_time)
        elif cmd == 'off_screen':
            rand = random.randint(0, len(opts['answer']['off_screen']) - 1)
            print(opts['answer']['off_screen'][rand])
            speak(opts['answer']['off_screen'][rand])
            win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
        elif cmd == 'off_windows':
            if windows_command:
                rand = random.randint(0, len(opts['answer']['off_windows']) - 1)
                print(opts['answer']['off_windows'][rand])
                speak(opts['answer']['off_windows'][rand])
                os.system('shutdown /p /f')
            else:
                print(opts['answer']['func_windows'])
                speak(opts['answer']['func_windows'])
        elif cmd == 'restart_windows':
            rand = random.randint(0, len(opts['answer']['restart_windows']) - 1)
            print(opts['answer']['restart_windows'][rand])
            speak(opts['answer']['restart_windows'][rand])
            os.system("shutdown -t 0 -r -f")
        elif cmd == 'how_are_you':
            rand = random.randint(0, len(opts['answer']['how_are_you']) - 1)
            print(opts['answer']['how_are_you'][rand])
            speak(opts['answer']['how_are_you'][rand])
        elif cmd == 'write':
            keyboard.write(argument)
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'thanks':
            rand = random.randint(0, len(opts['answer']['thanks']) - 1)
            print(opts['answer']['thanks'][rand])
            speak(opts['answer']['thanks'][rand])
        elif cmd == 'fire':
            print("Я вызвал скорую помощь, а также пожарных.")
            speak("Я вызвал скорую помощь, а также пожарных.")
            print("1. Покиньте место пожара. 2. Не паникуйте. 3. Не пользуйтесь лифтом. "
                  "4. В задымленном помещении продвигайтесь как можно ниже к полу.")
            speak("1. Покиньте место пожара. 2. Не паникуйте. 3. Не пользуйтесь лифтом. "
                  "4. В задымленном помещении продвигайтесь как можно ниже к полу.")
        elif cmd == 'creator':
            print(opts['answer']['creator'])
            speak(opts['answer']['creator'])
        elif cmd == 'yourself':
            print(opts['answer']['yourself'])
            speak(opts['answer']['yourself'])
        elif cmd == 'what_are_you_doing':
            rand = random.randint(0, len(opts['answer']['what_are_you_doing']) - 1)
            print(opts['answer']['what_are_you_doing'][rand])
            speak(opts['answer']['what_are_you_doing'][rand])
        elif cmd == 'turn':
            keyboard.press("left windows")
            keyboard.press_and_release('d')
            keyboard.release('left windows')
            print(opts["answer"]["turn"])
            speak(opts['answer']['turn'])
        elif cmd == 'ctrl+c':
            keyboard.press_and_release("ctrl+c")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'ctrl+v':
            keyboard.press_and_release("ctrl+v")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'ctrl+x':
            keyboard.press_and_release("ctrl+x")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'change_lang':
            keyboard.press_and_release("ctrl+shift")
            keyboard.press_and_release("alt+shift")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'delete':
            keyboard.press_and_release("delete")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'alt+f4':
            keyboard.press_and_release("alt+f4")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'ctrl+a':
            keyboard.press_and_release("ctrl+a")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'enter':
            keyboard.press_and_release("enter")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'esc':
            keyboard.press_and_release("esc")
            print(opts["answer"]["complete"])
            speak(opts["answer"]["complete"])
        elif cmd == 'what_is_your_name':
            print(opts["answer"]["what_is_your_name"])
            speak(opts["answer"]["what_is_your_name"])
        elif cmd == 'get_day':
            answer = get_day()
            print(answer)
            speak(answer)
        elif cmd == 'joke':
            print(argument)
            speak(argument)
        elif cmd == 'verse':
            print(argument)
            speak(argument)
        elif cmd == 'kill_process':
            if argument == '0':
                print(opts["answer"]["kill_process"]["deny"])
                speak(opts["answer"]["kill_process"]["deny"])
            elif kill_process(argument):
                print(opts["answer"]["complete"])
                speak(opts["answer"]["complete"])
            else:
                print(opts["answer"]["kill_process"]["deny"])
                speak(opts["answer"]["kill_process"]["deny"])
        elif cmd == 'open':
            if argument == '0':
                print(opts['answer']['open']['deny']['EXE'])
                speak(opts['answer']['open']['deny']['EXE'])
            elif open_exe(argument):
                print(opts["answer"]["open"]["accept"][0])
                speak(opts["answer"]["open"]["accept"][0])
            else:
                web_site = check_site(argument)
                if web_site is not None:
                    webbrowser.open(web_site)
                    print(opts["answer"]["open"]["accept"][1])
                    speak(opts["answer"]["open"]["accept"][1])
                else:
                    print(opts['answer']['open']['deny']['WebSite'])
                    speak(opts['answer']['open']['deny']['WebSite'])
        with cond_var:
            cond_var.notify()


if __name__ == "__main__":

    print('Loading...')
    addToPath()
    print('Started')

    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()

    while True:
        command = take_command()
        if command is not None:
            print('Вы сказали: ', command)
            s.send(command.encode())
            with cond_var:
                cond_var.wait()
        else:
            print('Вы ничего не сказали')

    s.close()
