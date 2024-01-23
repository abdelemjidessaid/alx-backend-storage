#!/usr/bin/env python3
"""
    Script that lists all logs of Nginx
"""


from pymongo import MongoClient


def list_logs():
    """
        Function that lists the logs
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count

    status = collection.count_documents({"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"    method {method}: {method_counts[method]}")
    print(f"{status} status check")


if __name__ == '__main__':
    list_logs()
