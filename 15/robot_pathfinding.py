import int_comp as ic
from collections import namedtuple
import random

class Direction(int):
   def opposite(self):
      if self == 0:
         return 1
      elif self == 1:
         return 0
      elif self == 2:
         return 3
      elif self == 3:
         return 2

class Robot:
   def __init__(self, int_comp, position):
      self.comp = int_comp
      self.position = position
      self.last_moves = []

   def try_move(self, direction):
      # 0 - up
      # 1 - down
      # 2 - left
      # 3 - right
      self.last_moves.append( (self.position, Direction(direction)) )
      self.comp.set_input(direction+1)
      out, state = self.comp.compute_result()
      # print()
      # print(direction, out, state)
      
      if out[0] == 0:
         del self.last_moves[-1] # did not move
         return False, self.position.next_tile(direction, '#')
      elif out[0] == 1:
         self.position = self.position.next_tile(direction, '.')
         return True, self.position
      elif out[0] == 2:
         self.position = self.position.next_tile(direction, '*')
         return True, self.position


   def undo_move(self):
      if self.last_moves:
         last_pos, last_direction = self.last_moves.pop()
         self.comp.set_input(last_direction.opposite()+1)
         self.comp.compute_result()
         self.position = last_pos
         return True
      else:
         return False


TileBase = namedtuple("Tile", "x y state")
class Tile(TileBase):
   def next_tile(self, direction, state=' '):
      x = self.x
      y = self.y
      if direction == 0:
         y -= 1
      elif direction == 1:
         y += 1
      elif direction == 2:
         x -= 1
      elif direction == 3:
         x += 1
      return Tile(x, y, state)

   def __eq__(self, other):
      return self.x == other.x and self.y == other.y


def dfs_explore(robot, print_=False):
   tiles = [robot.position]
   while True:
      if print_:
         print_tiles(tiles, robot.position)
      # move to the next node
      current_tile = robot.position
      
      moved = False
      for direction in range(4):
         if current_tile.next_tile(direction) not in tiles:
            moved, tile = robot.try_move(direction)
            if tile not in tiles:
               tiles.append(tile)
            if moved:
               break

      if not moved:
         if not robot.undo_move():
            break

   return tiles

def bfs_search(source, destination, tiles):
   visited = set()
   next_to_visit = [source]
   traceback = {}
   while next_to_visit:
      current_node = next_to_visit.pop(0)
      if current_node == destination:
         return traceback
      
      nodes = []
      for i in range(4):
         if tiles.count(current_node.next_tile(i)):
            tile = tiles[tiles.index(current_node.next_tile(i))]
            if tile.state != '#':
               nodes.append( tile )

      for node in nodes:
         if TileBase(*node) not in visited:
            visited.add(TileBase(*node))
            traceback[TileBase(*node)] = current_node
            next_to_visit.append(node)
   
   return None

def find_path_bfs(source, destination, tiles):
   traceback = bfs_search(source, destination, tiles)
   path = []
   if traceback:
      current_tile = destination
      while current_tile != source:
         path.append(current_tile)
         current_tile = traceback[TileBase(*current_tile)]

   return path

def print_tiles(tiles, robot_pos):
   min_x = min(tiles, key=lambda t: t.x).x
   width = max(tiles, key=lambda t: t.x).x - min_x + 1 
   min_y = min(tiles, key=lambda t: t.y).y
   height = max(tiles, key=lambda t: t.y).y - min_y + 1
   image = [[' ' for _ in range(width)] for _ in range(height)]
   print(width, height)
   for t in tiles:
      image[t.y-min_y][t.x-min_x] = t.state

   image[robot_pos.y-min_y][robot_pos.x-min_x] = 'x'

   for row in image:
      print(''.join(row))
   print()
   return image



program = [int(i) for i in input().split(',')]

comp = ic.Computer(program)
output, state = comp.compute_result()
start_pos = Tile(0,0,'.')
robot = Robot(comp, start_pos)

tiles = dfs_explore(robot)
print_tiles(tiles, start_pos)

destination = next((t for t in tiles if t.state == '*'))
print(destination)

path = find_path_bfs(Tile(0,0,'.'), destination, tiles)
print_tiles(path, path[0])
print("Path length:", len(path))