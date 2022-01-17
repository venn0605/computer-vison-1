import numpy as np
import matplotlib.pyplot as plt

def display_image(img):
    """ Show an image with matplotlib:

    Args:
        Image as numpy array (H,W,3)
    """

    return plt.imshow(img)


def save_as_npy(path, img):
    """ Save the image array as a .npy file:

    Args:
        Image as numpy array (H,W,3)
    """

    return np.save(path, img)


def load_npy(path):
    """ Load and return the .npy file:

    Args:
        Path of the .npy file
    Returns:
        Image as numpy array (H,W,3)
    """

    return np.load(path)


def mirror_horizontal(img):
    """ Create and return a horizontally mirrored image:

    Args:
        Loaded image as numpy array (H,W,3)

    Returns:
        A horizontally mirrored numpy array (H,W,3).
    """

    return np.fliplr(img)


def display_images(img1, img2):
    """ display the normal and the mirrored image in one plot:

    Args:
        Two image numpy arrays
    """

    fig, axs = plt.subplots(1, 2)
    # fig.subtitle('original and mirrored image')
    axs[0].imshow(img1)
    axs[1].imshow(img2)
    # fig = plt.figure(figsize=(10, 20))        ax1 = fig.add_subplot(2, 2, 1)

def load_image(path):
    return plt.imread(path)



"""Example code implementing the steps in Problem 1"""

img = load_image("U:/学习系列/cv1/assignment1-5/data/a1p1.png")
display_image(img)

save_as_npy("a1p1.npy", img)

img1 = load_npy("a1p1.npy")
display_image(img1)

img2 = mirror_horizontal(img1)
display_image(img2)

display_images(img1, img2)

print('end')
# cur_dir  = os.path.dirname(os.path.abspath(__file__))
# root_dir = os.path.dirname(cur_dir)