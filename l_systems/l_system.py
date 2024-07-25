class L_System:
    def __init__(self) -> None:
        self.population = self.axiom

    def __str__(self) -> str:
        return self.population
    
    def generate(self) -> None:
        new_population = ""
        for i in self.population:
            if i in self.rules.keys():
                new_population += self.rules[i]
            else:
                new_population += i
        
        self.population = new_population
