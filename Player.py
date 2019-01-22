class Player:
    def __init__(self, name, positions, price, proj_score):
        self.name = name
        self.positions = positions
        self.price = price
        self.proj_score = proj_score
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_positions(self):
        return self.positions
    def set_positions(self, positions):
        self.positions = positions
    def get_price(self):
        return self.price
    def set_price(self, price):
        self.price = price
    def get_proj_score(self):
        return self.proj_score
    def set_proj_score(self, proj_score):
        self.proj_score = proj_score