from numpy import ndarray, array, arange, inner, ceil, power, pi, e, angle
from abc import abstractmethod, ABC
from geometry import Lattice, Line2D

class MapBase(ABC):
  @abstractmethod
  def c_to_r5(self, z:complex) -> ndarray:
    ''' Defines the mapping from the complex plane to R^5. '''
  
  @abstractmethod
  def r5_to_r5(self, k:ndarray) -> ndarray:
    ''' Defines the projection inside R^5. '''

  @abstractmethod 
  def r5_to_c(self, k:ndarray) -> complex:
    ''' Defines the map from R^5 to the complex plane. '''
  
  def update_values(self, *args, **kwargs):
    """"""

  def get_solution_space(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
    """"""

class PenroseMap(MapBase):
  def __init__(self, gamma:ndarray) -> None:
    super().__init__()
    assert abs(sum(gamma)) <= 1e-10
    self.gamma = gamma
    zeta = e ** (2j*pi/5)
    self.zetas     = power(array([zeta]*5, None),  arange(5))
    self.inv_zetas = power(array([zeta]*5, None), -arange(5))
  
  def get_solution_space(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid. '''
        line = Line2D(imin - self.gamma[j], angle(self.zetas[j]) + pi/2)
        return (line, imin, imax, 1, -self.gamma[j])

  def c_to_r5(self, z: complex) -> ndarray:
    return ((z*self.inv_zetas).real + self.gamma).round(10)
  
  def r5_to_r5(self, k: ndarray) -> ndarray:
    return ceil(k)

  def r5_to_c(self, k: ndarray) -> complex:
    return inner(k, self.zetas)

class NotQuitePenroseMap(PenroseMap):
  def __init__(self, gamma: ndarray) -> None:
    super().__init__(gamma)
    zeta = e ** (1.1 * 2j*pi/5)
    self.zetas     = power(array([zeta]*5, None),  arange(5))
    self.inv_zetas = power(array([zeta]*5, None), -arange(5))
    # self.inflationmatrix = array([
    #   [0,1,0,0,0], 
    #   [1,0,1,0,0],
    #   [0,1,0,1,0],
    #   [0,0,1,0,1],
    #   [0,0,0,1,0],
    # ])
    # self.zetas = self.zetas @ self.inflationmatrix
    # self.inv_zetas = self.inv_zetas @ self.inflationmatrix
  
  def update_values(self, param:complex):
    zeta = e ** (param * 2j*pi/5)
    self.zetas     = power(array([zeta]*5, None),  arange(5))
    self.inv_zetas = power(array([zeta]*5, None), -arange(5))

