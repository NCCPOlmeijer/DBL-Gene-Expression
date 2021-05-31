# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:28:50 2021

@author: NoahPC
"""


import matplotlib.pyplot as plt
import numpy as np


def Histogram(cluster_uitvoer, FamilyCloneID):

    with open(cluster_uitvoer) as cluster_uitvoer:
        cluster_uitvoer_data = cluster_uitvoer.read().split()
        cluster_uitvoer = list(map(int, cluster_uitvoer_data))

    with open(FamilyCloneID) as FamilyCloneID:
        FamilyCloneID_data = FamilyCloneID.read().split()[2:]
        FamilyCloneID = list(map(int, FamilyCloneID_data))

    Family_no = FamilyCloneID[1::2]
    Family_cloneIDs = FamilyCloneID[::2]

    dict1 = {}

    for i in range(1, 27):
        dict1[i] = []

    for Family in range(len(Family_no)):
        dict1[Family_no[Family]].append(Family_cloneIDs[Family])

    Cluster_no = cluster_uitvoer[1::2]
    Cluster_cloneIDs = cluster_uitvoer[::2]

    dict2 = {}

    for i in range(0, 6):
        dict2[i] = []

    for Cluster in range(len(Cluster_no)):
        dict2[Cluster_no[Cluster]].append(Cluster_cloneIDs[Cluster])

    families = list(dict1.values())
    clusters = list(dict2.values())

    dist_lst = []

    for family in range(len(dict1)):
        g = [0]*6
        for cloneID in range(len(families[family])):
            for cluster in range(len(clusters)):
                if families[family][cloneID] in clusters[cluster]:
                    g[cluster] += 1
        dist_lst.append(g)

    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
              '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
              '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
              '#000075', '#808080', '#ffffff', '#000000', '#eb5b01', '#db8c62',
              '#f58b7a', '#288C00']

    i = 0
    lst = np.array(dist_lst)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.bar(range(6), lst[0], edgecolor='black', color=colors[0])
    sum_arr = lst[0]
    for data in lst[1:]:
        i += 1
        ax.bar(range(6), data, bottom=sum_arr, edgecolor='black',
               color=colors[i])
        sum_arr += data

    ax.legend(list(range(1, len(lst))), title='families',
              ncol=2, bbox_to_anchor=(1, 1))

    for c in ax.containers:
        labels = [a if a else '' for a in c.datavalues]
        ax.bar_label(c, labels=labels, label_type='center', size=10)

    ax.set_yticks(list(range(0, 24, 2)))
    ax.set_title('Distributie van families over de clusters', size=15)


cluster_uitvoer = "Data/Voorbeeld_clusterresult.txt"
familie_no = "Data/CloneIdFamily.txt"

Histogram(cluster_uitvoer, familie_no)
