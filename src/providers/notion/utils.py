import requests as rq;

class Connection:
    def __init__(self, key):
        _url = "";
        self._baseUrl = "https://api.notion.com/v1/";
        self._key = key;
        self._headers = {
            "Authorization": "Bearer " + self._key,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        };

    def set_url(self, url):
        self._url = self._baseUrl + url;

    def get_headers(self):
        return self._headers;

    def set_headers(self, headers):
        self._headers = headers;

    def get_key(self):
        return self._key;

    def get_connection(self, url):
        self.set_url(url);
        return self._url;




def create_csv():
    pass;
def read_csv():
    pass;