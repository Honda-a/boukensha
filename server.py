from baseclasses import gameobject
from random import randint, choice, random
from objects import Player, Mob, GameObjects
from gamemap import GameView
import constants as const
from pygase import GameState, Backend


class Game:

    def __init__(self):
        self.view_width = const.GAME_WIDTH
        self.view_height = const.GAME_HEIGHT
        self.create_gameobjects()
        self.view = GameView(self.gameobjects, self.view_width, self.view_height)
        self.backend = Backend(
            self.game_state,
            self.run
        )

    def create_gameobjects(self):
        """
        docstring
        """
        self.gameobjects = GameObjects()
        gameobject_dict = self.gameobjects.to_dict()
        self.game_state = GameState(
            player=gameobject_dict["player"],
            mob=gameobject_dict["mob"],
            map=[],
        )

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
        for player in self.gameobjects.player:
            while True:
                if self.view.game_map[player.y][player.x] == 0:
                    self.view.game_map[player.y][player.x] = player
                    break
                player.y = randint(0, self.view_height)
                player.x = randint(0, self.view_width)

    def update_enemy(self):
        for mob in self.gameobjects.mob:
            if mob.dead or random() > const.MOB_MOVEMENT:
                continue
            direction = choice(["a", "w", "d", "s"])
            mob.move(direction)
            self.update_object_pos(mob, auto=True)

    def update_player(self):
        for player_id, player in self.gameobjects.player.items():
            if player.dead:
                continue
            self.update_object_pos(player, auto=True)
            self.view.render(player_id=player_id)

    def run(self, game_state, dt):
        if not self.gameobjects.player:
            return {}
        self.update_enemy()
        self.update_player()
        return self.gameobjects.to_dict()

    def on_join(self, player_name, game_state, client_address, **kwargs):
        print(f"{player_name} joined.")
        player_id = len(game_state.player) + 1
        player = Player(self.view_width, self.view_width)
        player.player_id = player_id
        self.gameobjects.set_player(player_id, player)
        self.gameobjects.view_map = self.view.render(player_id)
        # Notify client that the player successfully joined the game.
        self.backend.server.dispatch_event(
            "PLAYER_CREATED", (player_id, self.gameobjects.to_dict()), target_client=client_address)
        return self.gameobjects.to_dict()

    def game_over(self):
        print("GAME OVER TRY NEXT TIME")
        quit()

    def on_move(self, player_id: str, direction: str, **kwargs):
        self.gameobjects.move_player(player_id=player_id, direction=direction)
        self.update_object_pos(self.gameobjects.player[player_id])
        return self.gameobjects.to_dict()

    def battle(self, attacker, enemy, auto=False) -> bool:
        if not enemy.vulnerable:
            if not auto:
                self.view.message = "Invulnerable object change direction"
            return False
        while not (attacker.dead == True or enemy.dead == True):
            if auto:
                attacker.attack(enemy, auto)
                enemy.attack(attacker, auto)
            else:
                enemy.stats()
                player_input = input("enemy ahead what to do?(attack / run / use magic(not usable))")
                if player_input in ["attack" ,"a"]:
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
main.backend.game_state_machine.register_event_handler("JOIN", main.on_join)
main.backend.game_state_machine.register_event_handler("MOVE", main.on_move)
main.backend.run("localhost", 5000)


# TODO:
#   Create map rendering
#   Create object classes
