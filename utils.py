class Dice:

    def roll(self, value: str):
        count, sides = value.split('d')
        sides = int(sides)
        count = int(count)
        import random
        return sum(random.randint(1, sides) for _ in range(count))
    
