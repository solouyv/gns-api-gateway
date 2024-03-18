from abc import ABC, abstractmethod

from .client_utils import CommonDictType

__all__ = ["IBaseAuthProvider"]


class IBaseAuthProvider(ABC):
    @abstractmethod
    def make_headers(self) -> CommonDictType:
        pass
