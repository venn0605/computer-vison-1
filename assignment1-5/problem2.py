import numpy as np
from scipy.ndimage import convolve
import matplotlib.pyplot as plt

def loaddata(path):
    """ Load bayerdata from file

    Args:
        Path of the .npy file
    Returns:
        Bayer data as numpy array (H,W)
    """

    return np.load(path)


def separatechannels(bayerdata):
    """ Separate bayer data into RGB channels so that
    each color channel retains only the respective
    values given by the bayer pattern and missing values
    are filled with zero

    Args:
        Numpy array containing bayer data (H,W)
    Returns:
        red, green, and blue channel as numpy array (H,W)
    """

    m = bayerdata.shape[0]
    n = bayerdata.shape[1]
    r_channel = np.zeros((m,n))
    g_channel = np.zeros((m,n))
    b_channel = np.zeros((m,n))
    for i in range(m):
        for j in range(n):
            if i%2 == 0 and j%2 == 1:
                r_channel[i, j] = bayerdata[i, j]
            if i%2 == 1 and j%2 == 0:
                b_channel[i, j] = bayerdata[i, j]
            if (i%2 == 0 and j%2 == 0) or (i%2 == 1 and j%2 == 1):
                g_channel[i, j] = bayerdata[i, j]

    return r_channel, g_channel, b_channel


def assembleimage(r, g, b):
    """ Assemble separate channels into image

    Args:
        red, green, blue color channels as numpy array (H,W)
    Returns:
        Image as numpy array (H,W,3)
    """
    m = r.shape[0]
    n = r.shape[1]
    image = np.zeros((m,n,3))
    image[:, :, 0] = r
    image[:, :, 1] = g
    image[:, :, 2] = b

    return image


def interpolate(r, g, b):
    """ Interpolate missing values in the bayer pattern
    by using bilinear interpolation

    Args:
        red, green, blue color channels as numpy array (H,W)
    Returns:
        Interpolated image as numpy array (H,W,3)
    """

    K_g = 1/4 * np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]])
    K_r = 1/4 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    K_b = 1/4 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])

    r_inter = convolve(r, K_r, mode='mirror')
    g_inter = convolve(g, K_g, mode='mirror')
    b_inter = convolve(b, K_b, mode='mirror')

    m = r.shape[0]
    n = r.shape[1]
    image_inter = np.zeros((m,n,3))
    image_inter[:, :, 0] = r_inter
    image_inter[:, :, 1] = g_inter
    image_inter[:, :, 2] = b_inter

    return image_inter


data = loaddata("U:/学习系列/cv1/assignment1-5/data/bayerdata.npy")
r, g, b = separatechannels(data)

img = assembleimage(r, g, b)
plt.imshow(img)

print('interpolation')
img_interpolated = interpolate(r, g, b)
plt.imshow(img_interpolated)

print('end')
