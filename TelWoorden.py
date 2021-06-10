# -*- coding: utf-8 -*-
"""
Created on Thu April 22 2021.

@author: NoahOlmeijer/20203063
"""


def TelWoorden(gen_beschrijving):
    """Programma maakt een dictionary aan met de frequentie van beschrijvingen.

    Parameters
    ----------
    gen_beschrijving : textfile
        Bevat per cloneID een tekstuele beschrijving van het
        (meest waarschijnlijke) bijbehorende gen.

    Uitvoer
    -------
    woord_freq: dictionary

    beschrijving: Een dictionary met alle woorden uit
    de beschrijvingen van het invoerbestand
    en de daarbijhorende woordfrequentie.
    """
    # inlezen van invoerbestand en rauwe data uit het invoerbestand
    # toewijzen aan variable 'gen_beschrijving'.
    with open(gen_beschrijving) as gen_beschrijving:
        gen_beschrijving = gen_beschrijving.readlines()[1::3]
        gen_beschrijving = [line.strip() for line in gen_beschrijving]

    # lijst aanmaken genaamd 'items' van alle losse woorden en integers
    # uit 'gen_beschrijving' zonder leestekens: '\x01', ',', '(', ')', '/'.
    items = ' '.join(gen_beschrijving).replace('\x01', ' ')

    for character in [',', '(', ')', '/', '[', ']', '"']:
        if character in items:
            items = items.replace(character, ' ')
    items = items.split()

    # lijst filteren op integers en '-'
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

    # sorteer dictionary 'woord_freq' op frequentie van laag naar hoog.
    woord_freq = {keys: values for keys, values in sorted(
        woord_freq.items(), key=lambda item: item[1], reverse=True)}

    item_lijst = list(woord_freq.items())

    with open('Data_out/Woord_frequentie.txt', 'w') as txt:
        for item in item_lijst:
            print('> ' + str(item[0]) + ': ' + str(item[1]))
            txt.write('> ' + str(item[0]) + ': ' + str(item[1]) + '\n')
