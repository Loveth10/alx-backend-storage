#!/usr/bin/env python3
"""
Change school topics
"""
import pymongo



def update_topics(mongo_collection, name, topics):
    '''
        using the update_many  method to update
        items in a collection
    '''
    db = mongo_collection.update_many(
                                {'name': name},
                                {'$set': {'topic': topics}}
                )

    return db
