import numpy as np
from matplotlib import pyplot as plt

class Integrator(object):

    def __init__(self, xgrid):
        self.init_graphics()
        self.__x = np.copy(xgrid)
        
    def init_graphics(self):
        self.fig = plt.figure()
        self.ax  = self.fig.gca()
        plt.ion()
        plt.show()

    def grid(self):
        return np.copy(self.__x)

    def update_graphics(self, u, t, w):

        #
        # Update plot and pause
        #
        plt.ylim([-0.1, 1.1])
        plt.plot(self.__x, u, 'k')
        plt.plot(self.__x, w, 'r')            
        plt.title('t={0:.4f}'.format(t))

    def pause(self, viewing_delay= 0.01):
        plt.pause(viewing_delay)

    def clear_graphics(self):
        self.fig.clf()

    def timestep(self, *args, **kwargs):
        raise NotImplementedError('timestep() method must be overridden in derived classes')

class UpwindEulerAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(UpwindEulerAdvectiveTransport, self).__init__(xgrid)
        
    def timestep(self, u, Peclet):
        up = np.roll(u, -1)
        return u - Peclet*(up-u)

class LaxFriedrichsAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(LaxFriedrichsAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        up = np.roll(u, -1)
        um = np.roll(u, +1)
        return 0.5*(up + um) - 0.5*Peclet*(up - um)

class LaxWendroffAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(LaxWendroffAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        up = np.roll(u, -1)
        um = np.roll(u, +1)
        return u - 0.5*Peclet*(up-um) + 0.5*Peclet*Peclet*(up - 2.0*u + um)

