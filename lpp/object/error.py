from lpp.object.object_base import Object, ObjectType


class Error(Object):
  def __init__(self, message: str) -> None:
    self.message = message

  def type(self) -> ObjectType:
    return ObjectType.ERROR

  def inspect(self) -> str:
    return f'Error: {self.message}'
