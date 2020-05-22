from io import BytesIO
from typing import Tuple, Dict

from play_mat.exceptions import TokenNotFoundException, InvalidMovementException
from play_mat.play_token import Token
from play_mat.play_map_image_processor import PlayMatImageProcessor

_UP = 'c'
_DOWN = 'b'
_LEFT = 'e'
_RIGHT = 'd'


class PlayMat(PlayMatImageProcessor):
    def __init__(self, server_id: str, url: str, offset: Tuple[int, int], square_size: int):
        super().__init__(server_id, url, offset, square_size)

    def _get_token(self, name: str) -> Token:
        if name in self._tokens:
            return self._tokens[name]
        raise TokenNotFoundException

    def remove_token(self, name: str):
        if name not in self._tokens:
            raise TokenNotFoundException
        del self._tokens[name]

    def add_token(self, name: str, url: str, position: Tuple[int, int] = (0, 0)):
        self._tokens[name] = Token(name, position, url)

    def move_token(self, name: str, movement:str):
        token = self._get_token(name)
        previous_position = token.position
        try:
            for move in movement:
                self._move_token(token, move)
        except InvalidMovementException:
            token.position = previous_position
            raise InvalidMovementException

    def _move_token(self, token: Token, direction: str):
        if direction == _UP:
            if token.position[1] <= 0:
                raise InvalidMovementException
            token.increment_position(y=-1)
            return
        if direction == _DOWN:
            if token.position[1] >= self._map_size[1] - 1:
                raise InvalidMovementException
            token.increment_position(y=1)
            return
        if direction == _LEFT:
            if token.position[0] <= 0:
                raise InvalidMovementException
            token.increment_position(x=-1)
            return
        if direction == _RIGHT:
            if token.position[0] >= self._map_size[0] - 1:
                raise InvalidMovementException
            token.increment_position(x=1)
            return
        raise InvalidMovementException

    def get_map(self) -> BytesIO:
        return self._process()

    def set_frame(self, name: str, url: str):
        if name not in self._tokens:
            raise TokenNotFoundException
        self._tokens[name].set_frame(url)
