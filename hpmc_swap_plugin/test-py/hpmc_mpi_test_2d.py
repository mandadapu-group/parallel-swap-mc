import hoomd
import hoomd.hpmc
#import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal

hoomd.context.initialize("--mode=cpu --notice-level=2");
system = hoomd.init.read_gsd("trajectory_mine_position.gsd",frame=0)
mc = hoomd.hpmc.integrate.sphere(d=0.2, seed=1);
mc.shape_param.set('A',diameter=0.5);
#boxMC = hoomd.hpmc.update.boxmc(mc,betaP=50.0,seed=1)
#boxMC.length(delta=(0.1,0.1,0.0), weight=4.0)
#logger = hoomd.analyze.log(filename='mylog.log', period=1,
#                     quantities=['pressure'])
d = hoomd.dump.gsd("trajectory1.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(100);
