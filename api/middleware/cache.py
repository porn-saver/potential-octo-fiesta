import hashlib

from cachetools import TTLCache
from fastapi import Request
from copy import copy

cache = TTLCache(maxsize=1000, ttl=300)


def checkCacheDate(request: Request):
    url: str = str(request.url).lower().replace(" ", "-")
    cache_key = f"cached_data:{url}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    return False


def setCacheData(request: Request, data):
    response = [value.toJson() for value in data]
    response = response[0] if len(response) == 1 else response
    aux = copy(request)
    url: str = str(aux.url).lower().replace(" ", "-")
    cache_key = f"cached_data:{url}"
    cache[cache_key] = response
    return response


def setCacheDataEnum(request: Request, enum, isJson: bool = False):
    response = enum if isJson else [{data.name: data.value for data in enum}]
    response = response[0] if len(response) == 1 else response
    aux = copy(request)
    url: str = str(aux.url).lower().replace(" ", "-")
    cache_key = f"cached_data:{url}"
    cache[cache_key] = response
    return response


async def getBody(request: Request):
    body = []
    return body
