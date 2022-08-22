import pygame as pg
import numpy as np
from abc import ABC, abstractmethod


g = 9.8

class Drawer(ABC):

    def draw(self):
        pass

    def draw_data(self):
        pass

class PendulumDraw(Drawer):

    def __init__(self, Win, object):

        self.object = object
        self.Win = Win

        self.data = [50]
    
    def draw(self):

        #get neccessary variables for drawing
        state = self.object.get_state()
        axis = self.object.get_axis()
        l = self.object.get_length()
        color = self.object.get_color()
        
        #Pendulum's position
        x = axis[0] + l * np.sin(state[0])
        y = axis[1] + l * np.cos(state[0])
                    
        #drawing
        pg.draw.lines(self.Win, color, False, [(axis[0], axis[1]), (x, y)], 2)
        pg.draw.circle(self.Win, color, (x, y), 20)       
        pg.draw.circle(self.Win, (255, 255, 255), (axis[0], axis[1]), 6)


    def draw_data(self):

        state = self.object.get_state()
        Energy = self.object.get_energy(state)
        data = self.data
        scale = 1000000000000
        
        #scrolling mechanism
        #change from initial energy
        if len(data) >= 1500:
            data.pop(0)
            data.append(250 - (Energy[1] - Energy[0]) * scale)
        else:
            data.append(250 - (Energy[1] - Energy[0]) * scale)

        #pairing index values with the list values in a new list
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y) for x, y in enumerate(data)], 1)




class DblPendulumDraw(Drawer):

    def __init__(self, Win, object):

        self.object = object
        self.Win = Win

        self.data = [0]
    
    def draw(self):

        #get neccessary variables for drawing
        state = self.object.get_state()
        axis = self.object.get_axis()
        l = self.object.get_lengths()
        color = self.object.get_color()

        #first pendulum's position
        x1 = axis[0] + l[0] * np.sin(state[0])
        y1 = axis[1] + l[0] * np.cos(state[0])

        #second pendulum's position
        x2 = x1 + l[1] * np.sin(state[1])
        y2 = y1 + l[1] * np.cos(state[1])

        #drawing  
        pg.draw.lines(self.Win, color, False, [(axis[0], axis[1]), (x1, y1)], 2)
        pg.draw.circle(self.Win, color, (x1, y1), 20)       
        pg.draw.circle(self.Win, (255, 255, 255), (axis[0], axis[1]), 6)
        pg.draw.lines(self.Win, color, False, [(x1, y1), (x2, y2)], 2)
        pg.draw.circle(self.Win, color, (x2, y2), 20)     


    def draw_data(self):

        state = self.object.get_state()
        Energy = self.object.get_energy(state)
        data = self.data
        scale = 100000000
        
        #scrolling mechanism
        #change from initial energy
        if len(data) >= 1500:
            data.pop(0)
            data.append(50 + (Energy[1] - Energy[0]) * scale)
        else:
            data.append(50 + (Energy[1] - Energy[0]) * scale)

        #pairing index values with the list values in a new list
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y) for x, y in enumerate(data)], 1)



class DrawBlock(Drawer):

    def __init__(self, Win, object):

        self.Win = Win
        self.object = object

        self.data = [0]

    def draw(self):
        
        state = self.object.get_state()
        state0 = self.object.get_state0()
        color = self.object.get_color()

        x1 = state0[0] + state[0]
        y1 = state0[1] + state[1]

        pg.draw.circle(self.Win, color, (x1, y1), 20)       

    def draw_data(self):

        state = self.object.get_state()
        Energy = self.object.get_energy(state)
        data = self.data
        scale = 100000000

        #scrolling mechanism
        #change from initial energy
        if len(data) >= 1500:
            data.pop(0)
            data.append(50 + (Energy[1] - Energy[0]) * scale)
        else:
            data.append(50 + (Energy[1] - Energy[0]) * scale)

        #pairing index values with the list values in a new list
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y) for x, y in enumerate(data)], 1)

class DrawPlatform(Drawer):

    def __init__(self, Win, object):

        self.Win = Win
        self.object = object

        self.data0 = [0]
        self.data1 = [0]
        self.data2 = [0]

    def draw(self):

        width = self.object.get_width()
        length = self.object.get_length()
        state = self.object.get_state()
        off = self.object.get_offset()
        axis = self.object.get_axis()

        widthx = width * np.sin(state[0])
        widthy = width * np.cos(state[0])

        #x right and left corners
        xrc = ((length - 2 * off) / 2) * np.cos(state[0])
        xlc = ((length + 2 * off) / 2) * np.cos(state[0])

        #y top and bottom corners
        ytc = ((length - 2 * off) / 2) * np.sin(state[0])
        ybc = ((length + 2 * off) / 2) * np.sin(state[0])

        #top right -> bottom right -> bottom left -> top left
        pg.draw.polygon(self.Win, self.object.color, ([axis[0] + xrc + widthx + off, axis[1] - ytc + widthy], [axis[0] + xrc - widthx + off, axis[1] - ytc - widthy], [axis[0] - xlc - widthx + off, axis[1] + ybc - widthy], [axis[0] - xlc + widthx + off, axis[1] + ybc + widthy]))
        pg.draw.circle(self.Win, (0, 0, 0), (axis[0] + off, axis[1]), 12)

    def draw_data(self):

        state = self.object.get_state()
        Energy = self.object.get_energy(state)
        data0 = self.data0
        data1 = self.data1
        data2 = self.data2
        scale = 1000
        
        #scrolling mechanism
        #change from initial energy
        #total  energy
        if len(data0) >= 1500:
            data0.pop(0)
            data0.append((Energy[1] - Energy[0]) / scale)
        else:
            data0.append((Energy[1] - Energy[0]) / scale)

        #kinetic  energy
        if len(data1) >= 1500:
            data1.pop(0)
            data1.append((Energy[3] - Energy[2]) / scale)
        else:
            data1.append((Energy[3] - Energy[2]) / scale)

        #potential energy
        if len(data2) >= 1500:
            data2.pop(0)
            data2.append((Energy[5] - Energy[4]) / scale)
        else:
            data2.append((Energy[5] - Energy[4]) / scale)
        #pairing index values with the list values in a new list
        #total energy
        pg.draw.line(self.Win, (0, 0, 0), (0, 200), (1800, 200), 1)   
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y + 200) for x, y in enumerate(data0)], 1)
   
        #kinetic energy
        pg.draw.line(self.Win, (0, 0, 0), (0, 400), (1800, 400), 1)  
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y + 400) for x, y in enumerate(data1)], 1)

        #potential energy
        pg.draw.line(self.Win, (0, 0, 0), (0, 600), (1800, 600), 1)
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y + 600) for x, y in enumerate(data2)], 1)


class DrawCartPendulum(Drawer):

    def __init__(self, Win, object):

        self.Win = Win
        self.object = object

    def draw(self):

        w = self.object.get_width()
        l = self.object.get_lengths()
        state = self.object.get_state()
        color = self.object.get_color()

        #pendulum position
        x = state[1] + l[1] * np.sin(state[0])
        y = state[2] + l[1] * np.cos(state[0])
        #x right and left corners
        edge = l[0] / 2

        #y top and bottom corners
        # ytc = ((l[0] - 20) / 2) * np.sin(0)
        # ybc = ((l[0] + 20) / 2) * np.sin(0)

        #top right -> bottom right -> bottom left -> top left
        pg.draw.polygon(self.Win, color, ([state[1] + edge, state[2] + w], [state[1] + edge, state[2] - w], [state[1] - edge, state[2] - w], [state[1] - edge, state[2] + w]))
        pg.draw.circle(self.Win, (0, 255, 0), (state[1], state[2]), 9)

        pg.draw.lines(self.Win, (0, 0, 0), False, [(state[1] - 1, state[2] - 1), (x - 1, y - 1)], 2)
        pg.draw.circle(self.Win, color, (x, y), 10)       


    def draw_data(self):
        pass

class DrawCartPendulumInX(Drawer):

    def __init__(self, Win, object):

        self.Win = Win
        self.object = object

    def draw(self):

        w = self.object.get_width()
        l = self.object.get_lengths()
        state = self.object.get_state()
        y = self.object.get_y()
        color = self.object.get_color()

        #pendulum position
        x = state[1] + l[1] * np.sin(state[0])
        yp = y + l[1] * np.cos(state[0])
        #x right and left corners
        edge = l[0] / 2

        #y top and bottom corners
        # ytc = ((l[0] - 20) / 2) * np.sin(0)
        # ybc = ((l[0] + 20) / 2) * np.sin(0)

        #top right -> bottom right -> bottom left -> top left
        pg.draw.polygon(self.Win, color, ([state[1] + edge, y + w], [state[1] + edge, y - w], [state[1] - edge, y - w], [state[1] - edge, y + w]))
        pg.draw.circle(self.Win, (0, 255, 0), (state[1], y), 9)

        pg.draw.lines(self.Win, (0, 0, 0), False, [(state[1] - 1, y - 1), (x - 1, yp - 1)], 2)
        pg.draw.circle(self.Win, color, (x, yp), 10)       


    def draw_data(self):
        pass


class drawParticle:

    def __init__(self, Win, *args):

        self.Win = Win
        self.objs = args
        self.data = []

    def draw(self):
        for objs in self.objs:
            state = objs.get_state()[:2]
            color = objs.get_color()
            center = np.array([-30, -30])

            pg.draw.circle(self.Win, color, state, 10)
            # part_img = pg.image.load('bub.png')
            # self.Win.blit(part_img, state + center)

    def draw_data(self):
        pass

class drawField:

    def __init__(self, Win, field):

        self.Win = Win
        self.field = field
        self.FONT = pg.font.SysFont("courier", 16)
        self.data = [500]
        self.mean = []

    def draw(self):

        n = self.field.get_particles()
        states = self.field.get_state()
        center = self.field.get_center()
        shape = self.field.get_shape()
        if shape == 0:
            boundary = self.field.get_bounds()
            pg.draw.rect(self.Win, (10, 90, 40), (boundary[0]-4, boundary[1]-4, boundary[2]-boundary[0]+8, boundary[3]-boundary[1]+8))
        elif shape == 1:      
            boundary = self.field.get_boundr()
            pg.draw.circle(self.Win, (10, 90, 40), center, boundary + 4)

        for i in range(n):
            pg.draw.circle(self.Win, (200, 200, 200), states[i][:2], 5)

    def draw_data(self, n):
        state = self.field.get_state()
        Energy = self.field.get_energy(state)

        data = self.data
        meanlist = self.mean
        mag = self.field.get_mag()
        average = 0
        scale = 1E29

        #scrolling mechanism
        #change from initial energy
        if len(data) >= 1500:
            data.pop(0)
            data.append(500 + (Energy[1] - Energy[0])*scale)
        else:
            data.append(500 + (Energy[1] - Energy[0])*scale)

        if n > 100:
            meanlist.append(Energy[0])

            average = sum(meanlist)/(n-100)

        #pairing index values with the list values in a new list
        energytext = self.FONT.render(f"Current  {round(Energy[0]*10**28, 3)}*10^-28J", 1, (200, 200, 200))
        meantext = self.FONT.render(f"Mean     {round(average*10**28, 3)}*10^-28J", 1, (200, 200, 200))
        magtext = self.FONT.render(f"Noise    {mag}", 1, (200, 200, 200))
        pg.draw.lines(self.Win, (255, 255, 255), False, [(x + 150, y) for x, y in enumerate(data)], 1)
        self.Win.blit(energytext, (100, 100))
        self.Win.blit(meantext, (100, 125))
        self.Win.blit(magtext, (100, 150))
        