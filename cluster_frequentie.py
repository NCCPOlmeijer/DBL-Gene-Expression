# -*- coding: utf-8 -*-
"""
Created on Wed May 5 2021.

@author: NoahOlmeijer/20203063
"""


def cluster_frequentie(gen_beschrijving, cluster_uitvoer):
    """Programma voor de analyse van woordfrequenties in clusters.

    Parameters
    ----------
    gen_beschrijving: tekstfile
    beschrijving: tekstbestand bevat per cloneID een tekstuele beschrijving
    van het (meest waarschijnlijke) bijbehorende gen.

    cluster_uitvoer: tekstfile
    beschrijving: tekstbestand bevat per cloneID de corresponderende cluster
    waar die in voorkomt.

    Uitvoer
    -------
    cluster_freq: dictionary

    Formaat: {'woord':[ci, ci+1, ..., ck-1]} met k aantal clusters, en ci
    de clusterfrequentie van het woord in cluster i

    beschrijving: Retourneert een dictionary met verschillende woorden en de
    corresponderende clusterfrequentie samenstelling.
    """
    # Inlezen van 'gen_beschrijving' en
    # rauwe data uit 'gen_beschrijving' toewijzen aan
    # variable 'gen_beschrijving'.

    with open(gen_beschrijving) as gen_beschrijving:
        gen_beschrijving = gen_beschrijving.readlines()

    # Inlezen van 'cluster_uitvoer' en
    # rauwe data uit 'cluster_uitvoer' toewijzen aan
    # variable 'cluster_uitvoer'.

    with open(cluster_uitvoer) as cluster_uitvoer:
        cluster_uitvoer = cluster_uitvoer.readlines()

    # lijst aanmaken genaamd 'items' van alle losse woorden en integers
    # uit 'data' zonder leestekens: '\x01', ',', '(', ')', '/'

    items = ' '.join([line.strip().lower() for line
                      in gen_beschrijving[1::3]]).replace('\x01', '')

    for character in [',', '(', ')', '/', '[', ']']:
        if character in items:
            items = items.replace(character, ' ')
    items = items.split()

    # lijsten aanmaken genaamd 'cloneIDs' en 'beschrijvingen' met inhoud
    # de cloneIDs en genbeschrijvingen, respectievelijk.

    cloneIDs = [line.strip() for line in gen_beschrijving[0::3]]
    beschrijvingen = [line.strip().lower() for line in gen_beschrijving[1::3]]

    # lijst aanmaken genaamd 'geen_integers' met uitsluitend woorden
    # uit beschrijvingen

    geen_integers = [woord for woord in items if not (
        woord.isdigit() or woord[0] == '-' and woord[1:].isdigit())]

    # lege dictionary aanmaken genaamd 'woord_freq'

    woord_freq = {}

    # per woord uit 'geen_integers' de frequentie bepalen
    # en toevoegen aan 'woord_freq'.

    for woord in geen_integers:
        if woord not in woord_freq:
            woord_freq[woord] = 1
        else:
            woord_freq[woord] += 1

    # lijst aanmaken genaamd 'unieke_woorden' met alle keys uit 'woord_freq'
    # (alle verschillende woorden uit 'gen_beschrijving')

    unieke_woorden = list(woord_freq.keys())

    # lege dictionary aanmaken genaamd 'beschrijving_cloneIDs'

    beschrijving_cloneIDs = {}

    # per woord uit 'unieke_woorden' kijken welke cloneIDs daarbij horen en
    # toevoegen aan 'beschrijving_cloneIDs'

    for woord in range(len(unieke_woorden)):
        for beschrijving in range(len(beschrijvingen)):
            if ' ' + unieke_woorden[woord] \
                   + ' ' in beschrijvingen[beschrijving]:
                if unieke_woorden[woord] not in beschrijving_cloneIDs:
                    beschrijving_cloneIDs[unieke_woorden[woord]] = \
                        [cloneIDs[beschrijving]]
                else:
                    beschrijving_cloneIDs[unieke_woorden[woord]].append(
                        cloneIDs[beschrijving])
            else:
                pass

    # lijsten aanmaken genaamd 'cloneID_values' en 'cloneID_keys'
    # met de values en keys uit 'beschrijving_cloneIDs', respectievelijk

    cloneID_values = list(beschrijving_cloneIDs.values())
    cloneID_keys = list(beschrijving_cloneIDs.keys())

    # lijst aanmaken genaamd 'cluster_data' met cloneIDs
    # en bijbehorende cluster

    cluster_data = [item for sublist in [
        line.strip().split() for line in cluster_uitvoer] for item in sublist]

    # lege dictionary aanmaken genaamd 'cluster_freq'

    cluster_freq = {}

    # ophalen van cluster aantal uit 'cluster_data' en toewijzen aan k

    k = int(max([line for line in cluster_data[1::2]]))+1

    # per woord kijken wat de samenstelling is van frequenties in de clusters

    for woord in range(len(cloneID_keys)):

        cluster_freq[cloneID_keys[woord]] = [0] * k

        for cloneID in range(len(cloneID_values[woord])):
            if cloneID_values[woord][cloneID] in cluster_data:
                cluster_index = cluster_data.index(
                    cloneID_values[woord][cloneID]) + 1
                cluster_value = int(cluster_data[cluster_index])
                cluster_freq[cloneID_keys[woord]][cluster_value] += 1
            else:
                pass

    return cluster_freq


GenDescription = 'Data/GenDescription2.txt'
clusterResultFile = "Data/Voorbeeld_clusterresult.txt"

if __name__ == '__main__':
    print(cluster_frequentie(GenDescription, clusterResultFile))
