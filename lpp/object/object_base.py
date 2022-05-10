from abc import (
    ABC,
    abstractmethod
)
from enum import (
    auto,
    Enum
)


class ObjectType(Enum):
  BOOLEAN = auto()
  INTEGER = auto()
  FLOAT = auto()
  STRING = auto()
  NULL = auto()


class Object(ABC):

  @abstractmethod
  def type(self) -> ObjectType:
    pass

  @abstractmethod
  def inspect(self) -> str:
    pass