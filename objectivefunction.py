#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ObjectiveFunction:
    def evaluate(self, solution):
        raise NotImplementedError()
    

class QAPObjectiveFunction(ObjectiveFunction):
    def __init__(self, dist_mat, flux_mat):
        self.dist_mat = dist_mat
        self.flux_mat = flux_mat
        
    def evaluate(self, solution):
        camino = solution.solution
        costo_camino = 0
        for i in range(len(camino)):
            for j in range(len(camino)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[camino[i]][camino[j]]
                    costo_camino = costo_camino + distance * flux
        return costo_camino

    def cost_i_to_j(self, k, l):
        camino = [k, l]
        costo_camino = 0
        for i in range(len(camino)):
            for j in range(i, len(camino)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[camino[i]][camino[j]]
                    costo_camino = costo_camino + distance * flux
        return costo_camino

