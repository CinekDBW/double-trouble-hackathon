from PIL import Image
from numpy import asarray, sqrt
import numpy as np
from scipy import ndimage
from scipy.ndimage.filters import convolve

path = "images/img4.jpg"
img = Image.open(path)
array = asarray(img)
img.show()

def grayscale(array):
    # changing from rgba to rgb if needed (png)
    array = array[..., :3]
    # matrix multiplication to get grayscale
    return np.dot(array, [0.2627, 0.6780, 0.0593])


def gauss(size, sigma=1):
    half = int(size) // 2
    x, y = np.mgrid[-half:half + 1, -half:half + 1]
    denom = 2.0 * np.pi * sigma ** 2
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2))) / denom
    return g


def sobel_filter(array):
    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1],
                   [0, 0, 0],
                   [-1, -2, -1]], np.float32)

    Ix = ndimage.filters.convolve(array, Kx)
    Iy = ndimage.filters.convolve(array, Ky)

    G = np.zeros(array.shape, dtype=np.float32)

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            G[i][j] = sqrt(Ix[i][j] ** 2 + Iy[i][j] ** 2)

    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)

    return (G, theta)


def non_max_suppression(array, theta):
    image = np.zeros(array.shape, dtype=np.int32)

    for i in range(theta.shape[0]):
        for j in range(theta.shape[1]):
            if (theta[i][j] < 0):
                theta[i][j] += np.pi

    for i in range(1, array.shape[0] - 1):
        for j in range(1, array.shape[1] - 1):
            q = 255
            r = 255

            if (0 <= theta[i, j] < np.pi / 8) or (np.pi * 7 / 8 <= theta[i, j] <= np.pi):
                q = array[i, j + 1]
                r = array[i, j - 1]
            elif np.pi / 8 <= theta[i, j] < np.pi * 3 / 8:
                q = array[i + 1, j - 1]
                r = array[i - 1, j + 1]
            elif np.pi * 3 / 8 <= theta[i, j] < np.pi * 5 / 8:
                q = array[i + 1, j]
                r = array[i - 1, j]
            elif np.pi * 5 / 8 <= theta[i, j] < np.pi * 7 / 8:
                q = array[i - 1, j - 1]
                r = array[i + 1, j + 1]
            if (array[i, j] >= q) and (array[i, j] >= r):
                image[i, j] = array[i, j]
            else:
                image[i, j] = 0
    return image


def threshold(array, lowRatio, highRatio):
    high = 255 * highRatio
    low = high * lowRatio

    output = np.zeros(array.shape, dtype=np.int32)

    weak = 25
    strong = 255

    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if array[i][j] >= high:
                output[i][j] = strong
            elif array[i][j] >= low:
                output[i][j] = weak

    return output, weak, strong


def hysteresis(array, weak_pix, strong_pix):
    y = array.shape[0]
    x = array.shape[1]

    # looking if there is a strong pixel around
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            if (array[j][i] == weak_pix):
                if ((array[j - 1][i - 1] == strong_pix) or
                        (array[j - 1][i] == strong_pix) or
                        (array[j - 1][i + 1] == strong_pix) or

                        (array[j][i - 1] == strong_pix) or
                        (array[j][i + 1] == strong_pix) or

                        (array[j + 1][i - 1] == strong_pix) or
                        (array[j + 1][i] == strong_pix) or
                        (array[j + 1][i + 1] == strong_pix)):
                    array[j][i] = strong_pix
                else:
                    array[j][i] = 0

    return array


array = grayscale(array)
array = convolve(array, gauss(5))
g, theta = sobel_filter(array)
array = non_max_suppression(g, theta)
array, weak_pix, strong_pix = threshold(array, 0.05, 0.20)
array = hysteresis(array, weak_pix, strong_pix)

img = Image.fromarray(array)
img.show()

filename = path.split('/')[-1].split('.')[0]
Image.fromarray(array).convert('RGB').save('outputs/'+filename+'.png')