#!/usr/bin/env python3
"""Change school topics"""


def update_topics(mongo_collection, name, topics):
    """hange school topics

    Args:
        mongo_collection(Collection)
        name: (str)
        topics: [str]
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
