import hoomd
#import hoomd.hpmc
import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal

hoomd.context.initialize("--mode=cpu --notice-level=2");
#Set their id's
#NParticles = 100
#Length = 10.0#*2.1
#d = 2
#LParticles = int(NParticles**0.5)

system = hoomd.init.read_gsd("trajectory1_mine_3d.gsd",frame=-1)
#system = hoomd.init.read_snapshot(snap);
#print(type(system))
#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=1.05), n=10);
#print(system.sysdef)
#print(hoomd.context.current.system_definition)
#print(hoomd.context.current.system.run)
mc = swap.integrate.pnt(d=0.2, seed=1,move_ratio=0.80);
mc.shape_param.set('A');
boxMC = swap.update.boxmc(mc,betaP=100.0,seed=1)
boxMC.length(delta=(1.0,1.0,1.0), weight=4.0)
d = hoomd.dump.gsd("trajectory1_mine_3d.gsd", period=10, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(10000);
