# Auxiliary code for plotting the threshold plots, 2D threshold as function of space-time weight ratio and 3D threshold as function of both space-time weight ratio and measurement-physical error ratio

import numpy as np
import toric_code_fast as toric
import lmfit
from joblib import Parallel, delayed


def fit_function(p, L, a=0.9, b=-1.5, c=-5., pth=0.03, v=0.7):
    return a + b*(p - pth)*np.power(L, 1./v) + c*(p - pth)**2*np.power(L, 2./v)


def toric_code(L, physical_error, measu_error, async_error, time, precision, space_weight, time_weight, model='3D_async'):

    ''' Calculates the the success ratio for the given model
    -----------------

    Parameters:
    
    L: lattice size
    physical_error: the probability a qubit suffers an error
    measu_error: the probability a measurement sufers an error
    async_error: the probability a measurement does not return any value
    time: L*times is the number of measurement rounds
    precision: precision of the simulation, i.e., how many times it is going to be repeated.
    space_weight: the weight for space distances when calculating the graph
    time_weight: the weight for time distances when calculating the graph
    model: model for the simulations
	2D: measurements are perfect
	3D: measurements are faulty with probability measu_error = measu_ratio * physical_error, and there are multiple measurement rounds
	3D_async: the measurements are asynchronous with probability async_error of not returning any value (value 0 in the model)
    -------------------

    Returns:

    float(success)/precision: the success ratio for the model
    '''

    if model == '3D_async':
        code = toric.toric_code_3D_async(L, physical_error, measu_error, async_error, time*L, space_weight, time_weight, method='shortest')
    elif model == '3D':
	code = toric.toric_code_3D(L, physical_error, measu_error, time*L, space_weight, time_weight)
    elif model == '2D':
	code = toric.toric_code_2D(L, physical_error)
       
    success = 0
    for n in xrange(precision):
	code.create_lattice()
	code.get_syndrome()
        code.correct_syndrome()
    	success += code.verify_logical_error()

    return float(success)/precision



def fitting_plot(L, physical_error, measu_ratio, async_error, time, precision, space_weight, time_weight, model='3D_async'):

    ''' Calculates the threshold values as a function of the physical error.
    -----------------

    Parameters:
    
    L: lattice size
    physical_error: the probability a qubit suffers an error
    measu_ratio: the ratio between the measurement error and qubit error
    async_error: the probability a measurement does not return any value
    time: L*times is the number of measurement rounds
    precision: precision of the simulation, i.e., how many times it is going to be repeated.
    space_weight: the weight for space distances when calculating the graph
    time_weight: the weight for time distances when calculating the graph
    model: model for the simulations
	2D: measurements are perfect
	3D: measurements are faulty with probability measu_error = measu_ratio * physical_error, and there are multiple measurement rounds
	3D_async: the measurements are asynchronous with probability async_error of not returning any value (value 0 in the model)
    -------------------

    Returns:

    plot: array with the threshold values for each physical error
    -------------------

    Important: the calculation is done in parallel with the library joblib
    '''


    plot = []

    for L0 in L:
	result = Parallel(n_jobs=-1)(delayed(toric_code)(L0, p, measu_ratio*p, async_error, time, precision, space_weight, time_weight, model) for p in physical_error)
	plot += result

    return plot



def threshold_plot(L, physical_error, measu_ratio, async_error, time, precision, space_weight, time_weight, model='3D_async'):

    ''' Calculates the threshold values as a function of the space-time weight ratio.
    -----------------

    Parameters:
    
    L: lattice size
    physical_error: the probability a qubit suffers an error
    measu_ratio: the ratio between the measurement error and qubit error
    async_error: the probability a measurement does not return any value
    time: L*times is the number of measurement rounds
    precision: precision of the simulation, i.e., how many times it is going to be repeated.
    space_weight: the weight for space distances when calculating the graph
    time_weight: the weight for time distances when calculating the graph
    model: model for the simulations
	2D: measurements are perfect
	3D: measurements are faulty with probability measu_error = measu_ratio * physical_error, and there are multiple measurement rounds
	3D_async: the measurements are asynchronous with probability async_error of not returning any value (value 0 in the model)
    -------------------

    Returns:

    threshold: array with the threshold values
    space_weight_final: array with the space-time weight ratio corresponding to the threshold values
    -------------------

    Important: the precision of the fitting is fixed at 6%, i.e., the relative error with the fixing must be less than 6%
    '''

    threshold = []
    space_weight_final = []
    p_fit = []
    L_fit = []
    mod = lmfit.Model(fit_function, independent_vars=['p', 'L'])

    for n in range(len(L)):
        for m in range(len(physical_error)):
	    p_fit += [physical_error[m]]
	    L_fit += [L[n]]


    for space_weight0 in space_weight:
        plot = fitting_plot(L, physical_error, measu_ratio, async_error, time, precision, space_weight0, time_weight, model)
        result = mod.fit(plot, p=p_fit, L=L_fit)

        print lmfit.fit_report(result.params, show_correl=False)

        if result.params['pth'].value > 0 and result.params['pth'].stderr/result.params['pth'].value < 0.06:
            threshold += [result.best_values['pth']]
	    space_weight_final += [space_weight0/float(time_weight)]


    return threshold, space_weight_final



def threshold_plot_3D(L, physical_error, measu_ratio, async_error, time, precision, space_weight, time_weight, model='3D_async'):

    ''' Calculates the a 3D plot for threshold values as a function of the space-time weight ratio and as a function of the measurement and physical error ratio
    -----------------

    Parameters:
    
    L: lattice size
    physical_error: the probability a qubit suffers an error
    measu_ratio: the ratio between the measurement error and qubit error
    async_error: the probability a measurement does not return any value
    time: L*times is the number of measurement rounds
    precision: precision of the simulation, i.e., how many times it is going to be repeated.
    space_weight: the weight for space distances when calculating the graph
    time_weight: the weight for time distances when calculating the graph
    model: model for the simulations
	2D: measurements are perfect
	3D: measurements are faulty with probability measu_error = measu_ratio * physical_error, and there are multiple measurement rounds
	3D_async: the measurements are asynchronous with probability async_error of not returning any value (value 0 in the model)
    -------------------

    Returns:

    threshold: array with the threshold values
    space_weight_final: array with the space-time weight ratio corresponding to the threshold values
    measu_ratio_final: array with the measurement and physical error ratio corresponding to the threshold values
    -------------------

    Important: the precision of the fitting is fixed at 6%, i.e., the relative error with the fixing must be less than 6%
    '''


    threshold = []
    measu_ratio_final = []
    space_weight_final = []
    p_fit = []
    L_fit = []
    mod = lmfit.Model(fit_function, independent_vars=['p', 'L'])

    for n in range(len(L)):
        for m in range(len(physical_error)):
	    p_fit += [physical_error[m]]
	    L_fit += [L[n]]


    for space_weight0 in space_weight:
	for measu_ratio0 in measu_ratio:
            plot = fitting_plot(L, physical_error, measu_ratio0, async_error, time, precision, space_weight0, time_weight, model)
            result = mod.fit(plot, p=p_fit, L=L_fit)

            print lmfit.fit_report(result.params, show_correl=False)

            if result.params['pth'].value > 0 and result.params['pth'].stderr/result.params['pth'].value < 0.06:
                threshold += [result.best_values['pth']]
	        space_weight_final += [space_weight0/float(time_weight)]
		measu_ratio_final += [error]


    return threshold, space_weight_final, measu_ratio_final
