class gameobject:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.dead: bool = False
        self._health: float
        self._damage: float
        self.charactar: str


    def take_damage(self, damage: int) -> None:
        self._health -= damage
        if self._health <= 0:
            self.dead = True

    def attack(self, enemy) -> None:
        enemy.take_damage(self._damage)

    def apply_magic(self, enemy) -> None:
        enemy.take_damage(self._damage)



class movingobject(gameobject):

    def move(self, direction):
        self.last_pos = (self.x, self.y)
        if direction.lower() in ["left", 'a'] and self.x > 0:
            self.x -= 1
        elif direction.lower() in ["right", 'd'] and self.x < self.view_width:
            self.x += 1
        elif direction.lower() in ["up", 'w'] and self.y < self.view_height:
            self.y += 1
        elif direction.lower() in ["down", 's'] and self.y > 0:
            self.y -= 1
