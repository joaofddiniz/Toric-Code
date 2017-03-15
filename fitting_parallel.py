import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
import plotting_parallel
#import multiprocessing as mp
from joblib import Parallel, delayed


precision = 3000
t = 1
p = np.linspace(0.027, 0.033, 10)
L = [4, 6, 8]
space_weight = 1
time_weight = 1
error_ratio = 1


shape1 = ['ro', 'bo', 'go', 'yo']
shape2 = ['r-', 'b-', 'g-', 'y-']
p_plot = []
L_plot = []

for n in range(len(L)):
    for m in range(len(p)):
	p_plot += [p[m]]
	L_plot += [L[n]]


pool = mp.Pool(processes=len(p))
parallel_result = [pool.apply_async(plotting.fitting_plot, args = (L, [p0], t, precision, error_ratio, space_weight, time_weight)) for p0 in p]
plot = []

result = Parallel(n_jobs=-1)(delayed(plotting.threshold_plot)(L, p, t, precision, error_ratio, space_weight0, time_weight) for space_weight0 in space_weight)

for m in range(len(L)):
    for n in parallel_result:
        plot += [n.get()[m]]


mod = Model(plotting.fit, independent_vars=['p', 'L'])
fit_result = mod.fit(plot, p=p_plot, L=L_plot)


fig, ax = plt.subplots()
for i in range(len(L)):
    ax.plot(100*p, plot[len(p)*i:len(p)*(i+1)], shape1[i])
    ax.plot(100*p, fit_result.best_fit[len(p)*i:len(p)*(i+1)], shape2[i], label='L = %s' % L[i])


print result.fit_report(show_correl=False)
legend = ax.legend(loc='upper right', shadow=True)	
ax.set_xlabel('error probability (%)')
ax.set_ylabel('Decoding success rate')
plt.title('threshold = %.4g %%' % (100*fit_result.best_values['pth']))
plt.show()

