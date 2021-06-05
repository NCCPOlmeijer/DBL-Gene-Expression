# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:26:20 2021

@author: 20203069
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
    with open(bestand) as file:
        lines = file.readlines()

    # Creëer een lege dictionary
    dic_data = {}
    # Verwijder alle newline karakters uit de string en split op de witruimtes
    for regel in lines:
        data = regel.strip().split()
        converteer_lijst = []
        # Transformeer de key, welke cloneID is, naar een integer
        key = int(data[0])
        # Transformeer de waarden in de lijst naar floats
        for i in range(1, dimensie+1):
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
    # Loop over de items in de invoer dictionary
    for key, value in dic.items():
        totale_som = 0
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


"""K-means"""


def verdeling_in_random_clusters(k, dictionary):
    """Deze functie voegt alle datapunten toe aan een random cluster.


       Parameter:
       ----------
       k: Integer voor het aantal clusters
       dictionary: Dictionary met als key de cloneID's en als
                   value een lijst van genormaliseerde waarden.


       Uitvoer:
       --------
       verdeling_cluster: Dictionary met als key het clusternummer en als value
                          een lijst met alle CloneID's die tot dit cluster
                          behoren.
    """
    # Creëer een lege dictionary
    verdeling_cluster = {}
    # Maak voor alle clusters(k) in de dictionary een lege lijst aan als value
    for i in range(1, k+1):
        verdeling_cluster[i] = []
    # Loop over alle items in de input dictionary
    for key, value in dictionary.items():
        # Bepaal voor alle datapunten een random clusternummer
        random_cluster = np.random.randint(1, k+1)
        # Voeg de CloneID van het datapunt toe aan de lijst van het
        # bijbehorende cluster. Dit is de value van de nieuwe dictionary
        verdeling_cluster[random_cluster].append(key)
    return verdeling_cluster


def minimale_afstand_tot_cluster(cluster_centrum, data_punten):
    """Deze functie bepaald welke cluster de minimale afstand tot een datapunt
       heeft.


       Parameter:
       ----------
       cluster_centrum: Dictionary met als key het clusternummer en als value
                        een lijst met waarden die samen het middelpunt van een
                        cluster vormen.
       data_punten: Dictionary met als key de cloneID's en als
                    value een lijst van genormaliseerde waarden.


       Uitvoer:
       --------
       cluster_nummer: integer die gelijk is aan het clusternummer
       minimale_afstand: float die minimale afstand geeft tussen het datapunt
                         en het clustenummer.
    """
    # Creëer variabelen die waardes hebben die kunnen worden aangepast
    minimale_afstand = "niet_gedefineerd"
    cluster_nummer = "niet_gedefineerd"
    # Loop over alle elementen van de dictionary die de clustercentra bevat
    for key_cluster, value_cluster in cluster_centrum.items():
        # Bereken afstand tussen de datapunt en het middelpunt van de cluster
        som = 0
        # Loop over de elementen binnen het bereik
        for g in range(0, len(value_cluster)):
            # Bereken de waarden van de afstand tussen de data punten en
            # het cluster centrum
            som += (value_cluster[g]-data_punten[g])**2
        afstand = som**0.5
        # Pas de minimale afstand variabele aan en het cluster nummer als de
        # minimale afstand als deze nog niet gedefineerd is of als deze groter
        # dan de huidige afstand is
        if minimale_afstand == "niet_gedefineerd" or \
           minimale_afstand > afstand:
            minimale_afstand = afstand
            cluster_nummer = key_cluster
    return cluster_nummer, minimale_afstand


"""Berekenen van centra """


def berekenen_van_centra(dimensie, indeling, waarde):
    """Deze functie berekend het middelpunt van een cluster door het
       gemiddelde te nemen van alle punten die tot dat cluster behoren
       per dimensie

       Parameter:
       ----------
       dimensie: Integer waarde voor de hoeveelheid dimensies.
       indeling: Dictionary met als key het clusternummer en als value een
                 lijst met alle CloneID's die tot dit cluster behoren.
       waarde: Dictionary met als key de cloneID's en als value een lijst van
               genormaliseerde waarden.

       Uitvoer:
       --------
       centrum: Dictionary met als key het clusternummer en als value een lijst
                waarden die samen het middelpunt van een cluster vormen.
    """
    # Creër een lege dictionary
    centrum = {}
    # Loop over alle items in de dictionary voor de indeling
    for key_indeling, value_indeling in indeling.items():
        # Creëer een lege lijst
        som = []
        # Loop over alle CloneID's die tot een clusternummer behoren
        for cloneid in value_indeling:
            som.append(waarde[cloneid])
        # Creëer een lege lijst
        som_list = []
        for dim in range(0, dimensie):
            totaal_som = 0
            for element in range(0, len(som)):
                # Bereken de afstand tot het centrum van een cluster
                totaal_som += som[element][dim]
            gemiddelde = totaal_som / len(som)
            som_list.append(gemiddelde)
        # Voeg de totale som toe aan de dictionary
        centrum[key_indeling] = som_list
    return centrum


"""Kwadratische fout"""


def bereken_kwadratische_fout(dimensie, data_clusters, norm_val, indeling):
    """Deze functie berekend de som van de kwadraten van de
       afstanden van iedere vector tot het centrum van zijn cluster.

       Parameter:
       ----------
       dimensie: Integer waarde voor de hoeveelheid dimensies.
       data_clusters: Dictionary met als key het clusternummer en als value
                      een lijst met waarden die samen het middelpunt van een
                      cluster vormen.
       norm_val: Dictionary met als key de cloneID's en als
                 value een lijst van genormaliseerde waarden.
       indeling: Dictionary met als key het clusternummer en als value een
                 lijst met alle CloneID's die tot dit cluster behoren.


       Uitvoer:
       --------
       final_kwadrat_fout: lijst met de gezamelijke kwadratische fout van alle
                           clusters over één iteratie
    """
    # Loopt over de indeling van de clusters
    kwadrat_fout = {}
    for key_indeling, value_indeling in indeling.items():
        # Creëer een lege lijst
        converteer_lijst3 = []
        # Loopt over alle lijsten met cloneID's
        for i in value_indeling:
            # Voeg alle lijsten met waarden die behoren bij een bepaalde
            # cloneID aan converteer_lijst3 toe
            converteer_lijst3.append(norm_val[i])
        # print(converteer_lijst3)
        totaal_som = 0
        # Creëer een lege dictionary
        # Loop over alle keys en values in de dictionary met clusterpunten

        # for value_cluster in data_clusters[key_indeling].items():
        #     # Loop over alle lijsten in converteer_lijst3
        for element in converteer_lijst3:
            som_kwad = 0
            for i in range(0, dimensie):
                # Formuleren van formule om de kwadratische fout te berekenen
                som_kwad += (element[i] - data_clusters[key_indeling][i])**2
            totaal_som += som_kwad
            # Voeg de totale som toe aan de dictionary
        kwadrat_fout[key_indeling] = totaal_som

    final_kwadrat_fout = []
    som_kwad_fout = 0
    for key_kf, value_kf in kwadrat_fout.items():
        som_kwad_fout += value_kf
    final_kwadrat_fout.append(som_kwad_fout)
    return final_kwadrat_fout


"""Optimaliseren k-means"""


def optimaliseren(bestandsnaam, k, dimensie):
    """Deze functie zal het algoritme voor de k-means optimaliseren.
       Dit zal worden gedaan door eerder aangemaakte functie aan te roepen
       totdat de kwadratische fout niet meer veranderd.

       Parameter:
       ----------
       bestandsnaam: Tekstbestand met de CloneID's en relatieve
                     expressiewaarden.
       k: Integer voor het aantal clusters.
       dimensie: Integer waarde voor de hoeveelheid dimensies.


       Uitvoer:
       --------
       nieuwe_groupering: Dictionary met als key het clusternummer en als value
                          een lijst met alle CloneID's die tot dit cluster
                          behoren.
    """
    x = 0
    vergelijk_kwad_fout = []
    lege_cluster = "Geen lege cluster."

    dictionary = lees_bestand_en_maak_dictionary(
        dimensie, bestandsnaam=bestand)

    genormaliseerde_waardes = normaliseer_data(dic=dictionary)
    # print(genormaliseerde_waardes)

    nieuwe_groupering = verdeling_in_random_clusters(
        k, genormaliseerde_waardes)
    # print(nieuwe_groupering)

    # Itereer over onderstaande code,
    # wanneer de onderstaande voorwaarden voldaan zijn
    while (len(vergelijk_kwad_fout) < 2 or vergelijk_kwad_fout[-1] != vergelijk_kwad_fout[-2]) and lege_cluster == "Geen lege cluster.":
        if [] in nieuwe_groupering.values():
            lege_cluster = "Er ontstaat een lege cluster, run het programma opnieuw of probeer een andere waarde voor k."
        else:
            cluster_centra = berekenen_van_centra(
                dimensie, indeling=nieuwe_groupering,
                waarde=genormaliseerde_waardes)

            # Creëer een lege dictionary
            nieuwe_groupering = {}
            # Creëer voor elke cluster een key met een bijbehorend clusternummer
            # en een lege lijst als value
            for i in range(1, k+1):
                nieuwe_groupering[i] = []

            # Loop over de dictionary die de genormaliseerde waarden bevat
            for key, lijst_waarden in genormaliseerde_waardes.items():
                # Roep de functie aan
                cluster_groep, minimum = minimale_afstand_tot_cluster(
                    cluster_centrum=cluster_centra, data_punten=lijst_waarden)
                # Voeg de key en de bijbehorende values aan de lege dictionary toe

                nieuwe_groupering[cluster_groep].append(key)

            kwadratische_fout = bereken_kwadratische_fout(
                dimensie, data_clusters=cluster_centra,
                norm_val=genormaliseerde_waardes, indeling=nieuwe_groupering)

            vergelijk_kwad_fout.append(kwadratische_fout)

            x += 1
    return nieuwe_groupering, lege_cluster


bestand = 'Data_out/Relatieve expressiewaarden.txt'
optimaliseren_k_means, inhoud_cluster = optimaliseren(
    bestandsnaam=bestand, k=5, dimensie=6)
print(optimaliseren_k_means, inhoud_cluster)


"""Omzetten formaat"""


def formaat_omzetten(oude_formaat):
    """Deze functie zal een dictionary omzetten naar een string.


        Parameter
        ---------
        oude_formaat: Dictionary met als key de CloneID's en als value het
                      clusternummer.


        Uitvoer
        -------
        nieuwe_formaat: String met de CloneID's en de clusternummers.
    """
    nieuwe_formaat = " "
    # Loop over alle keys en values in de dictionary
    for key, value in oude_formaat.items():
        for element in value:
            nieuwe_formaat += str(element) + 3*" " + str(key) + "\n"
    return nieuwe_formaat


nieuwe_formaat = formaat_omzetten(oude_formaat=optimaliseren_k_means)
print(nieuwe_formaat)

k = 5
# Wegschrijven naar een tekstbestand met de CloneID's en de clusternummers
f = open("nieuw_formaat" + str(k) + ".txt", "w")
f.write(nieuwe_formaat)
f.close()
