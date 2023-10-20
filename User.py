class User:
    user_id = None
    name = None
    email = None
    age = None
    recipes = {}

    def __init__(self, user_id, name, email, age, recipes):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.recipes = recipes
