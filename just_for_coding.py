import pymemcache
import pickle


my_key = '414902937'
cache = pymemcache.Client(("127.0.0.1", 11211))

def get_history(id=my_key):
    history = cache.get(str(id))
    if history is not None:
        history = pickle.loads(history)
        print(history)
        print(f'История составляет {len(history)} елементов, длина символов {len(str(history))}')
    else:
        print('История не найдена либо её срок жизни истёк.')

get_history()