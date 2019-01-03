#!/usr/python
""" Fire effect a la "DOOM"
    Original inspiration from Fabien Sanglard: http://fabiensanglard.net/doom_fire_psx/
"""


import random
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib import animation

import matplotlib
import numpy as np

# Values copied from https://github.com/fabiensanglard/DoomFirePSX/blob/master/flames.html
# Indiced from 0 to 36, white corresponds to 36 and 0 to black.
RGBS = [
  0x07, 0x07, 0x07,
  0x1F, 0x07, 0x07,
  0x2F, 0x0F, 0x07,
  0x47, 0x0F, 0x07,
  0x57, 0x17, 0x07,
  0x67, 0x1F, 0x07,
  0x77, 0x1F, 0x07,
  0x8F, 0x27, 0x07,
  0x9F, 0x2F, 0x07,
  0xAF, 0x3F, 0x07,
  0xBF, 0x47, 0x07,
  0xC7, 0x47, 0x07,
  0xDF, 0x4F, 0x07,
  0xDF, 0x57, 0x07,
  0xDF, 0x57, 0x07,
  0xD7, 0x5F, 0x07,
  0xD7, 0x5F, 0x07,
  0xD7, 0x67, 0x0F,
  0xCF, 0x6F, 0x0F,
  0xCF, 0x77, 0x0F,
  0xCF, 0x7F, 0x0F,
  0xCF, 0x87, 0x17,
  0xC7, 0x87, 0x17,
  0xC7, 0x8F, 0x17,
  0xC7, 0x97, 0x1F,
  0xBF, 0x9F, 0x1F,
  0xBF, 0x9F, 0x1F,
  0xBF, 0xA7, 0x27,
  0xBF, 0xA7, 0x27,
  0xBF, 0xAF, 0x2F,
  0xB7, 0xAF, 0x2F,
  0xB7, 0xB7, 0x2F,
  0xB7, 0xB7, 0x37,
  0xCF, 0xCF, 0x6F,
  0xDF, 0xDF, 0x9F,
  0xEF, 0xEF, 0xC7,
  0xFF, 0xFF, 0xFF
]

def group(lst, n):
  """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

  Group a list into consecutive n-tuples. Incomplete tuples are
  discarded e.g.
  >>> group(range(10), 3)
  [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
  """
  return zip(*[lst[i::n] for i in range(n)])


def transformToRGB(lst):
  """
   Change representation from 0-255 to 0-1, for triples value corresponding to RGB.
  """
  def normToOne(x): return float(x)/255.
  return [(normToOne(x), normToOne(y), normToOne(z)) for x, y, z in lst]





def makeFire(firePixels):
  FIRE_HEIGHT = firePixels.shape[0]
  FIRE_WIDTH = firePixels.shape[1]
  for x in range(1, FIRE_HEIGHT):  # It starts from 1 cause we never touch the bottom line
    for y in range(FIRE_WIDTH):
      spreadFire(x, y, firePixels)

def correctIndex(i, size):
  if i >= size:
    i = size -1
  if i < 0:
    i = 0
  return i

def spreadFire(x, y, firePixels):
  horiz = random.randint(-2, 2) + y
  verti = random.randint(-1, 6) + x
  horiz = correctIndex(horiz, firePixels.shape[1])
  verti = correctIndex(verti, firePixels.shape[0])
  colorIndex = firePixels[x-1, y] - random.randint(0, 3)
  if colorIndex < 0.:
    colorIndex = 0.
  firePixels[verti, horiz] = colorIndex


def update(iteration, im, data2):
  makeFire(data2)
  im.set_data(data2)
  return im


def main():
  rgbs = transformToRGB(group(RGBS, 3))
  colormap = matplotlib.colors.ListedColormap(rgbs, name='my_colormap')
  fig, ax = plt.subplots(1, 1)

  SIZE = 128
  # X is vertical while Y is horizontal. The origin (0,0) is in bottom left corner.
  # We init the  bottom line with white (36) and all other pixels are set to 0 (black).
  firePixels = np.zeros((SIZE, SIZE), dtype='int32')
  firePixels[0, :] = 36
  im = ax.imshow(firePixels, interpolation='nearest',
                 origin='lower',
                 cmap=colormap)

  anim = animation.FuncAnimation(
    fig, update, frames=150*50, interval=50, fargs=(im, firePixels))
  plt.show()


if __name__ == '__main__':
  main()
