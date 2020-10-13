from typing import overload
import constants as const


class gameobject:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.dead: bool = False
        self._health: float = 0.0
        self._damage: float = 0.0
        self._vulnerable: bool = True
        self.type: str = "object"
        self.name: str = self.type
        self.charactar: str = ""
        self.last_direction: str = ""

    @property
    def health(self) -> float:
        return round(self._health, 1)

    @health.setter
    def health(self, health: float) -> None:
        self._health = health

    @property
    def damage(self) -> float:
        return self._damage

    @damage.setter
    def damage(self, damage: float) -> None:
        self._damage = damage

    @property
    def vulnerable(self) -> bool:
        return self._vulnerable

    @vulnerable.setter
    def vulnerable(self, vulnerable: bool) -> None:
        self._vulnerable = vulnerable

    def take_damage(self, damage: int, auto: bool=False) -> None:
        if not auto:
            print(f"{self.charactar} took {damage} damage")
        self._health -= damage
        if self._health <= 0:
            self.dead = True

    def attack(self, enemy, auto: bool=False) -> None:
        if not auto:
            print(f"{self.charactar} attacks with {self._damage} damage")
        if enemy.vulnerable:
            enemy.take_damage(self._damage, auto)
            return True
        else: 
            return False

    def apply_magic(self, enemy) -> None:
        enemy.take_damage(self._damage)

    def stats(self):
        stats = f"""{self.name} stats:
health: {self.health}
damage: {self.damage}
type:   {self.type}
"""
        print(stats)

    def to_dict(self):
        return self.__dict__

    def __str__(self) -> str:
        return self.charactar


class movingobject(gameobject):
    def __init__(self) -> None:
        super().__init__()
        self.type = "moving"

    def move(self, direction: str=""):
        if not direction:
            direction = input("move to: ")
            if not direction:
                direction = self.last_direction
        self.last_direction = direction
        self.last_pos = (self.x, self.y)
        if direction.lower() in ["left", 'a']:
            self.x, _ = self.check_coord(coordX=self.x-1)
        elif direction.lower() in ["right", 'd']:
            self.x, _ = self.check_coord(coordX=self.x+1)
        elif direction.lower() in ["up", 'w']:
            _, self.y = self.check_coord(coordY=self.y+1)
        elif direction.lower() in ["down", 's']:
            _, self.y = self.check_coord(coordY=self.y-1)
        else:
            print("""wrong input please use ['left key', 'right key', 'up key', 'down key'] OR
            ['a key', 'd key', 'w key', 's key'] """)
            self.move()

    def move_to(self, coordX: int, coordY):
        self.last_pos = (self.x, self.y)
        self.x, self.y = self.check_coord(coordX, coordY)

    def check_coord(self, coordX: int=0, coordY: int=0):
        if coordX < 0:
            coordX = 0
        if coordX > self.view_width:
            coordX = self.view_width
        if coordY < 0:
            coordY = 0
        if coordY > self.view_height:
            coordY = self.view_height
        if coordX > self.view_width or coordY > self.view_height:
            coordX
        return coordX, coordY

    @classmethod
    def from_dict(cls, args: dict):
        for attr, val in args.items():
            setattr(cls, attr, val)
