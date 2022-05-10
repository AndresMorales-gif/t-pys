from lpp.object.object_base import Object, ObjectType


class Null(Object):

  def type(self) -> ObjectType:
    return ObjectType.NULL

  def inspect(self) -> str:
    return 'null'
