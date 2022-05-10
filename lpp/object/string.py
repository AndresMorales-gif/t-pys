from lpp.object.object_base import Object, ObjectType


class String(Object):
  def __init__(self, value: str) -> None:
    self.value = value

  def type(self) -> ObjectType:
    return ObjectType.STRING

  def inspect(self) -> str:
    return self.value
