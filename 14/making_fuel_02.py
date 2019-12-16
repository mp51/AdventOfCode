from collections import namedtuple

Item = namedtuple("Item", "name quantity")


class Recipe:
    def __init__(self, ingredients, prod):
        self.ingredients = ingredients
        self.product = prod

    def __str__(self):
        return f'{self.ingredients} => {self.product}'

class RecipesList(list):
    def __init__(self):
        self.spare_ingredients = dict()
        self.available_ores = 0

    def find_recipe_for(self, prod_name):
        for recipe in self:
            if recipe.product.name == prod_name:
                return recipe

    def calculate_ores_for(self, prod_name):
        prod_rec = self.find_recipe_for(prod_name)

        ores_needed = 0
        for ing in prod_rec.ingredients:
            if ing.name == "ORE":
                ores_needed += ing.quantity
            else:
                quantity_left = ing.quantity

                if ing.name in self.spare_ingredients.keys():
                    print(ing.name, self.spare_ingredients[ing.name])
                    quantity_left -= self.spare_ingredients[ing.name]
                    self.spare_ingredients[ing.name] -= ing.quantity - quantity_left

                while quantity_left > 0:
                    ores, q = self.calculate_ores_for(ing.name)
                    quantity_left -= q
                    ores_needed += ores

                if quantity_left < 0:
                    if ing.name in self.spare_ingredients.keys():
                        self.spare_ingredients[ing.name] += abs(quantity_left)
                    else:
                        self.spare_ingredients[ing.name] = abs(quantity_left)

        print(prod_rec.product.quantity, prod_name, ores_needed)
        return ores_needed, prod_rec.product.quantity


    def recycle_to_ore(self, prod_name):
        ores = 0
        rec = self.find_recipe_for(prod_name)

        for ing in rec.ingredients:
            if ing.name == "ORE":
                ores += ing.quantity
            else:
                ores += ing.quantity * self.recycle_to_ore(ing.name)

        return ores    

    def recycle_spare_ingredients(self):
        for name in self.spare_ingredients.keys():
            rec = self.find_recipe_for(name)
            q = rec.product.quantity
            can_be_recycled = self.spare_ingredients[name] // q
            self.spare_ingredients[name] = self.spare_ingredients[name] % q
            self.available_ores += can_be_recycled * self.recycle_to_ore(name)

    def make_product(self, prod_name):
        prod_rec = self.find_recipe_for(prod_name)
        # print("Trying to make", prod_name)

        produced = True
        if prod_name in self.spare_ingredients.keys() and self.spare_ingredients[prod_name] > 0:
            q = self.spare_ingredients[prod_name]
            self.spare_ingredients[prod_name] = 0
            return produced, q

        for ing in prod_rec.ingredients:
            if ing.name == "ORE":
                if ing.quantity <= self.available_ores:
                    self.available_ores -= ing.quantity
                    # print("Producing", prod_name, "for", ing.quantity, "ores")
                else:
                    print(self.available_ores, "ores is not enough to produce", prod_name)
                    produced = False
                    break
            else:
                quantity_left = ing.quantity
                
                ores_needed, q = self.calculate_ores_for(ing.name)
                while quantity_left > 0:
                    o_, q_ = self.calculate_ores_for(ing.name)
                    ores_needed += o_
                    quantity_left -= q_

                if ores_needed < self.available_ores:
                    self.available_ores -= ores_needed
                else:
                    produced = False
                    break

                if quantity_left < 0:
                    if ing.name in self.spare_ingredients.keys():
                        self.spare_ingredients[ing.name] += abs(quantity_left)
                    else:
                        self.spare_ingredients[ing.name] = abs(quantity_left)

                # quantity_left = ing.quantity
                # if ing.name in self.spare_ingredients.keys():
                #     quantity_left -= self.spare_ingredients[ing.name]
                #     self.spare_ingredients[ing.name] -= (ing.quantity - quantity_left)

                # while quantity_left > 0:
                #     success, q = self.make_product(ing.name)
                #     if success:
                #         quantity_left -= q
                #     else:
                #         produced = False
                #         break

                # if quantity_left < 0:
                #     if ing.name in self.spare_ingredients.keys():
                #         self.spare_ingredients[ing.name] += abs(quantity_left)
                #     else:
                #         self.spare_ingredients[ing.name] = abs(quantity_left)
                
                # if not produced:
                #     break
                
        # print(prod_name, "produced?", produced)
        return produced, prod_rec.product.quantity



    def print(self):
        for r in self:
            print(r)

recipes = RecipesList()

while True:
    recipe_str = input()
    if not recipe_str:
        break

    ingredients, prod = recipe_str.split('=>')
    # print(recipe_str)
    # print(ingredients, product)
    ingredients_list = ingredients.split(',')
    items = [Item(i.split()[1], int(i.split()[0])) for i in ingredients_list]

    prod = Item(prod.split()[1], int(prod.split()[0]))
    recipes.append(Recipe(items, prod))

recipes.print()

ores_for_1_fuel, _ = recipes.calculate_ores_for("FUEL")
print("Ores for 1 fuel unit:", ores_for_1_fuel)


recipes.available_ores = 1_000_000_000_000
fuel_units = 0

while True:
    fuel_units_produced = recipes.available_ores // ores_for_1_fuel
    fuel_units += fuel_units_produced
    recipes.available_ores = recipes.available_ores % ores_for_1_fuel

    for name in recipes.spare_ingredients.keys():
        recipes.spare_ingredients[name] *= fuel_units_produced
    
    print("Fuel units:", fuel_units, "Available ores:", recipes.available_ores)
    recipes.recycle_spare_ingredients()
    print("Available ores after recycling:", recipes.available_ores)

    if recipes.available_ores < ores_for_1_fuel:
        break


print("Ingredients left:")
for n, q in recipes.spare_ingredients.items():
    print(q, n)


# while True:
#     success, _ = recipes.make_product("FUEL")
#     if success:
#         fuel_units += 1
#     else:
#         break

# print(fuel_units)
# print("Ores left:", recipes.available_ores)
