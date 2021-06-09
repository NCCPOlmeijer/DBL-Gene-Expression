# -*- coding: utf-8 -*-
"""
Created on Tue May 25 2021.

@author: NoahOlmeijer/20203063
"""

import matplotlib.pyplot as plt


def expressie(cluster_invoer, familie_cloneID):
    """Programma genereert grafieken van de rel. expressiewaarde per fam. naam.

    Parameters
    ----------
    cluster_invoer: tekstbestand
    beschrijving: tekstbestand bevat per cloneID de relatieve
    expressiewaarden.

    familie_cloneID: tekstbestand
    beschrijving: tekstbestand bevat per cloneID de corresponderende fam. naam
    waar deze in voorkomt.

    Uitvoer
    -------
    cluster_freq: lijnplot van cluster_nummer.

    Formaat: meetwaarde-integer op x-as, relatieve expressiewaarde op y-as.
    """
    # inlezen van databestanden 'cluster_invoer' en 'familie_cloneID'.
    with open(cluster_invoer) as cluster_invoer:
        cluster_invoer_data = cluster_invoer.read().split()
        cloneID_lijst = list(map(int, cluster_invoer_data[::9]))

    with open(familie_cloneID) as familie_cloneID:
        familie_cloneID = familie_cloneID.read().split()[2:]
        familie_cloneID_data = list(map(int, familie_cloneID))

    # verander string in integer of float, afhankelijk van het nummertype.
    for nummer in range(len(cluster_invoer_data)):
        if cluster_invoer_data[nummer] not in cloneID_lijst:
            cluster_invoer_data[nummer] = float(cluster_invoer_data[nummer])

    # lijst aanmaken genaamd 'cluster_lijst' die de clusters bevatten.
    cluster_lijst = familie_cloneID_data[1::2]

    # lijst aanmaken van cloneIDs uit 'familie_cloneID'.
    cloneID_lijst = familie_cloneID_data[0::2]

    cloneID_dict = {}

    # de familienamen (keys) toevoegen met als waarde een lege lijst.
    for key in range(1, 27):
        cloneID_dict[key] = []

    # voeg alle cloneIDs toe aan de corresponderende cluster in de dictionary
    # genaamd 'cloneID_dict'.
    for cluster in range(len(cluster_lijst)):
        cloneID_dict[cluster_lijst[cluster]].append(
            cloneID_lijst[cluster])

    return cloneID_dict, cluster_invoer_data


def Plot_families(cloneID_dict, cluster_invoer_data, cluster_nummer):
    """Functie plot familie plots."""
    # genereer een lijst met integers 1 t/m 8 voor de plot.
    x_axis = list(range(1, 9))

    # plot alle meetwaarden van de cloneIDs in een bepaalde cluster en
    # stel de plottitel en astitels in.
    for nummer in cloneID_dict[cluster_nummer]:
        if nummer in cluster_invoer_data:
            ind = cluster_invoer_data.index(nummer)
            plt.plot(x_axis, cluster_invoer_data[ind+1:ind+9], '-x')
        else:
            pass

    plt.ylabel("Relatieve expressiewaarde")
    plt.title("Familie" + " " + str(cluster_nummer))

    plt.ylim(-7, 4)

    # sla de gegenereerde plot op in map Cluster_Plots.
    plt.savefig("Plots/Familie_plots/Familie_"
                + str(cluster_nummer)
                + ".png", dpi=200)

    # geef de plot weer in de IDE.
    plt.show()
