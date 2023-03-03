import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
path = os.path.dirname(os.path.abspath(__file__))


def torus(nx = 100, ny=100, r=1, R=2):
    theta = np.linspace(0, 2.*np.pi, ny)
    phi = np.linspace(0, 2.*np.pi, nx)
    theta, phi = np.meshgrid(theta, phi)
    c, a = R, r
    x = (c + a*np.cos(theta)) * np.cos(phi)
    y = (c + a*np.cos(theta)) * np.sin(phi)
    z = a * np.sin(theta)
    return x, y, z

def load_image(filename):
    img = plt.imread(filename)
    return img

def plot_image_on_torus(image, r=1, R=2, filename='catmap_torus.png'):
    x,y,z = torus(image.shape[0], image.shape[1], r=1, R=2)

    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_zlim(-3,3)
    ax1.plot_surface(x, y, z, rstride=5, cstride=5, facecolors=image) # color='k', edgecolors='w')
    ax1.view_init(36, 26)

    plt.savefig(path + f'/{filename}', dpi=200, bbox_inches='tight')

def plot_image(image, filename='catmap.png'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.imshow(image)
    plt.savefig(path + f'/{filename}', dpi=200, bbox_inches='tight')



if __name__ == '__main__':
    image = load_image(path + '/cat-stretching.png') #image = np.transpose(image, (1, 0, 2))
    plot_image_on_torus(image, filename='catmap_torus.png')
    plot_image(image, filename='catmap.png')