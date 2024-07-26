from l_system import L_System

class Bush2(L_System):
    axiom = 'F'
    rules = {
        'F': 'FF+[+F-F-F]-[-F+F+F]'
    }

if __name__ == '__main__':
    l_system = Bush2()

    for _ in range(5):
        print(l_system)
        l_system.generate()