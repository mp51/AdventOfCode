import int_comp as ic
from collections import namedtuple

def print_tiles(tiles):
   min_x = min(tiles.keys(), key=lambda pos: pos.x).x
   max_x = max(tiles.keys(), key=lambda pos: pos.x).x

   min_y = min(tiles.keys(), key=lambda pos: pos.y).y
   max_y = max(tiles.keys(), key=lambda pos: pos.y).y

   width = max_x - min_x
   height = max_y - min_y

   canvas = [[' ' for _ in range(width+1)] for _ in range(height+1)]

   for pos, color in tiles.items():
      if color == 1:
         canvas[pos.y-min_y][pos.x-min_x] = '#'

   canvas.reverse()
   for row in canvas:
      print(''.join(row))



Position = namedtuple("Position", "x y")

memory = [int(i) for i in input().split(',')]
memory.extend([0]*1000)

comp = ic.Computer(memory, 1)

directions = ["up", "right", "down", "left"]
dir_idx = 0

tiles = {Position(0,0) : 0} # position : color
colored_tiles = set()
colored_tiles_list = []
robot_pos = Position(0, 0)

while True:
   outputs, state = comp.compute_result()
   color, direction = outputs

   # paint tile
   current_color = tiles.get(robot_pos, 0)
   if current_color != color:
      tiles[robot_pos] = color
      colored_tiles.add(robot_pos)
   
   # adjust robot's direction
   if direction == 0: # turn left 90 degress
      dir_idx -= 1
      if dir_idx < 0:
         dir_idx = len(directions) - 1
   else:              # turn right 90 degrees
      dir_idx += 1
      if dir_idx == len(directions):
         dir_idx = 0

   # move robot
   dir_ = directions[dir_idx]
   prev_pos = robot_pos
   if dir_ == "up":
      robot_pos = Position(robot_pos.x, robot_pos.y+1)
   elif dir_ == "down":
      robot_pos = Position(robot_pos.x, robot_pos.y-1)
   elif dir_ == "right":
      robot_pos = Position(robot_pos.x+1, robot_pos.y)
   elif dir_ == "left":
      robot_pos = Position(robot_pos.x-1, robot_pos.y)

   # print("Moving", dir_, "from", prev_pos, "to", robot_pos)

   input_color = 0
   if robot_pos in tiles.keys():
      input_color = tiles[robot_pos]
   comp.set_input(input_color)

   if state == ic.State.FINISHED:
      break

print("Colored tiles:", len(colored_tiles))
print_tiles(tiles)