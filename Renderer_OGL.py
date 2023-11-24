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

#musica de fondo
pygame.mixer.init()
sound = pygame.mixer.Sound("musica_de_fondo.mp3")
sound.play()

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

maxHeight = 1   
minHeight = -3
maxZoom = -3.5
minZoom = 5

model = Model(filename=modelDino,translate=glm.vec3(0,-1,-7),rotation=glm.vec3(-60,0,-120),scale=glm.vec3(0.3,0.3,0.3))
model.loadTexture(textureDino)


#rend.scene.append( model )
rend.ObjActual = model

rend.camPosition = glm.vec3(model.translate.xy,0)
rend.target = model.translate
rend.camAngle = 0.0
rend.camRadio = abs(model.translate.z)

sensibilidadMovimientoY = 0.03
sensibilidadZoom = 0.5
sensibilidadMovimientoX = 0.06

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
        
        elif event.type == pygame.MOUSEMOTION:
            # Captura movimiento vertical del mouse para ajustar la altura de la cámara
            movX, movY = event.rel
            rend.camPosition.y = max(min(rend.camPosition.y + movY * sensibilidadMovimientoY, maxHeight), minHeight)
            
            rend.camAngle += movX * sensibilidadMovimientoX  # Ajusta 'sensibilidadMovimientoX' según necesidad

            # Mantén el ángulo dentro de un rango de 0-360 grados
            if rend.camAngle > 360:
                rend.camAngle -= 360
            elif rend.camAngle < 0:
                rend.camAngle += 360

            # Actualiza la posición de la cámara
            rend.camPosition.x = rend.target.x + rend.camRadio * sin(rend.camAngle * pi / 180)
            rend.camPosition.z = rend.target.z + rend.camRadio * cos(rend.camAngle * pi / 180)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Captura la rueda del mouse para ajustar el zoom
            if event.button == 4:  # Rueda arriba
                rend.camPosition.z = max(rend.camPosition.z - sensibilidadZoom, maxZoom)
            elif event.button == 5:  # Rueda abajo
                rend.camPosition.z = min(rend.camPosition.z + sensibilidadZoom, minZoom)

    
    
    rend.update()
        
    if keys[K_a]:
         model.rotation.z += 10 
    elif keys[K_d]:
         model.rotation.z -= 10 
    # Cambio de shaders
    if keys[K_0]:
        rend.setShaders(vertex_shader, fragment_shader)
    elif keys[K_1]:
        rend.setShaders(vertex_shader, colors_shader )
    elif keys[K_2]:
        rend.setShaders(vertex_shader, plasma_shaders )
    elif keys[K_3]:
        rend.setShaders(breathe_shader, fragment_shader )
    elif keys[K_4]:
        rend.setShaders(barca_vertex_shader, barca_shader )

    #Cambio de modelos
    if keys[K_u]:
        model = Model(filename=modelDino,translate=glm.vec3(0,-1,-7),rotation=glm.vec3(-60,0,-120),scale=glm.vec3(0.3,0.3,0.3))
        model.loadTexture(textureDino)
        rend.changeModel( model )
    elif keys[K_i]:
        model = Model(filename=modelDeadTree,translate=glm.vec3(0,-1.5,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.2,0.2,0.2))
        model.loadTexture(textureDeadTree1)
        rend.changeModel( model )
    elif keys[K_o]:
        model = Model(filename=modelhouse,translate=glm.vec3(-1,-2,-5),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.8,0.8,0.8))
        model.loadTexture(textureHouse)
        rend.changeModel( model )
    elif keys[K_p]:
        model = Model(filename=modelTower,translate=glm.vec3(0,-2.5,-7),rotation=glm.vec3(0,0,0),scale=glm.vec3(0.4,0.4,0.4))
        model.loadTexture(textureTower)
        rend.changeModel( model )
        

    

    rend.render()    
    pygame.display.flip()

pygame.quit()