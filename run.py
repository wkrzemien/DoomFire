#!/usr/python
# http://fabiensanglard.net/doom_fire_psx/


import random
import matplotlib.colors 
import matplotlib.pyplot as plt
from  matplotlib import animation

import matplotlib
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

FIRE_WIDTH = 512
FIRE_HEIGHT = 512 
# firePixels = FIRE_WIDTH * FIRE_WIDTH * [0]
# firePixels[FIRE_WIDTH * FIRE_WIDTH -1] = 36
def group(lst, n):
  """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
  
  Group a list into consecutive n-tuples. Incomplete tuples are
  discarded e.g.
  >>> group(range(10), 3)
  [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
  """
  return zip(*[lst[i::n] for i in range(n)])
def transformToRGB(lst):
  normToOne = lambda x: float(x)/255.
  return [(normToOne(x), normToOne(y), normToOne(z)) for x,y,z in lst]
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
# colormap = matplotlib.colors.Colormap(rgbs)

# 0 to 36
# init in bottom by white (36) and all other to 0 (black)
# we never change the bottom line


def makeFire(firePixels):
  for x in range(FIRE_WIDTH):
    for y in range(1, FIRE_HEIGHT):
      spreadFire(x,y, firePixels)


def spreadFire(x,y, firePixels):
  # rand = random.randint(0, 3) & 3
  # rand = random.randint(0, 3) 
  # dst = src - rand + 1
  step = 1./36. 
  val = firePixels[x,y -1] + step
  if val >1.:
    val = 1.
  firePixels[x,y] = val 
  # firePixels[dst - FIRE_WIDTH] = firePixels[src] - (rand & 1)

def init():
  pass
def update(num, im, data2):
  print data2
  makeFire(data2)
  im.set_data(data2)
  return (im, data2)

def main():
  print rgbs
  # pass
  # print colormap
  # print colormap(0.5)
  # https://stackoverflow.com/questions/15992149/how-to-update-pcolor-in-matplotlib
  # figure set up
  fig, ax = plt.subplots(1, 1)

  #fake data
  # x = np.linspace(0, 5, FIRE_WIDTH)
  # X, Y = np.meshgrid(x, x)
  firePixels = np.zeros((FIRE_WIDTH,FIRE_HEIGHT))
  firePixels[FIRE_HEIGHT-1,:]= 255./255
  # FIRE_WIDTH * FIRE_WIDTH * [0]
  # firePixels[FIRE_WIDTH * FIRE_WIDTH -1] = 36
  # makeFire(firePixels)
  data2= firePixels
  # data2 = np.sin(X ** 2 + Y **2)

  # plot the first time#fake data

  im = ax.imshow(data2, interpolation='nearest',
                 origin='bottom',
                 aspect='auto', # get rid of this to have equal aspect
                 vmin=np.min(data2),
                 vmax=np.max(data2),
                 # cmap='jet')
                 cmap=colormap)


# # update_data (imshow)
  anim = animation.FuncAnimation(fig, update, frames=150*50, interval=50, fargs=(im, data2))
  plt.show()

if __name__ == '__main__':
  main()
