import copy
import math


class Vector3D:
   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z

   def __repr__(self):
      return f'Vector3D({self.x}, {self.y}, {self.z})'

   def __str__(self):
      return f'<x={self.x}, y={self.y}, z={self.z}>'

   def __eq__(self, other):
      return self.x == other.x and self.y == other.y and self.z == other.z

class Moon:
   def __init__(self, position, velocity):
      self.position = position
      self.velocity = velocity

   def __repr__(self):
      return f'Moon({self.position}, {self.velocity})'

   def __str__(self):
      return f'pos={self.position}, vel={self.velocity}'

   def __eq__(self, other):
      return self.position == other.position and self.velocity == other.velocity

   def get_total_energy(self):
      get_energy = lambda xyz: abs(xyz.x) + abs(xyz.y) + abs(xyz.z)
      return get_energy(self.position) * get_energy(self.velocity)

   def move_step(self):
      self.position.x += self.velocity.x
      self.position.y += self.velocity.y
      self.position.z += self.velocity.z

class NBodySimulation:
   def __init__(self, moons):
      self.moons = moons
      self.initial_moons = copy.deepcopy(moons)

   def start(self, dimension):
      i = 1

      while True:
         i += 1

         # calculate gravity
         for j in range(len(self.moons)):
            for k in range(j+1, len(self.moons)):
               self._calc_gravity(self.moons[j], self.moons[k], dimension)

         # calculate positions
         for moon in self.moons:
            moon.move_step()

         # print results
         # print()
         # print(f"After {i+1} steps:")
         # for moon in moons:
         #    print(moon)
         print(i)

         position_match = True
         if i != 1:
            for idx, moon in enumerate(self.moons):
               if dimension == 'x':
                  if moon.position.x != self.initial_moons[idx].position.x:
                     position_match = False
                     break
               elif dimension == 'y':
                  if moon.position.y != self.initial_moons[idx].position.y:
                     position_match = False
                     break
               elif dimension == 'z':
                  if moon.position.z != self.initial_moons[idx].position.z:
                     position_match = False
                     break
            
            if position_match:
               return i

         

   def get_total_energy(self):
      energy = 0
      for moon in moons:
         energy += moon.get_total_energy()
      return energy

   def _calc_gravity(self, moon1, moon2, dimension):
      def calc_velocity_diff(pos1, pos2):
         if pos1 < pos2:
            return 1
         elif pos1 > pos2:
            return -1
         return 0

      if dimension == 'x':
         diff = calc_velocity_diff(moon1.position.x, moon2.position.x)
         moon1.velocity.x += diff
         moon2.velocity.x -= diff
      elif dimension == 'y':
         diff = calc_velocity_diff(moon1.position.y, moon2.position.y)
         moon1.velocity.y += diff
         moon2.velocity.y -= diff
      elif dimension == 'z':
         diff = calc_velocity_diff(moon1.position.z, moon2.position.z)
         moon1.velocity.z += diff
         moon2.velocity.z -= diff



# parse input
moons = []
input_line = input()
while input_line:

   position = Vector3D(*(int(val.strip(' xyz=')) for val in input_line.strip('<>').split(',')))
   velocity = Vector3D(0, 0, 0)
   moons.append( Moon(position, velocity) )

   input_line = input()

for moon in moons:
   print(moon) 

sim = NBodySimulation(moons)
steps = []
steps.append(sim.start('x'))
steps.append(sim.start('y'))
steps.append(sim.start('z'))

result = abs(steps[0]*steps[1]) // math.gcd(steps[0], steps[1])
result = abs(steps[2]*result) // math.gcd(steps[2], result)

print(f"Initial position reached after steps:", steps, result)