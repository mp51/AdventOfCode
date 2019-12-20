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

    def find_recipe_for(self, prod_name):
        for recipe in self:
            if recipe.product.name == prod_name:
                return recipe

    def calculate_ores_for(self, prod_name):
        prod_rec = recipes.find_recipe_for(prod_name)

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

ores = recipes.calculate_ores_for("FUEL")
print(ores)