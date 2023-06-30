"""Modules for working with cache."""
from collections import deque
import pickle
import aiomcache


class FixClient(aiomcache.Client):
    """
    Extended client module for working with shorter asynchronous methods.
    """
    async def update_history(self, block_id: int | str, new_history: deque, exptime):
        """
        This method to update cache.
        """
        block_id = str(block_id).encode('utf-8')
        new_history = pickle.dumps(new_history)
        await self.replace(key=block_id, value=new_history, exptime=exptime)

        return True

    async def get_or_create_history(self, block_id: int | str, maxlen: int, exptime: int):
        """
        This method to get or create cache with pickle & deque.
        """
        block_id = str(block_id).encode('utf-8')
        history = await self.get(block_id)
        if history is not None:
            history = pickle.loads(history)
            return history
        new_history = deque(maxlen=maxlen)
        await self.set(key=block_id, value=pickle.dumps(new_history), exptime=exptime)
        return new_history
