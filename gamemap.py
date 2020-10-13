from mapgenerator import RLDungeonGenerator as MapGanerator
import os
import constants as const


class GameView:

    def __init__(self, gameobjects, width, height):
        self.message = ""
        self.gameobjects = gameobjects
        map_ganerator = MapGanerator(width, height, self.gameobjects)
        self.game_map = map_ganerator.generate_map()

    def render(self, player_id) -> None:
        canvas = []
        player_x = self.gameobjects.player.get(player_id).x
        player_y = self.gameobjects.player.get(player_id).y

        camera_x_min = player_x - const.CAMERA_VIEW
        camera_x_max = player_x + const.CAMERA_VIEW
        camera_x_min = 0 if camera_x_min < 0 else camera_x_min
        camera_x_max = const.GAME_WIDTH if camera_x_max > const.GAME_WIDTH else camera_x_max

        camera_y_min = player_y - const.CAMERA_VIEW
        camera_y_max = player_y + const.CAMERA_VIEW
        camera_y_min = 0 if camera_y_min < 0 else camera_y_min
        camera_y_max = const.GAME_HEIGHT if camera_y_max > const.GAME_HEIGHT else camera_y_max

        camera_x = range(
            camera_x_min,
            camera_x_max
        )
        camera_y = range(
            camera_y_min,
            camera_y_max
        )
        for y in camera_y:
            row = []
            for x in camera_x:
                point = self.game_map[y][x]
                if point == 0:
                    row.append(" ")
                elif isinstance(point, object):
                    row.append(point.charactar)
                else:
                    row.append(point)
            canvas.append("".join(row))
        canvas.reverse()
        canvas = ['{:>60}'.format(row) for row in canvas]
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(canvas))
        print(self.message)
        self.message = ""
        return canvas
