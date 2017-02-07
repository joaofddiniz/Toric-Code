# Toric Code
import random


L = 3
p = 0.9

def random_error(p):
    return 1 if random.random() < p else 0


def sindrome(lattice_horizontal, lattice_vertical):
    sindrome_Z = [[0 for n in range(L)] for n in range(L)]
    sindrome_X = [[0 for n in range(L)] for n in range(L)]
    for n in range(L):
    	for m in range(L):
	    sindrome_Z[n][m] = lattice_horizontal[n][m]['X'] + lattice_horizontal[(n+1)%L][m]['X'] 
	    sindrome_Z[n][m] += lattice_vertical[n][m]['X'] + lattice_vertical[n][(m+1)%L]['X']
            sindrome_Z[n][m] %= 2
	    sindrome_X[n][m] = lattice_horizontal[n][m]['Z'] + lattice_horizontal[n][(m-1)%L]['Z'] 
	    sindrome_X[n][m] += lattice_vertical[n][m]['Z'] + lattice_vertical[(n-1)%L][m]['Z']
            sindrome_X[n][m] %= 2
    return sindrome_Z, sindrome_X



#def draw_lattice(lattice_horizontal, lattice_vertical, sindrome_Z, sindrome_X):
#    for n in range(L):
#        for m in range(L):
#	    print sindrome_X[n][m],
#	    print '-' * 4,
#	    print lattice_horizontal[n][m]['X'], lattice_horizontal[n][m]['Z'],
#	    print '-' * 4,
#       print sindrome_X[n][0]
#        for m in range (L):
#	    print '|', ' ' * 13,
#        print '|'
#        for m in range(L):
#	    print lattice_vertical[n][m]['X'], lattice_vertical[n][m]['Z'],
#	    print ' ' * 3,
#	    print sindrome_Z[n][m],
#	    print ' ' * 5,
#        print lattice_vertical[n][0]['X'], lattice_vertical[n][0]['Z']
#        for m in range (L):
#	    print '|', ' ' * 13,
#        print '|'
#        if n == L-1:
#	    for m in range(L):
#	        print sindrome_X[0][m],
#	        print '-' * 4,
#	        print lattice_horizontal[0][m]['X'], lattice_horizontal[0][m]['Z'],
#	        print '-' * 4,
#	    print sindrome_X[0][0]




def draw_lattice(lattice_horizontal, lattice_vertical, sindrome_Z, sindrome_X):
    for n in range(L):
        for m in range(L):
	    print '{0} ---- {1} {2} ----'.format(sindrome_X[n][m], lattice_horizontal[n][m]['X'], lattice_horizontal[n][m]['Z']),
        print sindrome_X[n][0]
        for m in range (L):
	    print '|', ' ' * 13,
        print '|'
        for m in range(L):
	    print '{0} {1}     {2}      '.format(lattice_vertical[n][m]['X'], lattice_vertical[n][m]['Z'], sindrome_Z[n][m]),
        print lattice_vertical[n][0]['X'], lattice_vertical[n][0]['Z']
        for m in range (L):
	    print '|', ' ' * 13,
        print '|'
    for m in range(L):
	print '{0} ---- {1} {2} ----'.format(sindrome_X[0][m], lattice_horizontal[0][m]['X'], lattice_horizontal[0][m]['Z']),
    print sindrome_X[0][0]



def draw_lattice(lattice_horizontal, lattice_vertical, sindrome_Z, sindrome_X):
    for n in range(L):
	print ' ' * 2,
        for m in range(L):
	    print '{0} ---- X:{1} Z:{2} ----'.format(sindrome_X[n][m], lattice_horizontal[n][m]['X'], lattice_horizontal[n][m]['Z']),
        print sindrome_X[n][0]
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
        for m in range(L):
	    print 'X:{0} Z:{1}      {2}     '.format(lattice_vertical[n][m]['X'], lattice_vertical[n][m]['Z'], sindrome_Z[n][m]),
        print 'X:{0} Z:{1}'.format(lattice_vertical[n][0]['X'], lattice_vertical[n][0]['Z'])
        for m in range (L):
	    print '   |', ' ' * 14,
        print '   |'
    print ' ' * 2,
    for m in range(L):
	print '{0} ---- X:{1} Z:{2} ----'.format(sindrome_X[0][m], lattice_horizontal[0][m]['X'], lattice_horizontal[0][m]['Z']),
    print sindrome_X[0][0]




#lattice = [[(0,0) for n in range(L)] for n in range(L)]
#lattice = [[{'X':0, 'Z':0} for n in range(L)] for n in range(L)]


#for n in range(L):
#    for m in range(L):
#        lattice[n][m]['X'] = random_error(p)
#        lattice[n][m]['Z'] = random_error(p)



lattice_horizontal = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]
lattice_vertical = [[{'X':random_error(p), 'Z':random_error(p)} for n in range(L)] for n in range(L)]


#sindrome_Z = [[0 for n in range(L)] for n in range(L)]
#sindrome_X = [[0 for n in range(L)] for n in range(L)]

#for n in range(L):
#    for m in range(L):
#	sindrome_Z[n][m] = lattice_horizontal[n][m]['X'] + lattice_horizontal[(n+1)%L][m]['X'] 
#	sindrome_Z[n][m] += lattice_vertical[n][m]['X'] + lattice_vertical[n][(m+1)%L]['X']
#       sindrome_Z[n][m] %= 2
#	sindrome_X[n][m] = lattice_horizontal[n][m]['Z'] + lattice_horizontal[n][(m-1)%L]['Z'] 
#	sindrome_X[n][m] += lattice_vertical[n][m]['Z'] + lattice_vertical[(n-1)%L][m]['Z']
#       sindrome_X[n][m] %= 2



sindrome_Z, sindrome_X = sindrome(lattice_horizontal, lattice_vertical)

draw_lattice(lattice_horizontal, lattice_vertical, sindrome_Z, sindrome_X)



