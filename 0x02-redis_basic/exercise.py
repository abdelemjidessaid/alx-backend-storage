#!/usr/bin/env python3
"""
    Module of class Cache
"""
import redis
import uuid
from typing import Union


class Cache:
    """
        Base class that stores the redis instance
    """

    def __init__(self) -> None:
        """
            The class Cache Constructor
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Method that generates a string using UUID lib
        """
        if data:
            key = str(uuid.uuid4())
            self._redis.set(key, data)
            return key
        else:
            return None
