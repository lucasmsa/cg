from OpenGL.GL import *

def windowResize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
