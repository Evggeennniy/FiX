# pylint: skip-file
def key_generator(keys):
    index = 0
    while True:
        yield keys[index]
        index = (index + 1) % len(keys)


def logging(text: str, color):
    colors = {
        'red': '\033[91m {} \033[0m',
        'green': '\033[92m {} \033[0m',
        'yellow': '\033[93m {} \033[0m',
        'blue': '\033[94m {} \033[0m',
    }
    print(colors.get(color).format(text)) # NOQA


def to_byte(block_id: int | str) -> bytes:
    block_id = bytes(str(block_id), 'utf-8')
    return block_id


def get_time() -> str:
    import datetime

    time_ = datetime.datetime.now()
    hour = time_.hour
    minute = time_.minute

    return f'{hour}:{minute}'
