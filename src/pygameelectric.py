import pygame as pg
import numpy as np
from spaces.electric import electricField as ef
from MathTools.Integrator import RK4Integrator as RK4
from DrawTools.Draw import *
from DrawTools.DrawSystem import *
from System import System
from Game.Controls import *


pg.init()

#in millimeters
Width, Height = 1800, 1000  
Win = pg.display.set_mode((Width, Height))
pg.display.set_caption("Electric Field")
GRAY = (200, 200, 200)

def main():
    run = True
    clock = pg.time.Clock()

    #init objects, system, integrator, drawers, system drawer, and controller
    field = ef(10, 1, 4)

    
    rksystem = RK4(field)

    draw = drawField(Win, field)

    ctrl = UIcontroller(field)


    print(field.boundr, field.center, field.acceleration, field.bounds)

    #frame rate and efficiency stuff
    counter = 0
    dt = 1/100
    max_count = 5

    while run:

        #get inputs to influence sim
        ctrlr = ctrl.inputs()
        if ctrlr == 0:
            run = False

        # print(field.size)
        field.set_acceleration()
 
        #entire dynamic integration process
        field.set_state(rksystem.integrate(field.get_state(), dt))

        if counter % max_count == 0:
            clock.tick(60)
            Win.fill((10, 40, 70))
            draw.draw()
            draw.draw_data(counter/max_count)
            pg.display.update()

        counter += 1

    pg.quit()


main()

