from tkinter import SEL
import glm 
import random
from numpy import array, float32
from OpenGL.GL import * 
from OpenGL.GL.shaders import compileProgram, compileShader
import time
class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        self.clearColor = [0,0,0]
        glGenerateMipmap(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glViewport(0,0,self.width,self.height)
        self.startTime = time.time()
        self.ObjActual = None        
        self.activeShader = None
        
        self.target = glm.vec3(0,0,0)
        self.camAngle = 0.0
        self.camRadio = 0.0
        
        self.fatness = 0.0
        
        self.filledMode = True

        # ViewMatrix
        self.camPosition = glm.vec3(0,0,0)        
        self.camRotation = glm.vec3(0,0,0)
        
        # Projection Matrix
        self.projectionMatrix = glm.perspective(glm.radians(60), 
                                                self.width/self.height,
                                                0.1,
                                                1000)
    
    def changeModel(self,model):
        self.ObjActual = model
        
    def getViewMatrix(self):
        identity = glm.mat4(1)
        
        translateMat = glm.translate(identity, self.camPosition)
        
        #rotation
        pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        yaw =   glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
        roll =  glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))
        rotationMat = pitch * yaw * roll
        
        camMatrix = translateMat * rotationMat
        
        return glm.inverse(camMatrix)
    def update(self):
        self.viewMatrix = glm.lookAt(self.camPosition,self.target,glm.vec3(0,1,0))
               
        
    def setShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                               compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else:
            self.activeShader = None

    def render(self):
        currentTime = time.time() - self.startTime        

        glClearColor(self.clearColor[0],self.clearColor[1],self.clearColor[2],1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClear(16640 | 256)

        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            
            glUniformMatrix4fv( glGetUniformLocation(self.activeShader, "viewMatrix"), 
                               1, GL_FALSE, glm.value_ptr( self.getViewMatrix()) )
            glUniformMatrix4fv( glGetUniformLocation(self.activeShader, "projectionMatrix"), 
                               1, GL_FALSE, glm.value_ptr( self.projectionMatrix) )
            
            glUniform1f(glGetUniformLocation(self.activeShader, "time"), currentTime)

            
            
        
        #for obj in self.scene:
        if self.activeShader is not None:
            glUniformMatrix4fv( glGetUniformLocation(self.activeShader, "modelMatrix"), 
                            1, GL_FALSE, glm.value_ptr( self.ObjActual.getModelMatrix()) )
        self.ObjActual.render()