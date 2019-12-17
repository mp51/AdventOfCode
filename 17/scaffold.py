import int_comp as ic
from functools import reduce

def print_image(img):
   for line in img:
      print(''.join(line))

def find_intersections(img):
   intersections = []
   for i in range(1, len(image)-1):
      for j in range(1, len(image[0])-1):
         if image[i][j] == '#' and image[i-1][j] == '#' and image [i+1][j] == '#' \
               and image[i][j+1] == '#' and image[i][j-1] == '#':
            intersections.append( (i,j) )
   return intersections

def calc_alignment_parameters_sum(intersections):
   result = 0
   for i in intersections:
      result += i[0] * i[1]
   return result

program = [int(i) for i in input().split(',')]
print(program)
comp = ic.Computer(program)
output, state = comp.compute_result()
# print(output, state)

output = [chr(n) for n in output]
image_str = ''.join(output)
image = [[i for i in line] for line in image_str.split()]
print_image(image)

intersections = find_intersections(image)
result = calc_alignment_parameters_sum(intersections)
print(result)