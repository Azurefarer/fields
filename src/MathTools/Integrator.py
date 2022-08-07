import numpy as np

class EulerIntegrator:

    def __init__(self, object):
        
        self.object = object


    def integrate(self, x, dt):

        x_dot = self.object.get_state_prime(x)
        x_1 = x + x_dot * dt

        return x_1


#4th order Runge Kutta integrator
class RK4Integrator:

    def __init__(self, object):
        
        self.object = object


    def integrate(self, x, dt):

        #get state prime 4 times
        x_dot1 = self.object.get_state_prime(x)
        k_1 = x_dot1

        x_dot2 = self.object.get_state_prime(x + k_1 * dt/2)
        k_2 = x_dot2 

        x_dot3 = self.object.get_state_prime(x + k_2 * dt/2)
        k_3 = x_dot3

        x_dot4 = self.object.get_state_prime(x + k_3 * dt)
        k_4 = x_dot4

        return x + 1/6 * ((k_1) + (k_2 * 2) + (k_3 * 2) + (k_4)) * dt
