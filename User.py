class User:
    user_id = None
    name = None
    username = None
    age = None
    recipes = {}

    def __init__(self, name, username, age = None, Recipe = None):
        self.name = name
        self.username = username
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
                