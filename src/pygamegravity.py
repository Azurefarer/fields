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
GRAY = (200, 200, 200)

def main():
    run = True
    clock = pg.time.Clock()

    #init objects, system, integrator, drawers, system drawer, and controller
    a = particle(1E14, 900, 500, [0, 0], 20, GRAY)
    b = particle(.1E14, 1000, 500, [0, 5], 5, GRAY)
    c = particle(.1E14, 800, 500, [0, -5], 5, GRAY)
    d = particle(.1E14, 900, 400, [5, 0], 5, GRAY)
    e = particle(.1E14, 900, 600, [-5, 0], 5, GRAY)
    f = particle(.1E14, 1100, 500, [0, 3], 5, GRAY)
    g = particle(.1E14, 700, 500, [0, -3], 5, GRAY)
    h = particle(.1E14, 900, 300, [3, 0], 5, GRAY)
    i = particle(.1E14, 900, 700, [-3, 0], 5, GRAY)



    gravity = gf(a, b, c, d, e, f, g, h, i)
    system = System(a, b, c, d, e, f, g, h, i)
    
    rksystem = RK4(system)

    draw = drawParticle(Win, a, b, c, d, e, f, g, h, i)
    drawsystem = DrawSystem(draw)

    ctrl = UIcontroller(a, b, c, d, e, f, g, h, i)


    #frame rate and efficiency stuff
    counter = 0
    dt = 1/25
    max_count = 5

    while run:


        #get inputs to influence sim
        ctrlr = ctrl.inputs()
        if ctrlr == 0:
            run = False


        gravity.set_force()

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

