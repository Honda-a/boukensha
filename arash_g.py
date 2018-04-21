from random import randint
import os
from time import sleep
import numpy
from baseclasses import gameobject, movingobject


class Wall(GameObject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_height - 1
        self.view_height = view_height - 1
        self.last_pos = (0, 0)
        self._damage = randint(0,1)
        self._health = 10
        self.charactar: str = "#"

class Player(movingobject):
    def __init__(self, view_width: int, view_height: int) -> None:
        super().__init__()
        self.view_width = view_height - 1
        self.view_height = view_height - 1
        self.last_pos = (0, 0)
        self.damage = randint(10, 45)
        self.health = 100
        self.charactar: str = "X"

class GameView:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.message = ""

    def render(self, map_frame, wall):
        canvas = []
        for y in map_frame:
            row = []
            for x in y:
                if x == 0:
                    row.append(" ")
                elif x == 1:
                    row.append(wall.charactar)
                else:
                    row.append(x)
            canvas.append("".join(row))
        canvas.reverse()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(canvas))
        print(self.message)


class Game:

    def __init__(self):
        self.view_width = 16
        self.view_height = 16
        self.game_map = np.random.rand(0,1,(self.view_height,self.view_width))#[[randint(0,randint(0,randint(0,1))) for _ in range(self.view_width)] for _ in range(self.view_height)]
        self.view = GameView(self.view_width, self.view_height)
        self.player = Player(self.view_width, self.view_height)
        self.wall = Wall(self.view_width, self.view_height)
        self.update_player_pos()
        self.view.render(self.game_map, self.wall)

    def update_player_pos(self):
        if self.game_map[self.player.y][self.player.x] == 0:
            self.game_map[self.player.last_pos[1]][self.player.last_pos[0]] = 0
            self.game_map[self.player.y][self.player.x] = self.player.charactar
        else:
            self.player.x = self.player.last_pos[0]
            self.player.y = self.player.last_pos[1]
            self.view.message = f"wall ahead turn some other direction {self.game_map[self.player.y][self.player.x]}"
            self.battle(player=self.player, enemy=self.wall)

    def run(self):
        while True:
            direction = input("move to: ")
            self.player.move(direction)
            self.update_player_pos()
            self.view.render(self.game_map, self.wall)

    def battle(self, player, enemy, auto=False) -> bool:
        while not (player.dead == True or enemy.dead == True):
            if auto:
                player.attack(enemy)
                enemy.attack(player)
            else:
                player_input = input("what to do?(attack / run / use magic(not usable))")
                if player_input == "attack":
                    player.attack(enemy)
                    print(player.health, enemy.dead)
                    enemy.attack(player)
                    print(player.health, enemy.health)
                elif player_input == "run":
                    print(player.health, enemy.health)
                    return False
                else:
                    print(player_input)
                    continue

main = Game()
main.run()
