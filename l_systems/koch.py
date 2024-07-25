from l_system import L_System

class Koch(L_System):
    axiom = 'F'
    rules = {
        'F': 'F+F-F-F+F'
        }
    


if __name__ == '__main__':
    koch = Koch()

    for _ in range(5):
        print(koch)
        koch.generate()