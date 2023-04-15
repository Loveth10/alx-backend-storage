#!/usr/bin/env python3
"""Log stats -new version"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    print("{:d} logs".format(nginx.count_documents({})))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print("\tmethod {}: {:d}".
              format(method,
                     nginx.count_documents({"method": method})))
    print("{:d} status check".format(
        nginx.count_documents({"method": "GET", "path": "/status"})))
    print("IPs:")
    ips = nginx.aggregate(
        [{"$group": {"_id": "$ip",
                     "count": {"$sum": 1},
                     "totalValue": {"$sum": "$value"}
                     },
          },
         {"$sort": {"count": -1}},
         {"$limit": 10}
         ])
    for d in ips:
        print("\t{}: {:d}".format(d.get('_id'), d.get('count')))
