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

    # openen van het 'cluster_uitvoer' bestand en uitlezen daarvan.
    with open('Data_out/cluster_uitvoer.txt') as cluster_uitvoer:
        cluster_data = cluster_uitvoer.read().strip().split()

    cloneID_lijst = [int(cloneID) for cloneID in cluster_data[0::2]]
    cluster_lijst = [int(cluster) for cluster in cluster_data[1::2]]

    # uitlezen van accessionnumber regels.
    with open('data/accessionnumbers.txt', 'r') as accessionnumbers:
        accessionnumbers = accessionnumbers.readlines()[1:]

    accession_IDs = []

    # Het eruit filteren van regels zonder EMBL-ID en opschonen van regels.
    for line in accessionnumbers:
        line = line.strip()
        line = line.replace('\t', ' ').split()
        if len(line) != 1:
            accession_IDs.append(line[0:2])

    # omzetten van accession_IDs (str) naar accession_IDs (int).
    for ID in accession_IDs:
        ID[0] = int(ID[0])

    # nested list omzetten in één lijst van cloneIDs gevolgt door accession_ID.
    accession_IDs = [item for elem in accession_IDs for item in elem]

    # uitlezen van k uit het 'cluster_uitvoer' bestand.
    k = int(max([line for line in cluster_data[1::2]]))

    # aanmaken van cloneID_dict met keys de clusters en values een lege lijst.
    cloneID_dict = {}

    for i in range(1, k+1):
        cloneID_dict[i] = []

    # cloneIDs toevoegen aan corresponderende cluster in cloneID_dict.
    for cloneID in range(len(cloneID_lijst)):
        cloneID_dict[cluster_lijst[cloneID]].append(cloneID_lijst[cloneID])

    # EMBL-IDs toevoegen aan EMBL_IDs uit key 'cluster_nummer'.
    EMBL_IDs = []

    for cloneID in range(len(cloneID_dict[cluster_nummer])):
        if cloneID_dict[cluster_nummer][cloneID] in accession_IDs:
            CLID = cloneID_dict[cluster_nummer][cloneID]
            EMBL_IDs.append(accession_IDs[accession_IDs.index(CLID)+1])

    # efetch verzamelt alle IDs in de lijst en retourneert
    # deze in vorm van fasta files.
    mouse_genes = Entrez.efetch(db="nucleotide", id=EMBL_IDs,
                                rettype='fasta', retmode="text")

    # openen van Mus Musculus sequences.fasta en toevoegen van alle genen
    # opgehaald uit EMBL uit 'cluster_nummer'.
    with open('Data_out/Mus Musculus sequences.fasta', 'w') as nieuw_document:
        nieuw_document.write(mouse_genes.read())

    # uitlezen van 'nieuw_document'.
    with open('Data_out/Mus Musculus sequences.fasta') as fasta_document:
        mRNA_sequenties = fasta_document.read()

    # uitlezen van sequenties en filteren op 'zoekterm'.
    sequenties = mRNA_sequenties.replace('\n', ' ').split('>')
    zoekterm_mouse_genes = ['>' + i for i in sequenties if zoekterm in i]

    # gefilterde 'zoekterm' genen schrijven naar 'filt_file'.
    with open("Data_out/Sequences_" + zoekterm + '_Cluster_'
              + str(cluster_nummer) + ".fasta", 'w') as filt_file:
        for gensum in zoekterm_mouse_genes:

            # formatteren van gen (1st line: summary, following lines mRNA
            # sequence, max. 70 char. per line).
            gene = gensum.split("sequence")
            mrna = gene[1].lstrip(' ').split(' ')

            summary = [gene[0].strip(' ')]

            for subgen in summary+mrna:
                print(subgen)
                filt_file.write(subgen + '\n')
