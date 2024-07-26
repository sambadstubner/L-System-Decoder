from l_system import L_System

class Bush(L_System):
    axiom = 'Y'
    rules = {
        'X': 'X[-FFF][+FFF]FX',
        'Y': 'YFX[+Y][-Y]'
    }

if __name__ == '__main__':
    l_system = Bush()

    for _ in range(5):
        print(l_system)
        l_system.generate()