import hoomd
import hoomd.hpmc
#import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal

hoomd.context.initialize("--mode=cpu");
#Set their id's
NParticles = 10**2
#Length = #*2.1
d = 2
Length = int(NParticles**0.5)
LParticles = int(NParticles**0.5)
MyBox = hoomd.data.boxdim(L=Length, dimensions=d)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
#count = 0
for i in range(LParticles):
    for j in range(LParticles):
        snap.particles.position[i*LParticles+j,0] = Length*(i/LParticles-0.5)
        snap.particles.position[i*LParticles+j,1] = Length*(j/LParticles-0.5)
        snap.particles.position[i*LParticles+j,2] = 0
        snap.particles.diameter[i*LParticles+j] = 0.5;#uniform(0.2,1.0);#(i+LParticles*j) % 2

system = hoomd.init.read_snapshot(snap);
#print(type(system))
#system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sq(a=int(Length/LParticles)), n=LParticles);
#print(system.particles.diameter)#.diameter)
#print(system.sysdef)
#print(hoomd.context.current.system_definition)
#print(hoomd.context.current.system.run)
mc = hoomd.hpmc.integrate.sphere(d=0.2, seed=1,move_ratio=1);
mc.shape_param.set('A', diameter=0.5);
d = hoomd.dump.gsd("trajectory.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(100);
