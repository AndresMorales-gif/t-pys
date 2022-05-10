from lpp.object.object_base import Object, ObjectType


class Integer(Object):
  def __init__(self, value: int) -> None:
    self.value = value

  def type(self) -> ObjectType:
    return ObjectType.INTEGER

  def inspect(self) -> str:
    return str(self.value)


class Float(Object):
  def __init__(self, value: float) -> None:
    self.value = value

  def type(self) -> ObjectType:
    return ObjectType.INTEGER

  def inspect(self) -> str:
    return str(self.value)
