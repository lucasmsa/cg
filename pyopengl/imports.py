import glfw
import numpy as np
from OpenGL.GL import *
import pyrr
from OpenGL.GL.shaders import compileProgram, compileShader
from math import sin, cos
from PIL import Image
import sys
sys.path.insert(1, 'functions')
from shaders import *
from texturesLoader import textureLoader
from windowsResize import windowResize