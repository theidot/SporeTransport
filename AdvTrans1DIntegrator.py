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

    def delta_plus(self, u):
        return np.roll(u, -1) - u

    def delta_zero(self, u):
        return np.roll(u, -1) - np.roll(u, 1)

    def delta_minus(self, u):
        return u - np.roll(u, 1)

    def delta_square(self, u):
        return np.roll(u, -1) - 2.0*u + np.roll(u, 1)

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
        um = np.roll(u, 1)
        return u - Peclet*self.delta_minus(u)

class LaxFriedrichsAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(LaxFriedrichsAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        up = np.roll(u, -1)
        um = np.roll(u, +1)
        return 0.5*(up + um) - 0.5*Peclet*self.delta_zero(u)

class LaxWendroffAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(LaxWendroffAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        return u - 0.5*Peclet*self.delta_zero(u) + 0.5*Peclet*Peclet*self.delta_square(u)

class BeamWarmingAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(BeamWarmingAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        ustar = u - Peclet*self.delta_minus(u)
        return 0.5*(u + ustar - Peclet*self.delta_minus(ustar) - Peclet*self.delta_square(np.roll(u, 1)))

class MacCormackAdvectiveTransport(Integrator):

    def __init__(self, xgrid):
        super(MacCormackAdvectiveTransport, self).__init__(xgrid)

    def timestep(self, u, Peclet):
        ustar = u - Peclet*self.delta_plus(u)
        return 0.5*(u + ustar - Peclet*self.delta_minus(ustar))

    

