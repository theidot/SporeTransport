#!/usr/bin/env python3

import argparse, sys
import numpy as np
from AdvTrans1DIntegrator import *

class TransParser(argparse.ArgumentParser):

    def __init__(self):
        super(TransParser, self).__init__(description="""Finite difference simulation of initial value\n
                                                         problem for 1D advective transport equation with\n
                                                         periodic boundary conditions""")

        self.add_argument('-N', '--time-steps', type = int, dest = 'time_steps', default = 1000,
                          help = 'Number of time points (not intervals)')
        self.add_argument('-t', '--delta-t', type = float, dest = 'dt', default = 0.05,
                          help = 'Time step (float)')
        self.add_argument('-J', '--grid-points', type = int, dest='grid_points', default = 1000,
                          help = 'Number of grid points (not intervals)')
        self.add_argument('-x', '--delta-x', type = float, dest = 'dx', default = 0.05,
                          help = 'Grid spacing (float)')
        self.add_argument('-v', '--velocity', type = float, dest = 'velocity', default = 0.9,
                          help = 'Velocity (float)')
        self.add_argument('-i', '--initial-condition', dest = 'ic', type = str,
                          default = 'lambda x : 0.0 if x < 1 or x > 2 else 1.0',
                          help = 'Initial condition as a string for eval()')
        self.add_argument('-m', '--method', choices = ['U', 'LF', 'LW'], default = 'U', dest = 'method',
                          help = 'Integration method (string)')
        self.add_argument('-u', '--update-frequency', type = int, dest = 'graphics_update', default = 10,
                          help = 'Update frequency for graphics (integer, number of timesteps)')

def main(args):
    x = args.dx*np.arange(0, args.grid_points, dtype=np.double)

    Peclet = args.velocity*args.dt/args.dx
    f = eval(args.ic)
    u = np.array([f(xi) for xi in x])

    if args.method == 'U':
        integrator = UpwindEulerAdvectiveTransport(x)
    elif args.method == 'LF':
        integrator = LaxFriedrichsAdvectiveTransport(x)
    elif args.method == 'LW':
        integrator = LaxWendroffAdvectiveTransport(x)
    else:
        raise NotImplementedError('Integration method "{0}" not implemented'.format(args.method))

    #
    # Time stepping loop
    #
    for n in range(args.time_steps):
        
        # Periodically compute error and update plot
        if n % args.graphics_update == 0:
            w = np.array([f(xi-args.velocity*n*args.dt) for xi in x])
            integrator.clear_graphics()
            integrator.update_graphics(u, n*args.dt, w)
            integrator.pause(0.001)

        #
        # Take timestep
        #
        u = integrator.timestep(u, Peclet)

    integrator.pause(2.0)
    
    return 0

if __name__ == '__main__':
    parser = TransParser()
    ns = parser.parse_args()

    rc = 1
    try:
        rc = main(ns)
    except KeyboardInterrupt as e:
        print('Exiting early...\n', e, file = sys.stderr)
    except Exception as e:
        print('Serious problem...\n', e, file = sys.stderr)        
    finally:
        sys.exit(rc)
    
