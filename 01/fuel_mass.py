def calc_fuel(mass):
   return mass//3 - 2

def calc_fuel_for_module(mass):
   fuel = calc_fuel(mass)
   total_fuel = 0
   while fuel > 0:
      print(fuel)
      total_fuel += fuel
      mass = fuel
      fuel = calc_fuel(mass)

   return total_fuel

mass = 0
while True:
   module_mass = input()
   if module_mass:
      mass += calc_fuel_for_module(int(module_mass))
   else:
      break

print("Result:", mass)