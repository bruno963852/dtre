from typing import Tuple

from src.char import Character
from src.image.exceptions import CharacterNotFoundInScenarioException, InvalidMovementException
from src.image.player_token import Token
from src.image.playmat import Playmat

_UP = 'u'
_DOWN = 'd'
_LEFT = 'l'
_RIGHT = 'r'

_ATTR_NAME = 'name'
_ATTR_MAP = 'map'
_ATTR_CHARACTERS = 'characters'


class Scenario:
    def __init__(self, server_id: str, channel_id: str, name: str, map_url: str = '', square_size: int = 0,
                 offset_pixels: Tuple[int, int] = (0, 0)):
        self._server_id = server_id
        self._channel_id = channel_id
        self._name = name
        self.characters = {}
        self._last_movement = []
        if map_url == '':
            self.map = Playmat(server_id, channel_id)
        else:
            self.map = Playmat(server_id=server_id, channel_id=channel_id, image_url=map_url,
                               offset_pixels=offset_pixels, square_size=square_size)

    @property
    def name(self):
        return self._name

    @property
    def dict(self) -> dict:
        chars = []
        for char in self.characters.values():  # type: Character
            chars.append(char.dict)
        return {
            _ATTR_NAME: self._name,
            _ATTR_MAP: self.map.dict,
            _ATTR_CHARACTERS: chars
        }

    @staticmethod
    def from_dict(dict_: dict, server_id: str, channel_id: str):
        map_ = Playmat.from_dict(
            dict_[_ATTR_MAP],
            server_id,
            channel_id
        )
        scenario = Scenario(
            server_id=server_id,
            channel_id=channel_id,
            name=dict_[_ATTR_NAME],
            map_url=map_.image_url,
            square_size=map_.square_size,
            offset_pixels=map_.offset,
        )
        chars = dict_[_ATTR_CHARACTERS]
        for char_dict in chars:
            char = Character.from_dict(char_dict, server_id, channel_id, map_.square_size)
            scenario.add_character(char)
        return scenario

    def remove_character(self, name: str):
        if name not in self.characters:
            raise CharacterNotFoundInScenarioException
        del self.characters[name]

    def add_character(self, character: Character):
        self.characters[character.name] = character

    def move_character(self, name: str, movement: str):
        moves = movement.split()
        if name not in self.characters:
            raise CharacterNotFoundInScenarioException
        char = self.characters[name]
        self._last_movement = [char.token.position]
        previous_position = char.token.position
        try:
            for move in moves:
                self._move_character(char.token, move)
        except InvalidMovementException:
            char.token.position = previous_position
            raise InvalidMovementException

    def _move_character(self, token: Token, direction: str):
        if len(direction) > 2:
            raise InvalidMovementException
        for subdir in direction:
            if subdir == _UP:
                if token.position[1] <= 0:
                    raise InvalidMovementException
                token.increment_position(y=-1)
            elif subdir == _DOWN:
                if token.position[1] >= self.map.size[1] - 1:
                    raise InvalidMovementException
                token.increment_position(y=1)
            elif subdir == _LEFT:
                if token.position[0] <= 0:
                    raise InvalidMovementException
                token.increment_position(x=-1)
            elif subdir == _RIGHT:
                if token.position[0] >= self.map.size[0] - 1:
                    raise InvalidMovementException
                token.increment_position(x=1)
            else:
                raise InvalidMovementException
        self._last_movement.append(token.position)

    def get_image(self, show_movement=False):
        movement = None
        if show_movement:
            movement = self._last_movement
        return self.map.get_full_map(self.characters, movement)

    # def set_frame(self, name: str, url: str):
    #     if name not in self._tokens:
    #         raise CharacterNotFoundException
    #     self._tokens[name].set_frame(url)
