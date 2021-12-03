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

def get_neighbor(cell: tuple[int, int], direction: int) -> tuple[int, int]:
    """ Finds cell's neighbor in given direction

    Args:
        cell (tuple[int, int]): Cell's coords in maze in format (x, y)
        direction (int): Numeric representation of direction

    Returns:
        tuple[int, int]: Coordinates of cell's neighbor in given direction
    """    

    if direction == Direction.N:
        return cell[0], cell[1] - 1
    elif direction == Direction.E:
        return cell[0] - 1, cell[1]
    elif direction == Direction.S:
        return cell[0], cell[1] + 1
    elif direction == Direction.W:
        return cell[0] + 1, cell[1]
    elif direction is None:
        return cell

    raise ValueError(f'Invalid direction value: {direction}')