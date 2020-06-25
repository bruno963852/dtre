
class Characteristic:
    def __init__(self, name: str, mod: int, die='1d20', value=0):
        self.name = name
        self.die = die
        self.mod = mod
        self._value = value

    def set_value(self, value: int):
        self._value = value

    def roll(self):
        pass

