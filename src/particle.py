import numpy as np

class particle:

    def __init__(self, mass, x, y, v, size, color):

        self.size = size
        self.mass = mass
        self.x = x
        self.y = y

        self.state = [x, y, v[0], v[1]]
        self.state0 = [x, y, v[0], v[1]]

        self.acceleration = []

        self.color = color

    def set_state(self, s):
        self.acceleration = []
        self.state = s

    def get_state(self):

        s = np.array(self.state)

        return s

    def get_state_prime(self, s):

        ax = self.acceleration[0]
        ay = self.acceleration[1]
        s_dot = np.array([s[2], s[3], ax, ay])

        return s_dot

    def set_acc(self, force):
        self.acceleration.append(force[0]/self.mass)
        self.acceleration.append(force[1]/self.mass)

    def get_mass(self):
        return self.mass

    def get_color(self):
        return self.color

    def get_state_size(self):
        return 4

    def get_size(self):
        return self.size
        
    def impulse(self):
        pass