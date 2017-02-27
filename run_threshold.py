#Threshold plot for 3D lattice (faulty measurements)

import numpy as np
import matplotlib.pyplot as plt
import toric_code as toric
#import toric_code_fast as toric

precision = 10000
t = 5

p = np.linspace(0.04, 0.06, 20)
L = [4, 8, 12, 16]

plot = []

for L0 in L:
    flag = []

    for p0 in p:
        success = 0

        for n in range(precision):
            code = toric.toric_code_3D(L0, p0, p0, t)
	    code.create_lattice()
	    code.get_syndrome()
	    code.correct_syndrome()
            success += code.verify_logical_error('Z')

        flag += [float(success)/precision]

    plot += [flag]


#plt.plot(p, plot[0])

fig, ax = plt.subplots()
ax.plot(p, plot[0], 'ro', label='L = 4')
ax.plot(p, plot[1], 'bo', label='L = 8')
ax.plot(p, plot[2], 'go', label='L = 12')
ax.plot(p, plot[3], 'yo', label='L = 16')
legend = ax.legend(loc='upper center', shadow=True)	
ax.set_xlabel('p (%)')
ax.set_ylabel('Decoding success rate (%)')
plt.show()
