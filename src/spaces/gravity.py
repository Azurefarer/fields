import numpy as np

G = 6.6743E-11

class gravitationalField:

    def __init__(self, *args):

        self.particle = args

    def set_force(self):

        for particle1 in self.particle:
            forcex = 0
            forcey = 0
            phi = 0
            for particle2 in self.particle:
                if particle1 is not particle2:
                    diffx, diffy = particle2.get_state()[:2] - particle1.get_state()[:2]
                    diffy = diffy * -1
                    d = np.linalg.norm((diffx, diffy))
                    if diffx == 0:
                        forcex += 0
                    elif diffx < 0:
                        forcex += -G * particle1.get_mass() * particle2.get_mass() / d**2
                    elif diffx > 0:
                        forcex += G * particle1.get_mass() * particle2.get_mass() / d**2
                    if diffy == 0:
                        forcey += 0
                    elif diffy > 0:
                        forcey += -G * particle1.get_mass() * particle2.get_mass() / d**2
                    elif diffy < 0:
                        forcey += G * particle1.get_mass() * particle2.get_mass() / d**2
                else:
                    pass
            force = np.linalg.norm((forcex, forcey))
            if forcex < 0:
                phi = np.arctan(forcey/forcex) + np.pi
            elif  forcex > 0:
                phi = np.arctan(forcey/forcex)
            elif forcex == 0:
                phi = 0
            particle1.set_acc(force, phi)

