from imports import *

cam = Camera()
width, height = 1280, 720
lastX, lastY = width/2, height/2
first_mouse = True
left, right, forward, backward, run, crouch = False, False, False, False, False, False

def key_input_callback(window, key, scancode, action, mode):
    
    global left, right, forward, backward, run, crouch

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
        cam.jump = 1

    if key == glfw.KEY_LEFT_CONTROL and action == glfw.PRESS:
        crouch = True
    
    if key == glfw.KEY_LEFT_SHIFT and action == glfw.PRESS:
        run = True

    # * if the key is released then it will reset the variables 
    # * related to the keys to False
    if key in [glfw.KEY_A, glfw.KEY_S, glfw.KEY_D, glfw.KEY_W, glfw.KEY_LEFT_SHIFT, glfw.KEY_SPACE, glfw.KEY_LEFT_CONTROL] and action == glfw.RELEASE:
        
        left, right, forward, backward, run = False, False, False, False, False

        if crouch:
            crouch = False
            cam.process_crouch(crouch)


def move(): 
  
    if left:
        cam.process_keyboard('LEFT', 0.25, run)

    if right:
        cam.process_keyboard('RIGHT', 0.25, run)

    if forward:
        cam.process_keyboard('FORWARD', 0.25, run)

    if backward:
        cam.process_keyboard('BACKWARD', 0.25, run)

    if cam.jump == 1 or cam.jump == 0:
        cam.process_jump(0.35)

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
    floor_indices, floor_buffer = Object_Loader.load_model('objects/grass.obj')
    floor_indices2, floor_buffer2 = Object_Loader.load_model('objects/asfalto.obj')
    floor_indices3, floor_buffer3 = Object_Loader.load_model('objects/amarelo.obj')
    predio_indices, predio_buffer = Object_Loader.load_model('objects/predio2.obj')
    sky_indices, sky_buffer = Object_Loader.load_model('objects/skybox.obj')
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width/height), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -5)

    glEnable(GL_DEPTH_TEST) 
    shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), 
    compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    # * VAO [vertex array object], it wil put the
    # * the vertices and indices inside an array 
    VAO = glGenVertexArrays(10)
    # * subsequent vertex attribute calls will be stored inside
    # * this VAO object
    VBO = glGenBuffers(10)
    
    # * Function created, located at functions/createsObject
    createObject(VAO, VBO, 0, car_buffer)
    createObject(VAO, VBO, 1, floor_buffer)
    createObject(VAO, VBO, 2, floor_buffer2)
    createObject(VAO, VBO, 3, floor_buffer3)
    createObject(VAO, VBO, 4, predio_buffer)
    createObject(VAO, VBO, 5, sky_buffer)
    #createObject(VAO, VBO, 7, wall_buffers)

    # * if the parameter is more than one it will generate an array 
    # * with slots of texture
    textures = glGenTextures(10)
    car_texture = textureLoader('textures/chibi.png', textures[0])
    floor_texture = textureLoader('textures/grass.jpg', textures[1])
    floor_texture2 = textureLoader('textures/asfalto.jpg', textures[2])
    floor_texture3 = textureLoader('textures/amarelo.jpg', textures[3])
    predio_texture = textureLoader('textures/predio.png', textures[4])
    sky_texture = textureLoader('textures/skybox_texture.jpg', textures[5])

    glUseProgram(shader)
    # * sets window default colors
    glClearColor(0.1, 0.1, 0.14, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_BLEND)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 6.5, 3.0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 7.0, 2.0, 1])

    # * creates a perspective projection matrix
    #projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, far=600)
    x=30
    y=60
    car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -5]))
    floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    floor_pos2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    floor_pos3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    predio_pos = []
    for i in range(20):
        if i<10:
            predio_pos.append(pyrr.matrix44.create_from_translation(pyrr.Vector3([20+(i*x), 0, 0])))
        else:
            predio_pos.append(pyrr.matrix44.create_from_translation(pyrr.Vector3([20+((i-10)*x), 0, y])))
    
    sky_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))



    # * these _loc elements will get their values from 
    # * the shaders [fragment shader and vertex shader]
    model_loc = glGetUniformLocation(shader, 'model')
    proj_loc = glGetUniformLocation(shader, 'projection')
    view_loc = glGetUniformLocation(shader, 'view')
    switcher_loc = glGetUniformLocation(shader, 'switcher')
    light_loc = glGetUniformLocation(shader, 'light')

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    #glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    

    # * game loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        move()

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
        #glBindTexture(GL_TEXTURE_2D, textures[0])
        # * set model matrix, with object position
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        # * Draw the object
        glDrawArrays(GL_TRIANGLES, 0, len(car_indices))

        #==================================================================
        glUniformMatrix4fv(light_loc, 1, GL_FALSE, rot_y)
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        #==================================================================

        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

        glBindVertexArray(VAO[2])
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos2)
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices2))

        glBindVertexArray(VAO[3])
        glBindTexture(GL_TEXTURE_2D, textures[3])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos3)
        glDrawArrays(GL_TRIANGLES, 0, len(floor_indices3))

        
        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, sky_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(sky_indices))

        for i in range(20):
            glBindVertexArray(VAO[4])
            glBindTexture(GL_TEXTURE_2D, textures[4])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio_pos[i])
            glDrawArrays(GL_TRIANGLES, 0, len(predio_indices))

        glfw.swap_buffers(window)


    # * free allocated resources
    glfw.terminate()

except (Exception):

    print("The exception thrown was: " + Exception)

