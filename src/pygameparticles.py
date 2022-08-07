import sys
import pygame as pg
import numpy as np
from spaces.gravity import gravitationalField as gf
from particle import particle
from MathTools.Integrator import RK4Integrator as RK4
from DrawTools.Draw import *
from DrawTools.DrawSystem import *
from System import System
from Game.Controls import *

pg.init()

#in millimeters
Width, Height = 1800, 1000  
Win = pg.display.set_mode((Width, Height))
pg.display.set_caption("Gravitational Field")


def main():
    run = True
    clock = pg.time.Clock()

    #init objects, system, integrator, drawers, system drawer, and controller
    a = particle(3E13, 1200, 200, [-3, 0], (200, 200, 200))
    b = particle(4E13, 1200, 800, [0, -3], (0, 200, 200))
    c = particle(4E13, 600, 200, [0, 3], (200, 0, 200))
    d = particle(3E13, 600, 800, [3, 0], (200, 200, 0))
    gravity = gf(a, b, c, d)
    system = System(a, b, c, d)
    
    rksystem = RK4(system)

    draw = drawParticle(Win, a, b, c, d)
    drawsystem = DrawSystem(draw)

    ctrl = UIcontroller(a, b, c, d)

    #frame rate and efficiency stuff
    counter = 0
    dt = 1/100
    max_count = 50

    while run:

        #get inputs to influence sim
        ctrlr = ctrl.inputs()
        if ctrlr == 0:
            run = False


        gravity.set_force()
        #print(a.acceleration, b.acceleration)
        # print('system state', system.get_state())
        #entire dynamic integration process
        system.set_state(rksystem.integrate(system.get_state(), dt))

        if counter % max_count == 0:
            clock.tick(60)
            Win.fill((10, 40, 70))
            drawsystem.draw()
            drawsystem.draw_data()
            pg.display.update()

        counter += 1

    pg.quit()


main()

