from l_system import L_System

class Bush3(L_System):
    axiom = 'F'
    rules = {
        'F': 'F[+FF][-FF]F[-F][+F]F'
    }

if __name__ == '__main__':
    l_system = Bush3()

    for _ in range(5):
        print(l_system)
        l_system.generate()