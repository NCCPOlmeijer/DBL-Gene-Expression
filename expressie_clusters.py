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
    waar deze in voorkomt.

    Uitvoer
    -------
    cluster_freq: lijnplot van {cluster_nummer} met de relatieve expressie-
    waarden en het clustergemiddelde.

    Formaat: meetwaarde-integer op x-as, relatieve expressiewaarde op y-as.
    """
    # inlezen van databestanden 'cluster_invoer' en 'cluster_resultaat'.
    with open(cluster_invoer) as cluster_invoer:
        cluster_invoer_data = cluster_invoer.read().split()

    with open(cluster_uitvoer) as cluster_uitvoer:
        cluster_uitvoer = cluster_uitvoer.read().split()
        cluster_uitvoer_data = list(map(int, cluster_uitvoer))
        cloneID_lijst = cluster_uitvoer_data[::2]

    # verander string in integer of float, afhankelijk van het nummertype.
    for nummer in range(len(cluster_invoer_data)):
        if cluster_invoer_data[nummer] not in cloneID_lijst:
            cluster_invoer_data[nummer] = float(cluster_invoer_data[nummer])

    # lijst aanmaken genaamd 'cluster_lijst' die de clusters bevatten.
    cluster_lijst = cluster_uitvoer_data[1::2]

    # k-aantal clusters ophalen
    k = int(max([line for line in cluster_uitvoer[1::2]]))

    cloneID_dict = {}

    for key in range(1, k+1):
        cloneID_dict[key] = []

    # voeg alle cloneIDs toe aan de corresponderende cluster in de dictionary
    # genaamd 'cloneID_dict'.
    for cluster in range(len(cluster_lijst)):
        cloneID_dict[cluster_lijst[cluster]].append(
            cloneID_lijst[cluster])

    return cloneID_dict, cluster_invoer_data


def Plot_clusters(cloneID_dict, cluster_invoer_data, cluster_nummer):
    """Functie plot de clusters."""
    # genereer een lijst met integers 1 t/m 8 voor de plot.
    x_axis = list(range(1, 9))

    som = [0] * 8
    iteratie = 0

    # plot alle meetwaarden van de cloneIDs in een bepaalde cluster en
    # stel de plottitel en astitels in.
    for nummer in cloneID_dict[cluster_nummer]:
        ind = cluster_invoer_data.index(nummer)
        plt.plot(x_axis, cluster_invoer_data[ind+1:ind+9], 'b-x', alpha=0.25)
        # optellen van expressiewaarden en opslaan in 'som'.
        z = zip(som, cluster_invoer_data[ind+1:ind+9])
        som = [x + y for (x, y) in z]
        iteratie += 1

    # gemiddelde berekenen van alle expressiewaarden per colom.
    gemiddelde = [num/iteratie for num in som]

    plt.plot(x_axis, gemiddelde, 'r-x')

    plt.ylabel("Relatieve expressiewaarde")
    plt.title("Cluster" + " " + str(cluster_nummer))

    plt.ylim(-13, 10)

    # sla de gegenereerde plot op in map Cluster_Plots.
    plt.savefig("Plots/Cluster_plots/Cluster_"
                + str(cluster_nummer)
                + ".png", dpi=200)

    # geef de plot weer in de IDE.
    plt.show()
