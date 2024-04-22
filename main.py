import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from Steiner_Sym import Steiner_Symetrisation
import random

init_points = [(-49, -21),
          (-5, 45),
          (21, 15)]

NB_SYMETRISATION = 15  # number of symetrisation before stop
PRECISION = 0.1   # width between points
INTERVAL = 3000 # ms bewtween symetrisation


steiner = Steiner_Symetrisation(init_points, base_norme=PRECISION)


fig, ax = plt.subplots(1, 1)
ax.set_xlim([-50,50])
ax.set_ylim([-50,50])

fig.set_size_inches(5,5)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

def print_perso(lst):
    for i in range(len(lst)):
        print(f"({round(lst[i][0], 3)}, {round(lst[i][1], 3)})", end=" ")
    print()

def animate(i):
    global steiner
    ax.clear()
    ax.set_xlim([-50,50])
    ax.set_ylim([-50,50])
    x_random = random.random()*2 - 1
    y_random = random.random()*2 - 1
    if i > 0:
        steiner.symmetrization(x_random, y_random)
        a = -x_random/y_random
        ax.plot([-50, 50], [-50*a, + 50*a])
    lst = steiner.get_points()
    p = Polygon(lst, closed=True, ec='r', fill=False)
    ax.add_patch(p)


if __name__ == "__main__":
    anim = FuncAnimation(fig, animate, frames=NB_SYMETRISATION , interval=INTERVAL, repeat=False)
    plt.show()
    plt.close()

