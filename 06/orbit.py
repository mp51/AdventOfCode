class OrbitNode:
   def __init__(self, name):
      self.name = name
      self.orbiting_objects = []
      self.center = None

   def set_center_object(self, center):
      self.center = center

   def add_orbiting_object(self, orbiting_obj):
      self.orbiting_objects.append(orbiting_obj)

   def get_indirect_orbits(self):
      if self.center:
         return 1 + self.center.get_indirect_orbits()
      else: 
         return 0

   def __repr__(self):
      return f'{self.name}'


# Get input 
orbit_pairs = []
orbits = dict()
while True:
   pair = input()
   if pair:
      inner, outer = pair.split(')')

      if inner not in orbits.keys():
         orbits[inner] = OrbitNode(inner)
      if outer not in orbits.keys():
         orbits[outer] = OrbitNode(outer)

      # orbits[inner].add_orbiting_object( orbits[outer] )
      orbits[outer].set_center_object( orbits[inner] )

   else:
      break


total_orbits = 0

for obj in orbits.values():
   indirect_orbits = obj.get_indirect_orbits()
   print(obj, indirect_orbits)
   total_orbits += indirect_orbits

print(total_orbits)


