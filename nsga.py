#!/usr/bin/env python
# -*- coding: utf-8 -*-

from objectivefunction import  QAPObjectiveFunction
from ga import GaSolution, GeneticOperators
from cparser import parse_qap
from solution import ParetoSet, ParetoFront
import numpy as np
import matplotlib.pyplot as plt

import random, math

class NSGA:
    def __init__(self, num_objectives, genetic_operators, p, q, 
                 cr=1.0, mr=0.1):
        self.num_objectives = num_objectives
        self.genetic_operators = genetic_operators
        self.crossover_rate = cr
        self.mutation_rate = mr
        
        self.sigma_share = 0.5 / math.pow(float(q), 1.0/float(p))
    
    def run(self, P, num_generations):
        for i in range(num_generations):
            fronts = self.classify_population(P)
            self.fitness_sharing(fronts)
            del P[:]

            for front in fronts.values():
                P.extend(front)
            mating_pool = self.selection(P)
            P = self.next_generation(mating_pool, len(P))

    def classify_population(self, population):

        fronts = {}
        n = {}
        S = {}
        for p in population:
            S[p] = []
            n[p] = 0
        
        fronts[1] = [] 
        pop_size = len(population)
        for p in population:
            for q in population:
                if p == q:
                    continue
                elif p.dominates(q):
                    S[p].append(q)
                elif q.dominates(p):
                    n[p] += 1
            if n[p] == 0:
                p.fitness = float(pop_size)
                fronts[1].append(p)
        
        i = 1
        while(len(fronts[i]) != 0):
            next_front = []
            for r in fronts[i]:
                for s in S[r]:
                    n[s] -= 1
                    if n[s] == 0:
                        next_front.append(s)
            i += 1
            fronts[i] = next_front
        return fronts
    
    def fitness_sharing(self, fronts):

        for i, front in fronts.items():
            min_dummy_fitness = 0.0
            if i > 1: 
                min_dummy_fitness = min([s.fitness for s in fronts[i-1]])
                min_dummy_fitness = min_dummy_fitness * 0.8
            for sol in front:
                if i > 1:
                    sol.fitness = min_dummy_fitness
                m = self.niche_count(sol, front)
                if m > 0:
                    sol.fitness = sol.fitness / m
        
    def niche_count(self, sol, front):
        m = 0.0
        import sys
        uppers = [0 for _ in range(len(sol.objectives))]
        lowers = [sys.maxsize for _ in range(len(sol.objectives))]
        for solution in front:
            for i, v in enumerate(solution.evaluation):
                if v > uppers[i]:
                    uppers[i] = v
                if v < lowers[i]:
                    lowers[i] = v
        for r in front:
            if r == sol: continue
            sh = 0.0
            dist = sol.distance(r, uppers, lowers)
            if dist <= self.sigma_share:
                sh = 1.0 - dist / self.sigma_share
            m += sh
        return m + 1
    
    def selection(self, population):
        pool = []
        pool_size = len(population)
        probs = self.probabilities(population)
        limits = [sum(probs[:i+1]) for i in range(len(probs))]
        while len(pool) < pool_size:
            aux = random.random()
            for i in range(len(limits)):
                if aux <= limits[i]:
                    pool.append(population[i])
                    break
        return pool
    
    def probabilities(self, population):
        probs = []
        total_fitness = 0.0
        for p in population:
            total_fitness += p.fitness
        for p in population:
            probs.append(p.fitness / total_fitness)
        return probs
    
    def next_generation(self, mating_pool, pop_size):
        Q = []
        
        while len(Q) < pop_size:
            parents = []
            parents.append(random.choice(mating_pool))
            other = random.choice(mating_pool)
            parents.append(other)
            if random.random() < self.crossover_rate:
                children = self.genetic_operators.crossover(parents[0], parents[1])
                Q.extend(children)
            else:
                Q.extend(parents)
        
        for ind in Q:
            if random.random() < self.mutation_rate:
                self.genetic_operators.mutation(ind)
                ind.evaluation = ind.evaluate()
        return Q


def iniciarQAP(n = 5, i = 0):
    total_individuos = 20
    total_generaciones = 100
    p, q = 2, 5
    operador = GeneticOperators()
    instancias = parse_qap()
    flux_mats = instancias[i][:-1]
    dist_mat = instancias[i][-1]
    numero_localidades = len(flux_mats[0])
    objs = []
    for cost_mat in flux_mats:
        objs.append(QAPObjectiveFunction(dist_mat, cost_mat))
    nsga = NSGA(len(objs), operador, p, q, mr=0.2)
    pareto_set = ParetoSet(None)
    for i in range(n):
        pop = []
        for i in range(total_individuos):
            sol = list(range(numero_localidades))
            random.shuffle(sol)
            pop.append(GaSolution(sol, objs))
        nsga.run(pop, total_generaciones)
        pareto_set.update(pop)
    pareto_front = ParetoFront(pareto_set)
    pareto_front.draw()
    return pareto_set
