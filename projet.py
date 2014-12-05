#!/usr/bin/python2
# -*- coding:UTF-8 -*

#A COMMENTER ...
 
import os
from math import *
####bibliotheque a installer::::
import matplotlib.pyplot as plt
import numpy as np
######

nucl_list = ["A", "T", "C", "G"]

class Genome:
	def __init__ (self, name, seq, k, family):
		self.name = name
		self.seq = seq
		self.sig = compute_kmere(seq + seq[0 : k], k)
		self.family = family
		self.prediction = "?"

####### :::  GESTION DES DICOS ::: ######	
# build every possibilities
def build_kmere_list(kmere_list, k):
	if k == 1:
		return kmere_list
	else:
		kmere_list_bis = []
		for elt in kmere_list:
			for nucl in nucl_list:
				kmere_list_bis.append(elt + nucl)
		return build_kmere_list(kmere_list_bis, (k - 1))

# initialise a zero
def build_empty_dict(l):
	my_dict = {}
	for elt in l:
		my_dict[elt] = 0.0
	return my_dict

#compteur
def compute_kmere(seq,k):
	l = build_kmere_list(nucl_list, k)
	my_dict = build_empty_dict(l)
	i = 0
	while i < len(seq) - k:
		key = seq[i : (i + k)]
		my_dict[key] += 1 
		i += 1	
	my_dict = set_freq_in_dict(my_dict)		
	return my_dict

def set_freq_in_dict(dico):
	total = sum(dico.values())
	for KEYS in dico.keys():
		dico[KEYS] = dico[KEYS] / total
	return dico

##### FUNCTIONS:::: READING FILES :::: ######

def get_seq_name(line):
	res_part = line.split("| ")
	res_part = res_part[1].split(",")
	res = res_part[0]
	print res
	return res

def process_my_file(my_file, k, dico):
	file_in = open(my_file, 'r')
	lines = file_in.readlines()
	file_in.close()
	file_name = get_seq_name(lines[0])
	seq = ""
	for i in range(1, len(lines)):
		seq = seq + lines[i][:-1]
	my_genome = Genome(file_name, seq, k, "?")
	return my_genome

def process_sequences(k, dico):	# RECUPERER SEQUENCES DANS UN DOSSIER "GENOMES"
	family_list = os.listdir("GENOMES")
	genomes_list = []
	os.chdir("./GENOMES/")
	for i in family_list:
		os.chdir("./" + i + "/")
		genomes_list.append(process_my_file("sequence.fasta", k, dico))
		os.chdir("./../")
	return genomes_list

#############################################
#############################################

# calcule distance euclidienne entre 2 signature
def score_between_sigs(dico1, dico2):
	liste1 = dico1.values()
	liste2 = dico2.values()	
	dist = 0
	for i in xrange(len(liste1)):
		dist = dist + pow(liste1[i] - liste2[i], 2)
	score = sqrt(dist)
	return score

# calcule la signature dune fenetre et calcule la distance entre cette signature et celle du genome
def compute_distrib_genome(genome_to_calc, size_window, gap_window, dico, k):
	sequence_a_parser = genome_to_calc.seq + genome_to_calc.seq[0 : size_window]
	scoring = []
	position = []
	for i in range(0, len(sequence_a_parser) - size_window, gap_window):
		position.append(i)
		dico_of_the_window = compute_kmere(sequence_a_parser[i : i + size_window], k)
		scoring.append(score_between_sigs(dico_of_the_window, genome_to_calc.sig))
	return(position, scoring)


# MORE INFO :::::: http://math.mad.free.fr/depot/numpy/courbe.html
# plt.clf()  ::: efface la fenetre graphique
# plt.savefig(nomfichier)  ::: sauvegarde 		
def plot_sig_genome(vectorposi, vectorscore, name):
	plt.plot(vectorposi, vectorscore)
	plt.ylabel('Distance windows vs Genome')
	plt.xlabel('position dans Genome')
	plt.savefig(name)
def close_graph():
	plt.close()



#MAIN

#test plot
def main(k):
	genomes = process_sequences(k, {})
	for g in genomes:
		(p,s) = compute_distrib_genome(g, 1000, 200, {}, 3)
		plot_sig_genome(p, s, g.name)



main(3)
