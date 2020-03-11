import gsd.hoomd
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import numba as nb
from numba import float64
from scipy.spatial import cKDTree
from scipy.integrate import quad, cumtrapz

with gsd.hoomd.open("trajectory_mine_position.gsd", "rb") as traj, gsd.hoomd.open("trajectory_mine_diameter.gsd", "rb") as trajis:
    position = []
    positionIS = []
    for k in range(len(traj[:])):
        n_particles = traj[k].particles.N
        l_particles = int(n_particles**0.5)
        boxsize = traj[k].configuration.box[0]
        
        position.append(traj[k].particles.position[10,0:2]+boxsize/2.0)
        positionIS.append(trajis[k].particles.position[10,0:2]+boxsize/2.0)
    position = np.array(position)
    positionIS = np.array(positionIS)
    #plt.plot(np.sqrt(position[:,0]**2+position[:,1]**2)-np.sqrt(position[0,0]**2+position[0,1]**2),label="Swapping positions")
    #plt.plot(np.sqrt(positionIS[:,0]**2+positionIS[:,1]**2)-np.sqrt(positionIS[0,0]**2+positionIS[0,1]**2),label="Swapping diameters")
    plt.plot(position[:,0],position[:,1],label="Swapping diameters")
    plt.plot(positionIS[:,0],positionIS[:,1],label="Swapping diameters")
    plt.show()
