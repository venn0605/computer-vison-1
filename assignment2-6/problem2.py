import numpy as np
import os
from PIL import Image


def load_faces(path, ext=".pgm"):
    """Load faces into an array (N, H, W),
    where N is the number of face images and
    H, W are height and width of the images.
    
    Hint: os.walk() supports recursive listing of files 
    and directories in a path
    
    Args:
        path: path to the directory with face images
        ext: extension of the image files (you can assume .pgm only)
    
    Returns:
        imgs: (N, H, W) numpy array
    """
    
    #
    # You code here
    #


def vectorize_images(imgs):
    """Turns an  array (N, H, W),
    where N is the number of face images and
    H, W are height and width of the images into
    an (N, M) array where M=H*W is the image dimension.
    
    Args:
        imgs: (N, H, W) numpy array
    
    Returns:
        x: (N, M) numpy array
    """
    
    #
    # You code here
    #


def compute_pca(X):
    """PCA implementation
    
    Args:
        X: (N, M) an numpy array with N M-dimensional features
    
    Returns:
        mean_face: (M,) numpy array representing the mean face
        u: (M, M) numpy array, bases with D principal components
        cumul_var: (N, ) numpy array, corresponding cumulative variance
    """

    #
    # You code here
    #


def basis(u, cumul_var, p = 0.5):
    """Return the minimum number of basis vectors 
    from matrix U such that they account for at least p percent
    of total variance.
    
    Hint: Do the singular values really represent the variance?
    
    Args:
        u: (M, M) numpy array containing principal components.
        For example, i'th vector is u[:, i]
        cumul_var: (N, ) numpy array, variance along the principal components.
    
    Returns:
        v: (M, D) numpy array, contains M principal components from N
        containing at most p (percentile) of the variance.
    
    """
    
    #
    # You code here
    #


def compute_coefficients(face_image, mean_face, u):
    """Computes the coefficients of the face image with respect to
    the principal components u after projection.
    
    Args:
        face_image: (M, ) numpy array (M=h*w) of the face image a vector
        mean_face: (M, ) numpy array, mean face as a vector
        u: (M, D) numpy array containing D principal components. 
        For example, (:, 1) is the second component vector.
    
    Returns:
        a: (D, ) numpy array, containing the coefficients
    """
    
    #
    # You code here
    #


def reconstruct_image(a, mean_face, u):
    """Reconstructs the face image with respect to
    the first D principal components u.
    
    Args:
        a: (D, ) numpy array containings the image coefficients w.r.t
        the principal components u
        mean_face: (M, ) numpy array, mean face as a vector
        u: (M, D) numpy array containing D principal components. 
        For example, (:, 1) is the second component vector.
    
    Returns:
        image_out: (M, ) numpy array, projected vector of face_image on 
        principal components
    """
    
    #
    # You code here
    #


def compute_similarity(Y, x, u, mean_face):
    """Compute the similarity of an image x to the images in Y
    based on the cosine similarity.

    Args:
        Y: (N, M) numpy array with N M-dimensional features
        x: (M, ) image we would like to retrieve
        u: (M, D) bases vectors. Note, we already assume D has been selected.
        mean_face: (M, ) numpy array, mean face as a vector

    Returns:
        sim: (N, ) numpy array containing the cosine similarity values
    """

    #
    # You code here
    #


def search(Y, x, u, mean_face, top_n):
    """Search for the top most similar images
    based on a given number of components in their PCA decomposition.
    
    Args:
        Y: (N, M) numpy array with N M-dimensional features
        x: (M, ) numpy array, image we would like to retrieve
        u: (M, D) numpy arrray, bases vectors. Note, we already assume D has been selected.
        mean_face: (M, ) numpy array, mean face as a vector
        top_n: integer, return top_n closest images in L2 sense.
    
    Returns:
        Y: (top_n, M) numpy array containing the top_n most similar images
        sorted by similarity
    """

    #
    # You code here
    #


def interpolate(x1, x2, u, mean_face, n):
    """Search for the top most similar images
    based on a given number of components in their PCA decomposition.
    
    Args:
        x1: (M, ) numpy array, the first image
        x2: (M, ) numpy array, the second image
        u: (M, D) numpy array, bases vectors. Note, we already assume D has been selected.
        mean_face: (M, ) numpy array, mean face as a vector
        n: number of interpolation steps (including x1 and x2)

    Hint: you can use np.linspace to generate n equally-spaced points on a line
    
    Returns:
        Y: (n, M) numpy arrray, interpolated results.
        The first dimension is in the index into corresponding
        image; Y[0] == project(x1, u); Y[-1] == project(x2, u)
    """

    #
    # You code here
    #
