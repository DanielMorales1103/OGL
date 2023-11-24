import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *
import glm
from math import pi,sin,cos

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)

modelDino = "dino.obj"
textureDino = "dino.jpg"

modelDeadTree = "DeadTree1.obj"
textureDeadTree1 = "arbol-gris.jpg"

modelhouse = "OldHouse.obj"
textureHouse = "Housebody.jpg"

modelTower = "tower.obj"
textureTower = "tower.jpg"

objectPosition = glm.vec3(0,0,-5)
maxHeight = 2   
minHeight = -2
maxZoom = -2
minZoom = 5

model = Model(filename=modelDino,translate=glm.vec3(0,-1,-5),rotation=glm.vec3(-60,0,-120),scale=glm.vec3(0.3,0.3,0.3))
model.loadTexture(textureDino)


#rend.scene.append( model )
rend.ObjActual = model

rend.camPosition = glm.vec3(model.translate.xy,0)
rend.target = model.translate
rend.camAngle = 0.0
rend.camRadio = abs(model.translate.z)

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
    
    #Movimiento de objeto con wasdqe    
    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime     
 
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime
    

    if keys[K_w]:
        newZoom = rend.camPosition.z - 5 * deltaTime
        rend.camPosition.z = max(newZoom, maxZoom)    
    elif keys[K_s]:
        newZoom = rend.camPosition.z + 5 * deltaTime
        rend.camPosition.z = min(newZoom, minZoom)
        
    if keys[K_q]:
        newHeight = rend.camPosition.y + 5 * deltaTime
        rend.camPosition.y = min(newHeight, maxHeight)       
    elif keys[K_e]:
        newHeight = rend.camPosition.y - 5 * deltaTime
        rend.camPosition.y = max(newHeight, minHeight)
    
    
    rend.update()
        
    # Cambio de shaders
    if keys[K_1]:
        rend.setShaders(vertex_shader, colors_shader )
    elif keys[K_2]:
        rend.setShaders(vertex_shader, plasma_shaders )
    elif keys[K_3]:
        rend.setShaders(breathe_shader, fragment_shader )
    elif keys[K_4]:
        rend.setShaders(barca_vertex_shader, barca_shader )

    #Cambio de modelos
    if keys[K_u]:
        model = Model(filename=modelDino,translate=glm.vec3(0,-1,-5),rotation=glm.vec3(-60,0,-120),scale=glm.vec3(0.3,0.3,0.3))
        model.loadTexture(textureDino)
        rend.changeModel( model )
    elif keys[K_i]:
        model = Model(filename=modelDeadTree,translate=glm.vec3(0,-1.5,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.3,0.3,0.3))
        model.loadTexture(textureDeadTree1)
        rend.changeModel( model )
    elif keys[K_o]:
        model = Model(filename=modelhouse,translate=glm.vec3(-1,-1,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.8,0.8,0.8))
        model.loadTexture(textureHouse)
        rend.changeModel( model )
    elif keys[K_p]:
        model = Model(filename=modelTower,translate=glm.vec3(0,-2,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.4,0.4,0.4))
        model.loadTexture(textureTower)
        rend.changeModel( model )

    rend.render()    
    pygame.display.flip()

pygame.quit()