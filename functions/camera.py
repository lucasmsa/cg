from math import sin, cos, radians
import pyrr

class Camera:
    def __init__(self):
        # * sets camera init
        self.camera_pos = pyrr.Vector3([0.0, 4.0, 3.0])
        self.camera_front = pyrr.Vector3([0.0, 0.0, -1])
        self.camera_up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.camera_right = pyrr.Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.35
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        # * create look at function
        return pyrr.matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
        
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        # * movements left and right
        self.jaw += xoffset
        # * movements up and down
        self.pitch += yoffset

        # * make the camera constrained to a determined angle [up and down]
        if constrain_pitch:

            if self.pitch > 44:
                self.pitch = 44
            
            if self.pitch < -44:
                self.pitch = -44
        
        self.update_camera_vectors()

    def process_keyboard(self, direction, velocity, run=0):
        if direction == 'FORWARD':
            self.camera_pos += self.camera_front * velocity
            self.camera_pos[1] = 4.0
        if direction == 'BACKWARD':
            self.camera_pos -= self.camera_front * velocity
            self.camera_pos[1] = 4.0
        if direction == 'LEFT':
            self.camera_pos -= self.camera_right * velocity
            self.camera_pos[1] = 4.0
        if direction == 'RIGHT':
            self.camera_pos += self.camera_right * velocity
            self.camera_pos[1] = 4.0

    def update_camera_vectors(self):

        front = pyrr.Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw) * cos(radians(self.pitch)))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = pyrr.vector.normalise(front)
        self.camera_right = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.camera_up = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_right, self.camera_front))

    
