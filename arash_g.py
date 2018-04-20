from random import randint
import os
class Player:
   def __init__(self, view_width, view_height):
       self.x = 0
       self.y = 0
       self.charactar = "X"
       self.view_width = view_height - 1
       self.view_height = view_height - 1
       self.last_pos = (0, 0)

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

class GameView:
   def __init__(self, width, height):
       self.width = width
       self.height = height
       self.message = ""

   def render(self, map_frame):
      canvas = []
      for y in map_frame:
          row = []
          for x in y:
              if x == 0:
                  row.append(" ")
              elif x == 1:
                  row.append("#")
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
       self.game_map = [[randint(0,randint(0,randint(0,1))) for _ in range(self.view_width)] for _ in range(self.view_height)]
       self.view = GameView(self.view_width, self.view_height)
       self.player = Player(self.view_width, self.view_height)
       self.update_player_pos()
       self.view.render(self.game_map)

   def update_player_pos(self):
       if self.game_map[self.player.y][self.player.x] == 0:
           self.game_map[self.player.last_pos[1]][self.player.last_pos[0]] = 0
           self.game_map[self.player.y][self.player.x] = self.player.charactar
       else:
           self.player.x = self.player.last_pos[0]
           self.player.y = self.player.last_pos[1]
           self.view.message = f"wall ahead turn some other direction {self.game_map[self.player.y][self.player.x]}"

   def run(self):
       while True:
           direction = input("move to: ")
           self.player.move(direction)
           self.update_player_pos()
           self.view.render(self.game_map)

main = Game()
main.run()
