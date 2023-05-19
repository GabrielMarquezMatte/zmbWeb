import json
from typing import Literal, Any
import requests

class RequesterFactory:
    @staticmethod
    def create(session:requests.Session, type:Literal["api","dummy"]):
        if (type == "api"):
            return APIRequester(session)
        elif (type == "dummy"):
            return DummyRequester()
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

class DummyRequester:
    @staticmethod
    def make_request(*_) -> dict[str,Any]:
        with open('json/file01.json') as f:
            return json.load(f)
