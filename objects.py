from baseclasses import gameobject, movingobject
from random import uniform
import constants as const

class Wall(gameobject):
    def __init__(self, view_width: int, view_height: int, x: int, y: int) -> None:
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height
        self.last_pos = (0, 0)
        self.x = x
        self.y = y
        self.health = 10
        self.type: str = const.types.OBJECT
        self.charactar: str = "#"
        self.name: str = "Wall"


class Player(movingobject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height
        self.last_pos = (0, 0)
        self.x = 0
        self.y = 0
        self.damage = round(uniform(10, 45), 1)
        self.health = 100
        self.type: str = const.types.PLAYER
        self.charactar: str = "X"
        self.name: str = "YOU"

class Mob(movingobject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height 
        self.last_pos = (0, 0)
        self.x = 0
        self.y = 0
        self.damage = round(uniform(1, 15), 1)
        self.health = round(uniform(1, 45), 1)
        self.type: str = const.types.MOB
        self.name: str = "enemy"
        self.charactar = "π"
