from abc import ABC, abstractmethod


class HasheadorPassword(ABC):
    @abstractmethod
    def hashear(self, password: str) -> str:
        ...

    @abstractmethod
    def verificar(self, password: str, password_hash: str) -> bool:
        ...