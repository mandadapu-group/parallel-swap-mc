import hoomd
#import hoomd.hpmc
import hoomd.hpmc_swap_plugin as swap
from numpy.random import uniform, normal, randint, choice

hoomd.context.initialize("--mode=cpu");
system = hoomd.init.read_gsd("trajectory_mine.gsd",frame=0)
mc = swap.integrate.pnt(d=0.2, seed=1,move_ratio=1);
d = hoomd.dump.gsd("trajectory_mine.gsd", period=1, group=hoomd.group.all(), dynamic=['attribute'],overwrite=True);
hoomd.run(100);
