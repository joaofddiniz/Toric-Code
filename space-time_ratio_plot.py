# Calculates threshold values of a given model as a function of space-time weight ratio

import numpy as np
import matplotlib.pyplot as plt
import plotting
import time

start = time.time()

L = [4, 6, 8]
precision = 10000
physical_error = np.linspace(0.025, 0.035, 20)
t = 1
space_weight = np.arange(1, 50)
time_weight = 25
async_error = [0.1]
measu_ratio = 1


for async_error0 in async_error:
    threshold, space_weight_final = plotting.threshold_plot(L, physical_error, measu_ratio, async_error0, t, precision, space_weight, time_weight, '3D')

    np.savetxt('threshold--measu_ratio=%s.txt' % (measu_ratio), threshold)
    np.savetxt('space_weight--measu_ratio=%s.txt' % (measu_ratio), space_weight_final)

    fig, ax = plt.subplots()
    ax.plot(space_weight_final, threshold, 'ro')
    ax.set_xlabel('space / time weight')
    ax.set_ylabel('threshold')
    plt.title('measu ratio = %s' % (measu_ratio))
    plt.savefig('///home/jd16456/threshold--measu_ratio={0}.png'.format(measu_ratio), bbox_inches='tight')
    print (time.time() - start)
    plt.show()

