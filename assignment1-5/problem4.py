import math
import numpy as np
from scipy import ndimage


def gauss2d(sigma, fsize):
  """
  Args:
    sigma: width of the Gaussian filter
    fsize: dimensions of the filter

  Returns:
    g: *normalized* Gaussian filter
  """

  g = np.zeros((fsize, 1))
  offset = fsize // 2
  for i in range(-offset, -offset + fsize):
     g[i + offset] = 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-(i**2) / 2*sigma**2) \
  
  g = g / g.sum()

  return g


def createfilters():
  """
  Returns:
    fx, fy: filters as described in the problem assignment
  """

  g = gauss2d(0.9, 3)
  d_x = np.array([-1, 0, 1])
  d_x = d_x[np.newaxis, :]
  fx = g.dot(d_x)
  fy = d_x.T.dot(g.T)

  return fx, fy


def filterimage(I, fx, fy):
  """ Filter the image with the filters fx, fy.
  You may use the ndimage.convolve scipy-function.

  Args:
    I: a (H,W) numpy array storing image data
    fx, fy: filters

  Returns:
    Ix, Iy: images filtered by fx and fy respectively
  """

  Ix = ndimage.convolve(I, fx, mode='constant', cval=0.0)
  Iy = ndimage.convolve(I, fy, mode='constant', cval=0.0)

  return Ix, Iy


def detectedges(Ix, Iy, thr):
  """ Detects edges by applying a threshold on the image gradient magnitude.

  Args:
    Ix, Iy: filtered images
    thr: the threshold value

  Returns:
    edges: (H,W) array that contains the magnitude of the image gradient at edges and 0 otherwise
  """

  magitude = np.sqrt(Ix**2 + Iy**2)
  edges= np.where(magitude >= thr, magitude, 0)

  return edges



def nonmaxsupp(edges, Ix, Iy):
  """ Performs non-maximum suppression on an edge map.

  Args:
    edges: edge map containing the magnitude of the image gradient at edges and 0 otherwise
    Ix, Iy: filtered images

  Returns:
    edges2: edge map where non-maximum edges are suppressed
  """
  m, n = edges.shape
  edges2 = np.zeros((m, n))
  for i in range(1, m-1):
        for j in range(1, n-1):
            theta = np.arctan(Iy[i, j] / Ix[i, j]) * 180 / np.pi
  # handle top-to-bottom edges: theta in [-90, -67.5] or (67.5, 90]
            if (-90 <= theta <= -67.5) or (67.5 < theta <= 90):
                  q, r = edges[i-1, j], edges[i+1, j]
  # handle left-to-right edges: theta in (-22.5, 22.5]
            elif -22.5 < theta <= 22.5:
                  q, r = edges[i, j-1], edges[i, j+1]
  # handle bottomleft-to-topright edges: theta in (22.5, 67.5]
            elif 22.5 < theta <= 67.5:
                  q, r = edges[i+1, j-1], edges[i-1, j+1]
  # handle topleft-to-bottomright edges: theta in [-67.5, -22.5]
            elif -67.5 <= theta <= -22.5:
                  q, r = edges[i-1, j-1], edges[i+1, j+1]

            if (edges[i, j] >= q) and (edges[i, j] >= r):
                  edges2[i, j] = edges[i, j]
  return edges2        
