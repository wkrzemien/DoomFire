#!/usr/python
# http://fabiensanglard.net/doom_fire_psx/


import random
import matplotlib.colors
import matplotlib.pyplot as plt
from matplotlib import animation

import matplotlib
import numpy as np


def pause():
  programPause = raw_input("Press the <ENTER> key to continue...")


FIRE_WIDTH = 320
FIRE_HEIGHT = 320


def group(lst, n):
  """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]

  Group a list into consecutive n-tuples. Incomplete tuples are
  discarded e.g.
  >>> group(range(10), 3)
  [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
  """
  return zip(*[lst[i::n] for i in range(n)])


def transformToRGB(lst):
  def normToOne(x): return float(x)/255.
  return [(normToOne(x), normToOne(y), normToOne(z)) for x, y, z in lst]


rgbs = [
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
rgbs = transformToRGB(group(rgbs, 3))
colormap = matplotlib.colors.ListedColormap(rgbs, name='my_name')

# 0 to 36
# init in bottom by white (36) and all other to 0 (black)
# we never change the bottom line


def makeFire(firePixels):
  for x in range(1, FIRE_WIDTH):
    for y in range(FIRE_HEIGHT):
      spreadFire4(x, y, firePixels)


def spreadFire1(x, y, firePixels):
  val = firePixels[x, y] + 1
  if val > 36.:
    val = 36.
  firePixels[x, y] = val


def spreadFire2(x, y, firePixels):
  val = firePixels[x-1, y] - 1
  if val < 0.:
    val = 0.
  firePixels[x, y] = val


def spreadFire3(x, y, firePixels):
  rand = random.randint(0, 3)
  val = firePixels[x-1, y] - rand
  if val < 0.:
    val = 0.
  firePixels[x, y] = val


def spreadFire4(x, y, firePixels):
  dst = random.randint(-2, 2) + y
  if dst >= FIRE_HEIGHT:
    dst = FIRE_HEIGHT - 1
  if dst < 0:
    dst = 0
  rand = random.randint(0, 3)
  val = firePixels[x-1, y] - rand
  if val < 0.:
    val = 0.
  firePixels[x, dst] = val


def update(num, im, data2):
  print "num=" + str(num)
  print data2
  pause()
  makeFire(data2)
  im.set_data(data2)
  return im


def main():
  fig, ax = plt.subplots(1, 1)

  SIZE = 320
  firePixels = np.zeros((SIZE, SIZE), dtype='int32')
  # X is vertical while Y is horizontal, the (0,0) is in bottom left corner
  firePixels[0, :] = 36
  im = ax.imshow(firePixels, interpolation='nearest',
                 origin='lower',
                 aspect='auto',  # get rid of this to have equal aspect
                 vmin=np.min(firePixels),
                 vmax=np.max(firePixels),
                 cmap=colormap)

  anim = animation.FuncAnimation(
      fig, update, frames=150*50, interval=50, fargs=(im, firePixels))
  plt.show()


if __name__ == '__main__':
  main()
