import os
import sys
import win32com.shell.shell as shell
import winsound
import ftplib as ftp
import ssl
import sched
import time
from pygame import mixer

HOST = input("Host\n")  # 'ftp.dlptest.com'
PORT = int(input("Port(DEFAULT: 21)\n"))  # 12121
USER = input("Username\n")  # 'dlpuser@dlptest.com'
PwD = input("Password\n")  # 'fLDScD4Ynth0p4OJ6bW6qCxjh'
SOUND_URL = 's.mp3'
mixer.init()
mixer.music.load(SOUND_URL)


def connect():
    ftps = ftp.FTP_TLS()
    # ftps.ssl_version = ssl.PROTOCOL_TLSv1_2
    ftps.debugging = 2
    ftps.connect(HOST, PORT)  # YOU CAN ADD SPECIFIC PORT
    ftps.login(USER, PwD)
    print("Connection established!")
    return ftps


data = ""


def check(initial=False):
    global data
    mixer.music.stop()
    with connect() as ftp:
        new_data = ''.join(ftp.nlst())
        if not initial:
            print("DATA", data)
            print('NEW DATA', new_data)
            if data != new_data:
                print("GOTCHA")
                mixer.music.play()
        data = new_data
        ftp.quit()


def run_as_admin():
    ASADMIN = 'asadmin'

    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(
            lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        print("I am root now.")
        check()


s = sched.scheduler(time.time, time.sleep)


def repeat(sc):
    check()
    s.enter(30, 1, repeat, (sc,))


check(True)
s.enter(30, 1, repeat, (s,))
s.run()

# run_as_admin()
