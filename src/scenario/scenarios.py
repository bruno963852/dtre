from typing import Dict

from src.scenario import Scenario


class Scenarios:

    _instance = None

    def __init__(self):
        self._scenarios = Dict[str, Scenario]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_scenario(cls, guild_id: str) -> Scenario:
        if guild_id not in cls.instance()._scenarios:
            raise KeyError("There's no scenario on this Guild")
        return cls.instance()._scenarios[guild_id]

    @classmethod
    def put_scenario(cls, guild_id: str, scenario: Scenario):
        cls.instance()._scenarios[guild_id] = scenario
