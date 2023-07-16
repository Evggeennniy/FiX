"""Modules for working with cache."""
from collections import deque
import pickle
import aiomcache


class BotCacheClient(aiomcache.Client):
    """
    Extended client module for working with shorter asynchronous methods.
    """

    LENGHT_OF_DATA = 15  # max length of data
    TIME_OF_EXP = 60 * 30  # seconds * minutes

    async def update_history(self, block_id: int | str, new_history: deque, update_time=TIME_OF_EXP):
        """
        This method to update cache.
        """
        block_id = str(block_id).encode('utf-8')
        new_history = pickle.dumps(new_history)
        await self.replace(key=block_id, value=new_history, exptime=update_time)

        return True

    async def get_or_create_history(self, block_id: int, maxlen: int = LENGHT_OF_DATA, exptime: int = TIME_OF_EXP):
        """
        This method to get or create cache with pickle & deque.
        """
        block_id = str(block_id).encode('utf-8')
        history = await self.get(key=block_id)
        if history is not None:
            history = pickle.loads(history)
            return history
        new_history = deque(maxlen=maxlen)
        await self.set(key=block_id, value=pickle.dumps(new_history), exptime=exptime)
        return new_history
