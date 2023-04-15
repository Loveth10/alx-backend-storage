#!/usr/bin/env python3
'''0.Create a Cache class. In the __init__ method, store an instance of the Redis client as a private variable named _redis (using redis.Redis()) and flush the instance using flushdb.


Type-annotate store correctly. Remember that data can be a str,
bytes, int or float.


1.Redis only allows to store string, bytes and numbers (and lists thereof). Whatever you store as single elements, it will be returned as a byte string. Hence if you store "a" as a UTF-8 string, it will be returned as b"a" when retrieved from the server.


Remember to conserve the original Redis.get behavior if the key does not exist.
'''


import redis
import uuid
from typing import Union, Callable
from functools import wraps

''' type annotation '''
difData = Union[int, float, str, bytes]

'''
    function that increments the count for that key every time
    the method is called and returns the value returned by the
    original method.
'''


def count_calls(method: Callable) -> Callable:
    ''' decorator returns a callable wraps from funtools'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' uses the incr method to keep count '''
        key = method.__qualname__
        myRedisDB = self._redis
        myRedisDB.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''decorator using the wrap method from functools'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            store the history of inputs and outputs for a particular
            function.
        '''
        input_key = method.__qualname__ + ':inputs'
        output_key = method.__qualname__ + ':outputs'
        input_str = str(args)
        ''' using rpush to append the input arguments.'''
        self._redis.rpush(input_key, input_str)
        ''' gets output by executing the wrapped func method '''
        output = method(self, *args, **kwargs)
        output_str = str(output)
        self._redis.rpush(output_key, output_str)
        return output
    return wrapper

def replay(fn: Callable):
    
    input_key = fn.__qualname__ + ':inputs'
    output_key = fn.__qualname__ + ':outputs'
    Input = fn._redis.lrange(input_key, 0, -1)
    Output = fn._redis.lrange(output_key, 0, -1)
    for i, (input_str, output_str) in enumerate(zip(Input, Output)):
        input_file = input_str.decode('utf-8')
        output_file = output_str.decode('utf-8')
    return (input_file, output_file)

class Cache:
    '''
        class creates an instance of the Redis saves in a private class
        attribute and generates a random key using the uuid4 method
    '''
    def __init__(self):
        ''' creates an instance of redis '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: difData) -> str:
        '''
            returns random generated value key
        '''
        _key: str = str(uuid.uuid4())
        self._redis.set(_key, data)
        return _key

    def get(self, key: str, fn=None):
        '''
            get method uses a callable function to decode data from str
            or uses the decode method to convert to a desired str
        '''
        data = self._redis.get(key)
        if fn:
            data = fn(data)
            return data
        else:
            return data

    def get_str(self, key: str):
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, fn=lambda x: int(x))
