from random import randint, choice
from objects import Player, Mob
from gamemap import GameView
import constants as const


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
        return {
            "player": self.player
        }
        

    def update_player_pos(self):
        if self.view.game_map[self.player.y][self.player.x] == 0:
            self.view.game_map[self.player.last_pos[1]][self.player.last_pos[0]] = 0
            self.view.game_map[self.player.y][self.player.x] = self.player
        else:
            enemy = self.view.game_map[self.player.y][self.player.x]
            self.player.x = self.player.last_pos[0]
            self.player.y = self.player.last_pos[1]
            self.battle(player=self.player, enemy=enemy)

    def set_player_pos(self):
        while True:
            if self.view.game_map[self.player.y][self.player.x] == 0:
                self.view.game_map[self.player.y][self.player.x] = self.player
                break
            self.player.y = randint(0, self.view_height)
            self.player.x = randint(0, self.view_width)

    # def update_enemy(self):
    #     for y in self.view.game_map:
    #         row = []
    #         for x in y:
    #             if x == 0:
    #                 row.append(" ")
    #             elif isinstance(x, Mob):
    #                 row.append(x.charactar)
    #             else:
    #                 row.append(x)

    def run(self):
        while True:
            self.player.move()
            self.update_player_pos()
            # self.update_enemy()
            self.view.render()

    def game_over(self):
        print("GAME OVER TRY NEXT TIME")
        quit()

    def battle(self, player, enemy, auto=False) -> bool:
        while not (player.dead == True or enemy.dead == True):
            if auto:
                player.attack(enemy)
                enemy.attack(player)
            else:
                enemy.stats()
                player_input = input("enemy ahead what to do?(attack / run / use magic(not usable))")
                if player_input in ["attack" ,"a"]:
                    player.attack(enemy)
                    self.view.message += f"\n player health: {player.health}, enemy dead: {enemy.dead}\n"
                    enemy.attack(player)
                    self.view.message += f"\n player health: {player.health}, enemy health: {enemy.health}\n"
                elif player_input == "run":
                    print(player.health, enemy.health)
                    break
                else:
                    print(player_input)
                    continue
        if player.dead:
            self.game_over()
        if enemy.dead:
            self.view.game_map[enemy.y][enemy.x] = 0


main = Game()
main.run()


# TODO:
#   Create map rendering
#   Create object classes
