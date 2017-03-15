import random
from blossom5 import pyMatch as pm

class toric_code_2D:

    # 2D version of the toric code - Measurements are perfect

    def __init__(self, L=5, p=0.1):

	''' 
	Parameters:
	    
	L: lattice size
	p: qubit error probability
	'''

	self.size = L
	self.prop = p

	self.lattice = {'H': [] , 'V': []}
	self.syndrome = [[1 for n in range(L)] for n in range(L)]
	self.syndrome_position = []

	self.graph = []
	self.pairs = []



    def random_error(self):
        return -1 if random.random() < self.prop else 1


    def create_lattice(self):

	'''Creates the lattice

	Parameters:

	self.size: lattice size
	self.prop in self.random_error(): qubit error probability	
	----------

	Returns:
	
	self.lattice is updated with values +1 (no error) and -1 (error)
	'''

	for A in ['H', 'V']:	
            self.lattice[A] = [[self.random_error() for n in range(self.size)] for n in range(self.size)]



    def get_syndrome(self):

	'''Gets the syndromes from the lattice

	Returns:

	self.syndrome is updated with values +1 (no syndrome) and -1 (syndrome)
	'''

        for n in range(self.size):
    	    for m in range(self.size):
	        self.syndrome[n][m] = self.lattice['H'][n][m] * self.lattice['H'][n][(m-1)%self.size]
	        self.syndrome[n][m] *= self.lattice['V'][n][m] * self.lattice['V'][(n-1)%self.size][m]




    def get_syndrome_position(self):

	'''Gets the syndrome's positions from the lattice

	Returns:

	self.syndrome_position is updated with tuples [n,m] for the syndrome's positions
	'''

        for n in range(self.size):
            for m in range(self.size):
	        syndrome_star = self.lattice['H'][n][m] * self.lattice['H'][n][(m-1)%self.size]
	        syndrome_star *= self.lattice['V'][n][m] * self.lattice['V'][(n-1)%self.size][m]

	        if syndrome_star == -1:
	            self.syndrome_position += [[n,m]]
	
 

    def get_graph(self):

        '''Returns a complete graph of the syndromes and their distances (weight)

	Parameters:
	
	n_syn: number of syndromes
	weight: distance between two syndromes
	[n, m, weight]: the distance between syndromes 'n' and 'm' is 'weight'
	------------

	Important:

	The syndromes (vertices in the graph) need to be labelled as 0, 1, ..., n_syn - 1
	------------

	Returns:
	
	self.graph is updated
	'''

        n_syn = len(self.syndrome_position)

        for n in range(n_syn):
            (x0, y0) = self.syndrome_position[n]

            for m in range(n+1, n_syn):
	        (x1, y1) = self.syndrome_position[m]
	        weight = min((x0-x1)%self.size, (x1-x0)%self.size) + min((y0-y1)%self.size, (y1-y0)%self.size)
	        self.graph += [[n, m, weight]]




    def get_pairs(self):

	'''Matches the closest syndromes (vertices) which are to be connected

	Parameters:
	
	n_syn: number of syndromes
	matching: an array with the syndrome's labels. The n-th element is matched with syndrome labelled 'n'
	pm.getMatching: blossom algorithm function
	-----------

	Returns:
	
	self.pairs is updated with the positions of the syndromes which are to be connected
	'''

        n_syn = len(self.syndrome_position)
        matching = pm.getMatching(n_syn, self.graph)
        self.pairs = [[self.syndrome_position[n], self.syndrome_position[matching[n]]] for n in range(n_syn) if n < matching[n]]



    def correct_syndrome(self):

	'''Corrects the syndromes by connecting the paired vertices together

	Parameters:
	
	n_syn: number of syndromes
	------------

	Returns:
	
	self.lattice is updated by correcting the qubits after connecting the syndromes
	'''

        self.get_graph()
        self.get_pairs()
        n_syn = len(self.syndrome_position)

        for n in range(n_syn/2):
            ((x0,y0), (x1,y1)) = self.pairs[n]

            if (x1-x0) % self.size < (x0-x1) % self.size:
	        for m in range((x1-x0) % self.size):
	            self.lattice['V'][(x1-m-1)%self.size][y1] *= -1

            else:
	        for m in range((x0-x1) % self.size):
	            self.lattice['V'][(x1+m)%self.size][y1] *= -1


            if (y1-y0) % self.size < (y0-y1) % self.size:
	        for m in range((y1-y0) % self.size):
	            self.lattice['H'][x0][(y1-m-1)%self.size] *= -1

            else:
	        for m in range((y0-y1) % self.size):
	            self.lattice['H'][x0][(y1+m)%self.size] *= -1


        

    def verify_logical_error(self):

        '''Verifies if there is a logical error or not due to errors

	Returns:
	
	0: logical error
	1: no logical error
	'''

        for n in range(self.size):
            n_errors_horizontal, n_errors_vertical = 0, 0

            for m in range(self.size):
	        n_errors_horizontal += (self.lattice['H'][m][n] - 1)/2
	        n_errors_vertical += (self.lattice['V'][n][m] - 1)/2

            if n_errors_horizontal % 2 == 1 or n_errors_vertical % 2 == 1:
	        return 0


        return 1



'''    def draw_lattice(self):

        # Draws the full lattice with the X and Z syndromes and qubits represented by X: X error, Z: Z error

        print '\nFull lattice:'
        print 'qubit = X: X error, Z: Z error\n'
        for n in range(self.size):
	    print ' ' * 2,
            for m in range(self.size):
	        print '{0:+} ---- '.format(self.syndrome['Z'][n][m]),
		print 'X:{0:+},Z:{1:+} ----'.format(self.lattice['H'][n][m]['X'], self.lattice['H'][n][m]['Z']),
            print "%+d" % self.syndrome['Z'][n][0]
            for m in range (self.size):
	        print '    |', ' ' * 16,
            print '    |'
            for m in range(self.size):
	        print 'X:{0:+},Z:{1:+}'.format(self.lattice['V'][n][m]['X'], self.lattice['V'][n][m]['Z']), 
		print '     {0:+}      '.format(self.syndrome['X'][n][m]),
            print 'X:{0:+},Z:{1:+}'.format(self.lattice['V'][n][0]['X'], self.lattice['V'][n][0]['Z'])
            for m in range (self.size):
	        print '    |', ' ' * 16,
            print '    |'
        print ' ' * 2,
        for m in range(self.size):
	    print '{0:+} ---- '.format(self.syndrome['Z'][0][m]), 
	    print 'X:{0:+},Z:{1:+} ----'.format(self.lattice['H'][0][m]['X'], self.lattice['H'][0][m]['Z']),
        print "%+d" % self.syndrome['Z'][0][0]
        print '\n'



    def draw_lattice_reduced(self):

        # Draws a reduced version of the lattice with the X and Z syndromes and the qubits represented by (X error, Z error)

        print '\nReduced lattice:'
        print 'qubit = (X error, Z error)\n'
        for n in range(self.size):
	    print ' ',
            for m in range(L):
	        print '{0:+} -- ({1:+},{2:+}) --'.format(self.syndrome['Z'][n][m], self.lattice['H'][n][m]['X'], self.lattice['H'][n][m]['Z']),
            print "%+d" % self.syndrome['Z'][n][0]
            for m in range (self.size):
	        print '   |', ' ' * 11,
            print '   |'
            for m in range(self.size):
	        print '({0:+},{1:+})    {2:+}   '.format(self.lattice['V'][n][m]['X'], self.lattice['V'][n][m]['Z'], self.syndrome['X'][n][m]),
            print '({0:+},{1:+})'.format(self.lattice['V'][n][0]['X'], self.lattice['V'][n][0]['Z'])
            for m in range (self.size):
	        print '   |', ' ' * 11,
            print '   |'
        print ' ',
        for m in range(self.size):
	    print '{0:+} -- ({1:+},{2:+}) --'.format(self.syndrome['Z'][0][m], self.lattice['H'][0][m]['X'], self.lattice['H'][0][m]['Z']),
        print "%+d" % self.syndrome['Z'][0][0]
        print '\n'



    def draw_errors(self, A):

        # Draws the lattice with the qubits with 'A' error

        print A, 'errors\n'
        for n in range(self.size):
	    print '',
            for m in range(self.size):
	        if self.lattice['H'][n][m][A] == -1:
	            print '-- x --',
	        else:
		    print '-------',
            print ''
            for m in range (self.size):
	        print '|', ' ' * 5,
            print '|'
            for m in range(self.size):
	        if self.lattice['V'][n][m][A] == -1:
	            print 'x      ',
	        else:
		    print '|      ',
	    if self.lattice['V'][n][0][A] == -1:
	        print 'x'
	    else:
	        print '|'
            for m in range (self.size):
	        print '|', ' ' * 5,
            print '|'
        print '',
        for m in range(self.size):
	    if self.lattice['H'][0][m][A] == -1:
	        print '-- x --',
	    else:
	        print '-------',
        print '\n'



    def draw_syndrome(self, A):

        # Draws the syndromes in the lattice

        for n in range(self.size):
            for m in range(self.size):
	        if A == 'Z' and self.syndrome[A][n][m] == -1:
	            print 'x -----',
	        else:
		    print '  -----',
	    if A == 'Z' and self.syndrome[A][n][0] == -1:
	        print 'x'
	    else:
	        print ''
            for m in range (self.size):
	        print '|', ' ' * 5,
            print '|'
            for m in range(self.size):
	        if A == 'X' and self.syndrome[A][n][m] == -1:
	            print '|   x  ',
	        else:
		    print '|      ',
            print '|'
            for m in range (self.size):
	        print '|', ' ' * 5,
            print '|'
        for m in range(self.size):
	    if A == 'Z' and self.syndrome[A][0][m] == -1:
	        print 'x -----',
	    else:
	        print '  -----',
        if A == 'Z' and self.syndrome[A][0][m] == -1:
	    print 'x',
        else:
	    print '',
        print '\n'
'''


######################################################################################
######################################################################################
######################################################################################


class toric_code_3D:

    def __init__(self, L=5, p=0.1, q=0.1, time=10, space_weight=1, time_weight=1):

	''' 
	Parameters:
	    
	L: lattice size
	p: qubit error probability
	q: measurement error probability
	time: number of round of measurements
	space_weight: weight for the space distance between syndromes. See 'get_graph()'
	time_weight: weight for the time distance between syndromes. See 'get_graph()'
	'''

	self.size = L
	self.prop1 = p
	self.prop2 = q
	self.time = time
	self.space_weight = space_weight
	self.time_weight = time_weight
	
	self.lattice = [{A: [[1 for n in range(L)] for n in range(L)] for A in ['H','V']} for n in range(time)]
	self.syndrome = [[[1 for n in range(L)] for n in range(L)] for n in range(time)]
	self.syndrome_position = []

	self.graph = []
	self.pairs = []



    def random_error(self, p):
        return -1 if random.random() < p else 1



    def create_lattice(self):

	'''Creates the lattice

	Parameters:

	self.size: lattice size
	self.time: number of measurements rounds
	self.prop1 in self.random_error(): qubit error probability
	----------

	Returns:
	
	self.lattice is updated with values +1 (no error) and -1 (error)
	'''

        for t in range(1, self.time):
            for n in range(self.size):
	        for m in range(self.size):
		    for A in ['H', 'V']:
			self.lattice[t][A][n][m] = self.random_error(self.prop1)*self.lattice[t-1][A][n][m]
		



    def get_syndrome(self):

	'''Gets the syndromes from the lattice and their position

	Parameters:

	self.prop2 in self.random_error(): measurement error probability
	-------------

	Returns:

	self.syndrome is updated with values +1 (no syndrome) and -1 (syndrome)
	self.syndrome_position is updated with tuples [n,m,t] for the syndrome's positions
	'''

        for n in range(self.size):
    	    for m in range(self.size):
	        for t in range(1, self.time):
		    self.syndrome[t][n][m] = self.lattice[t]['H'][n][m] * self.lattice[t]['H'][n][(m-1)%self.size]
	            self.syndrome[t][n][m] *= self.lattice[t]['V'][n][m] * self.lattice[t]['V'][(n-1)%self.size][m]
		    if t != self.time - 1:
	                self.syndrome[t][n][m] *= self.random_error(self.prop2)


	for n in range(self.size):
	    for m in range(self.size):
	        for t in range(self.time - 1):
		    if self.syndrome[t][n][m] != self.syndrome[t+1][n][m]:
		        self.syndrome_position += [[n,m,t]]

        



    def get_graph(self):

        '''Returns a complete graph of the syndromes and their distances (weight)

	Parameters:
	
	n_syn: number of syndromes
	self.space_weight: weight for the space distance between syndromes
	self.time_weight: weight for the time distance between syndromes
	weight: distance between two syndromes
	[n, m, weight]: the distance between syndromes 'n' and 'm' is 'weight'
	------------

	Important:

	The syndromes (vertices in the graph) need to be labelled as 0, 1, ..., n_syn - 1
	------------

	Returns:
	
	self.graph is updated
	'''

        n_syn = len(self.syndrome_position)

        for n in range(n_syn):
            (x0,y0,t0) = self.syndrome_position[n]

            for m in range(n+1, n_syn):
	        (x1,y1,t1) = self.syndrome_position[m]
	        weight = self.space_weight*(min((x0-x1)%self.size, (x1-x0)%self.size) + min((y0-y1)%self.size, (y1-y0)%self.size))
		weight += self.time_weight*abs(t0-t1)
	        self.graph += [[n, m, weight]]



    def get_pairs(self):

        '''Matches the closest syndromes (vertices) which are to be connected

	Parameters:
	
	n_syn: number of syndromes
	matching: an array with the syndrome's labels. The n-th element is matched with syndrome labelled 'n'
	pm.getMatching: blossom algorithm function
	-----------

	Returns:
	
	self.pairs is updated with the positions of the syndromes which are to be connected
	'''

        n_syn = len(self.syndrome_position)
        matching = pm.getMatching(n_syn, self.graph)
        self.pairs = [[self.syndrome_position[n], self.syndrome_position[matching[n]]] for n in range(n_syn) if n < matching[n]]




    def correct_syndrome(self):

        '''Corrects the syndromes by connecting the paired vertices together

	Parameters:
	
	n_syn: number of syndromes
	------------

	Returns:
	
	self.lattice is updated by correcting the qubits after connecting the syndromes
	'''

        self.get_graph()
        self.get_pairs()

        n_syn = len(self.syndrome_position)
        for n in range(n_syn/2):
            ((x0,y0,t0), (x1,y1,t1)) = self.pairs[n]

            if (x1-x0) % self.size < (x0-x1) % self.size:
	        for m in range((x1-x0) % self.size):
	            self.lattice[self.time-1]['V'][(x1-m-1)%self.size][y1] *= -1

            else:
	        for m in range((x0-x1) % self.size):
	            self.lattice[self.time-1]['V'][(x1+m)%self.size][y1] *= -1


            if (y1-y0) % self.size < (y0-y1) % self.size:
	        for m in range((y1-y0) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1-m-1)%self.size] *= -1

            else:
	        for m in range((y0-y1) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1+m)%self.size] *= -1




    def verify_logical_error(self):

        '''Verifies if there is a logical error or not due to errors

	Returns:
	
	0: logical error
	1: no logical error
	'''

        for n in range(self.size):
            n_errors_horizontal, n_errors_vertical = 0, 0

            for m in range(self.size):
	        n_errors_horizontal += (self.lattice[self.time-1]['H'][m][n] - 1)/2
	        n_errors_vertical += (self.lattice[self.time-1]['V'][n][m] - 1)/2

            if n_errors_horizontal % 2 == 1 or n_errors_vertical % 2 == 1:
	        return 0


        return 1



'''    def draw_lattice(self):

        # Draws the full lattice with the X and Z syndromes and qubits represented by X: X error, Z: Z error

        print '\nFull lattice:'
        print 'qubit = X: X error, Z: Z error\n'
        for t in range(self.time):
	    print 'time = ', t
            for n in range(self.size):
	        print ' ' * 2,
                for m in range(self.size):
	            print '{0:+} ---- '.format(self.syndrome[t]['Z'][n][m]), 
		    print 'X:{0:+},Z:{1:+} ----'.format(self.lattice[t]['H'][n][m]['X'], self.lattice[t]['H'][n][m]['Z']),
                print "%+d" % self.syndrome[t]['Z'][n][0]
                for m in range (self.size):
	            print '    |', ' ' * 16,
                print '    |'
                for m in range(self.size):
	            print 'X:{0:+},Z:{1:+}'.format(self.lattice[t]['V'][n][m]['X'], self.lattice[t]['V'][n][m]['Z']),
		    print '       {0:+}      '.format(self.syndrome[t]['X'][n][m]),
                print 'X:{0:+},Z:{1:+}'.format(self.lattice[t]['V'][n][0]['X'], self.lattice[t]['V'][n][0]['Z'])
                for m in range (self.size):
	            print '    |', ' ' * 16,
                print '    |'
            print ' ' * 2,
            for m in range(self.size):
	        print '{0:+} ---- '.format(self.syndrome[t]['Z'][l][0][m]), 
		print 'X:{0:+},Z:{1:+} ----'.format(self.lattice[t]['H'][l][0][m]['X'], self.lattice[t]['H'][l][0][m]['Z']),
            print "%+d" % self.syndrome[t]['Z'][0][0]
            print '\n'




    def draw_lattice_reduced(self):

        # Draws a reduced version of the lattice with the X and Z syndromes and the qubits represented by (X error, Z error)

        print '\nReduced lattice:'
        print 'qubit = (X error, Z error)\n'
        for t in range(self.time):
            print 'time = ', t
            for n in range(self.size):
	        print ' ',
                for m in range(self.size):
	            print '{0:+} -- '.format(self.syndrome[t]['Z'][n][m]), 
		    print '({0:+},{1:+}) --'.format(self.lattice[t]['H'][n][m]['X'], self.lattice[t]['H'][n][m]['Z']),
                print "%+d" % self.syndrome[t]['Z'][n][0]
                for m in range (self.size):
	            print '   |', ' ' * 11,
                print '   |'
                for m in range(self.size):
	            print '({0:+},{1:+})'.format(self.lattice[t]['V'][n][m]['X'], self.lattice[t]['V'][n][m]['Z']), 
		    print '    {0:+}   '.format(self.syndrome[t]['X'][n][m]),
                print '({0:+},{1:+})'.format(self.lattice[t]['V'][n][0]['X'], self.lattice[t]['V'][n][0]['Z'])
                for m in range (self.size):
	            print '   |', ' ' * 11,
                print '   |'
            print ' ',
            for m in range(self.size):
	        print '{0:+} -- '.format(self.syndrome[t]['Z'][0][m]), 
		print '({0:+},{1:+}) --'.format(self.lattice[t]['H'][0][m]['X'], self.lattice[t]['H'][0][m]['Z']),
            print "%+d" % self.syndrome[t]['Z'][0][0]
            print '\n'


    def draw_errors(self, A, FinalRound=False):

        # Draws the lattice with the qubits with 'A' error

        print A, 'errors\n'
        for t in range(FinalRound*(self.time - 1), self.time):
	    print 'time = ', t
            for n in range(self.size):
	        print '',
                for m in range(self.size):
	            if self.lattice[t]['H'][n][m][A] == -1:
	                print '-- x --',
	            else:
		        print '-------',
                print ''
                for m in range (self.size):
	            print '|', ' ' * 5,
                print '|'
                for m in range(self.size):
	            if self.lattice[t]['V'][n][m][A] == -1:
	                print 'x      ',
	            else:
		        print '|      ',
	        if self.lattice[t]['V'][n][0][A] == -1:
	            print 'x'
	        else:
	            print '|'
                for m in range (self.size):
	            print '|', ' ' * 5,
                print '|'
            print '',
            for m in range(self.size):
	        if self.lattice[t]['H'][0][m][A] == -1:
	            print '-- x --',
	        else:
	            print '-------',
            print '\n'



    def draw_syndrome(self, A, FinalRound=False):

        # Draws the syndromes in the lattice

	if A == 'Z':
	    print 'Star syndromes\n'
	elif A == 'X':
	    print 'Plaquette syndromes\n'

        for t in range(FinalRound*(self.time - 1), self.time):
	    print 'time = ', t
            for n in range(self.size):
                for m in range(self.size):
	            if A == 'Z' and self.syndrome[t][A][n][m] == -1:
	                print 'x -----',
	            else:
		        print '  -----',
	        if A == 'Z' and self.syndrome[t][A][n][0] == -1:
	            print 'x'
	        else:
	            print ''
                for m in range(self.size):
	            print '|', ' ' * 5,
                print '|'
                for m in range(self.size):
	            if A == 'X' and self.syndrome[t][A][n][m] == -1:
	                print '|   x  ',
	            else:
		        print '|      ',
                print '|'
                for m in range(self.size):
	            print '|', ' ' * 5,
                print '|'
            for m in range(self.size):
	        if A == 'Z' and self.syndrome[t][A][0][m] == -1:
	            print 'x -----',
	        else:
	            print '  -----',
            if A == 'Z' and self.syndrome[t][A][0][0] == -1:
	        print 'x',
            else:
	        print '',
            print '\n'

'''

######################################################################################
######################################################################################
######################################################################################


class toric_code_3D_faulty:

    def __init__(self, L=5, p=0.1, q=0.1, r=0.05, time=10, space_weight=1, time_weight=1):

	''' 
	Parameters:
	    
	L: lattice size
	p: qubit error probability
	q: measurement error probability
	r: probability that a measurement does not return any value
	time: number of round of measurements
	space_weight: weight for the space distance between syndromes. See 'get_graph()'
	time_weight: weight for the time distance between syndromes. See 'get_graph()'
	'''

	self.size = L
	self.prop1 = p
	self.prop2 = q
	self.prop3 = r
	self.time = time
	self.space_weight = space_weight
	self.time_weight = time_weight
	
	self.lattice = [{A: [[1 for n in range(L)] for n in range(L)] for A in ['H','V']} for n in range(time)]
	self.syndrome = [[[1 for n in range(L)] for n in range(L)] for n in range(time)]
	self.syndrome_position = []

	self.graph = []
	self.pairs = []



    def random_error(self, p):
        return -1 if random.random() < p else 1



    def create_lattice(self):

	'''Creates the lattice

	Parameters:

	self.size: lattice size
	self.time: number of measurements rounds
	self.prop1 in self.random_error(): qubit error probability
	----------

	Returns:
	
	self.lattice is updated with values +1 (no error) and -1 (error)
	'''

        for t in range(1, self.time):
            for n in range(self.size):
	        for m in range(self.size):
		    for A in ['H', 'V']:
			self.lattice[t][A][n][m] = self.random_error(self.prop1)*self.lattice[t-1][A][n][m]
		



    def get_syndrome(self):

	'''Gets the syndromes from the lattice and their position

	Parameters:

	self.prop2 in self.random_error(): measurement error probability
	-------------

	Returns:

	self.syndrome is updated with
		+1: no syndrome
		-1: syndrome
		0: measurement failed and did not return a value
	self.syndrome_position is updated with tuples [n,m,t] for the syndrome's positions
	'''

        for n in range(self.size):
    	    for m in range(self.size):
	        for t in range(1, self.time):
		    self.syndrome[t][n][m] = self.lattice[t]['H'][n][m] * self.lattice[t]['H'][n][(m-1)%self.size]
	            self.syndrome[t][n][m] *= self.lattice[t]['V'][n][m] * self.lattice[t]['V'][(n-1)%self.size][m]
		    if t != self.time - 1:
			if self.random_error(self.prop3) == -1:
			    self.syndrome[t][n][m] = 0
			else:
	                    self.syndrome[t][n][m] *= self.random_error(self.prop2)


	for n in range(self.size):
	    for m in range(self.size):
	        for t in range(1, self.time):
		    if self.syndrome[t][n][m] == -1:
			for l in range(1, t+1):
			    if self.syndrome[t-l][n][m] == -1:
				break
			    elif self.syndrome[t-l][n][m] == 1:
				self.syndrome_position += [[n, m, math.ceil((2*t-l)/2)]]
				break
			for l in range(1, self.time - t):
			    if self.syndrome[t+l][n][m] == -1:
				break
			    elif self.syndrome[t+l][n][m] == 1:
				self.syndrome_position += [[n, m, math.ceil((2*t+l)/2)]]
				break
        


    def get_graph(self):

        '''Returns a complete graph of the syndromes and their distances (weight)

	Parameters:
	
	n_syn: number of syndromes
	self.space_weight: weight for the space distance between syndromes
	self.time_weight: weight for the time distance between syndromes
	weight: distance between two syndromes
	[n, m, weight]: the distance between syndromes 'n' and 'm' is 'weight'
	------------

	Important:

	The syndromes (vertices in the graph) need to be labelled as 0, 1, ..., n_syn - 1
	------------

	Returns:
	
	self.graph is updated
	'''

        n_syn = len(self.syndrome_position)

        for n in range(n_syn):
            (x0,y0,t0) = self.syndrome_position[n]

            for m in range(n+1, n_syn):
	        (x1,y1,t1) = self.syndrome_position[m]
	        weight = self.space_weight*(min((x0-x1)%self.size, (x1-x0)%self.size) + min((y0-y1)%self.size, (y1-y0)%self.size))
		weight += self.time_weight*abs(t0-t1)
	        self.graph += [[n, m, weight]]



    def get_pairs(self):

        '''Matches the closest syndromes (vertices) which are to be connected

	Parameters:
	
	n_syn: number of syndromes
	matching: an array with the syndrome's labels. The n-th element is matched with syndrome labelled 'n'
	pm.getMatching: blossom algorithm function
	-----------

	Returns:
	
	self.pairs is updated with the positions of the syndromes which are to be connected
	'''

        n_syn = len(self.syndrome_position)
        matching = pm.getMatching(n_syn, self.graph)
        self.pairs = [[self.syndrome_position[n], self.syndrome_position[matching[n]]] for n in range(n_syn) if n < matching[n]]




    def correct_syndrome(self):

        '''Corrects the syndromes by connecting the paired vertices together

	Parameters:
	
	n_syn: number of syndromes
	------------

	Returns:
	
	self.lattice is updated by correcting the qubits after connecting the syndromes
	'''

        self.get_graph()
        self.get_pairs()

        n_syn = len(self.syndrome_position)
        for n in range(n_syn/2):
            ((x0,y0,t0), (x1,y1,t1)) = self.pairs[n]

            if (x1-x0) % self.size < (x0-x1) % self.size:
	        for m in range((x1-x0) % self.size):
	            self.lattice[self.time-1]['V'][(x1-m-1)%self.size][y1] *= -1

            else:
	        for m in range((x0-x1) % self.size):
	            self.lattice[self.time-1]['V'][(x1+m)%self.size][y1] *= -1


            if (y1-y0) % self.size < (y0-y1) % self.size:
	        for m in range((y1-y0) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1-m-1)%self.size] *= -1

            else:
	        for m in range((y0-y1) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1+m)%self.size] *= -1




    def verify_logical_error(self):

        '''Verifies if there is a logical error or not due to errors

	Returns:
	
	0: logical error
	1: no logical error
	'''

        for n in range(self.size):
            n_errors_horizontal, n_errors_vertical = 0, 0

            for m in range(self.size):
	        n_errors_horizontal += (self.lattice[self.time-1]['H'][m][n] - 1)/2
	        n_errors_vertical += (self.lattice[self.time-1]['V'][n][m] - 1)/2

            if n_errors_horizontal % 2 == 1 or n_errors_vertical % 2 == 1:
	        return 0


        return 1



'''    def draw_lattice(self):

        # Draws the full lattice with the X and Z syndromes and qubits represented by X: X error, Z: Z error

        print '\nFull lattice:'
        print 'qubit = X: X error, Z: Z error\n'
        for t in range(self.time):
	    print 'time = ', t
            for n in range(self.size):
	        print ' ' * 2,
                for m in range(self.size):
	            print '{0:+} ---- '.format(self.syndrome[t]['Z'][n][m]), 
		    print 'X:{0:+},Z:{1:+} ----'.format(self.lattice[t]['H'][n][m]['X'], self.lattice[t]['H'][n][m]['Z']),
                print "%+d" % self.syndrome[t]['Z'][n][0]
                for m in range (self.size):
	            print '    |', ' ' * 16,
                print '    |'
                for m in range(self.size):
	            print 'X:{0:+},Z:{1:+}'.format(self.lattice[t]['V'][n][m]['X'], self.lattice[t]['V'][n][m]['Z']),
		    print '       {0:+}      '.format(self.syndrome[t]['X'][n][m]),
                print 'X:{0:+},Z:{1:+}'.format(self.lattice[t]['V'][n][0]['X'], self.lattice[t]['V'][n][0]['Z'])
                for m in range (self.size):
	            print '    |', ' ' * 16,
                print '    |'
            print ' ' * 2,
            for m in range(self.size):
	        print '{0:+} ---- '.format(self.syndrome[t]['Z'][l][0][m]), 
		print 'X:{0:+},Z:{1:+} ----'.format(self.lattice[t]['H'][l][0][m]['X'], self.lattice[t]['H'][l][0][m]['Z']),
            print "%+d" % self.syndrome[t]['Z'][0][0]
            print '\n'




    def draw_lattice_reduced(self):

        # Draws a reduced version of the lattice with the X and Z syndromes and the qubits represented by (X error, Z error)

        print '\nReduced lattice:'
        print 'qubit = (X error, Z error)\n'
        for t in range(self.time):
            print 'time = ', t
            for n in range(self.size):
	        print ' ',
                for m in range(self.size):
	            print '{0:+} -- '.format(self.syndrome[t]['Z'][n][m]), 
		    print '({0:+},{1:+}) --'.format(self.lattice[t]['H'][n][m]['X'], self.lattice[t]['H'][n][m]['Z']),
                print "%+d" % self.syndrome[t]['Z'][n][0]
                for m in range (self.size):
	            print '   |', ' ' * 11,
                print '   |'
                for m in range(self.size):
	            print '({0:+},{1:+})'.format(self.lattice[t]['V'][n][m]['X'], self.lattice[t]['V'][n][m]['Z']), 
		    print '    {0:+}   '.format(self.syndrome[t]['X'][n][m]),
                print '({0:+},{1:+})'.format(self.lattice[t]['V'][n][0]['X'], self.lattice[t]['V'][n][0]['Z'])
                for m in range (self.size):
	            print '   |', ' ' * 11,
                print '   |'
            print ' ',
            for m in range(self.size):
	        print '{0:+} -- '.format(self.syndrome[t]['Z'][0][m]), 
		print '({0:+},{1:+}) --'.format(self.lattice[t]['H'][0][m]['X'], self.lattice[t]['H'][0][m]['Z']),
            print "%+d" % self.syndrome[t]['Z'][0][0]
            print '\n'


    def draw_errors(self, A, FinalRound=False):

        # Draws the lattice with the qubits with 'A' error

        print A, 'errors\n'
        for t in range(FinalRound*(self.time - 1), self.time):
	    print 'time = ', t
            for n in range(self.size):
	        print '',
                for m in range(self.size):
	            if self.lattice[t]['H'][n][m][A] == -1:
	                print '-- x --',
	            else:
		        print '-------',
                print ''
                for m in range (self.size):
	            print '|', ' ' * 5,
                print '|'
                for m in range(self.size):
	            if self.lattice[t]['V'][n][m][A] == -1:
	                print 'x      ',
	            else:
		        print '|      ',
	        if self.lattice[t]['V'][n][0][A] == -1:
	            print 'x'
	        else:
	            print '|'
                for m in range (self.size):
	            print '|', ' ' * 5,
                print '|'
            print '',
            for m in range(self.size):
	        if self.lattice[t]['H'][0][m][A] == -1:
	            print '-- x --',
	        else:
	            print '-------',
            print '\n'



    def draw_syndrome(self, A, FinalRound=False):

        # Draws the syndromes in the lattice

	if A == 'Z':
	    print 'Star syndromes\n'
	elif A == 'X':
	    print 'Plaquette syndromes\n'

        for t in range(FinalRound*(self.time - 1), self.time):
	    print 'time = ', t
            for n in range(self.size):
                for m in range(self.size):
	            if A == 'Z' and self.syndrome[t][A][n][m] == -1:
	                print 'x -----',
	            else:
		        print '  -----',
	        if A == 'Z' and self.syndrome[t][A][n][0] == -1:
	            print 'x'
	        else:
	            print ''
                for m in range(self.size):
	            print '|', ' ' * 5,
                print '|'
                for m in range(self.size):
	            if A == 'X' and self.syndrome[t][A][n][m] == -1:
	                print '|   x  ',
	            else:
		        print '|      ',
                print '|'
                for m in range(self.size):
	            print '|', ' ' * 5,
                print '|'
            for m in range(self.size):
	        if A == 'Z' and self.syndrome[t][A][0][m] == -1:
	            print 'x -----',
	        else:
	            print '  -----',
            if A == 'Z' and self.syndrome[t][A][0][0] == -1:
	        print 'x',
            else:
	        print '',
            print '\n'

'''

