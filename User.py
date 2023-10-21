class User:
    user_id = None
    name = None
    username = None
    password = None
    age = None
    recipes = {}

    def __init__(self, name, username, password, age = None, Recipe = None):
        self.name = name
        self.username = username
        self.password = password
        self.age = age
        self.recipes = [Recipe] if Recipe is not None else [] 
    def str(self):
        print(f"{self.name} with {self.username}")
        
    class Recipe:
        name = None
        cookTime = None
        ingredients = []
        
        def __init__(self, name, ingredients, cookTime=None):
            self.name = name
            self.cookTime = cookTime
            ingredients = ingredients
# class Recipe:
#     def __init__(self, name, ingredients, instructions, cook_time=None):
#         self.name = name
#         self.cook_time = cook_time
#         self.ingredients = ingredients
#         self.instructions = instructions 
        
    # def __str__(self):
    #     return f"{self.name}\nIngredients: {self.ingredients}\nInstructions: {self.instructions}\nCooking time: {self.cook_time}"

# class User:
#     def __init__(self, name, username, password, age=None, recipe=None):
#         self.user_id = None
#         self.name = name
#         self.username = username
#         self.password = password
#         self.age = age
#         self.recipes = [recipe] if recipe is not None else []
        
#     def __str__(self):
#         return f"{self.name} with {self.username}"

#     def add_recipe(self, recipe):
#         if isinstance(recipe, Recipe):
#             self.recipes.append(recipe)
#         else:
#             raise ValueError("Invalid recipe object")
                