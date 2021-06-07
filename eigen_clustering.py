# -*- coding: utf-8 -*-
"""
Created on Tue May 18 14:16:16 2021

@author: 20192379
"""


import numpy as np


"""Inlezen bestand en dictionary maken"""


def lees_bestand_en_maak_dictionary(dimensie, bestandsnaam):
    """Deze functie leest het inputbestand and creëert een dictionary.


       Parameter:
       ----------
       dimensie: Integer waarde voor de hoeveelheid dimensies.
       bestandsnaam: Tekstbestand met de CloneID's en relatieve
                     expressiewaarden.


       Uitvoer:
       --------
       dic_data: Dictionary met als key CloneID's en als value een lijst van
                 waarden.
    """
    # Inlezen van bestand
    infile = open(bestandsnaam)
    lines = infile.readlines()
    infile.close()

    # Creëer een lege dictionary
    dic_data = {}
    # Verwijder alle newline karakters uit de string en split op de witruimtes
    for regel in lines:
        data = regel.replace("\n", " ").split()
        converteer_lijst = []
        # Transformeer de key, welke cloneID is, naar een integer
        key = int(data[0])
        # Transformeer de waarden in de lijst naar floats
        for i in range(1, 9):
            converteer_lijst.append(float(data[i]))
        # Voeg de key en de bijbehorende waarden aan de lege dictionary toe
        dic_data[key] = converteer_lijst
    return dic_data


"""Normaliseren"""


def normaliseer_data(dic):
    """Deze functie creëert een dictionary.


       Parameter:
       ----------
       dic: Dictionary met als key CloneID's en als value een lijst van
            waarden.


       Uitvoer:
       --------
       genormaliseerde_data: Dictionary met als key de cloneID's en als
                             value een lijst van genormaliseerde waarden.
    """
    # Creëer een lege dictionary
    genormaliseerde_data = {}
    totale_som = 0
    # Loop over de items in de invoer dictionary
    for key, value in dic.items():
        # Loop over de items in de lijst van waarden
        for i in value:
            # Bereken de lengte van de vectoren
            totale_som += (i)**2
        vector_lengte = (totale_som)**0.5
        converteer_lijst2 = []
        # Loop over de elementen in de lijst van waarden
        for element in value:
            # Voeg de genormaliseerde waarden aan de converteer lijst toe
            converteer_lijst2.append((element/vector_lengte))
        # Voeg de key en de bijbehorende values aan de lege dictionary toe
        genormaliseerde_data[key] = converteer_lijst2
    return genormaliseerde_data


"""Aanmaak referentievector"""


def referentie(dimensie):
    """Deze functie retourneert een lijst alle genormaliseerde coördinaten
       die bij de referentievector hoort.


       Parameter:
       ----------
       dimensie: Integer waarde voor de hoeveelheid dimensies.


       Uitvoer:
       --------
       referentie_genormaliseerd: Lijst met coördinaten van de
                                  referentievector.
    """
    # Creëer een lege lijst voor alle coördinaten in de referentievector
    referentie_vector = []

    # Creëer een lege lijst voor alle genormaliseerde coördinaten in de
    # referentievector
    referentie_genormaliseerd = []
    # Voeg per iteratie een 1 toe aan de lijst referentie_vector
    for i in range(dimensie):
        referentie_vector.append(1)
    # Normaliseer de waarden uit referentie_vector en voegt deze toe aan de
    # lijst referentie_genormaliseerd
    for j in referentie_vector:
        x = referentie_vector[j]/(dimensie**0.5)
        referentie_genormaliseerd.append(x)
    return referentie_genormaliseerd


"""Berekenen inproducten"""


def inproducten_vectoren(dimensie, genormaliseerde_data,
                         referentie_genormaliseerd):
    """Deze functie retourneert een lijst met alle waarden voor het inproduct
       tussen de expressievectorenen de referentievector.


       Parameter:
       ----------
       genormaliseerde_data: Dictionary met als key de cloneID's en de
                             bijbehorende genormaliseerde vectoren als values.
       referentie_genormaliseerd: Lijst met genormaliseerde coördinaten van
                                  de referentievector.
       dimensie: Integer waarde voor de hoeveelheid dimensies.


       Uitvoer:
       --------
       lijst_inproduct: Lijst met de waardes van de inproducten.
    """
    # Creëer een lege lijst voor alle inproducten
    lijst_inproduct = []
    inproduct = 0

    # Loop over alle elementen in de dictionary genormaliseerde_data
    for key, value in genormaliseerde_data.items():
        # Berekent het inproduct tussen de referentie_waarden en de
        # genormaliseerde expressievectoren
        for i in range(0, dimensie):
            inproduct += referentie_genormaliseerd[i]*value[i]
        lijst_inproduct.append(inproduct)
        inproduct = 0
    # Sorteer alle waarden in de lijst met alle inproducten zodat ze van klein
    # naar groot op volgorde staan
    lijst_inproduct.sort()
    # print(lijst_inproduct)

    return lijst_inproduct


"""Aanmaken dictionary met CloneID en inproduct"""


def dict_inproduct(dimensie, genormaliseerde_data, referentie_genormaliseerd):
    """Deze functie berekent het inproduct tussen alle expressievectoren en de
       referentievector en geeft een dictionary met alle cloneID's als keys en
       bijbehorende inproducten als values. Deze inproducten zijn van klein
       naar groot gesorteerd.


       Parameter:
       ----------
       genormaliseerde_data: Dictionary met als key de cloneID's en de
                             bijbehorende genormaliseerde vectoren als values.
       referentie_genormaliseerd: Lijst met genormaliseerde coördinaten van de
                                  referentievector.
       dimensie: Integer waarde voor de hoeveelheid dimensies.


       Uitvoer:
       --------
       Clone_ID_gesorteerd: Dictionary met alle cloneID's als keys en
                            bijbehorende inproducten als values gesorteerd op
                            alle values van klein naar groot.
    """
    # Creëer een lege dictionary voor alle cloneID's met bijbehorende inproduct
    # en een lege dictionary met deze waarden gesorteerd op inproducten
    dictionary_inproduct = {}
    clone_ID_gesorteerd = {}
    inproduct = 0

    # Loop over alle elementen in de dictionary genormaliseerde_data
    for key, value in genormaliseerde_data.items():
        # Berekent het inproduct tussen de referentie_waarden en de
        # genormaliseerde expressievectoren
        for i in range(0, dimensie):
            inproduct += referentie_genormaliseerd[i]*value[i]
        dictionary_inproduct[key] = inproduct
        inproduct = 0

    # Sorteer alle values in dictionary_inproduct geeft deze terug als lijst
    inproduct_gesorteerd = sorted(dictionary_inproduct.values())
    # Loop over deze lijst met gesorteerde inproducten en voegt in een nieuwe
    # dictionary clone_ID_gesorteerd als key de cloneID en als value de
    # inproducten, gesorteerd op alle inproducten
    for j in inproduct_gesorteerd:
        for k in dictionary_inproduct.keys():
            if dictionary_inproduct[k] == j:
                clone_ID_gesorteerd[k] = dictionary_inproduct[k]
                break
    return clone_ID_gesorteerd


"""Maken van de clusters"""


def maken_clusters(k, lijst_inproducten, clone_ID_gesorteerd):
    """Deze functie retourneert een dictionary met alle cloneID's als keys en
       alle clusternummers als values. Deze values zijn van klein naar
       groot gesorteerd.


       Parameter:
       ----------
       lijst_inproducten: Een gesorteerde lijst met alle waarden voor het
                          inproduct.
       clone_ID_gesorteerd: Een gesorteerde dictionary met als key de
                            cloneID's en als values de inproducten.
       k: Integer waarde voor de hoeveelheid clusters.


       Uitvoer:
       --------
       dict_cloneid_clusternr: Dictionary met alle cloneID's als keys en het
                               bijbehorende clusternumer als value.
    """
    # Creëer lege dictionaries met als eerst het clusternummer als key en
    # inproduct als value, ten tweede een dictionary met als key het inproduct
    # en als value het clusternummer, ten derde een dictionary met als key het
    # cloneID en als value het clusternummer
    dict_clusternr_inproduct = {}
    dict_inproduct_clusternr = {}
    dict_cloneid_clusternr = {}
    dict_clusternr_stats = {}
    outliers = []

    # Deel de lijst met alle inproducten op in k delen
    clusters = np.array_split(lijst_inproducten, k)

    # Loop over de lengte van de hoeveelheid clusters
    for i in range(len(clusters)):
        # Converteer de index naar een lijst
        dict_clusternr_inproduct[i+1] = clusters[i].tolist()
        # Bereken per lijst met inproducten de standaar deviate en het
        # gemiddelde
        dict_clusternr_stats[i+1] = [np.std(clusters[i]), np.mean(clusters[i])]

    # Loop over alle elementen in de dictionary
    for key, value in dict_clusternr_inproduct.items():
        # Loop over alle elementen in de lijst van values
        for n in value:
            # Bepaal of de waardes outliers zijn, en zo ja, verwijder deze uit
            # de dictionary en voeg deze aan de lijst outliers toe
            if (n-dict_clusternr_stats[key][1]) > 2.5*dict_clusternr_stats[key][0]:
                outliers.append(n)
                value.remove(n)

    # Loop over alle outliers
    for l in outliers:
        # Als de outliers in de eerste cluster zitten en er wordt aan
        # onderstaande condities voldaan, voeg deze aan de value van het juiste
        # clusternummer in de dictionary toe.
        if abs(l-dict_clusternr_stats[1][1]) < 2.5*dict_clusternr_stats[1][0]:
            dict_clusternr_inproduct[1].append(l)
            dict_clusternr_inproduct[1].sort()
        elif abs(l-dict_clusternr_stats[k][1]) > 2.5*dict_clusternr_stats[k][0]:
            dict_clusternr_inproduct[k].append(l)
            dict_clusternr_inproduct[k].sort()
        # Voor de overige outliers, bekijk bij welke cluster deze het best
        # horen
        else:
            afstand = "niet gedefinieerd"
            cluster = "niet gedefinieerd"
            # Loop over de elementen in het bereik
            for m in range(1, k+1):
                # Bepaal de maximale en minimale inproducten
                inprod_max = dict_clusternr_inproduct[m].max()
                inprod_min = dict_clusternr_inproduct[m].min()
                # Bereken het verschil tussen de outlier en het maximale/minimale
                # inproduct
                inprod_verschil_max = abs(l-inprod_max)
                inprod_verschil_min = abs(l-inprod_min)
                # Bepaal of het minimale of maximale verschil kleiner is
                if inprod_verschil_max < inprod_verschil_min:
                    inprod_verschil = inprod_verschil_max
                elif inprod_verschil_max > inprod_verschil_min:
                    inprod_verschil = inprod_verschil_min
                # Wanneer de afstand nog niet gedefinieerd is of het verschil
                # kleiner dan de huidige afstand is, verander de variabele genaamd
                # afstand en het clusternummer
                if afstand == "niet gedefinieerd" or inprod_verschil < afstand:
                    afstand = inprod_verschil
                    cluster = m
            # Voeg de outlier aan de dictionary bij het juiste clusternummer toe
            dict_clusternr_inproduct[cluster].append(l)

    # Loop over de elementen in de dictionary
    for key1, value1 in dict_clusternr_inproduct.items():
        for j in value1:
            dict_inproduct_clusternr[j] = key1

    # Loop over de elementen in beide dictionaries en creëert een nieuwe
    # dictionary met dezelfde key als de key in clone_ID_gesorteerd en als
    # value de value van dict_inproduct_clusternr
    for (key2, value2), (key3, value3) in zip(clone_ID_gesorteerd.items(), dict_inproduct_clusternr.items()):
        dict_cloneid_clusternr[key2] = value3

    return dict_cloneid_clusternr


"""Samenvoegen van functies"""


def clusterproces(dimensie, bestand, k):
    """ Deze functie zal bovenstaande functies aanroepen.


       Parameter:
       ----------
       dimensie: Integer waarde voor de hoeveelheid dimensies.
       bestand: Tekstbestand met de CloneID's en relatieve expressiewaarden.
       k: Integer waarde voor de hoeveelheid clusters.


       Uitvoer:
       --------
       inproduct_clusters: Dictionary met als key de CloneID's en als value de
                           clusternummers.
   """

    dictionary = lees_bestand_en_maak_dictionary(
        dimensie, bestandsnaam=bestand)
    genormaliseerde_waardes = normaliseer_data(dic=dictionary)

    referentie_waarden = referentie(dimensie)

    gesorteerde_inproducten = inproducten_vectoren(
        dimensie, genormaliseerde_data=genormaliseerde_waardes,
        referentie_genormaliseerd=referentie_waarden)
    dict_inpro = dict_inproduct(
        dimensie, genormaliseerde_data=genormaliseerde_waardes,
        referentie_genormaliseerd=referentie_waarden)

    inproduct_clusters = maken_clusters(
        k, lijst_inproducten=gesorteerde_inproducten,
        clone_ID_gesorteerd=dict_inpro)

    return inproduct_clusters


bestand_path = 'Data_out/Relatieve expressiewaarden.txt'

eindindeling = clusterproces(dimensie=4, bestand=bestand_path, k=5)


"""Omzetten naar tekstbestand"""


def formaat_omzetten(oude_formaat):
    """Deze functie zal een dictionary omzetten naar een string.


       Parameter:
       ----------
       oude_formaat: Dictionary met als key de CloneID's en als value het
                     clusternummer.


       Uitvoer:
       --------
       nieuwe_formaat: String met de CloneID's en de clusternummers.
   """
    nieuwe_formaat = " "
    # Loop over alle keys en values in de dictionary
    for key, value in oude_formaat.items():
        nieuwe_formaat += str(key) + 3*" " + str(value) + "\n"
    return nieuwe_formaat


nieuwe_formaat = formaat_omzetten(oude_formaat=eindindeling)
print(nieuwe_formaat)


# Wegschrijven naar een tekstbestand met de CloneID's en de clusternummers
f = open("Data_out/cluster_uitvoer.txt", "w")
f.write(nieuwe_formaat)
f.close()
