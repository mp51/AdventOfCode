ORIGIN_POINT = (0,0)

def manhattan_distance(point1, point2):
   return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

class Direction:
   def __init__(self, init_str):
      self.direction = init_str[0]
      self.distance = int(init_str[1:])

   def __repr__(self):
      return self.direction + str(self.distance)

   def get_points(self, starting_point):
      if self.direction == "R":
         return [(starting_point[0] + i, starting_point[1]) for i in range(1, self.distance+1)]
      elif self.direction == "L":
         return [(starting_point[0] - i, starting_point[1]) for i in range(1, self.distance+1)]
      elif self.direction == "U":
         return [(starting_point[0], starting_point[1] + i) for i in range(1, self.distance+1)]
      elif self.direction == "D":
         return [(starting_point[0], starting_point[1] - i) for i in range(1, self.distance+1)]


class Wire:
   def __init__(self, directions):
      self.points = [ORIGIN_POINT]
      for direction in directions:
         self.points.extend(direction.get_points(self.points[-1]))
      # remove origin point so it's not counted as intersection
      del self.points[0]
      self.sort_points_by_dist_to_origin()
               
   def __repr__(self):
      return str(self.points)

   def sort_points_by_dist_to_origin(self):
      self.sorted_points = sorted(self.points, key=lambda p: manhattan_distance(ORIGIN_POINT, p))

   def get_intersection_closest_to_origin(self, other_wire):
      for p in self.sorted_points:
         if p in other_wire.sorted_points:
            print("Intersection:", p)
            return p
      return None



# Get input 
wires = []
while True:
   input_wire = input()
   if input_wire:
      wires.append( Wire( [Direction(i) for i in input_wire.split(',')] ) )
   else:
      break

# Print wires
for i, wire in enumerate(wires): print(f"Wire {i}:", wire)

intersections = []
for i, wire in enumerate(wires):
   for j in range(i+1, len(wires)):
      p = wire.get_intersection_closest_to_origin(wires[j])
      if p:
         intersections.append(p)

intersections = sorted(intersections, key=lambda p: manhattan_distance(ORIGIN_POINT, p))
dist = manhattan_distance(ORIGIN_POINT, intersections[0])
print("Intersection closest to the origin:", intersections[0], "Distance:", dist)

