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
        cam.process_keyboard('LEFT', 0.25, run)

    if right:
        cam.process_keyboard('RIGHT', 0.25, run)

    if forward:
        cam.process_keyboard('FORWARD', 0.25, run)

    if backward:
        cam.process_keyboard('BACKWARD', 0.25, run)

    if jump:
        cam.process_jump(0.2)
    else:
        cam.process_back_jump(0.2)

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
    floor_indices, floor_buffer = Object_Loader.load_model('objects/castle_city.obj')

    # car_texture_offset = len(car_indices)*12
    # floor_texture_offset = len(floor_indices)*12

    # car_normal_offset = (car_texture_offset + len(car_buffer[2]*8))
    # floor_normal_offset = (floor_texture_offset + len(floor_buffer[2]*8))

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width/height), 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, -5)

    glEnable(GL_DEPTH_TEST) 
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
    textures = glGenTextures(3)
    car_texture = textureLoader('textures/chibi.png', textures[0])
    floor_texture = textureLoader('textures/terrain colour.png', textures[1])

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
    light_loc = glGetUniformLocation(shader, 'light')

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    #glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    

    # * game loop
    while not glfw.window_should_close(window):
from imports import *

cam = Camera()
width, height = 1280, 720
lastX, lastY = width/2, height/2
first_mouse = True
left, right, forward, backward, run, jump, crouch = False, False, False, False, False, False ,False

class Light(object):

    def setup(self, i):
        glEnable(GL_LIGHT0 + i)
        glLightfv(GL_LIGHT0 + 1, GL_POSITION, self.light_position)
        
    _i = count()

    def __init__(self, light_position):
        self.i = next(self._i)
        self.light_position = light_position
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHTING, GL_POSITION, self.light_position)

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
        cam.process_keyboard('LEFT', 0.25, run)

    if right:
        cam.process_keyboard('RIGHT', 0.25, run)

    if forward:
        cam.process_keyboard('FORWARD', 0.25, run)

    if backward:
        cam.process_keyboard('BACKWARD', 0.25, run)

    if jump:
        cam.process_jump(0.2)
    else:
        cam.process_back_jump(0.2)

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
    predio_indices, predio_buffer = Object_Loader.load_model('objects/predio.obj')
    predio2_indices, predio2_buffer = Object_Loader.load_model('objects/predio2.obj')
    sky_indices, sky_buffer = Object_Loader.load_model('objects/skybox.obj')
    
    #light = Light([4, 4, 4])

    # car_texture_offset = len(car_indices)*12
    # floor_texture_offset = len(floor_indices)*12

    # car_normal_offset = (car_texture_offset + len(car_buffer[2]*8))
    # floor_normal_offset = (floor_texture_offset + len(floor_buffer[2]*8))

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
    createObject(VAO, VBO, 5, predio2_buffer)
    createObject(VAO, VBO, 6, sky_buffer)

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
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # * creates a perspective projection matrix
    #projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, 100)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width/height, 0.1, far=600)
    x=35
    y=35
    car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -5]))
    floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    floor_pos2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    floor_pos3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    predio_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(1*x), 0, 10+(1*y)]))
    predio2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(1*x), 0, 0+(1*y)]))
    predio3_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(2*x), 0, 0+(1*y)]))
    predio7_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(2*x), 0, 0+(1*y)]))
    predio8_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(2.3*x), 0, 0+(1.2*y)]))
    predio4_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(3*x), 0, 0+(1*y)]))
    predio5_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0+(4*x), 0, 0+(3*y)]))
    predio6_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0-(2*x), 0, 0-(1*y)]))
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
        #light.setup(0)
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

        glBindVertexArray(VAO[4])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio_indices))

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio2_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio3_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio4_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio5_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio6_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[6])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, sky_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(sky_indices))

        glBindVertexArray(VAO[7])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio7_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))

        glBindVertexArray(VAO[7])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, predio8_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(predio2_indices))


        glfw.swap_buffers(window)


    # * free allocated resources
    glfw.terminate()

except (Exception):

    print("The exception thrown was: " + Exception)

