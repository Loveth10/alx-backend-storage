#!/usr/bin/env python3
"""List all documents in Python"""
from typing import Dict


def list_all(mongo_collection):
    """Return list of all docs in collection"""
    if not mongo_collection:
        return []

    Prototype: def list_all(mongo_collection):
    Return an empty list if no document in the collection
    mongo_collection will be the pymongo collection object"""
    return mongo_collection.find()
