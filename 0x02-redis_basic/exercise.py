#!/usr/bin/env python3
"""
    Module of class Cache
"""
import redis
import uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
        Method that counts the calls of Cache methods
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
            Function that wraps called method and increment its
            call to Redis Database
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


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

    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
            Method that returns the data with the specific type
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)
        return value

    def get_str(self, data: bytes) -> str:
        """
            Method that converts bytes to string
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
            Method that converts bytes to integers
        """
        return int(data)
