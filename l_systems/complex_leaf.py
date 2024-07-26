from l_system import L_System

class ComplexLeaf(L_System):
    axiom = 'a'
    rules = {
        'F': '>F<',
        'a': 'F[+x]Fb',
        'b': 'F[-y]Fa',
        'x': 'a',
        'y': 'b'
        }
    


if __name__ == '__main__':
    leaf = ComplexLeaf()

    for _ in range(10):
        print(leaf)
        leaf.generate()