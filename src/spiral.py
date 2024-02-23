#!/usr/bin/env python3

from __future__ import annotations
import numpy as np
import math
import argparse
from enum import Enum

class Direction(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Coord:
    x: int
    y: int
    direction: Direction
    map_size: int
    
    def __init__(self, x: int, y: int, map_size: int, direction: Direction = Direction.NORTH):
        self.x = x
        self.y = y
        self.direction = direction
        self.map_size = map_size

    @property
    def is_inbounds(self) -> bool:
        return (self.x >= 0 and self.x < self.map_size) and (self.y >= 0 and self.y < self.map_size)
    
    def is_empty(self, s_map: np.array):
        if(not self.is_inbounds):
            return False
        return (s_map[self.y][self.x] == 0)

    def turn_cw(self, s_map: np.array) -> Coord:
        # Try going immediately left
        cw_pos = {
            Direction.NORTH: Coord(self.x + 1, self.y, self.map_size, Direction.EAST),
            Direction.EAST: Coord(self.x, self.y + 1, self.map_size, Direction.SOUTH),
            Direction.SOUTH: Coord(self.x - 1, self.y, self.map_size, Direction.WEST),
            Direction.WEST: Coord(self.x, self.y - 1, self.map_size, Direction.NORTH)
        }[self.direction]

        if(cw_pos.is_inbounds and cw_pos.is_empty(s_map)):
            self.x = cw_pos.x
            self.y = cw_pos.y
            self.direction = cw_pos.direction
            self.map_size = cw_pos.map_size
            return self

        # Try going straight ahead
        sa_pos = {
            Direction.NORTH: Coord(self.x, self.y - 1, self.map_size, Direction.NORTH),
            Direction.EAST: Coord(self.x + 1, self.y, self.map_size, Direction.EAST),
            Direction.SOUTH: Coord(self.x, self.y + 1, self.map_size, Direction.SOUTH),
            Direction.WEST: Coord(self.x - 1, self.y, self.map_size, Direction.WEST)
        }[self.direction]

        if(sa_pos.is_inbounds and sa_pos.is_empty(s_map)):
            self.x = sa_pos.x
            self.y = sa_pos.y
            self.direction = sa_pos.direction
            self.map_size = sa_pos.map_size
            return self
        raise RuntimeError('Nowhere to go!')


def main():
    parser = argparse.ArgumentParser(prog='spiral')
    parser.add_argument('num', type=int, help='number of numbers to spiral.')
    args = parser.parse_args()

    spiral_width = math.ceil(math.sqrt(args.num))
    spiral_center = math.floor(spiral_width / 2)
    missing = abs(args.num - math.pow(spiral_width, 2))

    cursor = Coord(spiral_center, spiral_center, spiral_width)
    spiral_map = np.zeros((spiral_width, spiral_width))

    try:
        for i in sorted(range(1, args.num + 1)):
            spiral_map[cursor.y][cursor.x] = i
            cursor = cursor.turn_cw(spiral_map)
    except RuntimeError as e:
        print(e)
    finally:
        print(f'\n{spiral_map}')


if __name__ == '__main__':
    main()

