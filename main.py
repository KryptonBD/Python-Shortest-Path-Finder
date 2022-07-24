import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "@", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "X", "#", "#", "#", "#", "#", "#", "#"]
]

# Print Maze Function
def onPrintMaze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    WHITE = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 3, "*", WHITE)
            else:
                stdscr.addstr(i, j * 3, value, GREEN)

# Find Starting Position
def onFindStart(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None

# Find Path
def onFindPath(maze, stdscr):
    start = "@"
    end = "X"
    start_position = onFindStart(maze, start)

    q = queue.Queue()
    q.put((start_position, [start_position]))

    visited = set()

    while not q.empty():
        current_position, path = q.get()
        row, col = current_position

        stdscr.clear()
        onPrintMaze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = onFindNeighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            nRow, nCol = neighbor
            if maze[nRow][nCol] == "#":
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


# Find Neighbors
def onFindNeighbors(maze, row, col):
    neighbors = []

    if row > 0: #outside maze upwards
        neighbors.append((row - 1, col))
    if row + 1 < len(maze): #outside maze downward
        neighbors.append((row + 1, col))

    if col > 0:
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    onFindPath(maze, stdscr)
    stdscr.getch()

wrapper(main)