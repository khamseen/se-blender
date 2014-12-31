from collections import namedtuple
from enum import IntEnum
from mathutils import Matrix, Vector

# just give proper axis names to the matrix indices
X = 0
Y = 1
Z = 2
W = 3

def sparse(values):
    """
    constructs a sparse matrix from a list of tuples (col, row, value)
    """
    result = Matrix()
    result.zero()
    result[W][W] = 1
    for cell in values:
        result.col[cell[0]][cell[1]] = cell[2]
    return result

# shorter but still understandable factory methods

def transX(x):
    return Matrix.Translation((x, 0, 0))

def transY(y):
    return Matrix.Translation((0, y, 0))

def transZ(z):
    return Matrix.Translation((0, 0, z))

def trans(vector):
    return Matrix.Translation(vector)

def rotX(rad):
    return Matrix.Rotation(rad, 4, 'X')

def rotY(rad):
    return Matrix.Rotation(rad, 4, 'Y')

def rotZ(rad):
    return Matrix.Rotation(rad, 4, 'Z')


# ----------------------------------- predefined transformations ------------------------------------ #


_mirrorX = Matrix((
    (-1.0,  0.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_mirrorY  = Matrix((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0, -1.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_mirrorZ = Matrix((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0, -1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))

_projectXY = Matrix((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_projectXZ = Matrix((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_projectYZ = Matrix((
    ( 0.0,  0.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))

_flipXY = Matrix((
    ( 0.0,  1.0,  0.0,  0.0),
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_flipXZ = Matrix((
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_flipYZ = Matrix((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))

class MatrixWithOpposite(Matrix):
    opposite = None

    def __neg__(self):
        return self.opposite

_rotHalfX = MatrixWithOpposite((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0, -1.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotMinusHalfX = MatrixWithOpposite((
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0, -1.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotFullX = MatrixWithOpposite(_mirrorY * _mirrorZ)

_rotHalfX.opposite = _rotMinusHalfX
_rotMinusHalfX.opposite = _rotHalfX
_rotFullX.opposite = _rotFullX

_rotHalfY = MatrixWithOpposite((
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    (-1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotMinusHalfY = MatrixWithOpposite((
    ( 0.0,  0.0, -1.0,  0.0),
    ( 0.0,  1.0,  0.0,  0.0),
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotFullY = MatrixWithOpposite(_mirrorX * _mirrorZ)

_rotHalfY.opposite = _rotMinusHalfY
_rotMinusHalfY.opposite = _rotHalfY
_rotFullY.opposite = _rotFullY

_rotHalfZ = MatrixWithOpposite((
    ( 0.0, -1.0,  0.0,  0.0),
    ( 1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotMinusHalfZ = MatrixWithOpposite((
    ( 0.0,  1.0,  0.0,  0.0),
    (-1.0,  0.0,  0.0,  0.0),
    ( 0.0,  0.0,  1.0,  0.0),
    ( 0.0,  0.0,  0.0,  1.0),
))
_rotFullZ = MatrixWithOpposite(_mirrorX * _mirrorY)

_rotHalfZ.opposite = _rotMinusHalfZ
_rotMinusHalfZ.opposite = _rotHalfZ
_rotFullZ.opposite = _rotFullZ

# now make them public as class-members to simplify imports

class mirror:
    x = yz = _mirrorX
    y = xz = _mirrorY
    z = xy = _mirrorZ

class flip:
    xy = _flipXY
    xz = _flipXZ
    yz = _flipYZ

class project:
    xy = _projectXY
    xz = _projectXZ
    yz = _projectYZ

class rot:
    x = _rotFullX
    y = _rotFullY
    z = _rotFullZ
    halfx = _rotHalfX
    halfy = _rotHalfY
    halfz = _rotHalfZ


class BoxCorner(IntEnum):
    """
    corner indices in terms of Object.bound_box,
    letter codes meaning Front/Back, Top/Bottom, Left/Right
    The directions are relative to a viewpoint in front of the object.
    So 'left' is 'left' in Blender but 'right' in Space Engineers and vice versa
    """
    FBL = 0
    FTL = 1
    BTL = 2
    BBL = 3
    FBR = 4
    FTR = 5
    BTR = 6
    BBR = 7

"""
The 8 vectors that define a bounding box
The fields are letter-coded: Front/Back, Top/Bottom, Left/Right
"""
BoundingBox = namedtuple('BoundingBox', ('fbl', 'ftl', 'btl', 'bbl', 'fbr', 'ftr', 'btr', 'bbr'))

_INF_M = float('-inf')
_INF_P = float('+inf')

def bounds(vertices):
    """
    Caculates the bounding-box around the given vertices.
    """
    minX = minY = minZ = _INF_P
    maxX = maxY = maxZ = _INF_M

    for v in vertices:
        x, y, z = v
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)
        minZ = min(minZ, z)
        maxZ = max(maxZ, z)

    return BoundingBox(
        Vector((minX, minY, minZ)), #FBL
        Vector((minX, minY, maxZ)), #FTL
        Vector((minX, maxY, maxZ)), #BTL
        Vector((minX, maxY, minZ)), #BBL
        Vector((maxX, minY, minZ)), #FBR
        Vector((maxX, minY, maxZ)), #FTR
        Vector((maxX, maxY, maxZ)), #BTR
        Vector((maxX, maxY, minZ)), #BBR
    )


def layers(bitset):
    """
    Takes a 20 bit bitset and turns it into sequence of 20 booleans.
    The first element in the sequence is the most significant bit of the bitset.
    """
    layers = [False] * 20
    for bit in range(20):
        layers[19-bit] = (bitset & (1 << bit) != 0)
    return layers


def bitset(layers):
    """
    Takes a sequence of 20 booleans and turns them into a bitset.
    The first element in the sequence is the most significant bit of the bitset.
    """
    bitset = 0x0
    for i, layer in enumerate(layers):
        if layer:
            bitset = bitset | (1 << (19 - i))
    return bitset