# -*- coding: utf-8 -*-
"""
Created on Mon May 10 2021.

@author: NoahOlmeijer/20203063
"""

import matplotlib.pyplot as plt


def expressie(cluster_invoer, cluster_uitvoer, cluster_nummer=0):
    """Programma genereert grafieken van de rel. expressiewaarde per cluster.

    Parameters
    ----------
    cluster_invoer: tekstbestand
    beschrijving: tekstbestand bevat per cloneID de relatieve
    expressiewaarden.

    cluster_uitvoer: tekstbestand
    beschrijving: tekstbestand bevat per cloneID de corresponderende cluster
    waar die in voorkomt.

    Uitvoer
    -------
    cluster_freq: lijnplot van cluster_nummer.

    Formaat: meetmoment op x-as, relatieve expressiewaarde op y-as.
    """
    # Inlezen van 'cluster_invoer' en
    # rauwe data uit 'cluster_invoer' toewijzen aan
    # variable 'cluster_invoer'.

    with open(cluster_invoer) as cluster_invoer:
        cluster_invoer_data = cluster_invoer.read().split()

    # Inlezen van 'cluster_uitvoer' en
    # rauwe data uit 'cluster_uitvoer' toewijzen aan
    # variable 'cluster_uitvoer'.

    with open(cluster_resultaat) as cluster_uitvoer:
        cluster_uitvoer = cluster_uitvoer.read().split()

    # lijst aanmaken genaamd 'cluster_uitvoer_data' met per cloneID de
    # corresponderende clusters.

    cluster_uitvoer_data = list(map(int, cluster_uitvoer))

    # lijst aanmaken genaamd 'cloneID_lijst' met alle cloneIDs op volgorde die
    # is aangeleverd in 'cluster_invoer_data'.

    cloneID_lijst = cluster_invoer_data[::9]

    # verander str in int of float afhankelijk van het nummertype.

    for nummer in range(len(cluster_invoer_data)):
        if cluster_invoer_data[nummer] in cloneID_lijst:
            cluster_invoer_data[nummer] = int(cluster_invoer_data[nummer])
        else:
            cluster_invoer_data[nummer] = float(cluster_invoer_data[nummer])

    # lijst aanmaken genaamd 'cluster_lijst' en cloneIDs_lijst die de
    # clusters en cloneIDs bevatten, respectievelijk.

    cluster_lijst = cluster_uitvoer_data[1::2]
    cloneIDs_lijst = cluster_uitvoer_data[0::2]

    # lege dictionary aanmaken genaamd 'cloneID_dict'

    cloneID_dict = {}

    # voeg alle cloneIDs toe aan de corresponderende cluster in de dictionary
    # genaamd 'cloneID_dict'.

    for cluster in range(len(cluster_lijst)):
        if cluster_lijst[cluster] not in cloneID_dict:
            cloneID_dict[cluster_lijst[cluster]] = [cloneIDs_lijst[cluster]]
        else:
            cloneID_dict[cluster_lijst[cluster]].append(
                cloneIDs_lijst[cluster])

    # genereer een lijst met integers 1 tot en met 8.

    x_axis = list(range(1, 9))

    # plot alle meetwaarden van de cloneIDs in een bepaalde cluster en
    # stel de plottitel en astitels in.

    for nummer in cloneID_dict[cluster_nummer]:
        ind = cluster_invoer_data.index(nummer)
        plt.plot(x_axis, cluster_invoer_data[ind+1:ind+9], '-x')

    plt.ylabel("Meetwaarden")
    plt.title("Cluster" + " " + str(cluster_nummer))

    # sla de gegenereerde plot op in map Cluster_Plots.

    plt.savefig("Cluster_Plots/Cluster_"
                + str(cluster_nummer)
                + ".png", dpi=300)

    # geef de plot weer in de IDE.

    plt.show()


cluster_invoer = "Data/Voorbeeld_clusterdata.txt"
cluster_resultaat = "Data/Voorbeeld_clusterresult.txt"

# aanroepen van functie expressie() voor alle 6 clusters range(6)

for i in range(6):
    expressie(cluster_invoer, cluster_resultaat, i)
