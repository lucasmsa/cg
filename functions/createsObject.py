from OpenGL.GL import *

def createObject(VAO, VBO, index, buffer):

        glBindVertexArray(VAO[index])
        # * these steps will be repeated throughout the creating of new objects
        # * Vertex buffer object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[index])
        glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)
        
        # * for the position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))
        # * for texture coordinates
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))
        # * for normal coordinates
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)
