import math
import numpy
import pygame
import sys

win_width, win_height = 1280, 720
anguloY = 0.0007
mat_rot_y = numpy.array([[math.cos(anguloY), 0, -math.sin(anguloY), 0],
                         [0, 1, 0, 0],
                         [math.sin(anguloY), 0, math.cos(anguloY), 0],
                         [0, 0, 0, 1]
                         ])
anguloX = 0.0005
mat_rot_x = numpy.array([[1, 0, 0, 0],
                         [0, math.cos(anguloX), math.sin(anguloX), 0],
                         [0, -math.sin(anguloX), math.cos(anguloX), 0],
                         [0, 0, 0, 1]
                         ])
translX, translY = 100, 100
mat_translad = numpy.array([[1, 0, 0, translX],
                            [0, 1, 0, translY],
                            [0, 0, 1, 0],
                            [translX, translY, 0, 1]
                           ])



class Objeto():
    def __init__(self, list_pts ,listaArestas):
        self.listPts = numpy.array(list_pts)
        self.listaArestas = listaArestas

    def rotateX(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_x)
    def rotateY(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_y)

    def drawObject(self):
        global screen
        pos_obj = numpy.matmul(self.listPts, mat_translad)
        for aresta in self.listaArestas:
            ponto_origem = (pos_obj[aresta.ptOrig][0], pos_obj[aresta.ptOrig][1])
            ponto_destino = (pos_obj[aresta.ptDest][0], pos_obj[aresta.ptDest][1])
            print(ponto_origem, ponto_destino)
            pygame.draw.line(screen, (0, 0, 0), ponto_origem, ponto_destino)





class Aresta():
    def __init__(self, ptOrig, ptDest):
        self.ptOrig, self.ptDest = ptOrig, ptDest

class Anima():
    def __init__(self, width, height):
        pass


cordenadas = [
            [-50, 0, 0, 1],
            [0, -50, 0, 1],
            [0, 0, 50, 1],
            [0, 50, 0, 1],
            [50, 0, 0, 1],
            [0, 0, -50, 1]
        ]
arestas = [Aresta(0,1),Aresta(0,2),Aresta(0,3),Aresta(0,5),Aresta(1,2),Aresta(1,4),Aresta(1,5),Aresta(2,4),Aresta(2,3),Aresta(3,4),Aresta(3,5),Aresta(4,5)]

teste = Objeto(cordenadas, arestas)

pygame.init()

screen = pygame.display.set_mode((win_width, win_height))
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    teste.rotateX()
    teste.rotateY()
    teste.drawObject()
    pygame.display.flip()
