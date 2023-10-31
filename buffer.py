from OpenGL.GL import *
from numpy import array, float32

class Buffer(object):
    def __init__(self,data):
        self.vertBuffer = array(data, dtype = float32)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)
    
    def render(self):
        pass
    
        