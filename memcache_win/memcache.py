"""Start this if you're using Windows"""
import sys
import subprocess

if __name__ == "__main__":
    try:
        print('Memcache запущен.')
        subprocess.call('memcache.exe', shell=True)
    except KeyboardInterrupt:
        print('Memcache Завершает работу.')
        sys.exit(0)
