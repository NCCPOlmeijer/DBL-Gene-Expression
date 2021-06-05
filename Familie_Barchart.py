# -*- coding: utf-8 -*-
"""
Created on Thu May 27 2021.

@author: NoahOlmeijer/20203063
"""


import matplotlib.pyplot as plt
import numpy as np


def Histogram(cluster_uitvoer, familie_cloneID, cluster_aantal):
    """Stacked bar chart van de distributie van families over de clusters.

    Parameters
    ----------
    cluster_uitvoer : tekstbestand
    beschrijving: tekstbestand bevat per cloneID de relatieve
    expressiewaarden.

    familie_cloneID : tekstbestand
    beschrijving: tekstbestand bevat per cloneID de corresponderende
    genfamilie.

    Uitvoer
    -------
    familie_barchart: stacked bar chart met op de x-as de clusters
    en de y-as de familiefrequentie.

    """
    # inlezen van databestanden 'cluster_uitvoer' en 'familie_cloneID'.
    with open(cluster_uitvoer) as cluster_uitvoer:
        cluster_uitvoer = cluster_uitvoer.read().split()
        cluster_uitvoer = list(map(int, cluster_uitvoer))

    with open(familie_cloneID) as familie_cloneID:
        familie_cloneID = familie_cloneID.read().split()[2:]
        familie_cloneID = list(map(int, familie_cloneID))

    # lijsten aanmaken van uitsluitend familienummers en cloneIDs.
    familie_nummers = familie_cloneID[1::2]
    familie_cloneIDs = familie_cloneID[::2]

    # aanmaken van dictionary met als keys de familienummers en values
    # een lege lijst.
    familie_dict = {}

    for familie_nummer in range(1, 27):
        familie_dict[familie_nummer] = []

    # alle cloneIDs toevoegen aan het corresponderende familienummer.
    for Family in range(len(familie_nummers)):
        familie_dict[familie_nummers[Family]].append(familie_cloneIDs[Family])

    # lijsten aanmaken van uitsluitend clusternummers en cloneIDs.
    Cluster_no = cluster_uitvoer[1::2]
    Cluster_cloneIDs = cluster_uitvoer[::2]

    # aanmaken van dictionary met als keys de clusternummers en values
    # een lege lijst.
    cluster_dict = {}

    for cluster_nummer in range(1, cluster_aantal+1):
        cluster_dict[cluster_nummer] = []

    # alle cloneIDs toevoegen aan het corresponderende clusternummer.
    for Cluster in range(len(Cluster_no)):
        cluster_dict[Cluster_no[Cluster]].append(Cluster_cloneIDs[Cluster])

    # lijsten aanmaken van alle cloneID lijsten uit beide dictionaries.
    families = list(familie_dict.values())
    clusters = list(cluster_dict.values())

    distributies = []

    # loop over alle familie lijsten.
    for familie in range(len(familie_dict)):
        # lege distributie lijst aanmaken.
        cur_dist = [0]*cluster_aantal
        # loop over alle cloneIDs in de familielijst.
        for cloneID in range(len(families[familie])):
            # loop over elke cluster lijst.
            for cluster in range(len(clusters)):
                # check of cloneID uit familie lijst in cluster lijst zit.
                if families[familie][cloneID] in clusters[cluster]:
                    # verhoog cluster index met 1.
                    cur_dist[cluster] += 1
        # voeg distributielijst toe aan distributies.
        distributies.append(cur_dist)

    # definieer kleuren.
    kleuren = [
        '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
        '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
        '#9a6324', '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
        '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080',
        '#e6beff', '#9a6324']

    # omzetten van lijst naar numpy array en aanmaken van subplot.
    distributies = np.array(distributies)
    fig, ax = plt.subplots(figsize=(10, 10))

    # eerste distributie toewijzen aan sum_arr.
    sum_arr = distributies[0]

    # aanmaken van stacked bar chart + plotten van eerste familie.
    ax.bar(range(1, cluster_aantal+1),
           sum_arr, edgecolor='black', color=kleuren[0])

    iteratie = 0

    # cumulatief plotten van elke distributie zodat een
    # stacked bar chart ontstaat met per bar een andere kleur uit 'kleuren'.
    for dist in distributies[1:]:
        iteratie += 1
        if iteratie > 12:
            ax.bar(range(1, cluster_aantal+1), dist, bottom=sum_arr,
                   edgecolor='black', color=kleuren[iteratie], hatch='/')
        else:
            ax.bar(range(1, cluster_aantal+1), dist, bottom=sum_arr,
                   edgecolor='black', color=kleuren[iteratie])
        sum_arr += dist

    # toevoegen van labels die de grootte aangeven per bar.
    for container in ax.containers:
        labels = [label if label else '' for label in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='center', size=10)

    # aanmaken van legenda.
    ax.legend(list(range(1, len(distributies)+1)), title='families',
              ncol=3, bbox_to_anchor=(1, 1))

    # toevoegen van plot -en astitels.
    ax.set_title('Distributie van families over de clusters', size=15)
    ax.set_ylabel('Familiefrequentie', size=15)
    ax.set_xlabel('Clusters', size=15)


cluster_uitvoer = "Data_out/cluster_uitvoer.txt"
familie_no = "Data/CloneIdFamily.txt"

Histogram(cluster_uitvoer, familie_no, 5)
