import string
from typing import List
from custom_exceptions import InvalidMovementException, InexistentEntityException
from entity import Entity

_WALL = '#'
_FLOOR = '·'
_START = '```ml\n'
_END = '```'
_LEGEND_COLLUMN_SIZE = 20
_STR_ALLIES = "'Allies'"
_STR_ENEMIES = "'Enemies'"

_MOV_LEFT = ('l', 'e')
_MOV_RIGHT = ('r', 'd')
_MOV_UP = ('u', 'c')
_MOV_DOWN = ('d', 'b')


class Grid:
    def __init__(self, height, width, allies: List[Entity] = [], enemies: List[Entity] = []):
        self._height = height
        self._width = width
        self._allies = allies
        self._enemies = enemies

    @property
    def enemies(self):
        return self._enemies

    @property
    def allies(self):
        return self._allies

    def to_json(self):
        pass

    def _draw_entity(self, index_x, index_y):
        if index_y < 0 or index_y >= self._height:
            return ''
        if index_x < 0 or index_x >= self._width:
            return ''
        for enemy_index, enemy in enumerate(self._enemies):
            if enemy.has_point((index_x, index_y)):
                return string.ascii_uppercase[enemy_index]
        for ally_index, ally in enumerate(self._allies):
            if ally.has_point((index_x, index_y)):
                return str(ally_index)
        return _FLOOR

    def _draw_upper_wall(self, index_y):
        if index_y >= 0:
            return ''
        wall = '  '
        for i in range(self._width):
            wall += string.ascii_lowercase[i]
        wall += "  | " + _STR_ALLIES + \
            ((_LEGEND_COLLUMN_SIZE - len(_STR_ALLIES)) * ' ') + ' | '
        wall += _STR_ENEMIES + \
            ((_LEGEND_COLLUMN_SIZE - len(_STR_ENEMIES)) * ' ') + ' |'
        wall += '\n '
        wall += ('#' * (self._width + 2)) + ' |'
        wall += (' ' * (_LEGEND_COLLUMN_SIZE + 2)) + '|  '
        wall += (' ' * (_LEGEND_COLLUMN_SIZE)) + '|'
        wall += '\n'
        return wall

    def _draw_lower_wall(self, index_y):
        if index_y >= self._height:
            wall = ' ' + (_WALL * (self._width + 2)) + ' |'
            wall += (' ' * (_LEGEND_COLLUMN_SIZE + 2)) + '|  '
            wall += (' ' * (_LEGEND_COLLUMN_SIZE)) + '|'
            wall += '\n'
            return wall
        return ''

    def _draw_left_wall(self, index_x, index_y):
        wall = ''
        if index_y < 0 or index_y >= self._height:
            return wall
        if index_x < 0:
            wall += string.ascii_lowercase[index_y] if index_y >= 0 else ' '
            wall += _WALL
        return wall

    def _draw_right_wall(self, index_x, index_y):
        wall = ''
        if index_y < 0 or index_y >= self._height:
            return wall
        if index_x >= self._width:
            wall += _WALL
            wall += ' |'
            if len(self._allies) > index_y:
                wall += ' ' + str(index_y) + ' - '
                wall += self._allies[index_y].name
                wall += ' ' * (_LEGEND_COLLUMN_SIZE -
                               len(self._allies[index_y].name) - 4) + ' | '
            else:
                wall += ' ' * (_LEGEND_COLLUMN_SIZE + 2)
                wall += '| '
            if len(self._enemies) > index_y:
                wall += ' ' + string.ascii_uppercase[index_y] + ' - '
                wall += self._enemies[index_y].name
                wall += ' ' * (_LEGEND_COLLUMN_SIZE -
                               len(self._enemies[index_y].name) - 4) + '|'
            else:
                wall += ' ' * (_LEGEND_COLLUMN_SIZE + 1)
                wall += '|'
            wall += '\n'
        return wall

    def to_string(self):
        map_string = _START
        for index_y in range(-1, self._height + 1):
            map_string += self._draw_upper_wall(index_y)

            for index_x in range(-1, self._width + 1):
                map_string += self._draw_left_wall(index_x, index_y)
                map_string += self._draw_entity(index_x, index_y)
                map_string += self._draw_right_wall(index_x, index_y)

            map_string += self._draw_lower_wall(index_y)
            # print(map_string)
            # pass
        map_string += _END
        return map_string

    def _get_entity_from_name(self, name) -> Entity:
        for ally in self._allies:
            if ally.name == name:
                return ally
        for enemy in self._enemies:
            if enemy.name == name:
                return enemy
        raise ValueError("entity doesn't exist")

    def can_move_to(self, name, pos_x, pos_y):
        ent = self._get_entity_from_name(name)
        if pos_x < 0 or pos_x + ent.size.x >= self._width or pos_y < 0 or pos_y + ent.size.y >= self._height:
            return False
        allentities = list(self._enemies)
        allentities.extend(self._allies)
        for other_ent in allentities:
            if pos_x + ent.size.x - 1 >= other_ent.position.x and \
                    pos_x <= other_ent.position.x + other_ent.size.x - 1 and \
                    pos_y + ent.size.y - 1 >= other_ent.position.y and \
                    pos_y <= other_ent.position.y + other_ent.size.y - 1:
                return False
        return True

    def _get_new_position_from_movement(self, name: str, movement: str):
        position = self._get_entity_from_name(name).position
        for mov in movement:
            if mov in _MOV_DOWN:
                position.y += 1
            elif mov in _MOV_UP:
                position.y -= 1
            elif mov in _MOV_LEFT:
                position.x -= 1
            elif mov in _MOV_RIGHT:
                position.x += 1
            else:
                raise InvalidMovementException
        return position

    def move_by(self, name: str, movement: str):
        position = self._get_new_position_from_movement(name, movement)
        if not self.can_move_to(name, position.x, position.y):
            raise InvalidMovementException
        self.move_to(name, position.x, position.y)

    def move_to(self, name, pos_x, pos_y):
        if not self.can_move_to(name, pos_x, pos_y):
            raise ValueError("Invalid Movement")
        entity = self._get_entity_from_name(name)
        entity.set_position(pos_x, pos_y)

    def add_enemy(self, name: str, pos_x: int, pos_y: int, size_x: int = 1, size_y: int = 1):
        self._enemies.append(Entity.fromDimmensions(
            name, pos_x, pos_y, size_x, size_y))

    def add_ally(self, name: str, pos_x: int, pos_y: int, size_x: int = 1, size_y: int = 1):
        self._allies.append(Entity.fromDimmensions(
            name, pos_x, pos_y, size_x, size_y))

    def remove_enemy(self, name):
        if not self.has_enemy(name):
            raise InexistentEntityException
        for index, enemy in enumerate(self._enemies):
            if enemy.name == name:
                del self._enemies[index]

    def remove_ally(self, name):
        if not self.has_ally(name):
            raise InexistentEntityException
        for index, ally in enumerate(self._allies):
            if ally.name == name:
                del self._allies[index]

    def has_enemy(self, name) -> bool:
        for enemy in self._enemies:
            if enemy.name == name:
                return True
        return False

    def has_ally(self, name) -> bool:
        for ally in self._allies:
            if ally.name == name:
                return True
        return False

    def has_entity(self, name) -> bool:
        return self.has_ally(name) or self.has_enemy(name)

    def to_dict(self) -> dict:
        allies = []
        for ally in self.allies:
            allies.append(ally.to_dict())
        enemies = []
        for enemy in self.enemies:
            enemies.append(enemy.to_dict())
        return {'height': self._height, 'width': self._width, 'allies': allies, 'enemies': enemies}

    @staticmethod
    def from_dict(d: dict):
        allies = []
        for ally in d['allies']:
            print(ally)
            allies.append(Entity.from_dict(ally))
        enemies = []
        for enemy in d['enemies']:
            enemies.append(Entity.from_dict(enemy))
        return Grid(d['height'], d['width'], allies, enemies)


if __name__ == "__main__":
    g = Grid(20, 20)
    g.add_ally('zezim', 5, 5)
    g.add_enemy('chikin', 7, 3, 2)
    print(g.to_string())
    # print(g.can_move_to('zezim', 8, 3))
    # print(g.can_move_to('chikin', 4, 5))
    # print(g.can_move_to('chikin', 10, 10))
    # print(g.move_to('chikin', 2, 2))
    # print(g.to_string())
    print(g.to_dict())
    d = g.to_dict()
    gg = Grid.from_dict(d)
    print(gg.to_string())
    print(g.move_by('zezim', 'l'))
