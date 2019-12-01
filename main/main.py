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
    def __init__(self, list_pts, listaArestas, listaFaces):
        self.listPts = numpy.array(list_pts)
        self.listaArestas = listaArestas
        xc = ((self.listPts[4][0]) + (self.listPts[0][0])) / 2
        yc = ((self.listPts[3][1]) + (self.listPts[1][1])) / 2
        zc = ((self.listPts[2][2]) + (self.listPts[5][2])) / 2
        self.center = [xc, yc, zc]
        self.relativeCenter = [xc, yc, zc]
        self.listaFaces = listaFaces


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


        self.pinta(self.listaFaces[0], (0, 0, 200), mat)
        self.pinta(self.listaFaces[2], (0, 0, 100), mat)
        self.pinta(self.listaFaces[3], (0, 0, 140), mat)
        self.pinta(self.listaFaces[7], (0, 0, 50), mat)


        # pontos = []
        # pontos2 = []
        # for face in self.listaFaces:
        #     for ponto in face:
        #         pontos.append([mat[ponto][0], mat[ponto][1]])
        #     pygame.draw.polygon(screen, (128, 25, 25), pontos)
        #
        # for ponto in self.listaFaces[0]:
        #         pontos2.append([mat[ponto][0], mat[ponto][1]])
        # pygame.draw.polygon(screen, (255, 50, 50), pontos2)

        for aresta in self.listaArestas:
            if aresta.ptOrig not in [9, 10] and aresta.ptDest not in [9, 10]:
                ponto_origem = (mat[aresta.ptOrig][0], mat[aresta.ptOrig][1])
                ponto_destino = (mat[aresta.ptDest][0], mat[aresta.ptDest][1])
                pygame.draw.line(screen, (255,255,255), ponto_origem, ponto_destino)


        return mat

    # função que altera os valores para translaçao
    def moveObject(self, Tx, Ty):
        mat_translad[3][0] += Tx
        mat_translad[3][1] += Ty

    def pinta(self, faces, cor, mat):
        pontos = []

        for ponto in faces:
            pontos.append([mat[ponto][0], mat[ponto][1]])
        pygame.draw.polygon(screen, cor, pontos)


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

def curva_bezier(vertices, num_pnts=30):
    if len(vertices) != 4 or num_pnts < 2:
        return None

    resultado = []

    x0 = vertices[0][0]
    x1 = vertices[1][0]
    x2 = vertices[2][0]
    x3 = vertices[3][0]
    
    y0 = vertices[0][1]
    y1 = vertices[1][1]
    y2 = vertices[2][1]
    y3 = vertices[3][1]

    ax = -x0 + 3 * x1 + -3 * x2 + x3
    ay = -y0 + 3 * y1 + -3 * y2 + y3
    bx = 3 * x0 + -6 * x1 + 3 * x2
    by = 3 * y0 + -6 * y1 + 3 * y2
    cx = -3 * x0 + 3 * x1
    cy = -3 * y0 + 3 * y1
    dx = x0
    dy = y0

    pointX = dx
    pointY = dy
    passos = num_pnts - 1 
    h = 1.0 / passos

    eq1_x = ax * (h * h * h) + bx * (h * h) + cx * h
    eq2_x = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    eq3_x = 6 * ax * (h * h * h)
    eq1_y = ay * (h * h * h) + by * (h * h) + cy * h
    eq2_y = 6 * ay * (h * h * h) + 2 * by * (h * h)
    eq3_y = 6 * ay * (h * h * h)

    resultado.append((int(pointX), int(pointY)))

    for i in range(passos):
        pointX += eq1_x
        pointY += eq1_y
        eq1_x += eq2_x
        eq1_y += eq2_y
        eq2_x += eq3_x
        eq2_y += eq3_y
        resultado.append((int(pointX), int(pointY)))

    return resultado

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

teste = Objeto(cordenadas, arestas, [])

vertices = [[0, 20, 0, 1],
			[20, 0, 0, 1],
			[60, 0, 0, 1],
		 	[80, 20, 0, 1],
			[60, 40, 0, 1],
			[20, 40, 0, 1],
			[0, 20, 40, 1],
			[20, 0, 40, 1],
			[60, 0, 40, 1],
			[80, 20, 40, 1],
			[60, 40, 40, 1],
			[20, 40, 40, 1]]

arestas2 = [Aresta(0, 1), Aresta(1, 2), Aresta(2, 3),Aresta(3, 4), Aresta(4, 5), Aresta(5, 0),
			Aresta(6, 7), Aresta(7, 8), Aresta(8, 9), Aresta(9, 10), Aresta(10, 11), Aresta(11, 6),
			Aresta(0, 6), Aresta(1, 7), Aresta(2, 8), Aresta(3, 9), Aresta(4, 10), Aresta(5, 11)]

faces = [[0, 1, 2, 3, 4, 5],
         [6, 7, 8, 9, 10, 11],
         [0, 1, 7, 6],
         [1, 2, 8, 7],
         [2, 3, 9, 8],
         [3, 4, 10, 9],
         [4, 5, 11, 10],
         [0, 5, 11, 6]]

prisma = Objeto(vertices, arestas2, faces)


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

    curva_vert = [vertices[2][:2],vertices[4][:2],vertices[8][:2],vertices[10][:2]]
    # for vert in curva_vert:
    #     vert += prisma.getCenter()
    curva = curva_bezier([(x[0], x[1]) for x in curva_vert]) #TODO curva de bezier
    pygame.draw.lines(screen, pygame.Color("white"), False, curva, 2)

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

    mat = prisma.drawLines()
    # print(teste.getRelativeCenter())

    pygame.display.flip()