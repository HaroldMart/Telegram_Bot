from abc import ABC, abstractmethod
from typing import List
from app.features.entertainment.core.models import Entertainment

class IEntertainmentRepository(ABC):
    @abstractmethod
    def getAllMedia() -> List[Entertainment]:
        pass

    @abstractmethod
    def getMedia() -> Entertainment:
        pass

    @abstractmethod
    def createMedia() -> Entertainment:
        pass

    @abstractmethod
    def updateMedia() -> Entertainment:
        pass

    @abstractmethod
    def deleteMedia() -> Entertainment:
        pass