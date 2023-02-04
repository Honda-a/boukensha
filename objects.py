from random import uniform

import constants as const
from baseclasses import gameobject, movingobject


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
        self.vulnerable = False


class Player(movingobject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height
        self.last_pos = (0, 0)
        self.x = 0
        self.y = 0
        self.damage = round(uniform(10, 45), 1)
        self.MAX_HP = 100
        self.health = self.MAX_HP
        self.type: str = const.types.PLAYER
        self.charactar: str = "X"
        self.name: str = "YOU"
        self.killed: dict = {
            f"{const.types.MOB}": 0,
            f"{const.types.BOSS}": 0,
            f"{const.types.SPRIT}": 0,
            f"{const.types.OBJECT}": 0,
        }

    def update(self, enemy: gameobject):
        """
        docstring
        """
        self.killed[enemy.type] += 1
        if self.killed[const.types.MOB] % 5 == 0:
            self.MAX_HP = self.MAX_HP * 2.25
            self.health = self.health * 2.25
            self.damage = self.damage * 2.5


class Mob(movingobject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_width
        self.view_height = view_height
        self.last_pos = (0, 0)
        self.x = 0
        self.y = 0
        self.damage = round(uniform(1, 15), 1)
        self.MAX_HP = round(uniform(1, 45), 1)
        self.health = self.MAX_HP
        self.type: str = const.types.MOB
        self.name: str = "enemy"
        self.charactar = "π"
        self.killed: dict = {
            f"{const.types.MOB}": 0,
            f"{const.types.BOSS}": 0,
            f"{const.types.SPRIT}": 0,
            f"{const.types.OBJECT}": 0,
        }

    def update(self, enemy: gameobject):
        """
        docstring
        """
        self.killed[enemy.type] += 1
        if self.killed[const.types.MOB] % 5 == 0:
            self.MAX_HP = self.MAX_HP * 1.25
            self.health = self.health * 1.25
            self.damage = self.damage * 1.5


"""
   _IIII_      
  |  - - |   / 
 | -      |-/  
|___|___|__|   
"""
