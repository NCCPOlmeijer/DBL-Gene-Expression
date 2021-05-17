# -*- coding: utf-8 -*-
"""
Created on Thu April 22 2021.

@author: NoahOlmeijer/20203063
"""

GenDescription = 'Data/GenDescription.txt'


def TelWoorden(bestandsnaam):
    """Programma maakt een dictionary aan met de frequentie van beschrijvingen.

    Parameters
    ----------
    bestandsnaam : textfile
        Bevat per cloneID een tekstuele beschrijving van het
        (meest waarschijnlijke) bijbehorende gen.

    Uitvoer
    -------
    woord_freq: dictionary

    beschrijving: Een dictionary met alle woorden uit
    de beschrijvingen van het invoerbestand
    en de daarbijhorende woordfrequentie.
    """
    # inlezen van invoerbestand en
    # rauwe data uit invoerbestand toewijzen aan variable 'data'.
    with open(bestandsnaam) as tekst_bestand:
        data = tekst_bestand.readlines()

    # lijst aanmaken genaamd 'items' van alle losse woorden en integers
    # uit 'data' zonder leestekens: '\x01', ',', '(', ')', '/'.
    items = ' '.join([line.strip().lower() for line
                      in data[1::3]]).replace('\x01', '')

    for character in [',', '(', ')', '/', '[', ']']:
        if character in items:
            items = items.replace(character, ' ')
    items = items.split()

    # lijst aanmaken genaamd 'geen_integers' met uitsluitend
    # woorden uit beschrijvingen.
    geen_integers = [woord for woord in items if not (
        woord.isdigit() or woord[0] == '-' and woord[1:].isdigit())]

    # lege dictionary aanmaken genaamd 'woord_freq'.
    woord_freq = {}

    # per woord uit 'geen_integers' de frequentie bepalen
    # en toevoegen aan 'woord_freq'.
    for woord in geen_integers:
        if woord not in woord_freq:
            woord_freq[woord] = 1
        else:
            woord_freq[woord] += 1

    # sorteer dictionary 'woord_freq' op frequentie van laag naar hoog.
    woord_freq = {keys: values for keys, values in sorted(
        woord_freq.items(), key=lambda item: item[1])}

    return woord_freq


if __name__ == "__main__":
    print(TelWoorden(GenDescription))
