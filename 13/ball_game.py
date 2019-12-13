import int_comp as ic
from collections import namedtuple

DrawInstruction = namedtuple("DrawInstruction", "x y id")

def print_tiles(tiles):
   print()
   for row in tiles:
      print(''.join(row))

def count_tiles(tiles, id):
   count = 0
   for tile in tiles:
      count += tile.count(id)
   return count

input_sequence = [int(i) for i in input().split(',')]
comp = ic.Computer(input_sequence, 0)
instructions, state = comp.compute_result()

draw_instructions = []
for i in range(0, len(instructions), 3):
   draw_instructions.append( DrawInstruction(instructions[i], instructions[i+1], instructions[i+2]) )

width = max(draw_instructions, key=lambda d: d.x).x
height = max(draw_instructions, key=lambda d: d.y).y
tiles = [ [' ' for _ in range(width+1)] for _ in range(height+1) ]

# fill tiles
for d in draw_instructions:
   if d.id == 0:
      s = ' '
   elif d.id == 1:
      s = '#'
   elif d.id == 2:
      s = 'x'
   elif d.id == 3:
      s = '_'
   elif d.id == 4:
      s = 'O'

   tiles[d.y][d.x] = s

print_tiles(tiles)
block_count = count_tiles(tiles, 'x')
print(block_count, "block tiles")