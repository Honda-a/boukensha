from typing import overload
import constants as const


class gameobject:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.dead: bool = False
        self._health: float = 0.0
        self._damage: float = 0.0
        self.type: str = "object"
        self.name: str = self.type
        self.charactar: str = ""

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

    def take_damage(self, damage: int) -> None:
        print(f"{self.charactar} took {damage} damage")
        self._health -= damage
        if self._health <= 0:
            self.dead = True

    def attack(self, enemy) -> None:
        print(f"{self.charactar} attacks with {self._damage} damage")
        enemy.take_damage(self._damage)

    def apply_magic(self, enemy) -> None:
        enemy.take_damage(self._damage)

    def stats(self):
        stats = f"""{self.name} stats:
health: {self.health}
damage: {self.damage}
type:   {self.type}
"""
        print(stats)
    
    def __str__(self) -> str:
        return self.charactar


class movingobject(gameobject):
    def __init__(self) -> None:
        super().__init__()
        self.type = "moving"

    def move(self):
        direction = input("move to: ")
        self.last_pos = (self.x, self.y)
        if direction.lower() in ["left", 'a'] and self.x > 0:
            self.x -= 1
        elif direction.lower() in ["right", 'd'] and self.x < self.view_width:
            self.x += 1
        elif direction.lower() in ["up", 'w'] and self.y < self.view_height:
            self.y += 1
        elif direction.lower() in ["down", 's'] and self.y > 0:
            self.y -= 1
        else:
            print("""wrong input please use ['left key', 'right key', 'up key', 'down key'] OR
            ['a key', 'd key', 'w key', 's key'] """)
            self.move()

    def move_to(self, coordX: int, coordY):
        self.last_pos = (self.x, self.y)
        self.x = coordX
        self.y = coordY
