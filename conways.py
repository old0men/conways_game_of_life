import pygame
import time
import random

repitition = f"inf"
timer = 0
count = 0
count_list = []


width = 800
window = pygame.display.set_mode((width, width))
pygame.display.set_caption("conway's game of life")

alive = (255, 255, 255)
dead = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Cell:

  def __init__(self, row, col, width, total_rows):
    self.row = row
    self.col = col
    self.x = row * width
    self.y = col * width
    self.color = dead
    self.neighbors = 0
    self.temp_state = 0
    self.state = 0
    self.width = width
    self.total_rows = total_rows

  def get_pos(self):
    return self.row, self.col

  def draw(self, window):
    pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

  def revive(self):
    self.color = alive
    self.state = 1

  def kill(self):
    self.color = dead
    self.state = 0

  def make_green(self):
    self.color = GREEN

  def make_red(self):
    self.color = RED

  def is_alive(self):
    return self.state == 1

  def is_dead(self):
    return self.state == 0

  def recognize_neighbor(self, grid):
    self.neighbors = 0

    # each checks if the grid is in bounds in it's direction and if its alive
    if self.row < self.total_rows-1 and grid[self.row+1][self.col].is_alive() == True:
      self.neighbors += 1 # right

    if self.row > 0 and grid[self.row-1][self.col].is_alive() == True:
      self.neighbors += 1 # left


    if self.col > 0 and grid[self.row][self.col-1].is_alive() == True:
      self.neighbors += 1 # up

    if self.row > 0 and self.col > 0 and grid[self.row-1][self.col-1].is_alive() == True:
      self.neighbors += 1 # up_left

    if self.row < self.total_rows - 1 and self.col > 0 and grid[self.row+1][self.col-1].is_alive() == True:
      self.neighbors += 1 # up_right


    if self.col < self.total_rows-1 and grid[self.row][self.col+1].is_alive() == True:
      self.neighbors += 1 # down

    if self.row > 0 and self.col < self.total_rows-1 and grid[self.row-1][self.col+1].is_alive() == True:
      self.neighbors += 1  # bottom_left

    if self.row < self.total_rows - 1 and self.col < self.total_rows-1 and grid[self.row+1][self.col+1].is_alive() == True:
      self.neighbors += 1 # bottom_right


def make_grid(total_rows, screen_width):

  grid = []
  gap = screen_width // total_rows
  for row in range(total_rows):
    grid.append([])
    for column in range(total_rows):
      cell = Cell(row, column, gap, total_rows)
      grid[row].append(cell)

  return grid



def print_grid(grid):
  for row in grid:
    for col in row:
      print(f"{col.row}, {col.col}, {col.color}")



def get_clicked_pos(pos, total_rows, width):
  gap = width // total_rows
  y, x = pos

  col = y // gap
  row = x // gap

  return row, col


def draw(win, grid):
  win.fill(dead)

  for row in grid:
    for spot in row:
      spot.draw(win)

  pygame.display.update()

def update_map(grid):
  for row in grid:
    for col in row:
      if col.temp_state == 1:
        col.revive()
      else:
        col.kill()

def conways_game_of_life(grid):
  count = 0
  for row in grid:
    for col in row:
      col.recognize_neighbor(grid)
      if col.is_alive() == True:
        count += 1
        # print(f"alive neighbors: {col.neighbors}\ndead neighbors: {8-col.neighbors}")
        if col.neighbors == 2 or col.neighbors == 3:
          col.temp_state = 1
        else:
          col.temp_state = 0
      if col.is_dead() == True and col.neighbors == 3:
        col.temp_state = 1

  print(f"amount of alive cells: {count}\n")
  update_map(grid)

  draw(window, grid)

  return count

def main(window, width, count):
  total_rows = 200
  grid = make_grid(total_rows, width)

  print_grid(grid)


  run = True
  while run:

    dead_list = []

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        print(pos)
        row, col = get_clicked_pos(pos, total_rows, width)
        print(f"row: {row}, col: {col}\n")
        cell = grid[col][row]
        cell.revive()
        cell = grid[col+1][row]
        cell.revive()
        cell = grid[col-1][row]
        cell.revive()
        cell = grid[col][row+1]
        cell.revive()
        cell = grid[col][row-1]
        cell.revive()
        cell = grid[col+1][row+1]
        cell.revive()
        cell = grid[col+1][row-1]
        cell.revive()
        cell = grid[col-1][row+1]
        cell.revive()
        cell = grid[col-1][row-1]
        cell.revive()


      if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        print(pos)
        row, col = get_clicked_pos(pos, total_rows, width)
        print(f"row: {row}, col: {col}\n")
        cell = grid[col][row]
        cell.kill()



      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          timer = 0
          while timer != repitition:
            timer += 1
            temp_count = conways_game_of_life(grid)
            count = temp_count
            print(f"count: {count}")
            count_list.append(count)
            if count == 0:
              timer = repitition
              print("due to death")
            try:
              if count_list[-3] == count_list[-2] and count_list[-3] == count_list[-1] and count_list[-2] == count_list[-1]:
                dead_list.append(count_list[-1])
            except:
              pass
            if len(dead_list) == 5:
              timer = repitition
              print("due to no change")
              dead_list = []
            print(dead_list)




    draw(window, grid)





main(window, width, count)