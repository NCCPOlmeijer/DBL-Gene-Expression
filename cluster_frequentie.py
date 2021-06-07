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
    # Inlezen van 'gen_beschrijving' en 'cluster_uitvoer'.
    with open(gen_beschrijving) as gen_beschrijving:
        gen_beschrijving = gen_beschrijving.readlines()

    with open(cluster_uitvoer) as cluster_uitvoer:
        cluster_data = cluster_uitvoer.read().split()

    # lijst aanmaken genaamd 'items' van alle losse woorden en integers
    # uit 'data' zonder leestekens: '\x01', ',', '(', ')', '/'.
    items = ' '.join([line.strip().lower() for line
                      in gen_beschrijving[1::3]]).replace('\x01', '')

    for character in [',', '(', ')', '/', '[', ']', '"']:
        if character in items:
            items = items.replace(character, ' ')
    items = items.split()

    # lijsten aanmaken genaamd 'cloneIDs' en 'beschrijvingen' met inhoud
    # de cloneIDs en genbeschrijvingen, respectievelijk.
    cloneIDs = [line.strip() for line in gen_beschrijving[0::3]]
    beschrijvingen = [' ' + line.strip().lower()
                      for line in gen_beschrijving[1::3]]

    # lijst aanmaken genaamd 'geen_integers' met uitsluitend woorden
    # uit beschrijvingen (int, letters, 'woorden' met lengte 1 verwijderen).
    geen_integers = []

    for woord in items:
        try:
            int(woord)
            pass
        except ValueError:
            if (woord != '-') and (len(woord) > 1):
                geen_integers.append(woord)

    woord_lijst = []

    lengte = len(geen_integers)
    volgende = False

    # voegt afkorting woorden samen zoals E. Coli / S. cerevisiae zodat het
    # niet resulteert in 'E.', 'Coli' of 'S.', 'cerevisiae'.
    for woord in range(lengte):
        if (geen_integers[woord].endswith('.')) and \
                (len(geen_integers[woord]) == 2):
            joined = geen_integers[woord] + ' ' + geen_integers[woord+1]
            woord_lijst.append(joined)
            volgende = True
        else:
            if not volgende:
                woord_lijst.append(geen_integers[woord])
                volgende = False
            else:
                volgende = False
                pass

    woord_freq = {}

    # per woord uit 'geen_integers' de frequentie bepalen
    # en toevoegen aan 'woord_freq'.
    for woord in woord_lijst:
        if woord not in woord_freq:
            woord_freq[woord] = 1
        else:
            woord_freq[woord] += 1

    # lijst aanmaken genaamd 'unieke_woorden' met alle keys uit 'woord_freq'.
    unieke_woorden = list(woord_freq.keys())

    # lege dictionary aanmaken genaamd 'beschrijving_cloneIDs'.
    beschrijving_cloneIDs = {}

    # per woord uit 'unieke_woorden' kijken welke cloneIDs daarbij horen en
    # toevoegen aan 'beschrijving_cloneIDs'.
    for woord in range(len(unieke_woorden)):
        for beschrijving in range(len(beschrijvingen)):
            if ' ' + unieke_woorden[woord] + ' ' \
                    in beschrijvingen[beschrijving]:
                if unieke_woorden[woord] not in beschrijving_cloneIDs:
                    beschrijving_cloneIDs[unieke_woorden[woord]] = \
                        [cloneIDs[beschrijving]]
                else:
                    beschrijving_cloneIDs[unieke_woorden[woord]].append(
                        cloneIDs[beschrijving])
            else:
                pass

    # lijsten aanmaken genaamd 'cloneID_values' en 'cloneID_keys'
    # met de values en keys uit 'beschrijving_cloneIDs', respectievelijk.
    cloneID_values = list(beschrijving_cloneIDs.values())
    cloneID_keys = list(beschrijving_cloneIDs.keys())

    # lege dictionary aanmaken genaamd 'cluster_freq'.
    cluster_freq = {}

    # ophalen van cluster aantal uit 'cluster_data' en toewijzen aan k.
    k = int(max([line for line in cluster_data[1::2]]))

    # per woord kijken wat de samenstelling is van frequenties in de clusters.
    for woord in range(len(cloneID_keys)):

        cluster_freq[cloneID_keys[woord]] = [0] * k

        for cloneID in range(len(cloneID_values[woord])):
            if cloneID_values[woord][cloneID] in cluster_data:
                cluster_index = cluster_data.index(
                    cloneID_values[woord][cloneID]) + 1
                cluster_value = int(cluster_data[cluster_index]) - 1
                cluster_freq[cloneID_keys[woord]][cluster_value] += 1
            else:
                pass

    return cluster_freq


GenDescription = 'Data/GenDescription.txt'
clusterResultFile = "Data/Voorbeeld_clusterresult.txt"

# print(cluster_frequentie(GenDescription, clusterResultFile))


def Format(cluster_freq, iteratie, woord, txt):
    """Netjes formatteren van data in drie regels.

    Regel één, een spatie tussen het groter dan teken en het woord.
    Regel twee, de distributie over de clusters van het woord.
    Regel drie, dubbel slashteken.

    Formaat Voorbeeld: > woord
                       [0, 1, 0, 1, 1, 0]
                       //
    """
    print('>', list(cluster_freq.items())[iteratie][0])
    print(cluster_freq[woord])
    print('//')

    txt.write('> ' + list(cluster_freq.items())[iteratie][0] + '\n')
    txt.write(str(cluster_freq[woord]) + '\n')
    txt.write('//\n')


def frequency_filter(cluster_freq, aantal_clusters, show_zero=True,
                     show_one=True, show_mult=True, show_full=True):
    """Functie kan distributies filteren op inhoud.

    Deze inhoud betreft zero lijsten: [0, 0, 0, ..., 0],
                        non-zero lijsten: [1, 2, 3, 2, 1, ...]
                        single-value lijsten: [0, 0, 1, 0, ..., 0]
                        multiple-value lijsten: [1, 2, 0, 2, 4, ...]
    """
    if show_zero:
        with open('Data_out/zero lijsten.txt', 'w') as txt:
            print('zero lijsten:')
            txt.write('zero lijsten:\n')
            iteratie = 0
            for woord in cluster_freq:
                if cluster_freq[woord].count(0) == aantal_clusters:
                    Format(cluster_freq, iteratie, woord, txt)
                iteratie += 1

    if show_one:
        with open('Data_out/single-value lijsten.txt', 'w') as txt:
            print('single-value lijsten:')
            txt.write('single-value lijsten:\n')
            iteratie = 0
            for woord in cluster_freq:
                if cluster_freq[woord].count(0) == aantal_clusters-1:
                    Format(cluster_freq, iteratie, woord, txt)
                iteratie += 1

    if show_mult:
        with open('Data_out/multiple-value lijsten.txt', 'w') as txt:
            print('multiple-value lijsten:')
            txt.write('multiple-value lijsten:\n')
            iteratie = 0
            for woord in cluster_freq:
                if (cluster_freq[woord].count(0) > 1) and \
                        (cluster_freq[woord].count(0) < aantal_clusters-1):
                    Format(cluster_freq, iteratie, woord, txt)
                iteratie += 1

    if show_full:
        with open('Data_out/non-zero lijsten.txt', 'w') as txt:
            print('non-zero lijsten:')
            txt.write('non-zero lijsten:\n')
            iteratie = 0
            for woord in cluster_freq:
                if cluster_freq[woord].count(0) == 0:
                    Format(cluster_freq, iteratie, woord, txt)
                iteratie += 1
