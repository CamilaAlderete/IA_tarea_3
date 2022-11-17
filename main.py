#!/usr/bin/env python
# -*- coding: utf-8 -*-


import moacs
import nsga
import sys
from solution import *
from metric import *

# para ejecutar python3 main.py <instancia>
def main():
    instancia = int(sys.argv[1]) - 1
    pareto_set_true = ParetoSet(None)
    
    pareto_set_nsga = nsga.iniciarQAP(i = instancia)
    pareto_front_nsga = ParetoFront(pareto_set_nsga)
    pareto_set_true.update(pareto_set_nsga.solutions)
    
    #pareto_set_moacs = moacs.testQap(i = instancia)
    #pareto_front_moacs = ParetoFront(pareto_set_moacs)    
    #pareto_set_true.update(pareto_set_moacs.solutions)
    
    pareto_front_true = ParetoFront(pareto_set_true)
    pareto_front_true.draw()
    
    m1 = DistanceMetric(pareto_front_true)
    m2 = DistributionMetric(1000.0)
    m3 = ExtensionMetric()
    
    print("Algoritmo NSGA")
    print("Distancia: ",str(m1.evaluate(pareto_front_nsga)))
    print("Distribucion:",str(m2.evaluate(pareto_front_nsga)))
    print("Extension:",str(m3.evaluate(pareto_front_nsga)))

    #print("Algoritmo MOACS")
    #print("Distancia: ",str(m1.evaluate(pareto_front_moacs)))
    #print("Distribucion:",str(m2.evaluate(pareto_front_moacs)))
    #print("Extension:",str(m3.evaluate(pareto_front_moacs)))
    
    return 0

# para ejecutar python3 main.py <instancia>
if __name__ == '__main__':
    main()

