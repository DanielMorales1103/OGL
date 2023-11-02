from OpenGL.GL import * 
from numpy import array, float32
import glm

class Model(object):
    def __init__(self,data):
        self.vertBuffer = array(data, dtype = float32)
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)
        
        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
        
    def getModelMatrix(self):
        identity = glm.mat4(1)
        
        translateMat = glm.translate(identity, self.position)
        
        #rotation
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw =   glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll =  glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))
        rotationMat = pitch * yaw * roll
        
        scaleMat = glm.scale(identity, self.scale)
        
        return translateMat * rotationMat * scaleMat
    
    def render(self):
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        glBufferData( GL_ARRAY_BUFFER,
                     self.vertBuffer.nbytes,
                     self.vertBuffer,
                     GL_STATIC_DRAW)
        
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 6,
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 6,
                              ctypes.c_void_p(4*3))
    
        glEnableVertexAttribArray(1)
        
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 6))