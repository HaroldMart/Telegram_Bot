from abc import ABC, abstractmethod
# from typing import Dict

class IConnection(ABC):
    @abstractmethod
    def set_url(self, url: str) -> None:
        pass

    @abstractmethod
    def get_headers(self) -> dict:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def get_connection(self, url) -> str:
        pass