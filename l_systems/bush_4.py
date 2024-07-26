from l_system import L_System

class Bush4(L_System):
    axiom = 'VZFFF'
    rules = {
        'V': '[+++W][---W]YV',
        'W': '+X[-W]Z',
        'X': '-W[+X]Z',
        'Y': 'YZ',
        'Z': '[-FFF][+FFF]F'
    }

if __name__ == '__main__':
    l_system = Bush4()

    for _ in range(5):
        print(l_system)
        l_system.generate()