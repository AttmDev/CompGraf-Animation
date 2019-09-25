import math
import numpy
import pygame
import sys

# Tamanho da tela
win_width, win_height = 1280, 720
clock = pygame.time.Clock()

# Ângulos
anguloX = 0.015
anguloY = 0.01

# Matriz de rotação y
# [x y z] como vetor linha
mat_rot_y = numpy.array([[math.cos(anguloY), 0, -math.sin(anguloY), 0],
                         [0, 1, 0, 0],
                         [math.sin(anguloY), 0, math.cos(anguloY), 0],
                         [0, 0, 0, 1]
                         ])

# Matriz de rotação x
mat_rot_x = numpy.array([[1, 0, 0, 0],
                         [0, math.cos(anguloX), math.sin(anguloX), 0],
                         [0, -math.sin(anguloX), math.cos(anguloX), 0],
                         [0, 0, 0, 1]
                         ])

translX, translY = win_width/2, win_height/2

# Matriz de Translação
mat_translad = numpy.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [translX, translY, 0, 1]
                           ])


# recebe uma lista de cordenadas e lista de arestas
class Objeto():
    def __init__(self, list_pts, listaArestas):
        self.listPts = numpy.array(list_pts)
        self.listaArestas = listaArestas
        xc = (abs(self.listPts[4][0]) - abs(self.listPts[0][0])) / 2
        yc = (abs(self.listPts[3][1]) - abs(self.listPts[1][1])) / 2
        zc = (abs(self.listPts[2][2]) - abs(self.listPts[5][2])) / 2
        self.center = [xc, yc, zc]
        self.relativeCenter = [xc, yc, zc]

    def rotateX(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_x)

    def rotateY(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_y)

    def drawObject(self):
        return numpy.matmul(self.listPts, mat_translad)

    def getCenter(self):
        return self.center

    def getRelativeCenter(self):
        r = numpy.copy(self.relativeCenter)
        r[0] += translX
        r[1] += translY
        return r

    def drawLines(self):
        global screen
        mat = self.drawObject()
        # print(mat)

        for aresta in self.listaArestas:
            ponto_origem = (mat[aresta.ptOrig][0],
                            mat[aresta.ptOrig][1])

            ponto_destino = (mat[aresta.ptDest][0],
                             mat[aresta.ptDest][1])

            pygame.draw.line(screen, (0, 0, 0), ponto_origem, ponto_destino)
        return mat

    def moveObject(self, matTranslad):
        self.listPts = numpy.matmul(self.listPts, matTranslad)
        self.relativeCenter[0] += matTranslad[3][0]
        self.relativeCenter[1] += matTranslad[3][1]
        self.relativeCenter[2] += matTranslad[3][2]


class Aresta():
    def __init__(self, ptOrig, ptDest):
        self.ptOrig, self.ptDest = ptOrig, ptDest

class Anima():
    def __init__(self, width, height):
        pass

# ---------------------------------- VARIAVEIS ----------------------------------
# [x y z] como vetor linha
cordenadas = [
            [-50, 0, 0, 1],
            [0, -50, 0, 1],
            [0, 0, 50, 1],
            [0, 50, 0, 1],
            [50, 0, 0, 1],
            [0, 0, -50, 1]
        ]
arestas = [Aresta(0, 1), Aresta(0, 2), Aresta(0, 3), Aresta(0, 5),
           Aresta(1, 2), Aresta(1, 4), Aresta(1, 5), Aresta(2, 4),
           Aresta(2, 3), Aresta(3, 4), Aresta(3, 5), Aresta(4, 5)]

teste = Objeto(cordenadas, arestas)

# velocidade do objeto
vel = numpy.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [1, 1, 0, 1]
                   ])

vel2 = numpy.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [-1, -1, 0, 1]
                   ])

quadroChave1 = numpy.array([[590, 360, 0, 1],
                            [640, 310, 0, 1],
                            [640, 360, 50, 1],
                            [640, 410, 0, 1],
                            [690, 360, 0, 1],
                            [640, 360, -50, 1]])

quadroChave2 = numpy.array([[738, 508, 0, 1],
                             [788, 458, 0, 1],
                             [788, 508, 50, 1],
                             [788, 558, 0, 1],
                             [838, 508, 0, 1],
                             [788, 508, -50, 1]])

quadro1 = numpy.array([641, 361, 0])
quadro2 = numpy.array([782, 502, 0])

def compare(mat1, mat2):
    total = len(mat1)*len(mat1[0])
    mi = 0
    for i in range(len(mat1)):
        for j in range(len(mat1[i])):
            if mat1[i][j] >= mat2[i][j]:
                mi += 1
            j+=j
        i+=i
    # print(mi/total)
    if mi/total >= 0.8:
        return True
    return False

# ---------------------------------- GAME LOOP ----------------------------------
pygame.init()

screen = pygame.display.set_mode((win_width, win_height))
i = 0
speed = vel
while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255))
    teste.rotateX()
    teste.rotateY()
    teste.rotateY()
    teste.moveObject(speed)
    mat = teste.drawLines()
    print("---------------------------------")
    print(teste.getCenter())
    r = teste.getRelativeCenter()
    print(r)

    if numpy.allclose(r, quadro2):
        speed = vel2
    if numpy.allclose(r, quadro1):
        speed = vel


    pygame.display.flip()

