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

   def get_connected_nodes(self):
      nodes = [*self.orbiting_objects]
      if self.center:
         nodes.append(self.center)
      return nodes

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

      orbits[inner].add_orbiting_object( orbits[outer] )
      orbits[outer].set_center_object( orbits[inner] )

   else:
      break


def bfs_search(source, destination):
   visited = set()
   next_to_visit = [source]
   traceback = {}
   while next_to_visit:
      current_node = next_to_visit.pop(0)
      if current_node == destination:
         return traceback
      
      nodes = current_node.get_connected_nodes()
      for node in nodes:
         if node not in visited:
            visited.add(node)
            traceback[node] = current_node
            next_to_visit.append(node)
   
   return None

def find_path_bfs(source, destination):
   traceback = bfs_search(source, destination)
   path = []
   if traceback:
      current_node = destination
      while current_node != source:
         path.append(current_node)
         current_node = traceback[current_node]

   return path


you =  orbits["YOU"]
san = orbits["SAN"]

# Search path from YOU to SAN
path = find_path_bfs(you, san)
print(path)
steps = len(path) - 2 # subtract 2 to exclude path steps to YOU and SAN directly
print(steps)
