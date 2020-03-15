from imports import *

try:

    glfw.init()

    window = glfw.create_window(1280, 720, "Parkour Game", None, None)


    # setting window initial position
    glfw.set_window_pos(window, 320, 120)

    glfw.set_window_size_callback(window, windowResize)

    # stores all data related to the rendering of the application  
    glfw.make_context_current(window)

    vertices = [-0.5, -0.5,  0.5, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 1.0,
            -0.5,  0.5, -0.5, 0.0, 1.0,

             0.5, -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0,

            -0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0,

             0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5,  0.5, 1.0, 1.0,
             0.5, 0.5,  0.5, 0.0, 1.0]

    indices = [ 0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    #colors = np.array(colors, dtype=np.float32)

    shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), 
    compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 5, ctypes.c_void_p(12))

    # * if the parameter is more than one it will generate an array 
    # * with slots of texture
    texture = glGenTextures(3)

    cube1_texture = textureLoader('textures/metal.jpg', texture[0])
    cube2_texture = textureLoader('textures/sloth.jpg', texture[1])
    cube3_texture = textureLoader('textures/bleurgh.png', texture[2])

    glUseProgram(shader)
    # sets window default colors
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # * creates a perspective projection matrix
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280/720, 0.1, 100)
    cube1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([1, 0, 0]))
    cube2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([-1, 0, 0]))
    cube3 = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 1, -2]))
    #translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    
    # * the view will work as a camera. when you move 1 in the x axis for example
    # * it's relative to moving to the right, or everything being translated to the left
    # view = pyrr.matrix44.create_from_translation(pyrr.Vector3([1, 0, 0]))

    # * look at function is an advaced version of view
    # * the parameters are: eye [ where the camera is positioned ],
    # * target [ where the camera is looking at ], up vector [ y axis up of the camera ]
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 3]),
    pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
    
    # * creates a orthogonal projection matrix
    # * the most important values to note are the last and the last but one values
    # * they will delimitate the projection space for the scene
    #projection = pyrr.matrix44.create_orthogonal_projection_matrix(0, 1280, 0, 720, -1000, 1000)
    #translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([500, 200, -3]))
    
    # * this will be used to increase the size of the object, at each axis
    # * afterwards [on game loop] it is necessary to combine the scale with 
    # * the other matrices
    #scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([200, 200, 200]))

    model_loc = glGetUniformLocation(shader, 'model')
    proj_loc = glGetUniformLocation(shader, 'projection')
    view_loc = glGetUniformLocation(shader, 'view')

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    

    # * game loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # calls glClearColor
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glBindTexture(GL_TEXTURE_2D, texture[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube1)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glBindTexture(GL_TEXTURE_2D, texture[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube2)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glBindTexture(GL_TEXTURE_2D, texture[2])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, cube3)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)


        #rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
        #rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
        
        # * this model holds the combined matrices
        # * note that the second model call uses itself as a parameter
        # * it applies all the transformations to the model
        #rotation = pyrr.matrix44.multiply(rot_x, rot_y)
        #model = pyrr.matrix44.multiply(scale, rotation)
        #model = pyrr.matrix44.multiply(model, translation)


        #glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x*rot_y)
        #glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        #glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_x @ rot_y)


        glfw.swap_buffers(window)


    # free allocated resources
    glfw.terminate()

except (Exception):

    print("The exception thrown was: " + Exception)
