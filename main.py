import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from Steiner_Sym import Steiner_Symetrisation
import random
import math


INIT_POINTS = [(-49, -5),
            (0,0),
          (-5, 45),
          (5, 15),
          (21, 15)]

NB_SYMETRISATION = -1       # number of symetrisation before stop, -1 for infinity
PRECISION = 0.1              # width between points
INTERVAL = 5000              # ms bewtween symetrisation
RANDOM_DIRECTIONS = True   # if True the directions will be random
DIRECTIONS = [(-0.55, 0.8),(0.65, 0.39),(-0.5, -0.32)]   # else we use thoses directions
APPROXIMATE = False  # if True the algorithme will approximate the symetrization
# else the values will be more exact but a lot of points will be created



def print_perso(lst):
    for i in range(len(lst)):
        print(f"({round(lst[i][0], 3)}, {round(lst[i][1], 3)})", end=" ")
    print()

# global variable to use inside animate
fig, ax = plt.subplots(1, 1)
steiner = Steiner_Symetrisation(INIT_POINTS, base_norme=PRECISION)
steiner.poly.convexHull()
index_direction = 0
radius = math.sqrt(steiner.get_volume()/math.pi)
circle = plt.Circle((0, 0), radius, color='g', fill=False)

def animate(i):
    global steiner
    global index_direction

    
    ax.clear()
    ax.set_xlim([-50,50])
    ax.set_ylim([-50,50])
    
    # choose of x_dir and y_dir
    if RANDOM_DIRECTIONS:
        x_dir = random.random()*2 - 1
        y_dir = random.random()*2 - 1
        print("dir = ", x_dir, y_dir)
    else:
        x_dir, y_dir = DIRECTIONS[index_direction]
        index_direction = (index_direction + 1 )% len(DIRECTIONS)

    # symmetrization
    if i > 0:
        if APPROXIMATE:
            steiner.symmetrization_approximated(x_dir, y_dir)
        else:
            steiner.symmetrization_correct(x_dir, y_dir)
        a = -x_dir/y_dir
        ax.plot([-50, 50], [-50*a, +50*a])
    ax.text(28, 55, f"perimeter : {round(steiner.get_perimeter(), 2)}")
    ax.text(-10, 55, f"circle perimeter : {round(2*math.pi*radius,2)}")
    ax.text(-40, 55, f"area : {round(steiner.get_volume(), 2)}")
    
    lst = steiner.get_points()
    ax.text(-10, -45, f"nb_points : {len(lst)}")
    p = Polygon(lst, closed=True, ec='r', fill=False)
    ax.add_patch(circle)
    ax.add_patch(p)
    

if __name__ == "__main__":
    ax.set_xlim([-50,50])
    ax.set_ylim([-50,50])
    
    anim = FuncAnimation(fig, animate, frames= 1000 if NB_SYMETRISATION == -1 else NB_SYMETRISATION+1, interval=INTERVAL, repeat=(NB_SYMETRISATION == -1))

    plt.show()
    plt.close()

