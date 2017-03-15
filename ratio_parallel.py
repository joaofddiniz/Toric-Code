import numpy as np
import matplotlib.pyplot as plt
import plotting_parallel as plotting
#import multiprocessing as mp
from joblib import Parallel, delayed

precision = 10000
t = 1
error_ratio = 1
space_weight = np.arange(1, 10)
time_weight = 1
p = np.linspace(0.025, 0.035, 10)
L = [4, 6, 8]

#pool = mp.Pool(processes=len(space_weight))
#results = [pool.apply_async(plotting.threshold_plot, args = (L, p, t, precision, error_ratio, space_weight0, time_weight)) for space_weight0 in space_weight]

result = Parallel(n_jobs=-1)(delayed(plotting.threshold_plot)(L, p, t, precision, error_ratio, space_weight0, time_weight) for space_weight0 in space_weight)

threshold = []
space_weight = []
for n in range(len(result)):
    if result[n] is not None:
        threshold += [result[n][0]]
        space_weight += [result[n][1]]


fig, ax = plt.subplots()
ax.plot([space/float(time_weight) for space in space_weight], threshold, 'ro')
ax.set_xlabel('space weight / time weight')
ax.set_ylabel('threshold')
plt.title('measurement error / qubit error = %.2g' % error_ratio)
plt.show()

