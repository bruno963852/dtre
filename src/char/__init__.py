from typing import List

from src.char.attack import Attack
from src.char.defense import Defense
from src.char.skill import Skill
from src.image.player_token import Token


class Character:

    def __init__(self, name: str, token: Token, defenses: List[Defense] = None, attacks: List[Attack] = None,
                 skills: List[Skill] = None, resistances: List[Skill] = None):
        self.name = name
        self.token = token
        self._defenses = defenses if defenses is not None else []
        self._attacks = attacks if attacks is not None else []
        self._skills = skills if skills is not None else []
        self._resistances = resistances if resistances is not None else []

