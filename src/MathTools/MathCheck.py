from tkinter import E
import numpy as np
import sympy as sp
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pygame as pg
from abc import ABC, abstractmethod



a = np.array([0, 5, 7])
b = np.array([0, 0, 6])
diffx, diffy = a[:2] - b[:2]
d = np.linalg.norm((diffy, diffx))

phi = np.rad2deg(np.arctan2(diffy, diffx))
print(d)
print(phi)

