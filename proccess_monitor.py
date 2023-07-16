# pylint: skip-file
"""The module that shows """
import utils
import psutil
import sys


def monitor_resources():
    while True:
        cpu_percent = psutil.cpu_percent(interval=5)
        ram_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('C:\PYTHON3\PracticeCODE\FiX').percent

        utils.logging(f"CPU: {cpu_percent}% - RAM: {ram_percent}% - Disk: {disk_percent}%")


if __name__ == "__main__":
    try:
        utils.logging('Монитор ресурсов начинает работу.')
        monitor_resources()
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        utils.logging('Монитор ресурсов завершает работу.')