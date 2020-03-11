import hoomd
#import hoomd.hpmc
import numpy as np
import hoomd.hpmc_swap_plugin as swap

hoomd.context.initialize("--mode=cpu --notice-level=2");
LParticles = 25
r = 0.45
d = 2
dmax = 1.0 
dmin = r*dmax
dbox = 0.05*dmax
dtrans = 0.6
#Set their id's
#NParticles = 100
#Length = 10.0#*2.1
#d = 2
#LParticles = int(NParticles**0.5)

system = hoomd.init.read_gsd("trajectory_mine_position.gsd",frame=-1)
#snap = system.take_snapshot()
#for i in range(len(snap.particles.diameter)):
#    hoomd.context.current.system_definition.getParticleData().setType(i,0);
#print(type(system))
#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=1.05), n=10);
#print(system.sysdef)
#print(hoomd.context.current.system_definition)
#print(hoomd.context.current.system.run)
#mc = swap.integrate.pnt(d=dtrans, seed=1,move_ratio=0.8,swap_mode='position',soft_mode='soft');#//10**6);
#mc = swap.integrate.pnt(d=dtrans, seed=1,move_ratio=0.0,swap_mode='position',soft_mode='hard');#//10**6);
mc = swap.integrate.sph_poly(d=dtrans, seed=1,move_ratio=0.95,swap_mode='diameter',soft_mode='hard');#//10**6);
mc.shape_param.set('A');
#boxMC = swap.update.boxmc(mc,betaP=10**12,seed=1)
#boxMC.length(delta=(dbox,dbox,0.0), weight=1.0)
#patch = swap.patch.lj(mc=mc, scaledr_cut=2**(1/6.0), eps=1.0,mode='shifted')
#patch = swap.patch.ludovic(mc=mc, kT=0.025)#, scaledr_cut=2**(1/6.0), eps=1.0,mode='shifted')
d = hoomd.dump.gsd("test_1.gsd", period=120000, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(12000000);
