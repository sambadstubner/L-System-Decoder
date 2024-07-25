from l_system import L_System

class Plant(L_System):
    axiom = '0'
    rules = {
        '1': '11',
        '0': '1[0]0'
        }
    


if __name__ == '__main__':
    plant = Plant()

    for _ in range(5):
        print(plant)
        plant.generate()