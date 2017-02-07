# João Fernando Doriguello Diniz
# 07/02/2017
# Implementation of the toric code with independent X and Z errors

import random

def random_error(p):
    return 1 if random.random() < p else 0


def sindrome(lattice):
    # Calculates the sindrome of the lattice and returns a dictionary with the X and Z sindromes
    sindrome_Z = [[0 for n in range(L)] for n in range(L)]
    sindrome_X = [[0 for n in range(L)] for n in range(L)]
    for n in range(L):
    	for m in range(L):
	    sindrome_Z[n][m] = lattice['H'][n][m]['X'] + lattice['H'][(n+1)%L][m]['X'] 
	    sindrome_Z[n][m] += lattice['V'][n][m]['X'] + lattice['V'][n][(m+1)%L]['X']
            sindrome_Z[n][m] %= 2
	    sindrome_X[n][m] = lattice['H'][n][m]['Z'] + lattice['H'][n][(m-1)%L]['Z'] 
	    sindrome_X[n][m] += lattice['V'][n][m]['Z'] + lattice['V'][(n-1)%L][m]['Z']
            sindrome_X[n][m] %= 2
    return {'X': sindrome_X, 'Z': sindrome_Z}


def draw_lattice(lattice, sindrome):
    # Draws the full lattice with the X and Z sindromes and qubits represented by X: X error, Z: Z error
    print '\nFull lattice:'
    print 'qubit = X: X error, Z: Z error\n'
    for n in range(L):
	print ' ' * 2,
        for m in range(L):
	    print '{0} ---- X:{1},Z:{2} ----'.format(sindrome['X'][n][m], lattice['H'][n][m]['X'], lattice['H'][n][m]['Z']),
        print sindrome['X'][n][0]
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
        for m in range(L):
	    print 'X:{0} Z:{1}      {2}     '.format(lattice['V'][n][m]['X'], lattice['V'][n][m]['Z'], sindrome['Z'][n][m]),
        print 'X:{0},Z:{1}'.format(lattice['V'][n][0]['X'], lattice['V'][n][0]['Z'])
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
    print ' ' * 2,
    for m in range(L):
	print '{0} ---- X:{1},Z:{2} ----'.format(sindrome['X'][0][m], lattice['H'][0][m]['X'], lattice['H'][0][m]['Z']),
    print sindrome['X'][0][0]
    print '\n'



def draw_lattice_reduced(lattice, sindrome):
    # Draws a reduced version of the lattice with the X and Z sindromes and the qubits represented by (X error, Z error)
    print '\nReduced lattice:'
    print 'qubit = (X error, Z error)\n'
    for n in range(L):
	print ' ',
        for m in range(L):
	    print '{0} -- ({1},{2}) --'.format(sindrome['X'][n][m], lattice['H'][n][m]['X'], lattice['H'][n][m]['Z']),
        print sindrome['X'][n][0]
        for m in range (L):
	    print '  |', ' ' * 9,
        print '  |'
        for m in range(L):
	    print '({0},{1})    {2}   '.format(lattice['V'][n][m]['X'], lattice['V'][n][m]['Z'], sindrome['Z'][n][m]),
        print '({0} {1})'.format(lattice['V'][n][0]['X'], lattice['V'][n][0]['Z'])
        for m in range (L):
	    print '  |', ' ' * 9,
        print '  |'
    print ' ',
    for m in range(L):
	print '{0} -- ({1},{2}) --'.format(sindrome['X'][0][m], lattice['H'][0][m]['X'], lattice['H'][0][m]['Z']),
    print sindrome['X'][0][0]
    print '\n'




#L = lattice size; p = error probability
 
L = int(raw_input('Enter lattice size L: '))
p = float(raw_input('Enter error probability p: '))

# The lattice can be seen as formed by two LxL separate lattices (each with LxL qubits): a vertical one, 
# where the qubits are connected mainly vertically, and a horizontal one, where the qubits are connected mainly horizontally
lattice_horizontal = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]
lattice_vertical = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]
lattice = {'H': lattice_horizontal, 'V': lattice_vertical}

sindrome = sindrome(lattice)


answer = raw_input('Show full lattice? [y]\n')
if answer in ('y', 'yes'):
    draw_lattice(lattice, sindrome)


answer = raw_input('Show reduced lattice? [y]\n')
if answer in ('y', 'yes'):
    draw_lattice_reduced(lattice, sindrome)



