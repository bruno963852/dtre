from typing import Dict

from src.scenario import Scenario


class Scenarios:

    _instance = None

    def __init__(self):
        self._scenarios = {}  # type: Dict[str, Scenario]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def get_scenario(cls, guild_id: str, channel_id: str) -> Scenario:
        key = f'{guild_id}/{channel_id}'
        if key not in cls.instance()._scenarios:
            raise KeyError("There's no scenario on this Guild")
        return cls.instance()._scenarios[key]

    @classmethod
    def put_scenario(cls, guild_id: str, channel_id: str, scenario: Scenario):
        key = f'{guild_id}/{channel_id}'
        cls.instance()._scenarios[key] = scenario
