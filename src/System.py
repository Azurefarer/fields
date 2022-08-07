import numpy as np


class System:

    def __init__(self, *args):
        
        self.args = args

    def set_state(self, s):
        
        j = 0
        for object in self.args:
            object.set_state(s[j:j + object.get_state_size()])
            j += object.get_state_size()
        

    def get_state(self):
        s = []
        for object in self.args:
            for j in range(object.get_state_size()):
                s.append(object.get_state()[j])

        return np.array(s)


    def get_state_prime(self, s):
        k = 0
        s_dot = np.array([])
        for object in self.args:

            state_slice = s[k:k + object.get_state_size()]
            object_state = object.get_state_prime(state_slice)
            s_dot = np.concatenate((s_dot, object_state))
            k += object.get_state_size()

        return np.array(s_dot)


    def get_state_size(self):

        size = 0
        for i in range(len(self.args)):
            size += self.args[i].get_state_size()

        return size
