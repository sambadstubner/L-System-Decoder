from l_system import L_System

class Algae(L_System):
    axiom = 'A'
    rules = {
        'A': 'AB',
        'B': 'A'
        }
    


if __name__ == '__main__':
    algae = Algae()

    for _ in range(5):
        print(algae)
        algae.generate()