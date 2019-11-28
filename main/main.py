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

Tx, Ty = win_width/2, win_height/2

# Matriz de Translação
mat_translad = numpy.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [Tx, Ty, 0, 1]
                           ])

# Matriz de projeção perspectiva
mat_proj = numpy.array([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, -1/750],
                        [0, 0, 0, 1]])


# recebe uma lista de cordenadas e lista de arestas
class Objeto():
    def __init__(self, list_pts, listaArestas):
        self.listPts = numpy.array(list_pts)
        self.listaArestas = listaArestas
        xc = ((self.listPts[4][0]) + (self.listPts[0][0])) / 2
        yc = ((self.listPts[3][1]) + (self.listPts[1][1])) / 2
        zc = ((self.listPts[2][2]) + (self.listPts[5][2])) / 2
        self.center = [xc, yc, zc]
        self.relativeCenter = [xc, yc, zc]

    # esse função retorna o centro do objeto
    def getCenter(self):
        return self.center

    # retorna o centro relativo a uma translação
    def getRelativeCenter(self):
        r = numpy.copy(self.relativeCenter)
        r[0] += Tx
        r[1] += Ty
        return r

    # função de rotação em X
    def rotateX(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_x)

    # função de rotação em Y
    def rotateY(self):
        self.listPts = numpy.matmul(self.listPts, mat_rot_y)

    # função que passa por todos os pntos  e cria os vértices para ser desenhados
    def drawObject(self):
        aux = numpy.matmul(self.listPts, mat_proj)
        return numpy.matmul(aux, mat_translad)


    # desenha as arestas
    def drawLines(self):
        global screen
        mat = self.drawObject()
        arst = sort_aresta(self.listPts,self.listaArestas) # tentando tirar todos as arestas na parte de tras
        for aresta in arst:
            ponto_origem = (mat[aresta.ptOrig][0],
                            mat[aresta.ptOrig][1])

            ponto_destino = (mat[aresta.ptDest][0],
                             mat[aresta.ptDest][1])

            pygame.draw.line(screen, (0, 0, 0), ponto_origem, ponto_destino)
        return mat

    # função que altera os valores para translaçao
    def moveObject(self, Tx, Ty):
        mat_translad[3][0] += Tx
        mat_translad[3][1] += Ty

    # função de cisalhamento
    def cisalhar(self, a, b):
        cis = numpy.array([[1, b, 0, 0],
                           [a, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        self.listPts = numpy.matmul(self.listPts, cis)

    def escalar(self, Sx, Sy):
        e = numpy.array([[Sx, 0, 0, 0],
                         [0, Sy, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        self.listPts = numpy.matmul(self.listPts, e)

    def espelhar(self):
        m = numpy.array([[-1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        self.listPts = numpy.matmul(self.listPts, m)

    def cisalharEscalar(self, a, b, Sx, Sy):
        cis = numpy.array([[1, b, 0, 0],
                           [a, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

        e = numpy.array([[Sx, 0, 0, 0],
                         [0, Sy, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

        matriz = numpy.matmul(cis, e)
        self.listPts = numpy.matmul(self.listPts, matriz)

    def cisalharMover(self, a, b, Tx, Ty):
        cis = numpy.array([[1, b, 0, 0],
                           [a, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        self.listPts = numpy.matmul(self.listPts, cis)
        mat_translad[3][0] += Tx
        mat_translad[3][1] += Ty



class Aresta():
    def __init__(self, ptOrig, ptDest):
        self.ptOrig, self.ptDest = ptOrig, ptDest


def sort_aresta(coords, arest):
    copia_aresta = arest.copy()
    menor_coord = -9999
    menor_obj = -999
    segundo_menor = menor_obj
    to_remove = []
    index = 0

    maior_x = 0
    menor_x = 0
    for c in coords:
        if c[2]> menor_coord:
            segundo_menor = menor_obj
            menor_coord = c[2]
            menor_obj = index
        if c[0]> maior_x:
            maior_xi = c
            maior_x = index
        if c[0]< menor_x:
            maior_xi = c
            menor_x = index
        index += 1


    for obj in copia_aresta:
        if obj.ptOrig == menor_obj or obj.ptDest == menor_obj:
            to_remove.append(obj)
    for obj in copia_aresta:
        if obj.ptOrig == segundo_menor or obj.ptDest == segundo_menor:
            if not obj.ptOrig == maior_x and not obj.ptOrig == menor_x:
                if not obj.ptDest == maior_x and not obj.ptDest == menor_x:
                    to_remove.append(obj)



    for obj in to_remove:
        try:
            copia_aresta.remove(obj)
        except:
            pass
    return copia_aresta

# ---------------------------------- VARIAVEIS ----------------------------------
# [x y z] como vetor linha
cordenadas = [
            [-35, 0, 25, 1],
            [-20, 0, -20, 1],
            [5, -80, 18.75, 1],
            [20, 0, -20, 1],
            [35, 0, 20, 1],
            [0, 0, 50, 1],
            [5, 80, 18.75, 1]
        ]
arestas = [Aresta(0, 1), Aresta(1, 2), Aresta(2, 3), Aresta(1, 3),
           Aresta(0, 2), Aresta(2, 4), Aresta(3, 4), Aresta(4, 5),
           Aresta(2, 5), Aresta(0, 5), Aresta(5, 6), Aresta(4, 6),
           Aresta(0, 6), Aresta(1, 6), Aresta(3, 6)]

teste = Objeto(cordenadas, arestas)


# ---------------------------------- GAME LOOP ----------------------------------
pygame.init()

screen = pygame.display.set_mode((win_width, win_height))

running = True
rotacaoX = False
rotacaoY = False

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Comandos de Rotação
            if event.key == pygame.K_p:
                pygame.display.toggle_fullscreen()

            # if event.key == pygame.K_r:
            #     if rotacaoX == False:
            # rotacaoX = True
                # else:
                #     rotacaoX = False
            # if event.key == pygame.K_y:
            #     if rotacaoY == False:
            # rotacaoY = True
                # else:
                #     rotacaoY = False

            # Comandos de Escala
            if event.key == pygame.K_w:
                teste.escalar(1, 2)
            if event.key == pygame.K_a:
                teste.escalar(0.5, 1)
            if event.key == pygame.K_d:
                teste.escalar(2, 1)
            if event.key == pygame.K_s:
                teste.escalar(1, 0.5)

            if event.key == pygame.K_e:
                teste.espelhar()


    screen.fill((200, 200, 200))
    # teste.fill((100, 100, 100))

    # if rotacaoX:
    # teste.rotateX()
    # if rotacaoY:
    teste.rotateY()

    keyinput = pygame.key.get_pressed()

    # Comandos de Movimentação
    if keyinput[pygame.K_LEFT]:
        teste.moveObject(-2, 0)
    if keyinput[pygame.K_RIGHT]:
        teste.moveObject(2, 0)
    if keyinput[pygame.K_UP]:
        teste.moveObject(0, -2)
    if keyinput[pygame.K_DOWN]:
        teste.moveObject(0, 2)

    # Comandos de Cisalhamento
    if keyinput[pygame.K_z]:
        teste.cisalhar(-0.02, 0)
    if keyinput[pygame.K_x]:
        teste.cisalhar(0.02, 0)
    if keyinput[pygame.K_c]:
        teste.cisalhar(0, -0.02)
    if keyinput[pygame.K_v]:
        teste.cisalhar(0, 0.02)

    if keyinput[pygame.K_h]:
        teste.cisalharEscalar(0.5, 0, 1.001, 0)

    if keyinput[pygame.K_u]:
        teste.cisalharMover(0.02, 0, 2, 0)

    mat = teste.drawLines()
    # print(teste.getRelativeCenter())

    pygame.display.flip()