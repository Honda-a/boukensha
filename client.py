from pygase import client
from baseclasses import gameobject
from random import randint, choice, random
from objects import Player, Mob, GameObjects
from gamemap import GameView
import constants as const
from pygase import Client
from time import sleep
import os


class PlayerClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)
        self.game_state: dict = {}

    # "PLAYER_CREATED" event handler
    def on_player_created(self, args):
        player_id, game_state = args
        # Remember the id the backend assigned the player.
        self.player_id = player_id
        self.game_state = game_state


class ClientGame:

    def __init__(self, client: PlayerClient):
        self.view_width = const.GAME_WIDTH
        self.view_height = const.GAME_HEIGHT
        self.loading = False
        self.message = ""
        self.client = client
        self.gameobjects = GameObjects()
        self.view = GameView(self.gameobjects, self.view_width, self.view_height)
        self.update_game_state()

    def move(self):
        direction = input("move to: ")
        if direction.lower() not in ['left', 'a', 'right', 'd', 'up', 'w', 'down', 's']:
            print("""wrong input please use ['left key', 'right key', 'up key', 'down key'] OR
            ['a key', 'd key', 'w key', 's key'] """)
            self.move()
        self.loading = True
        self.client.dispatch_event(
            event_type="MOVE",
            player_id=self.client.player_id,
            direction=direction,
            ack_callback=self.update_game_state
        )

    def update_game_state(self):
        self.message = self.client.game_state.get("message")
        self.loading = False


    def run(self):
        while True:
            self.move()
            while self.loading:
                print("waiting")
                sleep(0.1)
            self.render()

    def render(self):
        canvas = ['{:>60}'.format(row)
                  for row in self.client.game_state.get("view_map")]
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(canvas))
        print(self.message)

    def game_over(self):
        print("GAME OVER TRY NEXT TIME")
        quit()

client = PlayerClient()
client.connect_in_thread(hostname="localhost", port=5000)
client.dispatch_event("JOIN", input("Player name: "))
# Wait until "PLAYER_CREATED" has been handled.
while client.player_id is None:
    pass

main = ClientGame(client)
main.run()

# TODO:
#   Create map rendering
#   Create object classes
