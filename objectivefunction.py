#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ObjectiveFunction:
    def evaluate(self, solution):
        """ 
        @param solution: solución que se evaluaré con respecto a la
                         función objetivo.
        """
        raise NotImplementedError("evaluate method has to be implemented.")
    

class QAPObjectiveFunction(ObjectiveFunction):
    def __init__(self, dist_mat, flux_mat):
        """ 
        @param dist_mat: matriz de adyacencias de distancias parseada.
        @para flux_mat: matriz de adyacencias de flujos parseada.
        """
        self.dist_mat = dist_mat
        self.flux_mat = flux_mat
        
    def evaluate(self, solution):
        """ 
        @param solution: solución QAP con formato:
                         [2,3,5,...,n]. Se lee el edificio 2 se ubica en
                         la localidad 0.
                         .
        """ 
        path = solution.solution
        path_cost = 0
        for i in range(len(path)):
            for j in range(len(path)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[path[i]][path[j]]
                    path_cost = path_cost + distance * flux
        return path_cost

    def cost_i_to_j(self, k, l):
        path = [k, l]
        path_cost = 0
        for i in range(len(path)):
            for j in range(i, len(path)):
                    distance = self.dist_mat[i][j]
                    flux = self.flux_mat[path[i]][path[j]]
                    path_cost = path_cost + distance * flux
        return path_cost

