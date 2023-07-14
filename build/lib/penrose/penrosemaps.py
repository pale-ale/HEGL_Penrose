from numpy import ndarray, array, arange, inner, ceil, power, pi, e, angle, zeros
from numpy.linalg import norm
from abc import abstractmethod, ABC
from geometry import Lattice, Line2D

class MapBase(ABC):
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
    ''''''
  
  @abstractmethod
  def validate_values(self):
    ''''''
  
  def update_values(self, *args, **kwargs):
    ''''''

class PenroseMap(MapBase):
  def __init__(self, gamma:ndarray) -> None:
    super().__init__()
    #assert abs(sum(gamma)) <= 1e-10
    self.gamma = gamma
    zeta = e ** (2j*pi/5)
    self.c_to_r5_factor = power(array([zeta]*5, None), -arange(5))
    self.r5_to_c_factor = power(array([zeta]*5, None),  arange(5))
    self.validate_values()

  def get_solution_space(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid. '''
        line = Line2D(0, pi/2 - angle(self.c_to_r5_factor[j]))
        return (line, imin, imax, float(norm(self.c_to_r5_factor[j])), -self.gamma[j])

  def c_to_r5(self, z: complex) -> ndarray:
    return ((z*self.c_to_r5_factor).real + self.gamma).round(10)
  
  def r5_to_r5(self, k: ndarray) -> ndarray:
    return ceil(k)

  def r5_to_c(self, k: ndarray) -> complex:
    return inner(k, self.r5_to_c_factor)
  
  def angle2(self, angles:ndarray) -> ndarray:
    result = zeros(len(angles), dtype=float)
    for i,ang in enumerate(angles):
      result[i] = ang if ang > 0 else 2*pi + ang
    return result
  
  def validate_values(self, sum_cr5=True, sum_r5c=True):
    if sum_cr5:
      assert abs(sum(self.c_to_r5_factor)) <= 1e-10
    if sum_r5c:
      assert abs(sum(self.r5_to_c_factor)) <= 1e-10


class NotQuitePenroseMap(PenroseMap):
  def __init__(self, gamma: ndarray) -> None:
    super().__init__(gamma)
    zeta = e ** (2j*pi/5)
    self.c_to_r5_factor = power(array([zeta]*5, complex), -arange(5))
    self.r5_to_c_factor = power(array([zeta]*5, complex),  arange(5))
    self.validate_values()
  
  def c_to_r5(self, z: complex) -> ndarray:
    return ((z*self.c_to_r5_factor).real + self.gamma).round(10)
  
  def update_values(self, *params:complex):
    ''''''
    self.c_to_r5_factor = power(e, 1j * array(params), dtype=complex)

 # self.inflationmatrix = array([
    #   [0,1,0,0,0], 
    #   [1,0,1,0,0],
    #   [0,1,0,1,0],
    #   [0,0,1,0,1],
    #   [0,0,0,1,0],
    # ])
    # self.zetas = self.zetas @ self.inflationmatrix
    # self.wi = self.wi @ self.inflationmatrix