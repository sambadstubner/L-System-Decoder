from l_system import L_System

class Leaf(L_System):
    axiom = 'X'
    rules = {
        'X': 'F+[[X]-X]-F[-FX]+X',
        'F': 'FF'
    }

if __name__ == '__main__':
    leaf = Leaf()

    for _ in range(5):
        print(leaf)
        leaf.generate()