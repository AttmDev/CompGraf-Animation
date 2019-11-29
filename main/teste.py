# Implementation of Z-buffer Algorithm
# 4.14.2002.
# Jiwon Hahn

import math

def pixel(): return 32  # 32x32 grid of pixels


def inf(): return math.inf


def z_buffer_algo():
    zbuff = [[inf()] * pixel() for i in range(pixel())]  # initialize z buffer to inf
    intensity = [[0] * pixel() for i in range(pixel())]  # initialize intensity to zero

    print("Polygon 1(rectangular):")
    for x in range(pixel()):
        for y in range(pixel()):
            if (x >= 10 and x <= 25 and y >= 5 and y <= 25):  # point inside the rectangular
                z_depth = 10
                if z_depth < zbuff[x][y] or zbuff[x][y] == 'inf':
                    intensity[x][y] = 1
                    zbuff[x][y] = z_depth
    print("------------------------Z buffer-------------------------")
    for x in range(pixel() - 1, -1, -1):
        print(zbuff[x])

    print("------------------------Intensity------------------------")
    for x in range(pixel() - 1, -1, -1):
        print(intensity[x])
    print("---------------------------------------------------------")

    print("Polygon 2(triangle):")
    for x in range(pixel()):
        for y in range(pixel()):
            if (y <= x and y <= 100 - 3 * x and y >= 20 - 1.0 / 3 * x):
                z_depth = 30 - 3.0 / 4 * x - 1.0 / 4 * y
                if z_depth < zbuff[x][y] or zbuff[x][y] == 'inf':
                    intensity[x][y] = 2
                    zbuff[x][y] = z_depth
    print("------------------------Z buffer-------------------------")
    for x in range(pixel() - 1, -1, -1):
        print(zbuff[x])

    print("------------------------Intensity------------------------")
    for x in range(pixel() - 1, -1, -1):
        print(intensity[x])
    print("---------------------------------------------------------")


# test
z_buffer_algo()