import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
path = os.path.dirname(os.path.abspath(__file__))
images_path = path + '/images/'
frames_path = path + '/frames/'


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

    plt.savefig(images_path + f'/{filename}', dpi=200, bbox_inches='tight')

def plot_image(image, filename='catmap.png'):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.imshow(image)
    plt.savefig(images_path + f'/{filename}', dpi=200, bbox_inches='tight')

from PIL.Image import open as load_pic, new as new_pic

def save_image(image, filename='catmap.png'):
    with new_pic('RGB', image.shape[:2]) as canvas:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                #print(x, y, image[x, y, :3])
                canvas.putpixel((x, y), tuple(255*int(pix) for pix in image[x, y, :3]))
        canvas.save(images_path + f'/{filename}')

def catmap(path, iterations, keep_all=False, name="arnold_cat-{name}-{index}.png"):
    """
    Params
        path:str
            path to photograph
        iterations:int
            number of iterations to compute
        name:str
            formattable string to use as template for file names
    """
    title = os.path.splitext(os.path.split(path)[1])[0]
    n_nums = len(str(iterations)) # number of digits in iterations (for padding)
    counter = 0
    base_image_path = images_path+path
    image_path = base_image_path
    while counter < iterations:
        with load_pic(image_path) as image:
            if counter == 0:
                #re-save original image using the same name
                image.save(frames_path+name.format(name=title, index='0'*n_nums))

            dim = width, height = image.size
            with new_pic(image.mode, dim) as canvas:
                for x in range(width):
                    for y in range(height):
                        nx = (2 * x + y) % width
                        ny = (x + y) % height

                        pixel = image.getpixel((x, height-y-1))
                        canvas.putpixel((nx, height-ny-1), pixel)

        if counter > 0 and not keep_all:
            os.remove(image_path)
        counter += 1
        print(counter, end="\r")
        path = name.format(name=title, index=str(counter).rjust(n_nums, '0'))
        image_path = frames_path+path
        canvas.save(image_path)

    return canvas


def make_circle(r, n):
    """
    Returns an image of a circle of radius r on an nxn canvas
    """
    canvas = np.zeros((n, n, 4))
    canvas[:, :, 3] = 1 # set alpha channel to 1
    for x in range(n):
        for y in range(n):
            if (x - n/2)**2 + (y - n/2)**2 <= r**2:
                canvas[x, y, :3] = 1 # set color to white
    return canvas

    


if __name__ == '__main__':
    circle = make_circle(50, 500)
    save_image(circle, filename='circle_500.png')
    #image = load_image(images_path + 'cat-stretching.png') #image = np.transpose(image, (1, 0, 2))
    canvas = catmap('circle_500.png', 5, keep_all=True)
    # plot_image_on_torus(image, filename='catmap_torus.png')
    # plot_image(image, filename='catmap.png')