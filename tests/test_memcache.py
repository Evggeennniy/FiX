# pylint: skip-file
import asyncio
from ..cache import FixClient
from collections import deque


cache = FixClient("127.0.0.1", 11211)


def test_get_or_create_history():
    block_id = 'test'
    maxlen = 1
    exptime = 3

    result = asyncio.get_event_loop().run_until_complete(
        cache.get_or_create_history(block_id, maxlen, exptime)
    )
    assert result == deque(maxlen=maxlen)


def test_update_history():
    block_id = 'test'
    test_history = {'test': 'test'}
    maxlen = 1
    exptime = 3

    update = asyncio.get_event_loop().run_until_complete(
        cache.update_history(block_id, test_history, exptime)
    )
    result = asyncio.get_event_loop().run_until_complete(
        cache.get_or_create_history(block_id, maxlen, exptime)
    )
    assert update is True
    assert result == test_history


def test_cut_off_excess():
    block_id = 'test'
    test_history = {'test': 'test2'}
    maxlen = 1
    exptime = 3

    update = asyncio.get_event_loop().run_until_complete(
        cache.update_history(block_id, test_history, exptime)
    )
    result = asyncio.get_event_loop().run_until_complete(
        cache.get_or_create_history(block_id, maxlen, exptime)
    )
    assert update is True
    assert result == test_history
