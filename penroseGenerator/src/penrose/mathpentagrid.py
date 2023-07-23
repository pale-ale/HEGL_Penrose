''' Acts as a facade for the maps defined in penrosemaps.py. '''

import numpy as np
from penroseGenerator.src.core.geometry import Lattice
from penroseGenerator.src.penrose.penrosemaps import PenroseMap

class MathPentagrid():
    ''' Provides helpers for calculating a pentagrid and transforming vertices. '''
    def __init__(self, penrosemap:PenroseMap) -> None:
        assert isinstance(penrosemap, PenroseMap)
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
        ''' Return the vertices for the rhomb determined by the intersection of 2 grids. '''
        delta1 = np.zeros(5, float)
        delta1[r]=1
        delta2 = np.zeros(5, float)
        delta2[s]=1
        vertices = np.ndarray((4,2), float)
        epsilons = [[0,0], [0,1], [1,1], [1,0]]
        k_vals = self.get_Ks(z)
        for i,(e_1,e_2) in enumerate(epsilons):
            vertex5d = k_vals + e_1*delta1 + e_2*delta2
            vertex2d = self.penrosemap.r5_to_c(vertex5d)
            vertices[i:,] = np.array([vertex2d.real, vertex2d.imag])
        return vertices
