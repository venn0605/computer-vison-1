import numpy as np
import matplotlib.pyplot as plt


# Plot 2D points
def displaypoints2d(points):
  plt.figure(0)
  plt.plot(points[0,:],points[1,:], '.b')
  plt.xlabel('Screen X')
  plt.ylabel('Screen Y')
  plt.show()

# Plot 3D points
def displaypoints3d(points):
  fig = plt.figure(1)
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(points[0,:], points[1,:], points[2,:], 'b')
  ax.set_xlabel("World X")
  ax.set_ylabel("World Y")
  ax.set_zlabel("World Z")
  plt.show()


def cart2hom(points):
  """ Transforms from cartesian to homogeneous coordinates.

  Args:
    points: a np array of points in cartesian coordinates

  Returns:
    points_hom: a np array of points in homogeneous coordinates
  """

  shape = points.shape
  points_hom = np.concatenate((points, np.ones((1, shape[1]))), axis=0)
  # points_hom = np.ones((shape[0]+1, shape[1]))
  # points_hom[:-1, :] = points

  return points_hom

def hom2cart(points):
  """ Transforms from homogeneous to cartesian coordinates.

  Args:
    points: a np array of points in homogenous coordinates

  Returns:
    points_hom: a np array of points in cartesian coordinates
  """

  # shape = points.shape
  # points_car = np.zeros((shape[0], shape[1]-1))
  # for i in range(shape[0]):
  #       points_car[i, :] = points[i, :-1] / points[i, -1]

  return np.delete(points/points[-1], -1, axis=0)


def gettranslation(v):
  """ Returns translation matrix T in homogeneous coordinates for translation by v.

  Args:
    v: 3d translation vector

  Returns:
    T: translation matrix in homogeneous coordinates
  """
  n = len(v)
  T = np.identity(n+1)
  for i in range(n):
      T[i, -1] = v[i]

  return T


def getxrotation(d):
  """ Returns rotation matrix Rx in homogeneous coordinates for a rotation of d degrees around the x axis.

  Args:
    d: degrees of the rotation

  Returns:
    Rx: rotation matrix
  """

  d_radian = d * (np.pi/180)
  Rx = np.identity(4)
  Rx[1, 1] = np.cos(d_radian)
  Rx[1, 2] = - np.sin(d_radian)
  Rx[2, 1] = - Rx[1, 2]
  Rx[2, 2] = Rx[1, 1]

  return Rx



def getyrotation(d):
  """ Returns rotation matrix Ry in homogeneous coordinates for a rotation of d degrees around the y axis.

  Args:
    d: degrees of the rotation

  Returns:
    Ry: rotation matrix
  """
  d_radian = d * (np.pi/180)
  Ry = np.identity(4)
  Ry[0, 0] = np.cos(d_radian)
  Ry[0, 2] = np.sin(d_radian)
  Ry[2, 0] = - Ry[0, 2]
  Ry[2, 2] = Ry[0, 0]

  return Ry



def getzrotation(d):
  """ Returns rotation matrix Rz in homogeneous coordinates for a rotation of d degrees around the z axis.

  Args:
    d: degrees of the rotation

  Returns:
    Rz: rotation matrix
  """
  d_radian = d * (np.pi/180)
  Rz = np.identity(4)
  Rz[0, 0] = np.cos(d_radian)
  Rz[0, 1] = -np.sin(d_radian)
  Rz[1, 0] = - Rz[0, 1]
  Rz[1, 1] = Rz[0, 0]

  return Rz




def getcentralprojection(principal, focal):
  """ Returns the (3 x 4) matrix L that projects homogeneous camera coordinates on homogeneous
  image coordinates depending on the principal point and focal length.
  
  Args:
    principal: the principal point, 2d vector
    focal: focal length

  Returns:
    L: central projection matrix
  """

  L = np.zeros((3, 4))
  L[0, 0] = focal
  L[1, 1] = focal
  L[0, 2] = principal[0]
  L[1, 2] = principal[1]
  L[2, 2] = 1

  return L


def getfullprojection(T, Rx, Ry, Rz, L):
  """ Returns full projection matrix P and full extrinsic transformation matrix M.

  Args:
    T: translation matrix
    Rx: rotation matrix for rotation around the x-axis
    Ry: rotation matrix for rotation around the y-axis
    Rz: rotation matrix for rotation around the z-axis
    L: central projection matrix

  Returns:
    P: projection matrix
    M: matrix that summarizes extrinsic transformations
  """

  M = Rz.dot(Rx).dot(Ry).dot(T)
  P = L.dot(M)

  return P, M


def projectpoints(P, X):
  """ Apply full projection matrix P to 3D points X in cartesian coordinates.

  Args:
    P: projection matrix
    X: 3d points in cartesian coordinates

  Returns:
    x: 2d points in cartesian coordinates
  """

  X_hom = cart2hom(X)
  X_pro = P.dot(X_hom)
  x = hom2cart(X_pro)

  return x

def loadpoints():
  """ Load 2D points from obj2d.npy.

  Returns:
    x: np array of points loaded from obj2d.npy
  """

  return np.load(r'data\obj2d.npy')


def loadz():
  """ Load z-coordinates from zs.npy.

  Returns:
    z: np array containing the z-coordinates
  """

  return np.load(r'data\zs.npy')


def invertprojection(L, P2d, z):
  """
  Invert just the projection L of cartesian image coordinates P2d with z-coordinates z.

  Args:
    L: central projection matrix
    P2d: 2d image coordinates of the projected points
    z: z-components of the homogeneous image coordinates

  Returns:
    P3d: 3d cartesian camera coordinates of the points
  """

  P2d_hom = P2d * z
  L = np.delete(L, -1, axis=1)
  P3d = np.linalg.inv(L).dot(np.concatenate((P2d_hom, z), axis=0))

  return P3d


def inverttransformation(M, P3d):
  """ Invert just the model transformation in homogeneous coordinates
  for the 3D points P3d in cartesian coordinates.

  Args:
    M: matrix summarizing the extrinsic transformations
    P3d: 3d points in cartesian coordinates

  Returns:
    X: 3d points after the extrinsic transformations have been reverted
  """

  P3d_hom = cart2hom(P3d)
  X = np.linalg.inv(M).dot(P3d_hom)

  return X


def p3multiplecoice():
  '''
  Change the order of the transformations (translation and rotation).
  Check if they are commutative. Make a comment in your code.
  Return 0, 1 or 2:
  0: The transformations do not commute.
  1: Only rotations commute with each other.
  2: All transformations commute.
  '''

  return 0

if __name__ == "__main__":
    t = np.array([-27.1, -2.9, -3.2])
    principal_point = np.array([8, -10])
    focal_length = 8

    # model transformations
    T = gettranslation(t)
    Ry = getyrotation(135)
    Rx = getxrotation(-30)
    Rz = getzrotation(90)
    print(T)
    print(Ry)
    print(Rx)
    print(Rz)

    K = getcentralprojection(principal_point, focal_length)

    P,M = getfullprojection(T, Rx, Ry, Rz, K)
    print(P)
    print(M)
    print('test')

    points = loadpoints()
    displaypoints2d(points)

    z = loadz()

    Xt = invertprojection(K, points, z)

    Xh = inverttransformation(M, Xt)

    worldpoints = hom2cart(Xh)
    displaypoints3d(worldpoints)

    points2 = projectpoints(P, worldpoints)
    displaypoints2d(points2)

    plt.show()
