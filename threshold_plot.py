# Calculates the success rate of a given model for each physical error, and hence obtaining a single threshold value

import numpy as np
import matplotlib.pyplot as plt
import lmfit
import plotting


precision = 10000
t = 1
physical_error = np.linspace(0.016, 0.02, 20)
L = [4, 6, 8]

shape1 = ['ro', 'bo', 'go', 'yo']
shape2 = ['r-', 'b-', 'g-', 'y-']
p_fit = []
L_fit = []

for n in range(len(L)):
    for m in range(len(physical_error)):
	p_fit += [physical_error[m]]
	L_fit += [L[n]]


mod = lmfit.Model(plotting.fit_function, independent_vars=['p', 'L'])

space_weight = np.arange(1, 2)
time_weight = 1
async_error = [0.1]
measu_ratio = 0.1


for space_weight0 in space_weight:
    for async_error0 in async_error:

	plot = plotting.fitting_plot(L, physical_error, measu_ratio, async_error0, t, precision, space_weight0, time_weight, '3D_async')

	fit_result = mod.fit(plot, p=p_fit, L=L_fit)
	print lmfit.fit_report(fit_result.params, show_correl=False)

	fig, ax = plt.subplots()
	for i in range(len(L)):
    	    ax.plot(100*physical_error, plot[len(physical_error)*i:len(physical_error)*(i+1)], shape1[i])
            ax.plot(100*physical_error, fit_result.best_fit[len(physical_error)*i:len(physical_error)*(i+1)], shape2[i], label='L = %s' % L[i])

	legend = ax.legend(loc='upper right', shadow=True)
	ax.set_xlabel('physical error probability (%)')
	ax.set_ylabel('decoding success rate')
#	ax.set_xlim([2.7, 3.3])
#	plt.title('threshold = %.4g %%; space/time ratio = %s; t = %s' % (100*fit_result.best_values['pth'], float(space_weight0)/time_weight, t))
	plt.title('threshold = %.4g %%; async error = %s; space/time ratio = %s' % (100*fit_result.best_values['pth'], async_error, float(space_weight0)/time_weight))
#	plt.savefig('///home/jd16456/Documents/async_error_{0}-spacetime_ratio_{1}-t_{2}.png'.format(async_error, float(space_weight0)/time_weight, t), bbox_inches='tight')
#	plt.savefig('///home/jd16456/Figure7.png', bbox_inches='tight')
	plt.show()
	plt.close(fig)

