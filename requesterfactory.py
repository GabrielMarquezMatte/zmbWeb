import json
from typing import Literal, Any
import requests
import aiohttp
import aiofiles

class RequesterFactory:
    @staticmethod
    def create(session:requests.Session, type:Literal["api","dummy"]):
        if (type == "api"):
            return APIRequester(session)
        elif (type == "dummy"):
            return DummyRequester()
        else:
            raise ValueError(f"Tipo de requester {type} não existe")

class AsyncRequesterFactory:
    @staticmethod
    def create(session:aiohttp.ClientSession, type:Literal["api","dummy"]):
        if (type == "api"):
            return AsyncAPIRequester(session)
        elif (type == "dummy"):
            return AsyncDummyRequester()
        else:
            raise ValueError(f"Tipo de requester {type} não existe")

class APIRequester:
    def __init__(self, session:requests.Session):
        self.session = session

    def make_request(self, url:str, method:str, payload:dict[str,Any], verify:bool = True) -> dict[str,Any]:
        if method == "POST":
            response = self.session.post(url, json=payload, verify=verify)
        else:
            response = self.session.get(url, params=payload, verify=verify)
        if response.status_code in [200, 400]:
            return response.json()
        else:
            response.raise_for_status()

class AsyncAPIRequester:
    def __init__(self, session:aiohttp.ClientSession):
        self.session = session

    async def make_request(self, url:str, method:str, payload:dict[str,Any], verify:bool = True) -> dict[str,Any]:
        if method == "POST":
            response = await self.session.post(url, json=payload, verify_ssl=verify)
        else:
            response = await self.session.get(url, params=payload, verify_ssl=verify)
        if response.status in [200, 400]:
            return await response.json()
        else:
            response.raise_for_status()

class DummyRequester:
    @staticmethod
    def make_request(*_) -> dict[str,Any]:
        with open('json/file01.json') as f:
            return json.load(f)

class AsyncDummyRequester:
    @staticmethod
    async def make_request(*_) -> dict[str,Any]:
        async with aiofiles.open('json/file01.json') as f:
            return json.loads(await f.read())