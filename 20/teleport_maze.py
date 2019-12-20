import string

DIRECTIONS = [(-1,0), (0,1), (1, 0), (0, -1)]


# portal_name : [pos1, pos2]
# e.g.:
# "BC" : [(2, 3), (5, 6)]
PORTALS = {}
PORTAL_LETTERS = string.ascii_uppercase
PORTAL_LETTERS = PORTAL_LETTERS.strip('AZ')
for i in range(len(PORTAL_LETTERS)//2):
   PORTALS[PORTAL_LETTERS[2*i]+PORTAL_LETTERS[2*i + 1]] = []

print(PORTALS)

def explore_portals(maze):
   for i in range(len(maze)):
      for j in range(len(maze[0])):
         if maze[i][j] in PORTAL_LETTERS:
            # get full portal name (2 letters)
            portal_name = None
            for name in PORTALS.keys():
               if maze[i][j] in name:
                  portal_name = name
                  break
            
            # find the second letter pos
            letter_to_find = portal_name[0] if maze[i][j] != portal_name[0] else portal_name[1]

            print("Portal name:", portal_name)
            direction = None
            for d in DIRECTIONS:
               pos = (i+d[0], j+d[1])
               if maze[pos[0]][pos[1]] == letter_to_find:
                  direction = d
                  break

            if maze[i-direction[0]][j-direction[1]] == '.':
               new_pos = (i-direction[0],j-direction[1])
            elif maze[pos[0]+direction[0]][pos[1]+direction[1]] == '.':
               new_pos = (pos[0]+d[0], pos[1]+d[1])

            if new_pos not in PORTALS[portal_name]:
               PORTALS[portal_name].append(new_pos)


class Maze(list):
   def get_next_pos(self, pos, direction):
      new_pos = (pos[0]+direction[0], pos[1]+direction[1])
      next_tile = self[new_pos[0]][new_pos[1]]
      print(next_tile)
      if next_tile == '#':
         return None
      if next_tile == '.':
         return new_pos
      if next_tile in PORTAL_LETTERS:
         for portal_name in PORTALS.keys():
            if next_tile in portal_name:
               positions = PORTALS[portal_name]
               print(portal_name)
               return positions[0] if positions[0] != pos else positions[1]

   def print(self, current_pos):
      for i, row in enumerate(self):  
         for j, val in enumerate(row):
            if current_pos[0] == i and j == current_pos[1]:
               val = '@'
            print(val, end='')
         print()

board = Maze()

while True:
   row = input()
   if not row:
      break
   board.append(row)

# print board

explore_portals(board)
print(PORTALS)

current_pos = (2,9)
while True:
   in_ = input()
   if in_ == 'w':
      direction = DIRECTIONS[0]
   elif in_ == 'd':
      direction = DIRECTIONS[1]
   elif in_ == 's':
      direction = DIRECTIONS[2]
   elif in_ == 'a':
      direction = DIRECTIONS[3]

   next_pos = board.get_next_pos(current_pos, direction)
   if next_pos:
      current_pos = next_pos
   
   board.print(current_pos)
