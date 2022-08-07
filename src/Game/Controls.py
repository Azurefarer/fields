import pygame as pg
from abc import ABC, abstractmethod

pg.init()

class UIcontroller:

    def __init__(self, *args):
        
        self.args = args
        self.object = 0

    def inputs(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.object += 1
                if self.object >= len(self.args):
                    self.object = 0
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.object -= 1
                if self.object < 0:
                    self.object = len(self.args) - 1
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.args[self.object].impulse(0)
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.args[self.object].impulse(1)
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                self.args[self.object].impulse(2)
            elif event.type == pg.KEYDOWN and event.key == pg.K_w:
                self.args[self.object].impulse(3)
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                self.args[self.object].impulse(4)
            elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                self.args[self.object].impulse(5)
            
