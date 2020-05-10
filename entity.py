from typing import Sequence
from enum import Enum

class Vector2:
    def __init__(self, x: int, y:int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    def to_dict(self) -> dict:
        return {'x': self._x, 'y': self._y}

    @staticmethod
    def from_dict(d: dict):
        return Vector2(d['x'], d['y'])
    

class Rect:
    def __init__(self, position: Vector2, size: Vector2):
        self._position = position
        self._size = size

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, position: Vector2):
        self._position = position

    @property
    def size(self) -> Vector2:
        return self._size

    def has_point(self, point) -> bool:
        in_x = point[0] >= self.position.x and point[0] <= (self.position.x + self.size.x - 1)
        in_y = point[1] >= self.position.y and point[1] <= (self.position.y + self.size.y - 1)
        return in_x and in_y

    def to_dict(self) -> dict:
        return {'position': self._position.to_dict(), 'size': self._size.to_dict()}

    @staticmethod
    def from_dict(d: dict):
        return Rect(Vector2.from_dict(d['position']), Vector2.from_dict(d['size']))

class Entity:
    def __init__(self, name: str, rect: Rect):
        self._rect = rect
        self._name = name

    @staticmethod
    def fromDimmensions(name: str, pos_x: int, pos_y: int, size_x: int, size_y: int):
        return Entity(name, Rect(Vector2(pos_x, pos_y),  Vector2(size_x, size_y)))

    @property
    def position(self) -> Vector2:
        return Vector2(self._rect.position.x, self._rect.position.y)

    @property
    def size(self) -> Vector2:
        return self._rect.size

    @property
    def name(self) -> str:
        return self._name

    def set_position(self, pos_x, pos_y):
        self._rect.position = Vector2(pos_x, pos_y)

    def has_point(self, point):
        return self._rect.has_point(point)

    def to_dict(self):
        return {'name': self._name, 'rect': self._rect.to_dict()}

    @staticmethod
    def from_dict(d: dict):
        return Entity(d['name'], Rect.from_dict(d['rect']))
