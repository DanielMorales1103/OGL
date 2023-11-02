import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
import glm

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader )

triangleData = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 
                   0,  0.5, 0.0, 0.0, 1.0, 0.0,  
                   0.5, -0.5, 0.0, 0.0, 0.0, 1.0 ]

triangleModel =  Model(triangleData)
triangleModel.position.z = -5
triangleModel.scale = glm.vec3(3,3,3)

rend.scene.append( triangleModel )


isRunning = True
while isRunning:

    keys = pygame.key.get_pressed()
    deltaTime = clock.tick(60) / 1000  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    if keys[K_RIGHT]:
        if rend.clearColor[0] < 1.0:
            rend.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        if rend.clearColor[0] > 0.0:
            rend.clearColor[0] -= deltaTime
            
    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime        
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime
    if keys[K_w]:
        rend.camPosition.z -= 5 * deltaTime        
    elif keys[K_s]:
        rend.camPosition.z += 5 * deltaTime
    if keys[K_q]:
        rend.camPosition.y += 5 * deltaTime        
    elif keys[K_e]:
        rend.camPosition.y -= 5 * deltaTime
        
    triangleModel.rotation.y += 45 * deltaTime

    rend.render()    
    pygame.display.flip()

pygame.quit()