#!/usr/bin/python3
# -*- coding:UTF-8 -*

class Node:
	
	def __init__ (self, name, pere, genome=None):
		self.name = name
                self.niveau = 0
		self.fils = []
		self.pere = pere
                self.cpt_seq = 0
                self.sig = 0 #build_sig(new_sig)
		self.genome = genome

	def add_seq_until_root(self):
		self.cpt_seq += 1
		if self.pere is not None:
			self.pere.add_seq_until_root()
			
	def compute_new_sig(self, f_sig):
		self.sig = (self.sig * (self.cpt_seq-1) + f_sig) / self.cpt_seq 

	def add_fils(self, f):
		self.fils.append(f)
		self.add_seq_until_root()
		self.compute_new_sig(0) #TROUVER LES SIGS 
                
	def get_a_fils(self, a):
		res = None
		if self.fils is not []:
			for e in self.fils:
				if e.name == a:
					res = e		
		return res

	def is_a_fils(self, a):
		res = False
		if self.fils is not []:
			for e in self.fils:
				if e.name == a:
					res = True		
		return res

	def get_fils(self):
		return self.fils

	def get_root(self):
		if self.pere is not None:
			return self.pere.get_root()
		else:
			return self

	def print_tree(self, space):
		print(space + self.name)
		if self.fils is not []:
			for fils in self.fils:
				fils.print_tree(space + "-")

def set_in_tree(e_list, tree):
	while len(e_list) > 0:
		e = e_list.pop()
		if tree.is_a_fils(e):
			fils = tree.get_a_fils(e)
			return set_in_tree(e_list, fils)
		else:
			tree.add_fils(Node(e, tree))
			fils = tree.get_a_fils(e)
			return set_in_tree(e_list, fils)
	return tree.get_root()

def build_tree(tax_list, tree):
	for esp in tax_list:
		esp.reverse()
		tree = set_in_tree(esp, tree) 
	return tree


def process_taxlist():
	file_tax = open('taxlist.txt', 'r')
	lines_tax = file_tax.readlines()
	file_tax.close()
	file_req = open('LISTE_REQUETE.txt', 'r')
	lines_req = file_req.readlines()
	file_req.close()
        list_tax_req = []
        list_phyl = []
	found = False
	for line_r in lines_req:
		found = False		
		line_r = line_r.split(' ')
		line_r = ' '.join(line_r[0:3])
		for line_t in lines_tax:
			list_phyl = line_t.split("\t")
			if (line_r in list_phyl[0]) or (list_phyl[0] in line_r):
				found = True
				_ = list_phyl.pop()
				list_phyl.reverse()
				_ = list_phyl.pop()
				_ = list_phyl.pop()
				list_tax_req.append(list_phyl)
		if not found:
			print("ATTENTION UNE SEQ NON TROUVEE")
        return list_tax_req


def sort_my_list(l):
	l.sort()
	for e in l:
		e.reverse()
	return l

def main():
	l = process_taxlist()
	root = Node("Root", None)
	tree = build_tree(l, root)
	# tree.print_tree("-")
	return tree
	
main()
