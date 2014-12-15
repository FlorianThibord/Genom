#!/usr/bin/python3
# -*- coding:UTF-8 -*

class Node:
	
	def __init__ (self, name, pere):
		self.name = name
                self.niveau = 0
		self.fils = []
		self.pere = pere
                self.cpt_seq = 0
                self.sig = {} #build_sig(new_sig)
		self.genomes = []

	def add_seq_until_root(self, g):
		self.cpt_seq += 1
		self.genomes.append(g)
		self.compute_new_sig(g.sig)
		if self.pere is not None:
			self.pere.add_seq_until_root(g)
			
	def compute_new_sig(self, f_sig):
		for key in f_sig.keys():
			if self.sig.has_key(key):
				self.sig[key] = (self.sig[key] * (self.cpt_seq-1) + f_sig[key]) / self.cpt_seq 
			else:
				self.sig[key] = f_sig[key]

	def add_fils(self, f):
		self.fils.append(f)

	def add_leave_in_tree(self, g):
		name = g.name
		name = name.replace("\n", "")
		name = name.split(" ")		
		name = name[0] + " " + name[1] + " " + name[2] 
		node = self.get_a_leave(name)
		if node is None:
			print("None returned")
			print(name)
		node.add_seq_until_root(g)
		node.compute_new_sig(g.sig) 
		
	def get_a_leave(self, name):
		for e in self.fils:
			if (name in e.name):
				return e
			else:
				res = e.get_a_leave(name)
				if res != None:
					return res

	def get_a_fils(self, a):
		res = None
		if self.fils is not []:
			for e in self.fils:
				if (e.name in a) or (a in e.name):
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
		if self.cpt_seq > -1:
			print(space 
			      + self.name 
			      +  " >>> nbseq = " 
			      + str(self.cpt_seq) + " nb genomes = " 
			      + str(len(self.genomes)))
			if self.fils is not []:
				for fils in self.fils:
					fils.print_tree(space + "--")


					

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
				del list_phyl[1]
				_ = list_phyl.pop()
				list_phyl.reverse()
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
