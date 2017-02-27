import random
from blossom5 import pyMatch as pm

class toric_code_2D:

    def __init__(self, L=5, p=0.1):

	self.size = L
	self.prop = p

	self.lattice = {'H': [] , 'V': []}
	self.syndrome = {A: [[1 for n in range(L)] for n in range(L)] for A in ['X', 'Z']}
	self.syndrome_position = {'X': [], 'Z': []}

	self.graph = {'X': [], 'Z': []}
	self.pairs = {'X': [], 'Z': []}



    def random_error(self):
        return -1 if random.random() < self.prop else 1


    def create_lattice(self):

        # The lattice can be seen as formed by two LxL separate lattices (each with LxL qubits): a vertical one, 
        # where the qubits are connected mainly vertically, and a horizontal one, where the qubits are connected mainly horizontally
	
	for A in ['H', 'V']:	
            self.lattice[A] = [[{B:self.random_error() for B in ['X', 'Z']} for n in range(self.size)] for n in range(self.size)]



    def get_syndrome(self):

        # Calculates the syndrome of the lattice and returns a dictionary with the X and Z syndromes

        #self.syndrome = {A: [[1 for n in range(self.size)] for n in range(self.size)] for A in ['X', 'Z']}

        for n in range(self.size):
    	    for m in range(self.size):
	        self.syndrome['X'][n][m] = self.lattice['H'][n][m]['X'] * self.lattice['H'][(n+1)%self.size][m]['X']
	        self.syndrome['X'][n][m] *= self.lattice['V'][n][m]['X'] * self.lattice['V'][n][(m+1)%self.size]['X']
	        self.syndrome['Z'][n][m] = self.lattice['H'][n][m]['Z'] * self.lattice['H'][n][(m-1)%self.size]['Z']
	        self.syndrome['Z'][n][m] *= self.lattice['V'][n][m]['Z'] * self.lattice['V'][(n-1)%self.size][m]['Z']




    def get_syndrome_position(self):

        # Returns a dictionary with the syndromes' position.

        for n in range(self.size):
            for m in range(self.size):
	        syndrome_plaquette = self.lattice['H'][n][m]['X'] * self.lattice['H'][(n+1)%self.size][m]['X']
	        syndrome_plaquette *= self.lattice['V'][n][m]['X'] * self.lattice['V'][n][(m+1)%self.size]['X']
	        syndrome_star = self.lattice['H'][n][m]['Z'] * self.lattice['H'][n][(m-1)%self.size]['Z']
	        syndrome_star *= self.lattice['V'][n][m]['Z'] * self.lattice['V'][(n-1)%self.size][m]['Z']

	        if syndrome_plaquette == -1:
	            self.syndrome_position['X'] += [[n,m]]
	        if syndrome_star == -1:
	            self.syndrome_position['Z'] += [[n,m]]
	
 

    def get_graph(self):

        # Returns a complete graph of the X and Z syndromes and their distances (weight), with the syndromes (vertices)
        # labelled as 0, 1, ..., n_syndrome - 1

        for A in ['X', 'Z']:
            n_syn = len(self.syndrome_position[A])

            for n in range(n_syn):
                (x0, y0) = self.syndrome_position[A][n]

                for m in range(n+1, n_syn):
	            (x1, y1) = self.syndrome_position[A][m]
	            weight = min((x0-x1)%self.size, (x1-x0)%self.size) + min((y0-y1)%self.size, (y1-y0)%self.size)
	            self.graph[A] += [[n, m, weight]]




    def get_pairs(self):

        # Use the blossom algorithm function 'pm.getMatching' and return the pairs of matched vertices which are to be connected

        for A in ['X', 'Z']:
            n_syn = len(self.syndrome_position[A])
            matching = pm.getMatching(n_syn, self.graph[A])
            self.pairs[A] = [[self.syndrome_position[A][n], self.syndrome_position[A][matching[n]]] for n in range(n_syn) if n < matching[n]]



    def correct_syndrome(self):

        # Corrects the syndromes by connecting the paired vertices together and return the corrected lattice

        self.get_graph()
        self.get_pairs()
        n_syn = len(self.syndrome_position['Z'])

        for n in range(n_syn/2):
            ((x0,y0), (x1,y1)) = self.pairs['Z'][n]

            if (x1-x0)%self.size < (x0-x1)%self.size:
	        for m in range((x1-x0)%self.size):
	            self.lattice['V'][(x1-m-1)%self.size][y1]['Z'] *= -1

            else:
	        for m in range((x0-x1)%self.size):
	            self.lattice['V'][(x1+m)%self.size][y1]['Z'] *= -1


            if (y1-y0)%self.size < (y0-y1)%self.size:
	        for m in range((y1-y0)%self.size):
	            self.lattice['H'][x0][(y1-m-1)%self.size]['Z'] *= -1

            else:
	        for m in range((y0-y1)%self.size):
	            self.lattice['H'][x0][(y1+m)%self.size]['Z'] *= -1


        n_syn = len(self.syndrome_position['X'])
        for n in range(n_syn/2):
            ((x0,y0), (x1,y1)) = self.pairs['X'][n]

            if (x1-x0)%self.size < (x0-x1)%self.size:
	        for m in range((x1-x0)%self.size):
	            self.lattice['H'][(x1-m)%self.size][y1]['X'] *= -1

            else:
	        for m in range((x0-x1)%self.size):
	            self.lattice['H'][(x1+m+1)%self.size][y1]['X'] *= -1


            if (y1-y0)%self.size < (y0-y1)%self.size:
	        for m in range((y1-y0)%self.size):
	            self.lattice['V'][x0][(y1-m)%self.size]['X'] *= -1

            else:
	        for m in range((y0-y1)%self.size):
	           self.lattice['V'][x0][(y1+m+1)%self.size]['X'] *= -1





    def verify_logical_error(self, A):

        # Verifies if there is a logical error or not due to 'A' ('X' or 'Z') errors. If no, returns 1; if yes, returns 0

        for n in range(self.size):
            n_errors_horizontal, n_errors_vertical = 0, 0

            for m in range(self.size):
	        n_errors_horizontal += (self.lattice['H'][m][n][A] - 1)/2
	        n_errors_vertical += (self.lattice['V'][n][m][A] - 1)/2

            if n_errors_horizontal % 2 == 1 or n_errors_vertical % 2 == 1:
	        return 0


        return 1



    def draw_lattice(self):

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



######################################################################################
######################################################################################
######################################################################################


class toric_code_3D:

    def __init__(self, L=5, p=0.1, q=0.1, time=10):

	self.size = L
	self.prop1 = p
	self.prop2 = q
	self.time = time
	
	self.lattice = [{A: [[{'X':1, 'Z':1} for n in range(L)] for n in range(L)] for A in ['H','V']} for n in range(time)]
	self.syndrome = [{A: [[1 for n in range(L)] for n in range(L)] for A in ['X', 'Z']} for n in range(time)]
	self.syndrome_position = {'X': [], 'Z': []}

	self.graph = {'X': [], 'Z': []}
	self.pairs = {'X': [], 'Z': []}



    def random_error(self, p):
        return -1 if random.random() < p else 1



    def create_lattice(self):

        for t in range(1, self.time):
            for n in range(self.size):
	        for m in range(self.size):
		    for A in ['H', 'V']:
		        for B in ['X', 'Z']:
			    self.lattice[t][A][n][m][B] = self.random_error(self.prop1)*self.lattice[t-1][A][n][m][B]
		



    def get_syndrome(self):

        for n in range(self.size):
    	    for m in range(self.size):
	        for t in range(1, self.time):
                    self.syndrome[t]['X'][n][m] = self.lattice[t]['H'][n][m]['X'] * self.lattice[t]['H'][(n+1)%self.size][m]['X']
                    self.syndrome[t]['X'][n][m] *= self.lattice[t]['V'][n][m]['X'] * self.lattice[t]['V'][n][(m+1)%self.size]['X']
		    self.syndrome[t]['Z'][n][m] = self.lattice[t]['H'][n][m]['Z'] * self.lattice[t]['H'][n][(m-1)%self.size]['Z']
	            self.syndrome[t]['Z'][n][m] *= self.lattice[t]['V'][n][m]['Z'] * self.lattice[t]['V'][(n-1)%self.size][m]['Z']
		    if t != self.time - 1:
		        self.syndrome[t]['X'][n][m] *= self.random_error(self.prop2)
	                self.syndrome[t]['Z'][n][m] *= self.random_error(self.prop2)


	for n in range(self.size):
	    for m in range(self.size):
	        for t in range(self.time - 1):
		    for A in ['X', 'Z']:
		        if self.syndrome[t][A][n][m] != self.syndrome[t+1][A][n][m]:
		            self.syndrome_position[A] += [[n,m,t]]

        



    def get_graph(self):

        # Returns a complete graph of the X and Z syndromes and their distances (weight), with the syndromes (vertices)
        # labelled as 0, 1, ..., n_syndrome - 1

        for A in ['X', 'Z']:
            n_syn = len(self.syndrome_position[A])

            for n in range(n_syn):
                (x0,y0,t0) = self.syndrome_position[A][n]

                for m in range(n+1, n_syn):
	            (x1,y1,t1) = self.syndrome_position[A][m]
	            weight = min((x0-x1)%self.size, (x1-x0)%self.size) + min((y0-y1)%self.size, (y1-y0)%self.size) + abs(t0-t1)
	            self.graph[A] += [[n, m, weight]]



    def get_pairs(self):

        # Use the blossom algorithm function 'pm.getMatching' and return the pairs of matched vertices which are to be connected

        for A in ['X', 'Z']:
            n_syn = len(self.syndrome_position[A])
            matching = pm.getMatching(n_syn, self.graph[A])
            self.pairs[A] = [[self.syndrome_position[A][n], self.syndrome_position[A][matching[n]]] for n in range(n_syn) if n < matching[n]]




    def correct_syndrome(self):

        # Corrects the syndromes of the last measurement round at time (self.time - 1)

        self.get_graph()
        self.get_pairs()

        n_syn = len(self.syndrome_position['Z'])
        for n in range(n_syn/2):
            ((x0,y0,t0), (x1,y1,t1)) = self.pairs['Z'][n]

            if (x1-x0) % self.size < (x0-x1) % self.size:
	        for m in range((x1-x0) % self.size):
	            self.lattice[self.time-1]['V'][(x1-m-1)%self.size][y1]['Z'] *= -1

            else:
	        for m in range((x0-x1) % self.size):
	            self.lattice[self.time-1]['V'][(x1+m)%self.size][y1]['Z'] *= -1


            if (y1-y0) % self.size < (y0-y1) % self.size:
	        for m in range((y1-y0) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1-m-1)%self.size]['Z'] *= -1

            else:
	        for m in range((y0-y1) % self.size):
	            self.lattice[self.time-1]['H'][x0][(y1+m)%self.size]['Z'] *= -1


        n_syn = len(self.syndrome_position['X'])
        for n in range(n_syn/2):
            ((x0,y0,t0), (x1,y1,t1)) = self.pairs['X'][n]

            if (x1-x0) % self.size < (x0-x1) % self.size:
	        for m in range((x1-x0) % self.size):
	            self.lattice[self.time-1]['H'][(x1-m)%self.size][y1]['X'] *= -1

            else:
	        for m in range((x0-x1) % self.size):
	            self.lattice[self.time-1]['H'][(x1+m+1)%self.size][y1]['X'] *= -1


            if (y1-y0) % self.size < (y0-y1) % self.size:
	        for m in range((y1-y0) % self.size):
	            self.lattice[self.time-1]['V'][x0][(y1-m)%self.size]['X'] *= -1

            else:
	        for m in range((y0-y1) % self.size):
	            self.lattice[self.time-1]['V'][x0][(y1+m+1)%self.size]['X'] *= -1




    def verify_logical_error(self, A):

        # Verifies if there is a logical error or not due to 'A' ('X' or 'Z') errors. If no, returns 1; if yes, returns 0

        for n in range(self.size):
            n_errors_horizontal, n_errors_vertical = 0, 0

            for m in range(self.size):
	        n_errors_horizontal += (self.lattice[self.time-1]['H'][m][n][A] - 1)/2
	        n_errors_vertical += (self.lattice[self.time-1]['V'][n][m][A] - 1)/2

            if n_errors_horizontal % 2 == 1 or n_errors_vertical % 2 == 1:
	        return 0


        return 1



    def draw_lattice(self):

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
