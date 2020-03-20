from imports import *

cam = Camera()
width, height = 1280, 720
lastX, lastY = width/2, height/2
first_mouse = True
left, right, forward, backward, run, jump, crouch = False, False, False, False, False, False ,False

def key_input_callback(window, key, scancode, action, mode):
    
    global left, right, forward, backward, run, jump, crouch

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True

    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True

    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True

    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        jump = True

    if key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
        crouch = True
    
    if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
        run = True

    # * if the key is released then it will reset the variables 
    # * related to the keys to False
    if key in [glfw.KEY_A, glfw.KEY_S, glfw.KEY_D, glfw.KEY_W, glfw.KEY_LEFT_SHIFT, glfw.KEY_SPACE, glfw.KEY_LEFT_CONTROL] and action == glfw.RELEASE:
        
        left, right, forward, backward, run, jump = False, False, False, False, False, False

        if crouch:
            crouch = False
            cam.process_crouch(crouch)


def move(): 
  
    if left:
        cam.process_keyboard('LEFT', 0.025, run)

    if right:
        cam.process_keyboard('RIGHT', 0.025, run)

    if forward:
        cam.process_keyboard('FORWARD', 0.025, run)

    if backward:
        cam.process_keyboard('BACKWARD', 0.025, run)

    if jump:
        cam.process_jump(jump, 0.05)

    if crouch:
        cam.process_crouch(crouch)

def mouse_look_callback(window, xpos, ypos):

    global first_mouse, lastX, lastY

    # * when the mouse enters the window
    # * the lastX and lastY will be set to the
    # * second and third parameter of the function
    # * which is set by glfw
    # * if the values of lastX and lastY are not updated,
    # * the mouse will jump to the position relative to where
    # * it entered the window
    # * the first_mouse position is set to false 
    # * so that it only enters this function once
    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

try:

    glfw.init()

    window = glfw.create_window(width, height, "Parkour Game", None, None)

    # * setting window initial position
    glfw.set_window_pos(window, 320, 120)

    glfw.set_window_size_callback(window, windowResize)

    # * mouse operations
    # * the first one calculates mouse movements and updates it
    # * the second one checks if the mouse is on the window
    glfw.set_cursor_pos_callback(window, mouse_look_callback)
    # glfw.set_cursor_enter_callback(window, mouse_enter_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_key_callback(window, key_input_callback)

    # * stores all data related to the rendering of the application  
    glfw.make_context_current(window)

    # * load 3d objects
    car_indices, car_buffer = Object_Loader.load_model('objects/chibi.obj')
    floor_indices, floor_buffer = Object_Loader.load_model('objects/floor.obj')

    
    shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), 
    compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # * VAO [vertex array object], it wil put the
    # * the vertices and indices inside an array 
    VAO = glGenVertexArrays(2)
    # * subsequent vertex attribute calls will be stored inside
    # * this VAO object
    VBO = glGenBuffers(2)
    
    # * Function created, located at functions/createsObject
    createObject(VAO, VBO, 0, car_buffer)
    createObject(VAO, VBO, 1, floor_buffer)

    # * if the parameter is more than one it will generate an array 
    # * with slots of texture
    textures = glGenTextures(2)
    car_texture = textureLoader('textures/chibi.png', textures[0])
    floor_texture = textureLoader('textures/floor.jpg', textures[1])

    glUseProgram(shader)
    # * sets window default colors
    glClearColor(0.1, 0.1, 0.14, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # * creates a perspective projection matrix
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
    car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -5]))
    floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))


    # * these _loc elements will get their values from 
    # * the shaders [fragment shader and vertex shader]
    model_loc = glGetUniformLocation(shader, 'model')
    proj_loc = glGetUniformLocation(shader, 'projection')
    view_loc = glGetUniformLocation(shader, 'view')
    switcher_loc = glGetUniformLocation(shader, 'switcher')

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    #glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    

    # * game loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        move()

        cam.process_back_jump(jump, 0.5)

        # * calls glClearColor
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


        rot_x = pyrr.Matrix44.from_x_rotation(0.7 * glfw.get_time())
        rot_y = pyrr.Matrix44.from_y_rotation(0.6 * glfw.get_time())
        

        # * this model holds the combined matrices
        # * note that the second model call uses itself as a parameter
        # * it applies all the transformations to the model
        model = pyrr.matrix44.multiply(rot_y, car_pos)
        # * this will be repeated for drawing other elements with VAO
        # * bind the VAO to the vertex array
        glBindVertexArray(VAO[0])
        # * set the object texture
        glBindTexture(GL_TEXTURE_2D, textures[0])
        # * set model matrix, with object position
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        # * Draw the object
        glDrawArrays(GL_TRIANGLES, 0, len(car_indices))

        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

        glfw.swap_buffers(window)


    # * free allocated resources
    glfw.terminate()

except (Exception):

    print("The exception thrown was: " + Exception)
