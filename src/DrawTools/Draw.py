import pygame as pg
import numpy as np
from abc import ABC, abstractmethod


g = 9.8

WHITE = [255, 255, 255]

class Drawer(ABC):

    def draw(self):
        pass

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
            size = objs.get_size()
            center = np.array([-30, -30])

            pg.draw.circle(self.Win, color, state, size)
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
        psize = self.field.get_psizes()
        colors = self.field.get_colors()
        if shape == 0:
            boundary = self.field.get_bounds()
            pg.draw.rect(self.Win, (10, 90, 40), (boundary[0]-4, boundary[1]-4, boundary[2]-boundary[0]+8, boundary[3]-boundary[1]+8))
        elif shape == 1:      
            boundary = self.field.get_boundr()
            pg.draw.circle(self.Win, (10, 90, 40), center, boundary + 4)

        for i in range(n):
            pg.draw.circle(self.Win, colors[i], states[i][:2], psize[i])

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
        