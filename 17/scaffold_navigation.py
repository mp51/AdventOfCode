import int_comp as ic

def print_image(img):
   for line in img:
      print(''.join(line))


class Navigation:
   directions = ['^', '>', 'v', '<']
   def __init__(self, image):
      self.img = image
      self.robot_pos, self.direction = self.get_robot_pos()
      self.img_height = len(self.img)
      self.img_width = len(self.img[0])

   def find_intersections(self):
      intersections = []
      for i in range(1, len(self.img)-1):
         for j in range(1, len(self.img[0])-1):
            if self.img[i][j] == '#' and self.img[i-1][j] == '#' and self.img [i+1][j] == '#' \
                  and self.img[i][j+1] == '#' and self.img[i][j-1] == '#':
               intersections.append( (i,j) )
      return intersections

   def get_robot_pos(self):
      for i, row in enumerate(self.img):
         direction = next((x for x in row if x != '#' and x != '.'), None)
         if direction:
            j = row.index(direction)
            return (i, j), direction

   def move_robot(self):
      new_pos = None
      if self.direction == '^':
         new_pos = (self.robot_pos[0]-1, self.robot_pos[1])
      elif self.direction == 'v':
         new_pos = (self.robot_pos[0]+1, self.robot_pos[1])
      elif self.direction == '>':
         new_pos = (self.robot_pos[0], self.robot_pos[1]+1)
      elif self.direction == '<':
         new_pos = (self.robot_pos[0], self.robot_pos[1]-1)
      self.robot_pos = new_pos
      return self.robot_pos


   def turn_left(self):
      current_dir = Navigation.directions.index(self.direction)
      self.direction = Navigation.directions[current_dir - 1]

   def turn_right(self):
      current_dir = Navigation.directions.index(self.direction)
      idx = current_dir + 1
      if idx > 3:
         idx = 0
      self.direction = Navigation.directions[idx]

   def get_path(self):
      path = [self.robot_pos] # a list of points
      robot_directions = [self.direction] # a list of robot directions

      def check_next_pos():
         if self.direction == '^' and self.robot_pos[0] > 0 and self.img[self.robot_pos[0]-1][self.robot_pos[1]] == '#':
            return True
         elif self.direction == 'v' and self.robot_pos[0] < self.img_height-1 and self.img[self.robot_pos[0]+1][self.robot_pos[1]] == '#':
            return True
         elif self.direction == '>' and self.robot_pos[1] < self.img_width-1 and self.img[self.robot_pos[0]][self.robot_pos[1]+1] == '#':
            return True
         elif self.direction == '<' and self.robot_pos[1] > 0 and self.img[self.robot_pos[0]][self.robot_pos[1]-1] == '#':
            return True
         else:
            return False

      def get_next():
         found_next = True
         if not check_next_pos():
            self.turn_left()
            if not check_next_pos():
               self.turn_right()
               self.turn_right()
               if not check_next_pos():
                  found_next = False
         if found_next:
            path.append(self.move_robot())
            robot_directions.append(self.direction)
         return found_next

      while get_next(): continue
      return path, robot_directions


   def convert_to_nav_function(self, directions):
      function = [] # a list of inputs to the int computer
      forward = 0
      
      for i in range(1, len(directions)):
         if directions[i] == directions[i-1]:
            forward += 1
         else:
            if forward > 0:
               forward += 1
               function.append(forward)
               forward = 0
            if directions[i-1] == '^' and directions[i] == '>' \
               or directions[i-1] == '>' and directions[i] == 'v' \
                  or directions[i-1] == 'v' and directions[i] == '<' \
                     or directions[i-1] == '<' and directions[i] == '^':
               function.append('R')
            else:
               function.append('L')
      if forward > 0:
         function.append(forward)
      return function

         


program = [int(i) for i in input().split(',')]
comp = ic.Computer(program)
output, state = comp.compute_result()

output = [chr(n) for n in output]
image_str = ''.join(output)
image = [[i for i in line] for line in image_str.split()]
print_image(image)

navi = Navigation(image)
paths, directions = navi.get_path()
for p, d in zip(paths, directions):
   print(p, d)

nav_function = navi.convert_to_nav_function(directions)
for nf in nav_function:
   print(nf,end=', ')

# manually divided nav_function into routines:
routines = "A,B,A,C,B,A,C,B,A,C"
A = "L,12,L,12,L,6,L,6"
B = "R,8,R,4,L,12"
C = "L,12,L,6,R,12,R,8"

program[0] = 2
comp.reset_memory(program)

comp.set_string_input(routines)
comp.set_string_input(A)
comp.set_string_input(B)
comp.set_string_input(C)
comp.set_string_input('n')

result, state = comp.compute_result()
print(result, state)