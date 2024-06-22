from app.features.shared.interfaces import IConnection
import os, requests as rq
from dotenv import load_dotenv

load_dotenv()

# Config for notion api connection
KEY = os.environ["NOTION_SECRET"]
BASE_URL = "https://api.notion.com/v1/"
HEADERS = {
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Notion databases
ENTERTAINMENT_DB = os.environ["NOTION_DATABASE_ENTERTAINMENT"]

# Classes for connect and make request to notion api
class Connection(IConnection):
    def __init__(self, base_url : str, key : str, headers : str) -> None:
        self._url : str = ""
        self._base_url : str = base_url
        self._key : str = key
        self._headers : dict = headers

    def set_url(self, url) -> None:
        self._url = self._base_url + url

    def get_headers(self) -> dict:
        return self._headers

    def get_key(self) -> str:
        return self._key

    def get_connection(self, url) -> str:
        self.set_url(url)
        return self._url

class Notion:
    def __init__(self, connection : IConnection, database_id : str):
        self._database : str = database_id
        self._connection : IConnection = connection
        self._url : str
        self._data : dict = {
            "sorts": []
        }

    def filter_and_sort(self, filter = None, sort = None):
        if filter is not None:
            self._data["filter"] = filter
        if sort is not None and sort is list:
            for item in sort:
                self._data["sorts"].append(item)
        else:
            default_sort : dict = {"property": "Name", "direction": "ascending"}
            self._data["sorts"].append(default_sort)

    def build_connection(self, data : str = None):
        self._url = self._connection.get_connection("databases/" + self._database)
        if data is not None:
            self._url += data
        return self._url

    def request_data(self, data, url = None):
        try:
            if url is None:
                url = self._url
            response = rq.post(url = url, headers = self._connection.get_headers(), json = data);
            if response.status_code == 200:
                return response.json()
            else:
                print(response.text)
        except Exception as e:
            print(f"Error: {e}")