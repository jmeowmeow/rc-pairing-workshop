import sys
from time import sleep
import curses

# get the filename if present
grid_arg = sys.argv[1] if len(sys.argv) > 1 else None 

grid = []

blinker = """00000
00000
00100
00100
00100
00000"""

glider = """001000
000100
011100
000000
000000
000000"""

# default_grid = blinker
default_grid = glider

def init_grid(grid_arg, default_grid):
    grid = []
    if grid_arg:
        with open(grid_arg) as f:
            x = 0
            for line in f:
                line = line.strip()
                if len(line) > 0:
                  grid.append([])
                  for cell in range(len(line)):
                      cell_char = line[cell]
                      grid[x].append(int(cell_char))
                  x += 1
    else:
        grid_lines = default_grid.split("\n")
        for grid_line in range(len(grid_lines)):
            grid.append([])
            for cell in range(len(grid_lines[grid_line])):
                cell_char = grid_lines[grid_line][cell]
                grid[grid_line].append(int(cell_char))
    return grid

def game_of_life(grid):
    result = []
    for x in range(len(grid)):
        result.append([])
        grid_row = grid[x]
        for y in range(len(grid_row)):
            result[x].append(update_cell(x, y, grid))
    return result

def update_cell(cell_x, cell_y, grid):
    live = 0
    for x in range(max(0, cell_x - 1), min(len(grid), cell_x + 2)):
        for y in range(max(0, cell_y - 1), min(len(grid[x]), cell_y + 2)):
            if not (x == cell_x and y == cell_y):
                live += grid[x][y]
    if (grid[cell_x][cell_y] == 1):
        if (live < 2 or live > 3):
            return 0
        else:
            return 1
    else:
        if (live == 3):
            return 1
    return 0

def pretty_print(grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            print(grid[x][y], end="")
        print()

def curses_print(grid, scr):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            scr.addch(x, y, ord('@') if grid[x][y] == 1 else ord('.'))

def main(scr):
    grid = init_grid(grid_arg, default_grid)
    while True:
        grid = game_of_life(grid)
        curses_print(grid, scr)
        scr.refresh()
        sleep(.5) 

curses.wrapper(main)
