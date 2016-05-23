import matplotlib.pyplot as plt
import numpy as np

my_plt,axes = plt.subplots(2,2)
ax1 = my_plt.add_subplot(2,2,1)
ax2 = my_plt.add_subplot(2,2,2)
ax3 = my_plt.add_subplot(2,2,3)
ax4 = my_plt.add_subplot(2,2,4)

print(axes)
ax1.plot(np.random.randn(50).cumsum(),'b--')
plt.show()

fig, ax = plt.subplots(2,2,sharex=True,sharey=True)
for i in range(2):
    for j in range(2):
        ax[i,j].hist(np.random.randn(500),bins =50, color = 'k')
plt.subplots_adjust(wspace = 0, hspace = 0)
print(ax)

plt.show()
plt.mlab