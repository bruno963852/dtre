from typing import List

from src.char.attack import Attack
from src.char.defense import Defense
from src.char.skill import Skill
from src.image.player_token import Token

ATTR_NAME = 'name'
ATTR_TOKEN = 'token'


class Character:

    def __init__(self, name: str, token: Token, defenses: List[Defense] = None, attacks: List[Attack] = None,
                 skills: List[Skill] = None, resistances: List[Skill] = None):
        self.name = name
        self.token = token
        self._defenses = defenses if defenses is not None else []
        self._attacks = attacks if attacks is not None else []
        self._skills = skills if skills is not None else []
        self._resistances = resistances if resistances is not None else []

    @property
    def dict(self) -> dict:
        return {
            ATTR_NAME: self.name,
            ATTR_TOKEN: self.token.dict
        }

    @staticmethod
    def from_dict(dict_: dict, server_id: str, square_size: int):
        return Character(
            name=dict_[ATTR_NAME],
            token=Token.from_dict(
                dict_=dict_[ATTR_TOKEN],
                name=dict_[ATTR_NAME],
                server_id=server_id,
                square_size=square_size
            )
        )
