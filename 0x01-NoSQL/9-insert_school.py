#!/usr/bin/env python3
"""
    Script that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
        Function that inserts a new document in a collection based on kwargs
    """
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
