import numpy as np
import matplotlib.pyplot as plt

false_positive_rate = np.load('falsepos.npy')
true_positive_rate = np.load('truepos.npy')

plt.plot(false_positive_rate, true_positive_rate, 'b')
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([0,1])
plt.ylim([0,1])
plt.show()