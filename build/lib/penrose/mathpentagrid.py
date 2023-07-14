from math import e, pi
from geometry import Lattice, Line2D
from penrosemaps import MapBase
from numpy import ndarray, array, zeros

class MathPentagrid():
    ''' Provides helpers for calculating a pentagrid and transforming vertices. '''
    def __init__(self, penrosemap:MapBase) -> None:
        assert isinstance(penrosemap, MapBase)
        self.penrosemap = penrosemap

    def is_on_grid(self, z:complex, j:int):
        ''' Return whether `z` is part of the `j`-th grid. '''
        assert 0 <= j <= 4
        tmp = self.penrosemap.c_to_r5(z)[j]
        return abs(tmp - round(tmp, 11)) <= 1e-10
    
    def reverse_is_on_grid(self, j:int, imin:int=-5, imax:int=5) -> Lattice:
        ''' Return imax-imin of parameterized parallel lines representing the jth grid. '''
        return self.penrosemap.get_solution_space(j, imin, imax)
    
    def get_Ks(self, z:complex):
        ''' Returns the "indices" of the next integer grid line for every grid. '''
        return self.penrosemap.r5_to_r5(self.penrosemap.c_to_r5(z))

    def get_verts_from_intersect(self, z:complex, r:int, s:int):
        delta1 = zeros(5, int); delta1[r]=1
        delta2 = zeros(5, int); delta2[s]=1
        vertices = ndarray((4,2), float)
        es = [[0,0], [0,1], [1,1], [1,0]]
        ks = self.get_Ks(z)
        for i,(e1,e2) in enumerate(es):
            vertex5d = ks + e1*delta1 + e2*delta2
            vertex2d = self.penrosemap.r5_to_c(vertex5d)
            vertices[i:,] = array([vertex2d.real, vertex2d.imag])
        return vertices