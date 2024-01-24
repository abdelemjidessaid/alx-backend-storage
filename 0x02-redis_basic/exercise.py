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


def call_history(method: Callable) -> Callable:
    """
        Function that stores the history of inputs and outputs
        for a particular function
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """
            Function that wraps the called method
            and stores its args in Redis database
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)

        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
        Function that display the history of calls of
        a particular function
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


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

    @call_history
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
