# -*- coding: utf-8 -*-
"""
Created on Wed Jun 2 2021.

Author: Interpretatie
"""


def Entrez(cluster_nummer, zoekterm):
    """Functie zoekt genen op in EMBL uit een gespecificeerde cluster\
    en filtert op zoekterm.

    Parameters
    ----------
    cluster_nummer : integer
    beschrijving: het clusternummer waarin je de zoekterm wilt zoeken.

    zoekterm : String
    beschrijving: de zoekterm die je wilt gebruiken om genen op te filteren.

    Uitvoer
    -------
    Fasta file met alle genen in 'cluster_nummer' waar 'zoekterm' in voorkomt.
    """
    from Bio import Entrez

    # meldt gebruiker aan om de NCBI Entrez service te gebruiken
    Entrez.email = "n.c.c.p.olmeijer@student.tue.nl"

    with open('Data_out/cluster_uitvoer.txt') as cluster_uitvoer:
        cluster_data = cluster_uitvoer.read().strip().split()

    cloneID_lijst = [int(cloneID) for cloneID in cluster_data[0::2]]
    cluster_lijst = [int(cluster) for cluster in cluster_data[1::2]]

    with open('data/accessionnumbers.txt', 'r') as accessionnumbers:
        accessionnumbers = accessionnumbers.readlines()[1:]

    accession_IDs = []

    for line in accessionnumbers:
        line = line.strip()
        line = line.replace('\t', ' ').split()
        if len(line) != 1:
            accession_IDs.append(line[0:2])

    for ID in accession_IDs:
        ID[0] = int(ID[0])

    accession_IDs = [item for elem in accession_IDs for item in elem]

    k = int(max([line for line in cluster_data[1::2]]))
    cloneID_dict = {}

    for i in range(1, k+1):
        cloneID_dict[i] = []

    for cloneID in range(len(cloneID_lijst)):
        cloneID_dict[cluster_lijst[cloneID]].append(cloneID_lijst[cloneID])

    EMBL_IDs = []
    used_cloneID = []
    for cloneID in range(len(cloneID_dict[cluster_nummer])):
        if cloneID_dict[cluster_nummer][cloneID] in accession_IDs:
            CLID = cloneID_dict[cluster_nummer][cloneID]
            EMBL_IDs.append(accession_IDs[accession_IDs.index(CLID)+1])
            used_cloneID.append(CLID)

    # efetch verzameld alle id's in de lijst en returneert
    # deze in vorm van fasta files.
    invoer = Entrez.efetch(db="nucleotide", id=EMBL_IDs,
                           rettype='fasta', retmode="text")
    with open('Data_out/Mus Musculus sequences.fasta', 'w') as nieuw_document:
        nieuw_document.write(invoer.read())

    # leest de fasta files om deze in python te gebruiken
    with open('Data_out/Mus Musculus sequences.fasta') as fasta_document:
        mRNA_sequenties = fasta_document.read()

    sequenties = mRNA_sequenties.replace('\n', ' ').split('>')
    mens = ['>' + i for i in sequenties if zoekterm in i]

    with open("Data_out/Human Nucleotides.fasta", 'w') as filt_file:
        for gensum in mens:

            gene = gensum.split("sequence")
            mrna = gene[1].lstrip(' ').split(' ')

            summary = [gene[0].strip(' ')]

            for subgen in summary+mrna:
                print(subgen)
                filt_file.write(subgen + '\n')
