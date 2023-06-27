def key_generator(keys):
    index = 0
    while True:
        yield keys[index]
        index = (index + 1) % len(keys)


def logging(text: str):
    print(text) # NOQA


def to_byte(self, block_id: int | str):
    block_id = bytes(str(block_id), 'utf-8')
    return block_id
