from l_system import L_System

class CantorSet(L_System):
    axiom = 'A'
    rules = {
        'A': 'ABA',
        'B': 'BBB'
        }
    


if __name__ == '__main__':
    cantor = CantorSet()

    for _ in range(5):
        print(cantor)
        cantor.generate()