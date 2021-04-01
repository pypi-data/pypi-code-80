import argparse
import car_racer.config as config
from dotmap import DotMap
from car_racer.main import *
from car_racer.track import Track
from car_racer.car import Car


def parse_game_arguments():
    parser = argparse.ArgumentParser(description="Car Racer game",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--track_length",
                        type=int,
                        default=5000,
                        help="How long the track will be (in pixel)")
    parser.add_argument("--track_seed",
                        type=int,
                        default=0,
                        help="With which seed the track will be initialized")
    parser.add_argument("--corner_chance",
                        type=int,
                        default=30,
                        help="The chance of corners happening over straights")
    parser.add_argument("--corner_max_angle",
                        type=int,
                        default=90,
                        help="the maximum turn of a corner in degree")

    arguments = parser.parse_args()

    config.track = Track(arguments.track_length, arguments.track_seed,
                         DotMap(chance=arguments.corner_chance, max_angle=arguments.corner_max_angle))
    config.car = Car(config.track)


def race():
    parse_game_arguments()
    start_game()
