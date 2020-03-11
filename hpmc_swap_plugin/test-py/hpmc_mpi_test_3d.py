import hoomd
import hoomd.hpmc
#import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal

hoomd.context.initialize("--mode=cpu --notice-level=2");
#Set their id's
d = 3
NParticles = 20**d
#Length = #*2.1
Length = 2.0*int(NParticles**(1/d))

LParticles = int(NParticles**(1/d))
MyBox = hoomd.data.boxdim(L=Length, dimensions=d)
snap = hoomd.data.make_snapshot(N=NParticles, box=MyBox, particle_types=['A'])
system = hoomd.init.create_lattice(unitcell=hoomd.lattice.sc(a=Length/LParticles), n=LParticles);
for i in range(len(snap.particles.diameter)):
        #hoomd.context.current.system_definition.getParticleData().setDiameter(i,choice((uniform(0.1,0.4),uniform(0.7,1.0))));#(i+LParticles*j) % 2
        hoomd.context.current.system_definition.getParticleData().setDiameter(i,0.5);#(i+LParticles*j) % 2
mc = hoomd.hpmc.integrate.sphere(d=0.2, seed=1);
mc.shape_param.set('A',diameter=0.5);
d = hoomd.dump.gsd("trajectory_3d.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(100);
