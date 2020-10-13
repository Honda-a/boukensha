from dataclasses import dataclass


@dataclass(frozen=True)
class Types:
    OBJECT: str = "object"
    MOVING: str = "moving"
    PLAYER: str = "player"
    MOB: str = "mob"
    BOSS: str = "boss"
    SPRIT: str = "sprit"

types = Types()


GAME_WIDTH = 106
GAME_HEIGHT = 65
CAMERA_VIEW = 10

# 1 means every player move mobs move 0 means mob wont move
MOB_MOVEMENT = 0.2