import sys
import pygame
from argparse import ArgumentParser
from manual import Manual
from enum import Enum
from best_first_search import BestFS
from a_star_search import AStar


def get_game_class(game_type):
    return {
        "bestfs": BestFS,
        "a_star": AStar,
    }.get(game_type, BestFS)


parser = ArgumentParser(description="Start snakeAIs!")
parser.add_argument(
    "-gt",
    "--game_type",
    default="manual",
    type=str,
    help="type of game you want to play",
)
parser.add_argument(
    "-o",
    "--obstacles",
    default=False,
    type=bool,
    help="specify if you would like to include obstacles in the game",
)
args = vars(parser.parse_args())
game_type = args["game_type"]
game_has_obstaces = args["obstacles"]

pygame.init()
game_class = get_game_class(game_type)
game = game_class(game_has_obstaces)
score = game.main()

