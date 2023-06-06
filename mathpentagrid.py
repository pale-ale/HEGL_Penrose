from numpy import array, ndarray, power, fromiter, inner
from math import e, pi, ceil
from geometry import Line2D

class MathPentagrid():
    ''' Provides helpers for calculating a pentagrid and transforming vertices. '''
    def __init__(self, gamma:ndarray) -> None:
        assert abs(sum(gamma)) <= 1e-10
        self.gamma = gamma
        self.xi = e ** (2j*pi/5)
        self.xis = power(array([self.xi]*5), (0,1,2,3,4))

    def is_on_grid(self, z:complex, j:int):
        ''' Return whether `z` is part of the `j`-th grid. '''
        assert 0 <= j <= 4
        tmp = (z * (self.xi**-j)).real + self.gamma[j]
        return abs(tmp - round(tmp, 11)) <= 1e-10
    
    def reverse_is_on_grid(self, j:int, imin:int=-5, imax:int=5) -> list[Line2D]:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid. '''
        assert 0 <= j <= 4
        lines:list[Line2D] = []
        for i in range(imin, imax+1):
            line = Line2D(i - self.gamma[j], 2*pi*j/5 + pi/2)
            lines.append(line)
        return lines
    
    def get_kj(self, z:complex, j:int):
        ''' Returns the "index" of the next integer grid line. '''
        return ceil((z*self.xi**-j).real + self.gamma[j])
    
    def get_Ks(self, z:complex):
        ''' Returns the "indices" of the next integer grid line for every grid. '''
        return fromiter((self.get_kj(z, j) for j in range(5)), int, count=5)

    def k_times_xi(self, k:ndarray):
        ''' Return `k` transformed from 5D to 2D. '''
        return inner(k, self.xis)