import numpy as np
import toric_code_fast as toric
import lmfit


def fit(p, L, a=0.9, b=-1.5, c=-5., pth=0.03, v=0.7):
    return a + b*(p - pth)*np.power(L, 1./v) + c*(p - pth)**2*np.power(L, 2./v)


def fitting_plot(L, p, t, precision, error_ratio, space_weight, time_weight, model='3D'):

    plot = []

    for L0 in L:
        for p0 in p:
            success = 0
            for n in xrange(precision):

		if model == '3D':
                    code = toric.toric_code_3D(L0, p0, error_ratio*p0, t*L0, space_weight, time_weight)
	            code.create_lattice()
	            code.get_syndrome()

		elif model == '2D':
		    code = toric.toric_code_2D(L0, p0)
		    code.create_lattice()
		    code.get_syndrome_position()

	        code.correct_syndrome()
                success += code.verify_logical_error()

            plot += [float(success)/precision]

    return plot


def threshold_plot(L, p, t, precision, error_ratio, space_weight, time_weight, show_report=True):

    p_plot = []
    L_plot = []
    mod = lmfit.Model(fit, independent_vars=['p', 'L'])

    for n in xrange(len(L)):
        for m in xrange(len(p)):
	    p_plot += [p[m]]
	    L_plot += [L[n]]


    plot = fitting_plot(L, p, t, precision, error_ratio, space_weight, time_weight)
    result = mod.fit(plot, p=p_plot, L=L_plot)

    if show_report == True:
        print lmfit.fit_report(result.params, show_correl=False)

    if result.params['pth'].stderr/result.params['pth'].value < 0.02:
        return result.best_values['pth'], space_weight



