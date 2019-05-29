import random

yellow = "YELLOW"
brown = "BROWN"

r = random.Random()

def find_mangos():

    return r.choice([[[r.randint(0, 1000), r.randint(0, 1000), r.choice([yellow, brown])]], []])