import glfw
from OpenGL.GL import *

try:

    glfw.init()

    window = glfw.create_window(1280, 720, "Parkour Game", None, None)


    # setting window initial position
    glfw.set_window_pos(window, 320, 120)

    # stores all data related to the rendering of the application
    glfw.make_context_current(window)

    # game loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glfw.swap_buffers(window)


    # free allocated resources
    glfw.terminate()

except (Exception):

    print("The exception thrown was: " + Exception)
