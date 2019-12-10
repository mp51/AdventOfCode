import asteroids as ast
import math
from time import sleep

def print_asteroids(asteroids_map):
   for row in asteroids_map:
      print(''.join(row))
   print()

def shift_angle(angle_rad):
   angle_rad += math.pi/2
   while angle_rad > 2*math.pi:
      angle_rad -= 2*math.pi
   while angle_rad <= 0:
      angle_rad += 2*math.pi
   return angle_rad

class LaserShooter:
   def __init__(self, y, x, asteroids_map):
      # laser location
      self.y = y
      self.x = x 
      self.asteroids = asteroids_map
      self.asteroids[y][x] = 'X'
      self.shot_count = 0

   def start_shooting(self):
      while True:
         visible_asteroids = ast.get_visible_asteroids(self.asteroids, self.y, self.x)

         # sort asteroids locations by angle
         def get_angle(p):
            angle = shift_angle(math.atan2(p[0]-self.y, self.x - p[1]))
            return angle

         visible_asteroids = sorted(visible_asteroids, key=get_angle, reverse=True)

         if len(visible_asteroids) == 0:
            break

         for asteroid in visible_asteroids:
            self.shoot_asteroid(asteroid)
            print(f"{self.shot_count}th asteroid shot at:", asteroid)
            if self.shot_count == 200:
               print("200th asteroid shot at:", asteroid)
               return asteroid
      
   def shoot_asteroid(self, asteroid_loc):
      self.asteroids[asteroid_loc[0]][asteroid_loc[1]] = '*'
      self.shot_count += 1
      print_asteroids(self.asteroids)
      self.asteroids[asteroid_loc[0]][asteroid_loc[1]] = '.'
      # sleep(.1)
      
   

# get input map
asteroids_map = []
input_ = input()
while input_:
   asteroids_map.append( [i for i in input_] )
   input_ = input()

# get location of the laser
y, x, _ = ast.find_optimal_place_for_detector(asteroids_map)
print("Laser location:", y, x)


laser = LaserShooter(y, x, asteroids_map)
laser.start_shooting()

