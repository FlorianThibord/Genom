#!/usr/bin/python3
# -*- coding:UTF-8 -*

class Node:
	def __init__ (self, name, new_sig, niveau):
		self.name = name
                self.niveau = 0
		self.sous_noeuds = []
                self.cpt_seq = 0
                self.sig = build_sig(new_sig)
                


def process_taxlist(file):
        test = ["Archaeoglobus fulgidus DSM 4304", "oih", "ibuj"]
	file_in = open(file, 'r')
	lines = file_in.readlines()
	file_in.close()
        list_taxons = []
        list_p = []
	for line in lines:
                list_p = line.split('\t')        
                if len(list_p) > 2:
                    if (list_p[2] in test):
                        _ = list_p.pop()
                        list_p.reverse()
                        _ = list_p.pop()
                        _ = list_p.pop()
                        list_taxons.append(list_p)
                        print list_p
        return list_taxons

process_taxlist("taxlist.txt")
