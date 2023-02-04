from random import choice, randint

import constants as const
from gamemap import GameView
from objects import Mob, Player


class Game:
    def __init__(self):
        self.view_width = const.GAME_WIDTH
        self.view_height = const.GAME_HEIGHT
        self.gameobjects = self.create_gameobjects()
        self.view = GameView(self.gameobjects, self.view_width, self.view_height)
        self.set_player_pos()
        self.view.render()

    def create_gameobjects(self):
        """
        docstring
        """
        self.player = Player(self.view_width, self.view_height)
        return {"player": self.player, "mob": []}

    def update_object_pos(self, mover, auto=False):
        if mover.x > self.view_width or mover.y > self.view_height:
            mover
        if self.view.game_map[mover.y][mover.x] == 0:
            self.view.game_map[mover.last_pos[1]][mover.last_pos[0]] = 0
            self.view.game_map[mover.y][mover.x] = mover
        else:
            enemy = self.view.game_map[mover.y][mover.x]
            mover.x = mover.last_pos[0]
            mover.y = mover.last_pos[1]
            self.battle(attacker=mover, enemy=enemy, auto=auto)

    def set_player_pos(self):
        while True:
            if self.view.game_map[self.player.y][self.player.x] == 0:
                self.view.game_map[self.player.y][self.player.x] = self.player
                break
            self.player.y = randint(0, self.view_height)
            self.player.x = randint(0, self.view_width)

    def update_enemy(self):
        for mob in self.gameobjects["mob"]:
            direction = choice(["a", "w", "d", "s"])
            mob.move(direction)
            if not mob.dead:
                self.update_object_pos(mob, auto=True)

    def run(self):
        while True:
            self.player.move()
            self.update_object_pos(self.player)
            self.update_enemy()
            self.view.render()

    def game_over(self):
        print("GAME OVER TRY NEXT TIME")
        quit()

    def battle(self, attacker, enemy, auto=False) -> bool:
        if not enemy.vulnerable:
            if not auto:
                print("Invulnerable object change direction")
            return False
        while not (attacker.dead == True or enemy.dead == True):
            if auto:
                attacker.attack(enemy, auto)
                enemy.attack(attacker, auto)
            else:
                enemy.stats()
                player_input = input(
                    "enemy ahead what to do?(attack / run / use magic(not usable))"
                )
                if player_input in ["attack", "a"]:
                    attacker.attack(enemy)
                    self.view.message += f"\n attacker health: {attacker.health}, enemy dead: {enemy.dead}\n"
                    enemy.attack(attacker)
                    self.view.message += f"\n player health: {attacker.health}, enemy health: {enemy.health}\n"
                elif player_input == "run":
                    print(attacker.health, enemy.health)
                    break
                else:
                    print(player_input)
                    continue
        if attacker.dead:
            if attacker.type == const.types.PLAYER:
                self.game_over()
            else:
                self.view.game_map[attacker.y][attacker.x] = 0
                enemy.update(attacker)

        if enemy.dead:
            self.view.game_map[enemy.y][enemy.x] = 0
            attacker.update(enemy)


main = Game()
main.run()


# TODO:
#   Create map rendering
#   Create object classes
