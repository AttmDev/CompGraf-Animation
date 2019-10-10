import math
import numpy
import pygame
import sys


#################### Matrizes e Variáveis ############################

janelaLargura = 1280
janelaAltura = 720
clock = pygame.time.Clock()

# [x y z] como vetor linha
matrizOriginal = numpy.array([[0, 1, 1, 1],
					          [1, 0, 1, 1],
					          [1, 1, 2, 1],
					          [1, 2, 1, 1],
					          [2, 1, 1, 1],
					          [1, 1, 0, 1]])

arestas = [[0, 1], [0, 2], [0, 3], [0, 5], [1, 2], [1, 4], [1, 5], [2, 4], [2, 3], [3, 4], [3, 5], [4, 5]]


escalaX = 50
escalaY = 50
escalaZ = 50

matrizEscala = numpy.array([[escalaX, 0, 0, 0],
							[0, escalaY, 0, 0],
							[0, 0, escalaZ, 0],
							[0, 0, 0, 1]])


anguloX = 0.002

matrizRotacaoX = numpy.array([[1, 0, 0, 0],
							  [0, math.cos(anguloX), math.sin(anguloX), 0],
							  [0, -math.sin(anguloX), math.cos(anguloX), 0],
							  [0, 0, 0, 1]])


anguloY = 0.003

matrizRotacaoY = numpy.array([[math.cos(anguloY), 0, -math.sin(anguloY), 0],
							  [0, 1, 0, 0],
							  [math.sin(anguloY), 0, math.cos(anguloY), 0],
							  [0, 0, 0, 1]])


anguloZ = 0.001

matrizRotacaoZ = numpy.array([[math.cos(anguloZ), math.sin(anguloZ), 0, 0],
							  [-math.sin(anguloZ), math.cos(anguloZ), 0,  0],
							  [0, 0, 1, 0],
							  [0, 0, 0, 1]])


translacaoX = janelaLargura/2 - escalaX/2
translacaoY = janelaAltura/2 - escalaY/2
translacaoZ = 0

matrizTranslacao = numpy.array([[1, 0, 0, 0],
								[0, 1, 0, 0],
								[0, 0, 1, 0],
								[translacaoX, translacaoY, translacaoZ, 1]])


matrizTranslacaoInversa = numpy.array([[1, 0, 0, 0],
									   [0, 1, 0, 0],
									   [0, 0, 1, 0],
									   [-translacaoX, -translacaoY, -translacaoZ, 1]])


matrizProjecao = numpy.array([[1, 0],
							  [0, 1],
							  [0, 0],	
							  [0, 0]])

#################### Funções ##########################

def rotacionarX(mResultante):
	mOriginal = numpy.matmul(mResultante, matrizTranslacaoInversa)
	mRotacionada = numpy.matmul(mOriginal, matrizRotacaoX)
	return numpy.matmul(mRotacionada, matrizTranslacao)


def rotacionarY(mResultante):
	mOriginal = numpy.matmul(mResultante, matrizTranslacaoInversa)
	mRotacionada = numpy.matmul(mOriginal, matrizRotacaoY)
	return numpy.matmul(mRotacionada, matrizTranslacao)


def rotacionarZ(mResultante):
	mOriginal = numpy.matmul(mResultante, matrizTranslacaoInversa)
	mRotacionada = numpy.matmul(mOriginal, matrizRotacaoZ)
	return numpy.matmul(mRotacionada, matrizTranslacao)



#################### Game Loop ############################

matrizResultante = numpy.matmul(matrizOriginal, matrizEscala)
matrizResultante = numpy.matmul(matrizResultante, matrizTranslacao)

pygame.init()
screen = pygame.display.set_mode((janelaLargura, janelaAltura))
while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			sys.exit()

	screen.fill((255, 255, 255))



	matrizProjetada = numpy.matmul(matrizResultante, matrizProjecao)
	for aresta in arestas:
		pygame.draw.line(screen, (0, 0, 0), matrizProjetada[aresta[0]], matrizProjetada[aresta[1]])

	pygame.display.flip()




