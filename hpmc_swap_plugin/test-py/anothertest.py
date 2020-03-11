import hoomd
#import hoomd.hpmc
import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal

hoomd.context.initialize("--mode=cpu --notice-level=9");
#Set their id's
#NParticles = 100
#Length = 10.0#*2.1
#d = 2
#LParticles = int(NParticles**0.5)

system = hoomd.init.read_gsd("trajectory.gsd",frame=0)
#system = hoomd.init.read_snapshot(snap);
#print(type(system))
#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=1.05), n=10);
#print(system.sysdef)
#print(hoomd.context.current.system_definition)
#print(hoomd.context.current.system.run)
mc = swap.integrate.pnt(d=0.5, seed=1);
mc.shape_param.set('A', maxdiameter=1.0);
d = hoomd.dump.gsd("trajectory1.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(100);
