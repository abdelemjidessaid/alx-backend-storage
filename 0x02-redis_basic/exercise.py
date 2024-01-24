#!/usr/bin/env python3
"""
    Module of class Cache
"""
import redis
import uuid


class Cache:
    """
        Base class that stores the redis instance
    """
    def __init__(self) -> None:
        """
            The class Cache Constructor
        """
        self.__redis = redis.Redis()

    def store(self, data: [str, bytes, int, float]) -> str:
        """
            Method that generates a string using UUID lib
        """
        key = str(uuid.uuid4())
        self.__redis.set(key, data)

        return key
