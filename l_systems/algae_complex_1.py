from l_system import L_System

class AlgaeComplex(L_System):
    axiom = 'aF'
    rules = {
        'a': 'FFFFFv[+++h][---q]fb',
        'b': 'FFFFFv[+++h][---q]fc',
        'c': 'FFFFFv[+++fa]fd',
        'd': 'FFFFFv[+++h][---q]fe',
        'e': 'FFFFFv[+++h][---q]fg',
        'g': 'FFFFFv[---fa]fa',
        'h': 'ifFF',
        'i': 'fFFF[--m]j',
        'j': 'fFFF[--n]k',
        'k': 'fFFF[--o]l',
        'l': 'fFFF[--p]',
        'm': 'fFn',
        'n': 'fFo',
        'o': 'fFp',
        'p': 'fF',
        'q': 'rfF',
        'r': 'fFFF[++m]s',
        's': 'fFFF[++n]t',
        't': 'fFFF[++o]u',
        'u': 'fFFF[++p]',
        'v': 'Fv'
    }

if __name__ == '__main__':
    l_system = AlgaeComplex()

    for _ in range(15):
        print(l_system)
        l_system.generate()