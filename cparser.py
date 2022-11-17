#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

instanciasQAP = ["input" + os.sep + "qapUni.75.0.1.qap.txt", "input" + os.sep + "qapUni.75.p75.1.qap.txt"]


def parse_qap():
	mat_objs = [] 
	for s, ins in enumerate(instanciasQAP):
		f = open(ins, "r")
		n = int(f.readline())
		mat_objs.append([])
		for i in range(3):
			mat_objs[s].append([])
			for j in range(n):
				mat_objs[s][i].append([float(e) for e in f.readline().split()])
			f.readline()
		f.close()
	return mat_objs

	
if __name__ == "__main__":
	print("Len parseado : ",len(parse_qap()) )
