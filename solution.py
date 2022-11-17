#!/usr/bin/env python
# -*- coding: utf-8 -*-

from objectivefunction import *

import numpy as np
import matplotlib.pyplot as plt

class Solution:
    def __init__(self, solution, objectives):
        self.solution = solution
        self.objectives = objectives
        
    def evaluate(self):
        return [o.evaluate(self) for o in self.objectives]
        
    def dominates(self, other_solution):
        band = False 
        for obj in self.objectives:
            if obj.evaluate(self) > obj.evaluate(other_solution):
                band = False
                break
            else:
                if obj.evaluate(self) <= obj.evaluate(other_solution):
                    band = True
        return band
    
    def __eq__(self, other):
        return self.solution == other.solution
    
    def __ne__(self, other):
        return self.solution != other.solution


class ParetoSet:

    def __init__(self, solutions=None):
        self.solutions = solutions
        
    def update(self, candidates):
        if not self.solutions:
            self.solutions = [candidates[0]]
            candidates = candidates[1:]
            
        for candidate in candidates:
            band, to_delete = self.domination_check(candidate)
            if not band: 
                self.solutions = [s for s in self.solutions if s not in to_delete]
                self.solutions.append(candidate)

    def domination_check(self, candidate):
        to_delete = []
        for solution in self.solutions:
            if solution.dominates(candidate):
                return True,[] 
            else:
                if candidate.dominates(solution): 
                    to_delete.append(solution)         
        return False, to_delete 
                
class ParetoFront:
    def __init__(self, pareto_set):
        self.pareto_front = [s.evaluate() for s in pareto_set.solutions]
        
    def draw(self, subplot=111):
        fig = plt.figure()
        pf_ax = fig.add_subplot(subplot)
        pf_ax.set_title(u"Pareto Front")
        for p in self.pareto_front:
            pf_ax.scatter(p[0], p[1], marker='o', facecolor='red')
        plt.show()
    
