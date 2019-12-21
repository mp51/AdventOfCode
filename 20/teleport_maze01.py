import string
from collections import namedtuple

PositionBase = namedtuple("Position", "i j")
class Position(PositionBase):
   def __add__(self, other):
      return Position(self.i + other.i, self.j + other.j)

   def __sub__(self, other):
      return Position(self.i - other.i, self.j - other.j)

   def __gt__(self, other):
      return self.i > other.i and self.j > other.j

   def __lt__(self, other):
      return self.i < other.i and self.j < other.j

DIRECTIONS = [Position(-1,0), Position(0,1), Position(1, 0), Position(0, -1)]

class Maze(list):
   def __init__(self):
      self.portals = {}

   def at(self, position):
      if position > Position(0,0) \
         and position.i < len(self) \
            and position.j < len(self[position.i]):
         return self[position.i][position.j]
      return None

   def get_next_pos(self, pos, direction):
      new_pos = pos + direction
      n = self.at(new_pos)
      print(n)
      if n is None or n == '#': 
         return None
      if n == '.':
         return new_pos

      # Next tile is a portal or entry/exit point
      nn = self.at(new_pos + direction)
      if nn is None:
         return None

      portal_name = ''.join(sorted(n+nn))
      if portal_name in self.portals.keys():
         positions = self.portals[portal_name]
         return positions[0] if positions[0] != pos else positions[1]

      return None

   def print(self, current_pos):
      for i, row in enumerate(self):  
         for j, val in enumerate(row):
            if current_pos[0] == i and j == current_pos[1]:
               val = '@'
            print(val, end='')
         print()

   def explore_portals(self):
      def get_near_field_pos(first_pos, second_pos):
         direction = first_pos - second_pos
         field_pos = first_pos + direction
         def check_if_valid_field():
            field = self.at(field_pos)
            if field is not None and field == '.':
               return True
            else:
               return False

         if check_if_valid_field():
            return field_pos
         
         field_pos = second_pos - direction
         if check_if_valid_field():
            return field_pos

         return None

      for i, row in enumerate(self):  
         for j, val in enumerate(row):
            if val in string.ascii_uppercase:
               pos = Position(i,j)
               for d in DIRECTIONS:
                  next_pos = pos + d
                  next_val = self.at(next_pos)
                  if next_val is None:
                     continue
                  if next_val in string.ascii_uppercase:
                     if next_val != val:
                        # This might be a portal. Check near fields.
                        field_pos = get_near_field_pos(pos, next_pos)
                        if field_pos is not None:
                           portal_name = ''.join(sorted(val+next_val))
                           print("Found portal", portal_name, field_pos)
                           if portal_name in self.portals.keys():
                              if len(self.portals[portal_name]) < 2 and field_pos not in self.portals[portal_name]:
                                 if self._is_outer_portal(pos):
                                    self.portals[portal_name].append(field_pos)
                                 else:
                                    self.portals[portal_name].insert(0, field_pos)
                           else:
                              self.portals[portal_name] = [field_pos]
                     elif val == 'A':
                        # Entry pos
                        self.entry_pos = get_near_field_pos(pos, next_pos)
                        print("Found entry pos:", self.entry_pos)
                     elif val == 'Z':
                        # Exit pos
                        self.exit_pos = get_near_field_pos(pos, next_pos)
                        print("Found exit pos:", self.exit_pos)

   def _is_outer_portal(self, pos):
      for d in DIRECTIONS:
         npos = pos + d + d + d
         if self.at(npos) is None:
            return True
      return False

def bfs_search(source, destination, maze):
   visited = set()
   next_to_visit = [source]
   traceback = {}
   while next_to_visit:
      current_pos = next_to_visit.pop(0)
      if current_pos == destination:
         return traceback
      
      for i in range(4):
         next_pos = maze.get_next_pos(current_pos, DIRECTIONS[i])
         if next_pos is not None and next_pos not in visited:
            visited.add(next_pos)
            next_to_visit.append(next_pos)
            traceback[next_pos] = current_pos
   
   return None

def find_path_bfs(source, destination, maze):
   traceback = bfs_search(source, destination, maze)
   path = []
   if traceback:
      current_pos = destination
      while current_pos != source:
         path.append(current_pos)
         current_pos = traceback[current_pos]

   return path



maze = Maze()

while True:
   row = input()
   if not row:
      break
   maze.append(row)

maze.explore_portals()
print(maze.portals)

path = find_path_bfs(maze.entry_pos, maze.exit_pos, maze)
print(path)
print("Shortest path length:", len(path))


# Manual walk:
# current_pos = entry_pos
# while True:
#    in_ = input()
#    if in_ == 'w':
#       direction = DIRECTIONS[0]
#    elif in_ == 'd':
#       direction = DIRECTIONS[1]
#    elif in_ == 's':
#       direction = DIRECTIONS[2]
#    elif in_ == 'a':
#       direction = DIRECTIONS[3]

#    next_pos = maze.get_next_pos(current_pos, direction)
#    if next_pos:
#       current_pos = next_pos
   
#    maze.print(current_pos)
