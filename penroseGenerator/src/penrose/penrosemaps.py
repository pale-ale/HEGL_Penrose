'''
Contians a colleciton of maps used in the generation of Penrose (and Penrose-like) tilings.
'''

from abc import abstractmethod, ABC
from numpy import ndarray, array, arange, inner, ceil, power, pi, e, angle, modf, sqrt #pylint: disable=E0611
from numpy.linalg import norm
from penroseGenerator.src.core.geometry import Lattice, Line2D

class MapBase(ABC):
    '''
    The Base class for every map used to draw Penrose-like tilings.
    '''
    gamma:ndarray
    @abstractmethod
    def c_to_r5(self, z:complex) -> ndarray:
        ''' Defines the mapping from the complex plane to R^5. '''

    @abstractmethod
    def r5_to_r5(self, k:ndarray) -> ndarray:
        ''' Defines the projection inside R^5. '''

    @abstractmethod
    def r5_to_c(self, k:ndarray) -> complex:
        ''' Defines the map from R^5 to the complex plane. '''

    @abstractmethod
    def get_solution_space(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
        ''' The explicit version of the grid lines. '''

class PenroseMap(MapBase):
    '''
    Use this to obtain a normal penrose tiling
    '''
    def __init__(self, gamma:ndarray) -> None:
        super().__init__()
        self.phi =  (1+sqrt(5)) / 2
        self.gamma = gamma
        zeta = e ** (2j*pi/5)
        self.c_to_r5_factor = power(array([zeta]*5, None), -arange(5))
        self.r5_to_c_factor = power(array([zeta]*5, None),  arange(5))
        self.inflationmatrix = self.phi * array([
            [0,1,0,0,1],
            [1,0,1,0,0],
            [0,1,0,1,0],
            [0,0,1,0,1],
            [1,0,0,1,0],
        ], dtype=float)
        self.deflationmatrix = 1/self.phi * .5 * array([
            [1,1,-1,-1,1],
            [1,1,1,-1,-1],
            [-1,1,1,1,-1],
            [-1,-1,1,1,1],
            [1,-1,-1,1,1],

        ], dtype=float)
        self.validate_values()

    def get_solution_space(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid. '''
        line = Line2D(0, pi/2 - angle(self.c_to_r5_factor[j]))
        scale = 1/float(norm(self.c_to_r5_factor[j]))
        return (line, imin, imax, scale, -self.gamma[j] * scale )

    def c_to_r5(self, z: complex) -> ndarray:
        return ((z*self.c_to_r5_factor).real + self.gamma).round(10)

    def r5_to_r5(self, k: ndarray) -> ndarray:
        return ceil(k)

    def r5_to_c(self, k: ndarray) -> complex:
        return inner(k, self.r5_to_c_factor)

    def inflate(self):
        ''' Generate a new penrose map from the ecurrent one with smalle tiles. '''
        self.c_to_r5_factor = self.c_to_r5_factor @ self.inflationmatrix
        self.gamma = modf((self.gamma @ self.inflationmatrix))[0]

    def deflate(self):
        ''' Generate a new penrose map from the ecurrent one with larger tiles. '''
        self.c_to_r5_factor = self.c_to_r5_factor @ self.deflationmatrix
        self.gamma = modf((self.gamma @ self.deflationmatrix))[0]

    def validate_values(self, sum_cr5=True, sum_r5c=True):
        ''' Ensure that the sums of the different map values are zero. '''
        if sum_cr5:
            assert abs(sum(self.c_to_r5_factor)) <= 1e-10
        if sum_r5c:
            assert abs(sum(self.r5_to_c_factor)) <= 1e-10
