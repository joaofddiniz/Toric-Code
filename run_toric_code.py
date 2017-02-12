# Joao Fernando Doriguello Diniz
# 10/02/2017

import random
import toric_code as toric


#L = lattice size; p = error probability
L = int(raw_input('Enter lattice size L: '))
p = float(raw_input('Enter error probability p: '))


lattice = toric.create_lattice(L, p)
syndrome = toric.syndrome(L, lattice)


answer = raw_input('Show full lattice? [y]\n')
if answer in ('y', 'yes'):
    toric.draw_lattice(L, lattice, syndrome)


answer = raw_input('Show reduced lattice? [y]\n')
if answer in ('y', 'yes'):
    toric.draw_lattice_reduced(L, lattice, syndrome)



