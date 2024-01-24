#!/usr/bin/env python3
"""
    Module that contains a function that obtain the
    HTML content of a particular URL and returns it
"""
import requests
import redis
import time
from functools import wraps


r = redis.Redis(host='localhost', port=6379, db=0)


def cache_page(func):
    """
        Function that caches the page content
    """
    @wraps(func)
    def wrapper(url):
        """
            Wrapper function
        """
        cached_result = r.get(url)
        if cached_result is not None:
            return cached_result.decode()

        page_content = func(url)
        r.setex(url, 10, page_content)

        count_key = f"count:{url}"
        r.incr(count_key)

        return page_content

    return wrapper


@cache_page
def get_page(url):
    """
        Function that fetches the HTML content of the visited URL
    """
    response = requests.get(url)
    return response.text


slow_url = "http://slowwly.robertomurray.co.uk"
page_content = get_page(slow_url)
print(page_content)

cached_content = get_page(slow_url)
print(cached_content)

time.sleep(10)

new_content = get_page(slow_url)
print(new_content)

count_key = f"count:{slow_url}"
access_count = r.get(count_key)
print(f"Access count for {slow_url}: {access_count.decode()}")

r.close()
