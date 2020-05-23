from typing import Dict, Tuple

from src.char import Character
from src.image.exceptions import CharacterNotFoundException, InvalidMovementException
from src.image.player_token import Token
from src.image.playmat import Playmat

_UP = 'c'
_DOWN = 'b'
_LEFT = 'e'
_RIGHT = 'd'


class Scenario:
    def __init__(self, server_id: str, name: str, map_url: str, square_size: int, offset_pixels: Tuple[int, int]):
        self._server_id = server_id
        self._name = name
        self.characters = {}
        self.map = Playmat(server_id, map_url, offset_pixels, square_size)

    def remove_character(self, name: str):
        if name not in self.characters:
            raise CharacterNotFoundException
        del self.characters[name]

    def add_character(self, name: str, url: str, position: Tuple[int, int] = (0, 0)):
        token = Token(name, position, url, self.map.square_size, self._server_id)
        self.characters[name] = Character(name, token)

    def move_character(self, name: str, movement: str):
        if name not in self.characters:
            raise CharacterNotFoundException
        char = self.characters[name]
        previous_position = char.token.position
        try:
            for move in movement:
                self._move_character(char.token, move)
        except InvalidMovementException:
            char.token.position = previous_position
            raise InvalidMovementException

    def _move_character(self, token: Token, direction: str):
        if direction == _UP:
            if token.position[1] <= 0:
                raise InvalidMovementException
            token.increment_position(y=-1)
            return
        if direction == _DOWN:
            if token.position[1] >= self.map.size[1] - 1:
                raise InvalidMovementException
            token.increment_position(y=1)
            return
        if direction == _LEFT:
            if token.position[0] <= 0:
                raise InvalidMovementException
            token.increment_position(x=-1)
            return
        if direction == _RIGHT:
            if token.position[0] >= self.map.size[0] - 1:
                raise InvalidMovementException
            token.increment_position(x=1)
            return
        raise InvalidMovementException

    def get_image(self):
        return self.map.get_map_with_tokens(self.characters)

    # def set_frame(self, name: str, url: str):
    #     if name not in self._tokens:
    #         raise CharacterNotFoundException
    #     self._tokens[name].set_frame(url)
