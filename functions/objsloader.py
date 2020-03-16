import numpy as np

class Object_Loader:
    
    buffer = []

    # * Used for searching data inside the obj file
    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            
            # * in the face [f] values
            elif data_type == 'int':
                coordinates.append(int(d) - 1)

    # * sorting vertex buffer to use it in glDrawArrays function
    @staticmethod
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for element, index in enumerate(indices_data):
            # * used for sorting vertex coordinates [x, y, z]
            if element % 3 == 0:
                start = index * 3
                end = start + 3
                Object_Loader.buffer.extend(vertices[start:end])

            # * used for sorting texture coordinates [u, v]
            elif element % 3 == 1:
                start = index * 2
                end = start + 2
                Object_Loader.buffer.extend(textures[start:end])

            # * used for sorting the normal vectors
            elif element % 3 == 2:
                start = index * 3
                end = start + 3
                Object_Loader.buffer.extend(normals[start:end])

    @staticmethod
    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals):
        num_vertices = len(vertices) // 3

        for i in range(num_vertices):
            start = i * 3
            end = start + 3
            Object_Loader.buffer.extend(vertices[start:end])

            for j, data in enumerate(indices_data):
                if j % 3 == 0 and data == i:
                    start = indices_data[j +1] * 2
                    end = start - 2
                    Object_Loader.buffer.extend(textures[start:end])

                    start = indices_data[j + 2] * 3
                    end = start + 3
                    Object_Loader.buffer.extend(normals[start:end])

                    break

    @staticmethod
    def show_buffer_data(buffer):
        for i in range(len(buffer)//8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])

    @staticmethod
    def load_model(file, sorted=True):
        # * contains each of the coordinates values
        vertex_coordinates = []
        texture_coordinates = []
        normals_coordinates = []

        # * contains all vertices, texture and normal indices
        all_indices = []
        # * will contain the indices for indexed drawing
        indices = []

        with open(file, 'r') as f:
            line = f.readline()
            while line:

                values = line.split()
                
                if values:

                    if values[0] == 'v':
                        Object_Loader.search_data(values, vertex_coordinates, 'v', 'float')
                    
                    elif values[0] == 'vt':
                        Object_Loader.search_data(values, texture_coordinates, 'vt', 'float')
                    
                    elif values[0] == 'vn':
                        Object_Loader.search_data(values, normals_coordinates, 'vn', 'float')
                    
                    elif values[0] == 'f':

                        for value in values[1:]:
                            
                            val = value.split('/')
                            Object_Loader.search_data(val, all_indices, 'f', 'int')
                            indices.append(int(val[0]) - 1)

                line = f.readline()

        if sorted:
            # * glDrawArrays
            Object_Loader.create_sorted_vertex_buffer(all_indices, vertex_coordinates, texture_coordinates, normals_coordinates)
        else: 
            # * glDrawElements
            Object_Loader.create_unsorted_vertex_buffer(all_indices, vertex_coordinates, texture_coordinates, normals_coordinates)

        # * create a local copy of the buffer list, otherwise it overwrite the static field buffer
        buffer = Object_Loader.buffer.copy()
        # * after copying, set it back to an empty list
        Object_Loader.buffer = []
        
        # * buffer will look store these values:
        # * [x, y, z, [u, v] => textures, normals_x, normals_y, normals_z]
        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
