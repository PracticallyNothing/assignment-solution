#!/bin/python3

import time

debugMode = False


def validate(m, n, inLayer):
    """
    Check if the input is actually a valid problem.
    """

    # The problem is unsolvable if the number of tiles is odd.
    # (Since there would be a 1 tile hole left over)
    if (n * m) % 2 == 1:
        return False

    w, h = m, n
    checked = [[False for x in range(w)] for y in range(h)]

    # FILO queue of tiles that have yet to be checked.
    queue = []

    # Loop that checks whether the input layer
    # has any bricks that are an incorrect size.
    for y in range(h):
        for x in range(w):
            # If the current tile has already been considered, skip it.
            if checked[y][x]:
                continue

            # Number of tiles that are part of this brick.
            # Must be 2 for the input layer to be valid.
            brickSize = 0

            # Initialize the first element of the queue.
            queue.append([x, y])

            while len(queue) > 0:
                xx, yy = queue[0][0], queue[0][1]

                if checked[yy][xx]:
                    queue.pop(0)
                    continue

                brickSize += 1

                # Mark the current tile as checked
                checked[yy][xx] = True

                # If we aren't at the right edge and the tile to our
                # right has the same brick number as our current tile,
                # queue it to check its neighbours.
                if xx < w-1 and inLayer[yy][xx] == inLayer[yy][xx+1]:
                    queue.append([xx+1, yy])

                # If we aren't at the bottom and the tile below us
                # has the same brick number as our current tile,
                # queue it to check its neighbours.
                if yy < h-1 and inLayer[yy][xx] == inLayer[yy+1][xx]:
                    queue.append([xx, yy+1])

                # We're done with this tile, so discard it.
                queue.pop(0)

            # The problem is invalid if there's a brick
            # that isn't exactly 2 tiles in size.
            if brickSize != 2:
                print(
                    "Error: Brick %d at (%d, %d) size must be 2, but is %d."
                    % (inLayer[y][x], x, y, brickSize)
                )
                return False

    return True


def checkSolution(w, h, l1, l2):
    """
    Check if a given solution matches the requirements
    of the task.

    w and h are the width and height of the layers,
    l1 is the input layer,
    l2 is the solution
    """

    # Array for tracking checked tiles.
    # If a tile has already been checked, it gets skipped.
    checked = [[False for x in range(w)] for y in range(h)]

    # We need only check that no bricks from the second layer,
    # lie entirely on bricks from the first.
    for y in range(h):
        for x in range(w):
            if checked[y][x]:
                continue

            checked[y][x] = True

            if x < w-1 and l2[y][x] == l2[y][x+1]:
                if l1[y][x] != l1[y][x+1]:
                    checked[y][x+1] = True
                    continue
                else:
                    print(
                        ("Invalid solution!" +
                         " Brick %d from layer 2 lies entirely" +
                         " on top of brick %d from layer 1!")
                        % (l2[y][x], l1[y][x]))
                    return False
            elif y < h-1 and l2[y][x] == l2[y+1][x]:
                if l1[y][x] != l1[y+1][x]:
                    checked[y+1][x] = True
                    continue
                else:
                    print(
                        ("Invalid solution!" +
                         " Brick %d from layer 2 lies entirely" +
                         " on top of brick %d from layer 1!")
                        % (l2[y][x], l1[y][x]))
                    return False
    return True


def solve(m, n, inLayer):
    """
    Generate a solution for a given input layer of size M by N.
    """

    # If there is only one row or only one column, there will
    # be no solution, so we can just exit early.
    if n == 1 or m == 1:
        print("No solution: There is only one row or only one column.")
        return -1

    # Aliases for m and n as width and height
    w, h = m, n
    # Where the result is stored
    outLayer = [[0 for x in range(w)] for y in range(h)]
    # A variable to track which brick number should be used next.
    nextBrickNum = 0

    start = time.time_ns()

    # Algorithm:
    # - scan left to right, top to bottom
    # - check if current position has already been solved
    # - if not, try to horizontally or vertically place a brick at the location
    # - if we can't place a brick, it means the problem will have no solution
    for y in range(h):
        for x in range(w):
            if outLayer[y][x] != 0:
                continue

            nextBrickNum += 1
            outLayer[y][x] = nextBrickNum

            if x < w-1 and inLayer[y][x] != inLayer[y][x+1]:
                outLayer[y][x+1] = nextBrickNum
            elif y < h-1 and inLayer[y][x] != inLayer[y+1][x]:
                outLayer[y+1][x] = nextBrickNum
            else:
                print("No solution at x: %d, y: %d" % (x, y))
                return -1

            if debugMode:
                print("Step %d: " % (nextBrickNum))
                for row in outLayer:
                    print(row)

    print(("Solution found! Time it took: %d ns") % (time.time_ns() - start))
    return outLayer


if __name__ == "__main__":
    n, m = tuple(map(int, input().split()))
    inLayer = [list(map(int, input().split())) for i in range(n)]

    if validate(m, n, inLayer):
        solution = solve(m, n, inLayer)

        if solution != -1:
            for row in solution:
                print(row)
            if checkSolution(m, n, inLayer, solution):
                print("Solution is valid.")
        else:
            print(solution)
    else:
        print("ERROR: Invalid input!")
