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
dbox = 0.5*dtrans#dtrans
A = 2.0/(1/dmin**2-1/dmax**2)
mode = 'position'

class my_pdf(st.rv_continuous):
    def _pdf(self,x):
        return A/x**(3)
my_cv = my_pdf(a=dmin,b=dmax,name='my_pdf')
#Set their id's
d = 3
LParticles = 10
NParticles = LParticles**d
Length = dmax*LParticles
rho = NParticles/Length**d
MyBox = hoomd.data.boxdim(L=Length, dimensions=d)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sc(a=Length/LParticles), n=LParticles);
for i in range(len(snap.particles.diameter)):
    hoomd.context.current.system_definition.getParticleData().setDiameter(i,my_cv.rvs());#(i+LParticles*j) % 2
snapshots = 100
runtime = 10**4
betaP = 37*rho
print("betaP is: {}".format(37*rho))
mc = swap.integrate.pnt(d=dtrans, seed=1,move_ratio=0.8, swap_mode=mode);
mc.shape_param.set('A');
boxMC = swap.update.boxmc(mc,betaP=betaP,seed=1)
boxMC.length(delta=(dbox,dbox,dbox), weight=1.0)
d = hoomd.dump.gsd("dump3d.gsd", period=runtime/snapshots, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(runtime);
lastDT = datetime.datetime.now()
print("Simulation length: {}".format(lastDT-currentDT))
