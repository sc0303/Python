import matplotlib.pyplot as plt
import numpy as np

my_plt = plt.figure()
ax1 = my_plt.add_subplot(2,2,1)
ax2 = my_plt.add_subplot(2,2,2)
ax3 = my_plt.add_subplot(2,2,3)
ax4 = my_plt.add_subplot(2,2,4)

ax1.plot(np.random.randn(50).cumsum(),'b--')