from lpp.object.object_base import Object, ObjectType


class Boolean(Object):
  def __init__(self, value: bool) -> None:
    self.value = value

  def type(self) -> ObjectType:
    return ObjectType.BOOLEAN

  def inspect(self) -> str:
    return 'true' if self._value else 'false'
