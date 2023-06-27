# from ..utils import logging

## Start this if you're using Windows

import subprocess

if __name__ == "__main__":
    try:
        print('Memcache запущен.')
        subprocess.call('memcache.exe', shell=True)
    except KeyboardInterrupt:
        print('Memcache Завершает работу.')
        exit()
