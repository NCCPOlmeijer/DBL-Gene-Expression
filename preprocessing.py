# -*- coding: utf-8 -*-
"""
Created on Fri Jun 4 2021.

@author:
"""

import numpy as np
import matplotlib.pyplot as plt


def Uitplotten(df, data_bestand, wanneer='voor een correctie.',
               x='P1Sig', y='P2Sig', kleurp='b', kleurd='r',
               lijnstijl='--', klassen=False):
    """Functie voor het plotten van P1Sig en P2Sig uit een dataframe \
    en een diagonale P1Sig = P2Sig lijn toevoegt \
    Indien klassen = True worden de verschillende klassen \
    in verschillende kleuren geplot.

    Parameters
    ----------
    df: Dataframe waaruit de data geplot wordt.
    wanneer: Een toevoeging voor de titel van het plot dat bedoelt is om
    uit te leggen voor welke stap dit is gemaakt,
    standaard = 'voor een correctie.'.

    x:  De X waarden die van het dataframe uitgeplot worden,
    standaard = 'P1Sig'.
    y: De Y waarden die van het dataframe uitgeplot worden,
    standaard = 'P2Sig'.

    kleurp: De kleur van de datapunten indien klassen=False, standaard = 'b'.
    kleurd: De kleur van de diagonale lijn, standaard = 'r'.

    lijnstijl: De stijl van de diagonale lijn, standaard = '--'.
    klassen: Boolean die bepaalt of verschillende klassen gekleurd
    geplot worden (True) of alle klassen één kleur (False), standaard = False
    kleuren: Dictionary die de klassen a, b, c, d
    verschillende kleuren toewijst (Indien klasses=True), standaard =
    {"a": "blue", "b": "cyan", "c": "green", "d": "yellow"}.

    Uitvoer
    -------
    Visualisatie: Scatterplot van één dag.

    Formaat: P1Sig op X-as, P2Sig op Y-as.
    """
    # Maak een dictionary aan die de verschillende klasse
    # aan verschillende kleuren linkt.
    kleuren = {
        "a": "blue",
        "b": "cyan",
        "c": "green",
        "d": "yellow"
    }

    # Code voor scatterplot zelf
    if klassen:
        fig, ax = plt.subplots(figsize=(6, 5))
        for klasse, groep in df.copy().groupby('Klasse'):
            groep.plot(kind='scatter', x=x, y=y,
                       c=kleuren[klasse], ax=ax, s=0.5)
        plt.legend(['a', 'b', 'c', 'd'])
        ax.set_title('Scatterplot van ' + data_bestand + ' van ' +
                     x + ' en ' + y + ' na de indeling van de punten')

    else:
        ax = df.plot(kind='scatter', x=x, y=y, c=kleurp, s=0.5)
        ax.set_title('Scatterplot van ' + data_bestand +
                     ' van ' + x + ' en ' + y + ' ' + wanneer)

    # Voegt een lijn toe aan de plot
    identiteit, = ax.plot([], [], color=kleurd, ls=lijnstijl)

    # sla de gegenereerde plot op in map Plots/Scatter_plots.
    plt.savefig("Plots/Scatter_plots/Scatter" + data_bestand + ".png", dpi=200)

    def callback(ax):
        """Functie die de waardes van de diagonale lijn berekent.

        Parameters
        ----------
        ax: Plot waarvan de waardes berekend moeten worden.

        Uitvoer
        ----------
        identiteit: Voegt waardes toe aan identiteit voor diagonale lijn.

        Geinspireerd door:
        https://stackoverflow.com/questions/22104256/does-matplotlib-have-a
        -function-for-drawing-diagonal-lines-in-axis-coordinates
        """
        x_laag, x_hoog = ax.get_xlim()
        y_laag, y_hoog = ax.get_ylim()
        laag = max(x_laag, y_laag)
        hoog = min(x_hoog, y_hoog)
        identiteit.set_data([laag, hoog], [laag, hoog])

    # Voer de functie uit
    callback(ax)

    # Verandert de diagonaal die al in de plot zit dus daarvoor wordt
    # de callback functie gebruikt
    ax.callbacks.connect('xlim_veranderd', callback)
    ax.callbacks.connect('ylim_veranderd', callback)

    plt.show(block=False)


def hist_uitplotten(df, wanneer, kolom='Rel exp',
                    titel='Frequentie relatieve expressiewaarde van',
                    xlabel='Relatieve expressiewaarde',
                    ylabel='Frequentie'):
    """
    Functie plot een histogram voor rel. expressiewaarden uit een kolom.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.
    wanneer: Een toevoeging voor de titel van het plot dat bedoelt is om
    uit te leggen van welke dag dit is gemaakt.

    kolom: Kolom die gebruikt moet worden voor de waardes van het uitplotten,
    standaard = 'Rel exp'.

    titel: Titeldeel die figuur krijgt, standaard ='Frequentie relatieve
    expressiewaarde van'.

    xlabel: Label voor de X-as, standaard = 'Relatieve expressiewaarde'.
    ylabel: Label voor de Y-as, standaard = 'Frequentie'.

    Uitvoer
    ----------
    Visualisatie: Histogram van één dag.
    Formaat: Relatieve expressiewaarde op X-as, Frequentie op Y-as.
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    df.hist(column=kolom, bins=30, ax=ax)

    ax.set_title(titel + ' ' + wanneer)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # sla de gegenereerde plot op in map Plots/Histogram_preprocessing.
    plt.savefig("Plots/Histogram_preprocessing/"
                + wanneer + ".png", dpi=200)

    plt.show(block=False)


def Indeling(df, ruis=2.5):
    """Functie voor het toevoegen van een nieuwe kolom \
    aan het aangegeven dataframe deze kolom wordt volgens \
    conditie per rij gevuld met de passende letter a, b, c of d.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.
    ruis: De daadwerkelijke signaalruisverhouding in de buurt van de spot die
    als grens genomen wordt, standaard = 2.5.

    Uitvoer
    ----------
    df_ind: Dataframe.
    Formaat: Bevat 8 + 1 nieuwe kolom 'Klasse'.

    Beschrijving: Retourneert een dataframe waarin iedere spot wordt ingedeeld
    in klasse a, b, c of d.
    """
    # Laat ruis de werkenlijke waarde aannemen.
    ruis = ruis * 10

    # Maak een kopie zodat je de ingevoerde dataframe niet veranderd.
    df_ind = df.copy()

    # Condities vaststellen
    condities = [(df_ind['P1STB'] >= ruis) & (df_ind['P2STB'] >= ruis),
                 (df_ind['P1STB'] >= ruis) & (df_ind['P2STB'] <= ruis),
                 (df_ind['P1STB'] <= ruis) & (df_ind['P2STB'] >= ruis),
                 (df_ind['P1STB'] <= ruis) & (df_ind['P2STB'] <= ruis)]

    # Letters respectievelijk aan condities voor kolom Klasse
    keuzes = ['a', 'b', 'c', 'd']

    # Voor ieder gen de juiste letter toevoegen aan kolom Klasse
    df_ind['Klasse'] = np.select(condities, keuzes)

    return df_ind


def Spotfilter(df, ogrens=0.5, bgrens=1.5):
    """Functie filtert een dataframe op basis van de kolom over spotgrootte.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.

    ogrens: De ondergrens waarmee vergeleken wordt, standaard = 0.50,
    betekent dat de ondergrens 50% van de gemiddelde waarde is.

    bgrens: De bovengrens waarmee vergeleken wordt, standaard = 1.50,
    betekent dat de bovengrens 150% van de gemiddelde waarde is.

    Uitvoer
    ----------
    df_filt: Dataframe.
    Formaat: Bevat onveranderde hoeveelheid van 9 kolommen.

    Uitvoer: Retourneert een dataframe waarin spots met een spotgrootte buiten
    de onder- of bovengrens zijn verwijderd.
    """
    # Maak een kopie zodat je de ingevoerde dataframe niet veranderd.
    df_filt = df.copy()

    # Gemiddelde spotgrootte berekenen
    spotgem = df_filt['P1Cov'].mean()

    # Print hoeveel van de punten boven en onder de grens liggen
    print('Er liggen zoveel punten onder de ondergrens: ' +
          str(len(df_filt[df_filt['P1Cov'] < ogrens * spotgem].index)))
    print('Er liggen zoveel punten boven de bovengrens: ' +
          str(len(df_filt[df_filt['P1Cov'] > bgrens * spotgem].index)))

    # Als waarde P1Cov niet voldoet aan conditie wordt spot verwijderd
    df_filt.drop(df_filt[df_filt['P1Cov'] < ogrens *
                         spotgem].index, inplace=True)
    df_filt.drop(df_filt[df_filt['P1Cov'] > bgrens *
                         spotgem].index, inplace=True)

    return df_filt


def Rel_expressie_punten(df, wanneer, punten,
                         con1='P1Sig', con2='P2Sig', waarde=0.7):
    """Functie berekent de rel. expressiewaarden en voegt toe aan nieuwe kolom.

    'Rel exp' toevoegt per spot, op basis van iedere klassewaarde (a,b,c of d)
    wordt er een voorafgestelde hoeveelheid punten toegevoegt aan
    de nieuwe kolom 'Punten' en er wordt bepaald hoe veel spots een absolute
    relatieve expressiewaarde boven een vastgestelde waarde hebben.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.
    wanneer: Een toevoeging voor de geprinte regel dat bedoelt is om
    uit te leggen over welke dag het gaat.
    con1: De eerste waarde die gebruikt en vergeleken moet worden, standaard =
    'P1Sig'.
    con2: De tweede waarde die gebruikt en vergeleken moet worden, standaard =
    'P2Sig'.
    punten: De hoeveelheid punten die respectievelijk worden toegewezen aan
    a,b,c of d, standaard = [0, 1, 1, 5].
    waarde: De waarde waarboven de absolute relatieve expressie moet liggen
    voordat het geteld wordt, standaard = 0.7.

    Uitvoer
    ----------
    df_re: Dataframe.

    Formaat: Bevat 9 + 2 nieuwe kolommen 'Rel exp' en 'Punten'.

    Uitvoer: Retourneert een dataframe met een nieuwe kolom voor de relatieve
    expressiewaarde per spot en een nieuwe kolom met een vooraf bepaalde
    puntenwaarde.

    Regel: Geprinte tekstregel.

    Formaat: 'Het aantal genen boven of gelijk aan de absolute waarde van '
    + parameter waarde + ' op ' + parameter wanneer + ' is ' + aantal spots
    met een relatieve expressiewaarde boven vastgestelde waarde'.
    """
    # Maak een kopie zodat je de ingevoerde dataframe niet veranderd.
    df_re = df.copy()

    # Condities definieren.
    condities = [(df_re[con1]/df_re[con2] >= 1),
                 (df_re[con1]/df_re[con2] < 1)]

    # Keuzes definieren.
    keuzes = [(df_re[con1]/df_re[con2])-1, (-df_re[con2]/df_re[con1])+1]

    # Relatieve expressiewaarde in de dataframe voegen gebaseerd
    # op de condities en keuzes.
    df_re['Rel exp'] = np.select(condities, keuzes)

    # Nieuwe condities definieren.
    condities = [(df_re['Klasse'] == 'a'),
                 (df_re['Klasse'] == 'b'),
                 (df_re['Klasse'] == 'c'),
                 (df_re['Klasse'] == 'd')]

    # Puntenwaardes in de dataframe voegen gebaseerd op de condities en keuzes.
    df_re['Punten'] = np.select(condities, punten)

    # Maak een nieuwe dataframe met de absolute waarde
    # van de relatieve expressiewaarden.
    hoeveel = df_re['Rel exp'].abs()
    hoeveel = hoeveel[~ (hoeveel < waarde)]
    hoeveel = hoeveel.shape[0]

    # print out hoeveel absolute relatieve expressiewaarden
    # groter of gelijk zijn aan de gekozen waarde.
    print('Het aantal genen boven of gelijk aan de absolute waarde van ' +
          str(waarde) + ' op ' + wanneer + ' is ' + str(hoeveel), '\n')

    return df_re


def Functies_aanroepen(df, data_bestand, punten, ongefilterd, spotfilt=True):
    """Functie past ruwe dataframe aan m.b.v. eerder gedefineerde functies.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.
    filt: Zorgt ervoor dat de filter functie uit of aan staat.
    Standaard staat deze aan.

    Uitvoer
    ----------
    Scatterplot visualisaties van de relaties tussen P1Sig en P2Sig; een
    histogram van de relatieve expressie waardes van verschillende genen;

    Retourneert een dataframe met een aangepaste P2Sig kolom, met een nieuwe
    kolom voor de logaritmische waarde van beide P1Sig en P2Sig, voor de
    relatieve expressiewaarde per spot en een nieuwe kolom met een vooraf
    bepaalde puntenwaarde.
    """
    # Roep functie aan om het onbewerkte dataframe te plotten.
    Uitplotten(df, data_bestand)

    # Maak een kopie van de dataframe en voeg 2 nieuwe kolommen toe
    df_bewerkt = df.copy()
    df_bewerkt['log P1Sig'] = np.log(df_bewerkt[['P1Sig']])
    df_bewerkt['log P2Sig'] = np.log(df_bewerkt[['P2Sig']])

    # Nieuwe plot maken gebruik makend van de 2 nieuwe kolommen
    Uitplotten(df_bewerkt, data_bestand,
               wanneer='na de logaritmische correctie.',
               x='log P1Sig', y='log P2Sig')

    # Verander de P2Sig waardes door het te vermenigvuldigen
    # met de ratio tussen P1Sig en P2Sig
    S1 = df_bewerkt['P1Sig'].sum()
    S2 = df_bewerkt['P2Sig'].sum()
    df_bewerkt['P2Sig'] = df_bewerkt['P2Sig'] * (S1/S2)

    # Herdefinieer 'log PsSig' met de gecallibreerde P2Sig waardes
    df_bewerkt['log P2Sig'] = np.log(df_bewerkt[['P2Sig']])

    # Maak een nieuwe plot met de correcte log P2Sig kolom
    Uitplotten(df_bewerkt, data_bestand=data_bestand,
               wanneer='na de S1/S2 correctie.',
               x='log P1Sig', y='log P2Sig',
               kleurp='black', kleurd='orange', lijnstijl='-.')

    # Roep een functie op die de verschillende spots een klasse toewijst.
    df_ingedeeld = Indeling(df_bewerkt)

    #  Conditie checken voor ongefilterd als False en spotfilt als True ,
    #  als dit zo is de functie van het filteren op spotgrootte oproepen.
    if not ongefilterd and spotfilt:
        df_ingedeeld = Spotfilter(df_ingedeeld)

    # Maak een nieuwe plot met de verschillende klasses van de spots.
    Uitplotten(df_ingedeeld, data_bestand, klassen=True,
               x='log P1Sig', y='log P2Sig')

    # Roep een functie aan om de relatieve expressiewaarden aan
    # de dataframe toe te voegen.
    df_relatief = Rel_expressie_punten(df_ingedeeld, data_bestand, punten)

    # Roep een functie aan die de relatieve expressie uit plot.
    hist_uitplotten(df_relatief, wanneer=data_bestand)

    return df_relatief


def Punten_samenvoegen(df):
    """Functie voegt punten die de genen van alle dagen hebben gehad samen \
    en verwijderd GenID's als deze boven een bepaalde grens liggen.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.

    Uitvoer
    ----------
    Een dataframe met alleen de relatieve expressie waardes van de GenIds die
    niet verwijderd zijn.
    """
    # Kolommen selecteren die beginnen met 'Punten' in de rel_samen dataframe
    som_kolom = df.filter(regex='^Punten', axis=1)

    # Kolommen aanmaken voor de som van de columns van 'sum_column'
    df['Totaalpunten'] = som_kolom.sum(axis=1)

    # Kolommen verwijderen van aantallen punten per dag
    df = df.drop(som_kolom, axis=1)

    # Gen ids verwijderen met een hogere 'totaal score' van 1 per dag
    df.drop(df[df['Totaalpunten'] > 1].index, inplace=True)

    # Kolom met de totaal score verwijderen.
    df.drop(['Totaalpunten'], axis=1, inplace=True)

    return df


def Rel_expressie_filter(df, rgrens):
    """Functie verwijdert GenID's die voor alle dagen geen enkele rel \
    expressiewaarde boven de rgrens bevat.

    Parameters
    ----------
    df: Dataframe die bewerkt moet worden.
    rgrens: De relatieve expressiegrens waarmee vergeleken wordt.

    Uitvoer
    ----------
    Een dataframe met alleen de relatieve expressie waardes van de GenIds die
    niet verwijderd zijn.
    df: Dataframe.

    Formaat: Bevat onveranderde hoeveelheid van 8 kolommen.

    Uitvoer: Retourneert een dataframe waarin GenID's zonder een relatieve
    expressiewaarde boven de rgrens zijn verwijderd.
    """
    # Kolom aanmaken voor de hoogste absolute waarde voor elk GenID.
    df['Max_rel_exp'] = df.abs().max(axis=1)

    # GenID's verwijderen waar de hoogste absolute waarde niet hoger dan
    # de rgrens is.
    df.drop(df[df['Max_rel_exp'] < rgrens].index, inplace=True)

    # Kolom verwijderen voor de hoogste absolute waarde
    df.drop(['Max_rel_exp'], axis=1, inplace=True)

    return df
