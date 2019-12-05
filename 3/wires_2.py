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

   def get_intersections_and_steps(self, other_wire):
      intersections = []
      for i in range(len(self.points)):
         for j in range(len(other_wire.points)):
            if self.points[i] == other_wire.points[j]:
               steps = i+j + 2 # add two due to removed origin point
               intersections.append((self.points[i], steps)) 
      return intersections


# Get input 
wires = []
while True:
   input_wire = input()
   if input_wire:
      wires.append( Wire( [Direction(i) for i in input_wire.split(',')] ) )
   else:
      break

# Print wires
for i, wire in enumerate(wires): print(f"Wire {i} length:", len(wire.points))

intersections = []
for i, wire in enumerate(wires):
   for j in range(i+1, len(wires)):
      intersections.extend(wire.get_intersections_and_steps(wires[j]))

intersections = sorted(intersections, key=lambda p: p[1]) # sort by step count to the intersection
print("Intersection closest to the origin:", intersections[0][0], "Steps:", intersections[0][1])

