import math
import copy

def get_visible_asteroids(asteroids_map, y, x, print_map=False):
   asteroids = copy.deepcopy(asteroids_map)
   asteroids[y][x] = 'X'
   for i in range(len(asteroids)):
      for j in range(len(asteroids[0])):
         if i == y and x == j:
            continue

         if asteroids[i][j] == '#':
            # distance to the given asteroid:
            dy = y - i
            dx = x - j

            if dy == 0:
               divisor = abs(dx)
            elif dx == 0:
               divisor = abs(dy)
            else: 
               divisor = math.gcd(dy, dx)

            dy /= divisor
            dx /= divisor

            next_i = i+dy
            next_j = j+dx

            if next_i == y and next_j == x:
               continue

             # check if on other side of given asteroid
            def same_side(current_pos, last_pos, asteroid_pos):
               sign = lambda a: (a>0) - (a<0)
               curennt_dist = (asteroid_pos[0] - current_pos[0], asteroid_pos[1] - current_pos[1])
               last_dist = (asteroid_pos[0] - last_pos[0], asteroid_pos[1] - last_pos[1])
               return sign(curennt_dist[0]) == sign(last_dist[0]) and sign(curennt_dist[1]) == sign(last_dist[1])
           

            last_i = i
            last_j = j
            blocked = []
            while same_side((next_i, next_j), (last_i, last_j), (y, x)):
               # check if in sight
               if asteroids[int(next_i)][int(next_j)] != '.':
                  blocked.append( (last_i, last_j) )
                  last_i, last_j = next_i, next_j
               next_i += dy
               next_j += dx

            for a in blocked:
               asteroids[int(a[0])][int(a[1])] = 'B' # asteroid blocked


   visible_asteroids = []
   for i in range(len(asteroids)):
      for j in range(len(asteroids[0])):
         if asteroids[i][j] == '#':
            visible_asteroids.append( (i, j) )
         
   if print_map:
      for row in asteroids:
         print(row)

   return visible_asteroids


def find_optimal_place_for_detector(asteroids):
   results = []
   for i in range(len(asteroids)):
      for j in range(len(asteroids[0])):
         if asteroids[i][j] == '#':
            results.append( (i, j, len(get_visible_asteroids(asteroids, i, j))) )
   return max(results, key=lambda x:x[2])

if __name__ == "__main__":
   asteroids = []
   input_ = input()
   while input_:
      asteroids.append( [i for i in input_] )
      input_ = input()

   print("Maximum visible asteroids:", find_optimal_place_for_detector(asteroids))