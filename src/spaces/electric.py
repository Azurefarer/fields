import numpy as np

k = 8.9875517923E9      #coulommb's constant
e = 1.60217663E-19      #charge of an electron
SCALE = 1E3             #1 unit on the screen is 1mm
masse = 9.10938E-31     #mass of electron

class electricField:

    def __init__(self, particles, shape, size):
        
        self.shape = shape
        self.n = particles
        self.size = size
        self.center = [900, 500]

        self.states = np.zeros((self.n, 4))
        self.states0 = np.zeros((self.n, 4))

        self.bounds = np.array(self.center*2) + np.array([-50, -50, 50, 50])*self.size 

        if shape == 0:
                    #square
            self.boundr = np.linalg.norm((0, self.bounds[0]-self.center[0]))
            for i in range(self.n):
                rx = np.random.randint(self.bounds[0], self.bounds[2])
                ry = np.random.randint(self.bounds[1], self.bounds[3])
                self.states[i] = [rx, ry, 0, 0]
                self.states0[i] = [rx, ry, 0, 0]
        elif shape == 1:
                    #circle
            self.boundr = np.linalg.norm((0, self.bounds[0]-self.center[0]))
            for i in range(self.n):
                r = np.random.randint(0, self.boundr)
                phi = np.random.rand()*2*np.pi
                self.states[i] = [self.center[0] + r*np.cos(phi), self.center[1] + r*np.sin(phi), 0, 0]
                self.states0[i] = [self.center[0] + r*np.cos(phi), self.center[1] + r*np.sin(phi), 0, 0]
        elif shape == 2:
            self.bounds = 'rectangle'


        self.states_prime = np.zeros((self.n, 4))

        self.charges = np.zeros(self.n)
        for i in range(self.n):
            self.charges[i] = e

        self.masses = np.zeros(self.n)
        for i in range(self.n):
            self.masses[i] = masse

        self.directions = np.zeros(self.n)
        self.acceleration = np.zeros((self.n, 2))

        self.mag = 0

    def set_state(self, s):
        self.states = s

    def get_state(self):
        s = self.states
        return s

    def get_state_prime(self, s):
        z = 1
        s_dot = self.states_prime
        a = self.acceleration
        mag = self.mag
        

        for i in range(self.n):
            randa = (np.random.rand()-.5)*mag, (np.random.rand()-.5)*mag
            damp = -s[i][2]*z, -s[i][3]*z
            s_dot[i] = np.array([s[i][2], s[i][3], a[i][0] + damp[0] + randa[0], a[i][1] + damp[1] + randa[1]])

        return s_dot

    def set_acceleration(self):
        if self.shape == 0:
            self.set_acc_square()
        elif self.shape == 1:
            self.set_acc_circle()
        elif self.shape == 2:
            self.set_acc_rect()

    def set_forces(self):

        n = self.n
        forcesx = np.zeros([n, n])
        forcesy = np.zeros([n, n])

        for i in range(n):
            particle1 = self.states[i]
            forcex = 0
            forcey = 0
            phi = 0

            for j in range(i + 1, n):    
                particle2 = self.states[j]
                diffx, diffy = particle2[:2] - particle1[:2]

                d = np.linalg.norm((diffx, diffy))*SCALE/100000
                phi = np.arctan2(diffy, diffx)

                forcex = -k * self.charges[i] * self.charges[j] / d**2 * np.cos(phi)
                forcey = -k * self.charges[i] * self.charges[j] / d**2 * np.sin(phi)
                forcesx[i][j], forcesx[j][i] = forcex, -forcex
                forcesy[i][j], forcesy[j][i] = forcey , -forcey

        forcextot = forcesx.sum(axis=1)
        forceytot = forcesy.sum(axis=1)

        return forcextot, forceytot

    def set_acc_square(self):
        forcextot = self.set_forces()[0]
        forceytot = self.set_forces()[1]
        
        n = self.n

        for i in range(n):
            particle = self.states[i]

            self.directions[i] = np.arctan2(particle[3], particle[2])
            
            if particle[0] < self.bounds[0] or particle[0] > self.bounds[2]:
                self.acceleration[i] = [-forcextot[i]/self.masses[i], forceytot[i]/self.masses[i]]
                # self.directions[i] = np.pi - self.directions[i]
                particle[2] = -particle[2]
            elif particle[1] < self.bounds[1] or particle[1] > self.bounds[3]:
                self.acceleration[i] = [forcextot[i]/self.masses[i], -forceytot[i]/self.masses[i]]
                # self.directions[i] = 2*np.pi - self.directions[i]
                particle[3] = -particle[3]
            else:
                self.acceleration[i] = [forcextot[i]/self.masses[i], forceytot[i]/self.masses[i]]

    def set_acc_circle(self):
        forcextot = self.set_forces()[0]
        forceytot = self.set_forces()[1]
        
        center = np.array((self.center))
        R = self.boundr
        n = self.n

        for i in range(n):
            particle = self.states[i]
            v = np.array([particle[2], particle[3]])

            self.directions[i] = np.arctan2(particle[3], particle[2])

            diffx, diffy = particle[:2] - center

            r = np.array([diffx, diffy])

            rmag = self.get_rmag(i)
            vmag = self.get_vmag(i)
            theta = np.arccos(np.dot(v, r)/vmag/rmag)
            
            if rmag > R:
                self.acceleration[i] = [-forcextot[i]/self.masses[i]*.5, -forceytot[i]/self.masses[i]*.5]
                particle[2], particle[3] = vmag*np.cos(self.directions[i] - np.pi + 2*theta), vmag*np.sin(self.directions[i] - np.pi + 2*theta)

            else:
                self.acceleration[i] = [forcextot[i]/self.masses[i], forceytot[i]/self.masses[i]]

    def set_acc_rect(self):
        pass

    def get_rmag(self, i):
        center = np.array(self.center)
        particle = self.states[i]
        diffx, diffy = particle[:2] - center
        rmag = np.linalg.norm((diffx, -diffy))

        return rmag

    def get_vmag(self, i):
        particle = self.states[i]
        vmag = np.linalg.norm((particle[2], -particle[3]))
        return vmag

    def get_shape(self):
        return self.shape

    def get_bounds(self):
        return self.bounds

    def get_boundr(self):
        return self.boundr
    
    def get_center(self):
        return self.center

    def get_particles(self):
        return self.n

    def get_mag(self):
        return self.mag

    def get_energy(self, s):
        
        n = self.n
        u = np.zeros([n,n])
        u0 = np.zeros([n,n])

        for i in range(n):
            particle1 = s[i]
            particle10 = self.states0[i]

            for j in range(i + 1, n):    
                particle2 = s[j]
                particle20 = self.states0[j]
                diffx, diffy = particle2[:2] - particle1[:2]
                diffx0, diffy0 = particle20[:2] - particle10[:2]

                d = np.linalg.norm((diffx, diffy))*SCALE/100000
                d0 = np.linalg.norm((diffx0, diffy0))*SCALE/100000

                u[i][j] = k*self.charges[i]*self.charges[j]/d
                u0[i][j] = k*self.charges[i]*self.charges[j]/d0
        
        u_tot = u.sum()
        u0_tot = u0.sum()
        return u_tot, u0_tot


    def set_params(self):
        self.bounds = np.array(self.center*2) + np.array([-50, -50, 50, 50])*self.size
        self.boundr = np.linalg.norm((0, self.bounds[0]-self.center[0]))


    def impulse(self, direction):
        if direction == 0:
            self.mag += 250
        if direction == 1:
            self.mag -= 250
        if direction == 3:
            self.size = self.size*1.33
        if direction == 2:
            self.size = self.size*.75
        
        self.set_params()

        