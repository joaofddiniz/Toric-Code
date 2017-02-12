# Decoder

import toric_code as toric
import decoder as decoder


#L = lattice size; p = error probability
L = int(raw_input('Enter lattice size L: '))
p = float(raw_input('Enter error probability p: '))
print '\n'


lattice = toric.create_lattice(L, p)
syndrome = toric.syndrome(L, lattice)

flag = 'l'

while flag in ['l', 'z', 'x', 's', 'p', 'n', 'd']:

    print 'Show complete lattice? [l]'
    print 'Show Z errors? [z]'
    print 'Show X errors? [x]'
    print 'Show star syndromes? [s]'
    print 'Show plaquette syndromes? [p]'
    print 'Decode the lattice? [d]'
    print 'Set new values for L and p? [n]'
    print 'Exit? [exit]'

    flag = raw_input()
    print '\n'

    if flag == 'l':
	toric.draw_lattice_reduced(L, lattice, syndrome)
    elif flag == 'z':
	toric.draw_errors(L, lattice, 'Z')
    elif flag == 'x':
	toric.draw_errors(L, lattice, 'X')
    elif flag == 's':
	toric.draw_syndrome(L, syndrome, 'Z')
    elif flag == 'p':
	toric.draw_syndrome(L, syndrome, 'X')
    elif flag == 'd':
	syndrome_position = decoder.syndrome_position(L, syndrome)
	graph = decoder.get_graph(L, syndrome_position)
	pairs = decoder.get_pairs(syndrome_position, graph)
	lattice = decoder.correct_syndrome(L, lattice, syndrome_position, pairs)
	syndrome = toric.syndrome(L, lattice)
	print 'Solved!'
    elif flag == 'n':
	L = int(raw_input('Enter lattice size L: '))
	p = float(raw_input('Enter error probability p: '))
	lattice = toric.create_lattice(L, p)
	syndrome = toric.syndrome(L, lattice)

    print '\n'


