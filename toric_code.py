# Joao Fernando Doriguello Diniz
# 07/02/2017
# Implementation of the toric code with independent X and Z errors

import random

def random_error(p):
    return 1 if random.random() < p else 0


def syndrome(lattice):
    # Calculates the syndrome of the lattice and returns a dictionary with the X and Z syndromes
    syndrome_Z = [[0 for n in range(L)] for n in range(L)]
    syndrome_X = [[0 for n in range(L)] for n in range(L)]
    for n in range(L):
    	for m in range(L):
	    syndrome_Z[n][m] = lattice['H'][n][m]['X'] + lattice['H'][(n+1)%L][m]['X'] 
	    syndrome_Z[n][m] += lattice['V'][n][m]['X'] + lattice['V'][n][(m+1)%L]['X']
            syndrome_Z[n][m] %= 2
	    syndrome_X[n][m] = lattice['H'][n][m]['Z'] + lattice['H'][n][(m-1)%L]['Z'] 
	    syndrome_X[n][m] += lattice['V'][n][m]['Z'] + lattice['V'][(n-1)%L][m]['Z']
            syndrome_X[n][m] %= 2
    return {'X': syndrome_X, 'Z': syndrome_Z}


def draw_lattice(lattice, syndrome):
    # Draws the full lattice with the X and Z syndromes and qubits represented by X: X error, Z: Z error
    print '\nFull lattice:'
    print 'qubit = X: X error, Z: Z error\n'
    for n in range(L):
	print ' ' * 2,
        for m in range(L):
	    print '{0} ---- X:{1},Z:{2} ----'.format(syndrome['X'][n][m], lattice['H'][n][m]['X'], lattice['H'][n][m]['Z']),
        print syndrome['X'][n][0]
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
        for m in range(L):
	    print 'X:{0},Z:{1}      {2}     '.format(lattice['V'][n][m]['X'], lattice['V'][n][m]['Z'], syndrome['Z'][n][m]),
        print 'X:{0},Z:{1}'.format(lattice['V'][n][0]['X'], lattice['V'][n][0]['Z'])
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
    print ' ' * 2,
    for m in range(L):
	print '{0} ---- X:{1},Z:{2} ----'.format(syndrome['X'][0][m], lattice['H'][0][m]['X'], lattice['H'][0][m]['Z']),
    print syndrome['X'][0][0]
    print '\n'



def draw_lattice_reduced(lattice, syndrome):
    # Draws a reduced version of the lattice with the X and Z syndromes and the qubits represented by (X error, Z error)
    print '\nReduced lattice:'
    print 'qubit = (X error, Z error)\n'
    for n in range(L):
	print ' ',
        for m in range(L):
	    print '{0} -- ({1},{2}) --'.format(syndrome['X'][n][m], lattice['H'][n][m]['X'], lattice['H'][n][m]['Z']),
        print syndrome['X'][n][0]
        for m in range (L):
	    print '  |', ' ' * 9,
        print '  |'
        for m in range(L):
	    print '({0},{1})    {2}   '.format(lattice['V'][n][m]['X'], lattice['V'][n][m]['Z'], syndrome['Z'][n][m]),
        print '({0} {1})'.format(lattice['V'][n][0]['X'], lattice['V'][n][0]['Z'])
        for m in range (L):
	    print '  |', ' ' * 9,
        print '  |'
    print ' ',
    for m in range(L):
	print '{0} -- ({1},{2}) --'.format(syndrome['X'][0][m], lattice['H'][0][m]['X'], lattice['H'][0][m]['Z']),
    print syndrome['X'][0][0]
    print '\n'




#L = lattice size; p = error probability
L = int(raw_input('Enter lattice size L: '))
p = float(raw_input('Enter error probability p: '))


# The lattice can be seen as formed by two LxL separate lattices (each with LxL qubits): a vertical one, where the qubits are connected mainly vertically, and a horizontal one, where the qubits are connected mainly horizontally
lattice_horizontal = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]
lattice_vertical = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]
lattice = {'H': lattice_horizontal, 'V': lattice_vertical}


syndrome = syndrome(lattice)


answer = raw_input('Show full lattice? [y]\n')
if answer in ('y', 'yes'):
    draw_lattice(lattice, syndrome)


answer = raw_input('Show reduced lattice? [y]\n')
if answer in ('y', 'yes'):
    draw_lattice_reduced(lattice, syndrome)


