import hoomd
import numpy as np
#import hoomd.jit
import hoomd.hpmc_swap_plugin as swap
import scipy.stats as st
from scipy.integrate import quad
from numpy.random import uniform, normal, randint, choice, seed
seed(0)
hoomd.context.initialize("--mode=cpu --notice-level=2");
#Set their id's
#NParticles = 25**2
#Length = #*2.1

r = 0.45
d = 2
dmax = 1.0 
dmin = r*dmax
dbox = 0.1*dmax
dtrans = 0.6
#count = 0

#Define particle size distribution function
class my_pdf(st.rv_continuous):
    def _pdf(self,x):
        A = 2.0/(1/dmin**2-1/dmax**2)
        return A/x**(3)
my_cv = my_pdf(a=dmin,b=dmax,seed=1,name='my_pdf')
avgdim = my_cv.mean()

dmax = dmax/avgdim
dmin = r*dmax
dbox = 0.1*dmax
dtrans = 0.6

#Define particle size distribution function
class my_newpdf(st.rv_continuous):
    def _pdf(self,x):
        A = 2.0/(1/dmin**2-1/dmax**2)
        return A/x**(3)
my_cv = my_newpdf(a=dmin,b=dmax,seed=1,name='my_pdf')

rho = 1.00
LParticles = 32;#//32
N = LParticles*LParticles
Length =  LParticles/rho**0.5
#Length = LParticles/rho**0.5
#print(my_cv.mean())
a = Length/LParticles

NParticles = LParticles**2
Length = dmax*LParticles
MyBox = hoomd.data.boxdim(L=Length, dimensions=d)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
#Set their id's
#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=a), n=LParticles);
#snap = system.take_snapshot()
#print(snap.box)
bins = LParticles#@NParticles
deltax = (dmax-dmin)/bins 
#return A/x**(3)
dstart = dmin
dfinish = dmin+deltax
count = 0
binindex = 0
def f(x):
    return NParticles*(2.0/(1/dmin**2-1/dmax**2)/x**3)
"""
for i in range(len(snap.particles.diameter)):
    numP = int(quad(f,dstart,dfinish)[0])     #hoomd.context.current.system_definition.getParticleData().setDiameter(i,my_cv.rvs());
    hoomd.context.current.system_definition.getParticleData().setDiameter(i,uniform(dstart,dfinish));
    if (count >= numP):
        print(numP)
        count = 0
        binindex += 1
        dstart += deltax
        dfinish += deltax
    count += 1
    #hoomd.context.current.system_definition.getParticleData().setDiameter(i,dmax)#my_cv.rvs());
    #hoomd.context.current.system_definition.getParticleData().setDiameter(i,my_cv.rvs());
"""
snap.particles.types = ['A']
for i in range(LParticles):
    for j in range(LParticles):
        snap.particles.position[i*LParticles+j,0] = Length*(i/LParticles-0.5)
        snap.particles.position[i*LParticles+j,1] = Length*(j/LParticles-0.5)
        snap.particles.position[i*LParticles+j,2] = 0
        snap.particles.typeid[i*LParticles+j] = 0
        snap.particles.diameter[i*LParticles+j] = uniform(0.8,1.0)#0.5;#choice((uniform(0.1,0.4),uniform(0.7,1.0)));#(i+LParticles*j) % 2
        #snap.particles.charge[i*LParticles+j] = snap.particles.diameter[i*LParticles+j]#0.5;#choice((uniform(0.1,0.4),uniform(0.7,1.0)));#(i+LParticles*j) % 2

system = hoomd.init.read_snapshot(snap);
#mc = swap.integrate.pnt(d=0.2, seed=1,move_ratio=0.8,swap_mode='position',soft_mode='hard');#//10**6);
mc = swap.integrate.sph_poly(d=0.2, seed=1,move_ratio=0.95,swap_mode='diameter',soft_mode='hard');#//10**6);
mc.shape_param.set('A');
#boxMC = swap.update.boxmc(mc,betaP=25.0,seed=1)
#boxMC.length(delta=(dbox,dbox,0.0), weight=1.0)
patch = swap.patch.lj(mc=mc, kT=1.0, scaledr_cut=2**(1/6.0), eps=1.0,mode='force-shift')
#patch = swap.patch.ludovic(mc=mc,kT=0.25)#, scaledr_cut=2**(1/6.0), eps=1.0,mode='shifted')
#patch = swap.patch.lj(mc=mc, scaledr_cut=4.5, eps=1.0,mode='shifted')
d = hoomd.dump.gsd("trajectory_mine_position.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(1000);#//500000);
