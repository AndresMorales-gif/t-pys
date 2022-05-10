from lpp.object.object_base import Object, ObjectType


class Return(Object):
  def __init__(self, value: Object) -> None:
    self.value = value

  def type(self) -> ObjectType:
    return ObjectType.RETURN

  def inspect(self) -> str:
    return self.value.inspect()