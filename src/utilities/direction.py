class Direction:
    N = NORTH = 0
    E = EAST = 1
    S = SOUTH = 2
    W = WEST = 3

def left(direction: int) -> int:
    return (direction - 1) % 4

def right(direction: int) -> int:
    return (direction + 1) % 4

def opposite(direction: int) -> int:
    return (direction + 2) % 4