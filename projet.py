#!/usr/bin/python3
# -*- coding:UTF-8 -*

#A COMMENTER ...

import os
from math import *
####bibliotheque a installer::::
import matplotlib.pyplot as plt
import numpy as np
import scipy as stats
import pylab
import tree_build
######


nucl_list = ["A","T","G","C"]

class Genome:
	def __init__ (self, name, seq, k, dico_commun):
		self.name = name
		self.seq = seq
		self.sig = compute_kmere(seq + seq[0:k], k, dico_commun)
		self.famille="?"
		self.prediction="?"


####### :::  GESTION DES DICOS ::: ######	
# build every possibilities
def build_kmere_list(kmere_list, k):
	if k == 1 :
		return kmere_list
	else :
		kmere_list_bis=[]
		for elt in kmere_list :
			for nucl in nucl_list :
				kmere_list_bis.append(elt + nucl)
		return build_kmere_list(kmere_list_bis, (k - 1))

# initialise a zero
def build_empty_dict(l):
	my_dict = {}
	for elt in l :
		my_dict[elt] = 0.0
	return my_dict

#compteur
def compute_kmere(seq, k, my_dict):
	i = 0
	list_keys = my_dict.keys()
	while i < len(seq) - k:
		key = seq[i : (i + k)]
		if (key in list_keys):		######## GESTION DES ERREURS DE SEQUENCAGES 
			my_dict[key] += 1 
		i += 1	
	my_dict = set_freq_a_dico(my_dict)		
	return my_dict

# passage du dictionnaire en frequences
def set_freq_a_dico(dictio):
	total = sum(dictio.values())
	for KEYS in dictio.keys():
		dictio[KEYS] = dictio[KEYS] / total
	return dictio

##### FUNCTIONS:::: READING FILES :::: ######

def get_seq_name(line):
	res_part = line.split("| ")
	res_part = res_part[1].split(",")
	res = res_part[0]
	return res

def process_my_file(my_file, k, dico_commun):
	file_in = open(my_file, 'r')
	lines = file_in.readlines()
	file_in.close()
	file_name = get_seq_name(lines[0])
	seq = ""
	for i in range(1, len(lines)):
		seq = seq + lines[i][:-1]
	my_genome = Genome(file_name, seq, k, dico_commun)
	return my_genome


def lecture_dossier_sequences(directory_to_read, k, dico_commun):
# RECUPERER SEQUENCES DANS UN DOSSIER "GENOMES"
	listedesfichiers = os.listdir(directory_to_read)
	liste_des_genomes = []
	for i in range(0, len(listedesfichiers) - 1):
		liste_des_genomes.append(
			process_my_file(directory_to_read + "/" + listedesfichiers[i], k, dico_commun))
		# liste_des_genomes[i].famille = directory_to_read.split("/")[1]
	return liste_des_genomes

# DEPRECATED
# def process_sequences(k, dico):	# RECUPERER SEQUENCES DANS UN DOSSIER "GENOMES"
# 	family_list = os.listdir("GENOMES")
# 	genomes_list = []
# 	os.chdir("./GENOMES/")
# 	for i in family_list:
# 		os.chdir("./" + i + "/")
# 		genomes_list.append(process_my_file("sequence.fasta", k, dico))
# 		os.chdir("./../")
# 	return genomes_list

def write_score(liste):
	file_out= open("sauvegarde.txt", 'w')
	
	for i in liste:
		file_out.write(str(i)+'\n')
	file_out.close()

def write_every_dico(list_genome):
	file_out=open("sauvegarde_dico.txt", 'w')
	
	for j in list_genome:
		file_out.write(j.name)
	file_out.write("\n")
		
	dico_key=list_genome.sig.keys()
	for i in dico_key:
		for j in list_genome:
			file_out.write(j.sig[i]+";")
		file_out.write("\n")
	file_out.close()



#############################################
#############################################

# calcule distance euclidienne entre 2 signature
def calculator_score_between_2signature(dico1,dico2):
	liste1=dico1.values()
	liste2=dico2.values()	
	dist=0
	for i in xrange(len(liste1)):
		dist=dist+pow(liste1[i] - liste2[i],2)
	score=sqrt(dist)
	return score

# calcule la signature dune fenetre et calcule la distance entre cette signature et celle du genome
def calc_distrib_along_genome(genome_to_calc, size_window, gap_window, dico, k):
	sequence_a_parser = genome_to_calc.seq + genome_to_calc.seq[0:size_window]
	scoring = []
	position = []
	for i in range(0, len(sequence_a_parser) - size_window, gap_window):
		position.append(i)
		dico_of_the_window = compute_kmere(sequence_a_parser[i:i+size_window], k, dico)
		scoring.append(calculator_score_between_2signature(dico_of_the_window, genome_to_calc.sig))
	return(position, scoring)

def build_matrix_distance(liste_genome_to_analyze):	#calc matrix optimiser (temps calc diviser par2)
	matrix=range(len(liste_genome_to_analyze))
	for i in range(len(matrix)):
		matrix[i]=range(len(liste_genome_to_analyze))
	
	for i in range(1,len(matrix)):
		for j in range(i+1):
			if (i == j):
				matrix[i][j]=0.0
			else :
				matrix[i][j]=calculator_score_between_2signature(liste_genome_to_analyze[i].sig,liste_genome_to_analyze[j].sig)
				matrix[j][i]=matrix[i][j]
	return matrix


# MORE INFO :::::: http://math.mad.free.fr/depot/numpy/courbe.html
# plt.clf()  ::: efface la fenetre graphique
# plt.savefig(nomfichier)  ::: sauvegarde 		
def plot_signature_genome(vectorposi, vectorscore, name):
	plt.plot(vectorposi,vectorscore)
	plt.ylabel('Distance windows vs Genome')
	plt.xlabel('position dans Genome')
	plt.savefig(name)
def close_graph():
	plt.close()


########################
# TEST STATISTIQUE

def test_normalite(vector_to_analyze,choose_save):
	res_norm=scipy.stats.shapiro(vector_to_analyze)
	###
	
	# AFFICHAGE GRAPHE
	stats.probplot(measurements, dist="norm", plot=pylab)
	pylab.show()
	if (choose_save ==1):
		plt.savefig('qqplot.png')
	return res_norm

#############################################
#############################################
	
####### APPRENTISSAGE BAYESIEN & RESEAU NEURONE #########
##### ATTENTION LA CLASS NEURONE NE SIGNIFIE PAS forcement que l'object est un neurone, ca peut etre une classe dapprentissage toute simple

class Neurone:
	def __init__ (self, name,liste_apprentissage):
		self.name = name
		self.weight=estimated_weight_of_class(liste_apprentissage)
		self.nb_of_member=len(liste_apprentissage)
		
### ESTIMATION DE POIDS PAR APPROCHE BAYSIENNE
def estimated_weight_of_class(liste_famille):
	W_estimation=[]
	list_of_signature=[]
	for i in liste_famille:
		list_of_signature.append(i.sig.values())
	
	for i in range(len(list_of_signature[0])):
		w=0.0
		for j in range(len(list_of_signature)):
			w=w+list_of_signature[j][i]
		w=w/len(list_of_signature)
		W_estimation.append(w)
	
	return W_estimation

### SCORE == SOMME ::: DES POIDS X VARIABLES
def scoring_one_neuron(the_neuron, the_target):
	score=0
	dico_value=the_target.sig.values()
	for i in range(len(the_neuron.weight)):
		score=score+ the_neuron.weight[i]*dico_value[i]
	return score

## MAP POUR APPROCHE BAYSIENNE
def maximum_a_posteriori(list_class,target_to_class):
	liste_score=[]
	for i in list_class:
		liste_score.append(scoring_one_neuron(i,target_to_class))
	
	target_to_class.prediction=list_neuron[np.argmax(liste_score)].name     ## Function necessitant numpy
	print( "Genome classer avec le groupe "+ target_to_class.prediction)

#DOSSIEr classified_genome est necessaire dans la racine, les genomes clusteriser par groupe de classe
def generate_class_baysien(k,dico_partage):
	liste_of_directory=os.listdir("classified_genome")
	list_class_of_bayesien=[]
	for i in range(1,len(liste_of_directory)):	# COMMENCE A  1 car FICHIER .BS
		print(liste_of_directory[i])
		genomes_for_a_class=lecture_dossier_sequences("classified_genome/"+liste_of_directory[i],k,dico_partage)
		list_class_of_bayesien.append(Neurone(i,genomes_for_a_class))
	return list_class_of_bayesien


# FONCTION ESTIMATEUR DU SEUIL DES VALEURS DE CHAQUE VARIABLE POUR DISCRITISATION
# PAR ANALYSE DE LA DISTRIBUTION DES VALEURS POUR RESEAU NEURONE
#   < SEUIL -> 0    >SEUIL -> 1 
def estimated_bin_dico(liste_genome):
	dico_bin=liste_genome[0].sig
	n=round(len(liste_genome)/2)
	for i in dico_bin.keys():
		vector_of_one_key=[]
		for j in liste_genome:
			vector_of_one_key.append(liste_genome.sig[i])
		vector_of_one_key.sort()
		dico_bin[i]=vector_of_one_key[n]				
	return dico_bin

# 


###### http://mirrors.vbi.vt.edu/mirrors/ftp.ncbi.nih.gov/genomes/Bacteria/Shewanella_MR_4_uid58345/NC_008321.fna
########################################################





#MAIN

#test plot
def main(k):
	directory_to_read = "GENOMES"
	l = build_kmere_list(nucl_list, k)
	dico_main = build_empty_dict(l)
	genomes = lecture_dossier_sequences(directory_to_read, k, dico_main)
	i = 0
	for g in genomes:
		i += 1
		k = i
		if i > 4:
			print(i)
			break
		(p,s) = calc_distrib_along_genome(g, 1000, 200, dico_main, k)
#		plot_signature_genome(p, s, g.name)
	tree = tree_build.main()
	print(tree.name)



main(2)





