#!/usr/bin/python3
# -*- coding:UTF-8 -*

from ftplib import FTP

def process_taxlist():
    file_in = open('LISTE_REQUETE.txt', 'r')
    lines = file_in.readlines()
    file_in.close()
    list_nom = []
    list_noms = []
    noms = ''
    i = 0
    for line in lines:
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        line = line.replace("/", "_")
        line = line.replace("-", "_")
        i += 1
        list_nom = line.split(' ')
        if len(list_nom) > 2:
            noms = list_nom[0] + '_' + list_nom[1] + '_' + list_nom[2]
            list_noms.append(noms)
        else:
            print("Erreur sur p_t : ", i, "->",line)
    print("liste: ", list_noms)
    return list_noms

ftp = FTP('ftp.ncbi.nih.gov')
ftp.login()
ftp.cwd('/genomes/Bacteria/')
files = ftp.nlst()
list3_noms = process_taxlist()
st = ""
i = 0
for name in list3_noms:
    for f in files:
        if (name in f):
            ftp.cwd(f)
            files_dir = ftp.nlst()
            i = 0
            for file_d in files_dir:
                if '.fna' in file_d:
                    i += 1
                    st = 'RETR ' + file_d
                    my_f = name + '_' + str(i) + '.fasta'
                    ftp.retrbinary(st, open(my_f, 'wb').write)
            ftp.cwd('../')
