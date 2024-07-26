from typing import Self

class L_System:
    axiom: str = ""
    population: str = ""
    rules: dict = {}


    def __init__(self) -> None:
        self.population = self.axiom

    def __str__(self) -> str:
        return self.population
    
    @classmethod
    def from_params(cls, axiom: str, rules: dict) -> Self:
        l_system = L_System()
        l_system.axiom = axiom
        l_system.rules = rules
        l_system.population = axiom
        return l_system 
    
    def generate(self) -> None:
        new_population = ""
        for i in self.population:
            if i in self.rules.keys():
                new_population += self.rules[i]
            else:
                new_population += i
        
        self.population = new_population
