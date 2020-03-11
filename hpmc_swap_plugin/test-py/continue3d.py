import hoomd
#import hoomd.hpmc
import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal, randint, choice, lognormal
import scipy.stats as st
import matplotlib.pyplot as plt
import datetime
currentDT = datetime.datetime.now()
hoomd.context.initialize("--mode=cpu --notice-level=2");
#define the particle size distribution
r = 0.4492
dmax = 1.0
dmin = r*1.0 
dtrans = 0.115
dbox = 0.005*dtrans#dtrans
A = 2.0/(1/dmin**2-1/dmax**2)
mode = 'position'

d = 3
LParticles = 10
NParticles = LParticles**d
Length = dmax*LParticles
dV = (Length+dbox)**3-Length**3 
print(dV)
snapshots = 100
runtime = 10**3
system = hoomd.init.read_gsd("dump3d.gsd",frame=-1)
mc = swap.integrate.pnt(d=dtrans, seed=1,move_ratio=0.8, swap_mode=mode);
mc.shape_param.set('A');
boxMC = swap.update.boxmc(mc,betaP=37.0,seed=1)
boxMC.volume(delta=dV, weight=1.0)
d = hoomd.dump.gsd("dump3d_2.gsd", period=runtime/snapshots, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(runtime);
lastDT = datetime.datetime.now()
print("Simulation length: {}".format(lastDT-currentDT))
