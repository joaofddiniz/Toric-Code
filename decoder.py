# Joao Fernando Doriguello Diniz
# 07/02/2017
# Functions of the decoder

import random
import toric_code as toric
from blossom5 import pyMatch as pm


def syndrome_position(L, syndrome):

    # Given the matrix of the syndromes, return a dictionary with the syndromes' position.

    syndrome_position = {'X': [], 'Z': []}

    for n in range(L):
        for m in range(L):
	    for A in ['X', 'Z']:
	        if syndrome[A][n][m] == 1:
	            syndrome_position[A] += [[n,m]]

    return syndrome_position
	

def get_graph(L, syndrome_position):

    # Return a complete graph of the X and Z syndromes and their distances (weight), with the syndromes (vertices)
    # labelled as 0, 1, ..., n_syndrome - 1

    graph = {'X': [], 'Z': []}

    for A in ['X', 'Z']:
        n_syndrome = len(syndrome_position[A])
	
        for n in range(n_syndrome):
            (x0, y0) = syndrome_position[A][n]
	
            for m in range(n+1,n_syndrome):
	        (x1, y1) = syndrome_position[A][m]
	        weight = min((x0 - x1)%L, (x1 - x0)%L) + min((y0 - y1)%L, (y1 - y0)%L)
	        graph[A] += [[n, m, weight]]

    return graph



def get_pairs(syndrome_position, graph):

    # Use the blossom algorithm function 'pm.getMatching' and return the pairs of matched vertices which are to be connected

    pairs = {'X': [], 'Z': []}

    for A in ['X', 'Z']:
        n_syndrome = len(syndrome_position[A])
        matching = pm.getMatching(n_syndrome, graph[A])
	
        for n in range(n_syndrome/2):
            i, j = matching[2*n], matching[2*n+1]
            pairs[A] += [[syndrome_position[A][i], syndrome_position[A][j]]]

    return pairs



def correct_syndrome(L, lattice, syndrome_position, pairs):

    # Correct the syndromes by connecting the paired vertices together and return the corrected lattice

    n_syndrome = len(syndrome_position['Z'])
    for n in range(n_syndrome/2):
        ((x0,y0), (x1,y1)) = pairs['Z'][n]
	
        if (x1-x0)%L < (x0-x1)%L:
	    for m in range((x1-x0)%L):
	        lattice['V'][(x1-m-1)%L][y1]['Z'] ^= 1
        else:
	    for m in range((x0-x1)%L):
	        lattice['V'][(x1+m)%L][y1]['Z'] ^= 1
		
        if (y1-y0)%L < (y0-y1)%L:
	    for m in range((y1-y0)%L):
	        lattice['H'][x0][(y1-m-1)%L]['Z'] ^= 1
        else:
	    for m in range((y0-y1)%L):
	        lattice['H'][x0][(y1+m)%L]['Z'] ^= 1


    n_syndrome = len(syndrome_position['X'])
    for n in range(n_syndrome/2):
        ((x0,y0), (x1,y1)) = pairs['X'][n]
	
        if (x1-x0)%L < (x0-x1)%L:
	    for m in range((x1-x0)%L):
	        lattice['H'][(x1-m)%L][y1]['X'] ^= 1
        else:
	    for m in range((x0-x1)%L):
	        lattice['H'][(x1+m+1)%L][y1]['X'] ^= 1
		
        if (y1-y0)%L < (y0-y1)%L:
	    for m in range((y1-y0)%L):
	        lattice['V'][x0][(y1-m)%L]['X'] ^= 1
        else:
	    for m in range((y0-y1)%L):
	        lattice['V'][x0][(y1+m+1)%L]['X'] ^= 1


    return lattice


