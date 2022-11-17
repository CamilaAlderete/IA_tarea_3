#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, sys, math
from solution import Solution
import numpy as np

class GaSolution(Solution, object):
    def __init__(self, solution, objectives):
        Solution.__init__(self, solution, objectives)
        self.fitness = float(sys.maxsize)
        self.evaluation = self.evaluate()
    
    def distance(self, other, u, l):
        me_objs = self.evaluation
        other_objs = other.evaluation
        dist = 0.0
        i = 0
        for v1, v2 in zip(me_objs, other_objs):
            if u[i] != l[i]:
                dist += math.pow(v1-v2, 2) / math.pow(u[i]-l[i], 2.0)
            i += 1
        return math.sqrt(dist)

    def solutions_distance(self, other):
        me_objs = self.evaluate()
        other_objs = other.evaluate()
        dist = 0.0
        for v1, v2 in zip(me_objs, other_objs):
            dist += math.pow(v1-v2, 2)
        return math.sqrt(dist)
    
    def __cmp__(self, other):
        return self.fitness - other.fitness

    def dominates(self, other):
        if other.__class__.__name__ == "Solution":
            return Solution.dominates(self, other)

        band = False 
        for i, obj_eval in enumerate(self.evaluation):
            if obj_eval > other.evaluation[i]:
                band = False
                break
            else:
                if obj_eval <= other.evaluation[i]:
                    band = True
        return band
    
    def __hash__(self):
        return hash(tuple(self.solution))


class GeneticOperators:

    def crossover(self, sol_a, sol_b):

        hijo = [-1 for n in range(len(sol_a.solution))]
        k = 0
        
        while True:
            hijo[k] = sol_a.solution[k]
            k = sol_a.solution.index(sol_b.solution[k])
            if hijo[k] >= 0:
                break
        
        for i, s in enumerate(sol_b.solution):
            if hijo[i] < 0:
                hijo[i] = s
        
        return [GaSolution(hijo, sol_a.objectives)]
    
    def mutation(self, sol):

        n = len(sol.solution) - 1
        i = random.randint(0, n)
        j = random.randint(0, n)
        while i == j:
            import time
            random.seed(time.time())
            j = random.randint(0, n)
        sol.solution[i], sol.solution[j] = sol.solution[j], sol.solution[i]
