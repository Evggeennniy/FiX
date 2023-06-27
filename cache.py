from collections import deque
import pickle
import aiomcache


class FixClient(aiomcache.Client):
    async def update_history(self, block_id: int | str, new_history: deque, exptime):
        block_id = str(block_id).encode('utf-8')
        new_history = pickle.dumps(new_history)
        await self.replace(block_id, new_history, exptime=exptime)

        return True

    async def get_or_create_history(self, block_id: int | str, maxlen: int, exptime: int):
        block_id = str(block_id).encode('utf-8')
        history = await self.get(block_id)
        if history is not None:
            history = pickle.loads(history)
            return history
        new_history = deque(maxlen=maxlen)
        await self.set(block_id, pickle.dumps(new_history), exptime=exptime)
        return new_history


cache = FixClient("127.0.0.1", 11211)
