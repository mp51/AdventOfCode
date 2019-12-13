import int_comp as ic
from collections import namedtuple


class GameTiles(list):
   def print_tiles(self):
      print()
      print("Score:", self.score)
      for row in self:
         print(''.join(row))

   def count_tiles(self, id):
      count = 0
      for row in self:
         count += row.count(id)
      return count

   def set_score(self, score):
      self.score = score

def get_tiles_dimensions(instructions):
   width = 0
   height = 0
   for i in range(0, len(instructions), 3):
      if instructions[i] > width:
         width = instructions[i]
      if instructions[i+1] > height:
         height = instructions[i+1]
   return width, height

def create_or_update_game_tiles(instructions, width, height, tiles=None):
   if tiles is None:
      tiles = GameTiles([ [' ' for _ in range(width+1)] for _ in range(height+1) ])

   paddle_pos = None
   ball_pos = None
   for i in range(0, len(instructions), 3):
      x = instructions[i]
      y = instructions[i+1]
      val = instructions[i+2]

      if val == 0:
         s = ' '
      elif val == 1:
         s = '#'
      elif val == 2:
         s = 'x'
      elif val == 3:
         s = '_'
         paddle_pos = x
      elif val == 4:
         s = 'O'
         ball_pos = x

      if x == -1 and y == 0:
         tiles.set_score(val)
      else:
         tiles[y][x] = s

   return tiles, ball_pos, paddle_pos


input_sequence = [int(i) for i in input().split(',')]
input_sequence[0] = 2
comp = ic.Computer(input_sequence, 0)

instructions, state = comp.compute_result()
width, height = get_tiles_dimensions(instructions)
tiles, ball_pos, paddle_pos = create_or_update_game_tiles(instructions, width, height)

tiles.print_tiles()
block_count = tiles.count_tiles('x')
print(block_count, "block tiles")

# game loop
while state == ic.State.WAITING_FOR_INPUT:
   move = 0
   if ball_pos > paddle_pos:
      move = 1
   elif ball_pos < paddle_pos:
      move = -1

   comp.set_input(move)
   result, state = comp.compute_result()
   tiles, ball_pos, paddle_pos = create_or_update_game_tiles(result, width, height, tiles)
   tiles.print_tiles()
