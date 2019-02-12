from matplotlib import pyplot as plt
import neurom as nm
from neurom import viewer
# Need to change path
path = './H17.06.006.11.09.04_591274508_m.swc'
nrn = nm.load_neuron(path)
fig, ax = viewer.draw(nrn, mode='3d')
ax.grid(False)
ax.axis('off')
ax.set_title('')
for angle in range(0, 360, 5):
    ax.view_init(0, angle)
    ax.set_title('')
    plt.pause(.001)

input("Press Enter to continue...")