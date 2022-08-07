import pygame as pg
import numpy as np
from abc import ABC, abstractmethod
from DrawTools.Draw import *

class DrawSystem(Drawer):

    def __init__(self, *args):

        self.args = args

    def draw(self):

        for drawing in self.args:
            drawing.draw()

    def draw_data(self):

        for data in self.args:
            data.draw_data()
