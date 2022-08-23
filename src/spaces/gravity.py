import numpy as np

G = 6.6743E-11

class gravitationalField:

    def __init__(self, *args):

        self.particle = args

    def set_force(self):
        obj = self.particle
        n = len(obj)
        forcesx = np.zeros([n, n])
        forcesy = np.zeros([n, n])
        for i in range(len(obj)):
            particle1 = obj[i]
            forcex = 0
            forcey = 0
            phi = 0

            for j in range(i + 1, len(obj)):    
                particle2 = obj[j]
                collision_param = obj[i].get_size() +  obj[j].get_size()
                diffx, diffy = particle2.get_state()[:2] - particle1.get_state()[:2]

                d = np.linalg.norm((diffx, diffy))

                phi = np.arctan2(diffy, diffx)

                forcex = G * particle1.get_mass() * particle2.get_mass() / d**2 * np.cos(phi)
                forcey = G * particle1.get_mass() * particle2.get_mass() / d**2 * np.sin(phi)
                if d <= collision_param:
                    forcex, forcey = -forcex, -forcey
                forcesx[i][j], forcesx[j][i] = forcex, -forcex
                forcesy[i][j], forcesy[j][i] = forcey , -forcey




        forcextot = forcesx.sum(axis=1)
        forceytot = forcesy.sum(axis=1)

        for i in range(len(obj)):
            force = []
            force.append(forcextot[i])
            force.append(forceytot[i])
            obj[i].set_acc(force)


