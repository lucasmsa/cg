from math import sin, cos, radians
import pyrr
import time


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
        self.jump = -1

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

            if self.pitch > 179:
                self.pitch =179
            
            if self.pitch < -179:
                self.pitch = -179
        
        self.update_camera_vectors()

    def process_keyboard(self, direction, velocity, run=0):
        
        if run:
            velocity *= 1.75
        
        if direction == 'FORWARD':
            self.camera_pos[0] += self.camera_front[0] * velocity
            self.camera_pos[2] += self.camera_front[2] * velocity

        if direction == 'BACKWARD':
            self.camera_pos[0] -= self.camera_front[0] * velocity
            self.camera_pos[2] -= self.camera_front[2] * velocity

        if direction == 'LEFT':
            self.camera_pos[0] -= self.camera_right[0] * velocity
            self.camera_pos[2] -= self.camera_right[2] * velocity

        if direction == 'RIGHT':
            self.camera_pos[0] += self.camera_right[0] * velocity
            self.camera_pos[2] += self.camera_right[2] * velocity

    def process_jump(self, velocity):
        if self.jump == 1:
            if self.camera_pos[1] >= self.camera_up[1] * 12:
                self.jump = 0
            else:
                self.camera_pos[1] += self.camera_up[1] * velocity
        elif self.jump == 0:
            if self.camera_pos[1] <= self.camera_up[1] * 4:
                self.jump = -1
            else:
                self.camera_pos[1] -= self.camera_up[1] * velocity

    def process_crouch(self, crouching):
        if crouching:
            self.camera_pos[1] = self.camera_up[1] * 2.5
        else:
            self.camera_pos[1] = self.camera_up[1] * 4

    def update_camera_vectors(self):

        front = pyrr.Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw) * cos(radians(self.pitch)))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = pyrr.vector.normalise(front)
        self.camera_right = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_front, pyrr.Vector3([0.0, 1.0, 0.0])))
        self.camera_up = pyrr.vector.normalise(pyrr.vector3.cross(self.camera_right, self.camera_front))

    
