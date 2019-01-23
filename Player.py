class Player:
    def __init__(self, name, team, price, proj_score):
        self.name = name
        self.team = team
        self.price = price
        self.proj_score = proj_score
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_team(self):
        return self.team
    def set_team(self, team):
        self.team = team
    def get_price(self):
        return self.price
    def set_price(self, price):
        self.price = price
    def get_proj_score(self):
        return self.proj_score
    def set_proj_score(self, proj_score):
        self.proj_score = proj_score