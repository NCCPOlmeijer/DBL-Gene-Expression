# -*- coding: utf-8 -*-
"""
Created on Fri Jun 4 2021.

@author: NoahOlmeijer/20203063
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import preprocessing
import pandas as pd
import os


class Genexpressie:
    """Applicatie die de OGO Genexpressie fases/programma's uitvoert."""

    def __init__(self, parent):

        parent.title("OGO - Genexpressie - Groep 7 - 2020/2021")
        parent.geometry("510x310")
        parent.configure(background="white")

        self.create_tabs()
        self.Tab_labels()
        self.Preprocessing_widgets()

    def create_tabs(self):
        """Functie maakt tabbladen aan."""
        self.tabControl = ttk.Notebook(root)

        self.Preprocessing = ttk.Frame(self.tabControl)
        self.Clustering = ttk.Frame(self.tabControl)
        self.Interpretatie = ttk.Frame(self.tabControl)

        self.tabControl.add(self.Preprocessing, text='Preprocessing')
        self.tabControl.add(self.Clustering, text='Clustering')
        self.tabControl.add(self.Interpretatie, text='Interpretatie')

        self.tabControl.pack(expand=True, fill="both", side="top")

    def Tab_labels(self):
        """Functie maakt tabblad labels aan."""
        self.paddings = {'padx': (120, 0), 'pady': (10, 10)}

        ttk.Label(self.Preprocessing,
                  text='Schakel de filters aan/uit en stel de R-Grens in:') \
            .grid(column=0, row=0, **self.paddings, sticky='W')
        ttk.Label(self.Clustering, text='Clusterfase interface').grid(
            column=0, row=0, **self.paddings)
        ttk.Label(self.Interpretatie, text='Interpretatiefase interface').grid(
            column=0, row=0, **self.paddings)

        ttk.Button(self.Preprocessing, text='Verwerk data', width=20,
                   command=self.Preprocessing_fase).grid(
                       column=0, row=6, padx=(30, 10), pady=(0, 5), sticky='W')

    def Preprocessing_widgets(self):
        """Functie maakt widgets en labels aan."""
        self.padx = {'padx': (120, 0)}

        self.label1 = ttk.Label(self.Preprocessing, text='CloneID-Filter:')
        self.label1.grid(row=1, **self.padx, pady=10, sticky='W')
        self.combobox1 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox1.current(0)
        self.combobox1.grid(column=0, row=1, padx=230, sticky='W')

        self.label2 = ttk.Label(self.Preprocessing, text='Spot-Filter:')
        self.label2.grid(row=2, **self.padx, pady=10, sticky='W')
        self.combobox2 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox2.current(0)
        self.combobox2.grid(column=0, row=2, padx=230, sticky='W')

        self.label3 = ttk.Label(self.Preprocessing, text='Expressie-Filter:')
        self.label3.grid(row=3, **self.padx, pady=10, sticky='W')
        self.combobox3 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox3.current(0)
        self.combobox3.grid(column=0, row=3, padx=230, sticky='W')

        self.label4 = ttk.Label(self.Preprocessing, text='R-Grens:')
        self.label4.grid(row=4, **self.padx, pady=10, sticky='W')
        self.v = tk.StringVar(value=0.7)
        self.entry1 = ttk.Entry(self.Preprocessing, textvar=self.v, width=23)
        self.entry1.grid(column=0, row=4, padx=230, sticky='W')
        self.answer = ttk.Label(self.Preprocessing, text='')
        self.answer.grid(column=0, row=5, padx=(180, 0), pady=10, sticky='W')

        self.progressbar = ttk.Progressbar(self.Preprocessing, length=300)
        self.progressbar.grid(column=0, row=6, padx=180,
                              pady=(0, 5), sticky='W')

    def Preprocessing_fase(self):
        """Functie voert preprocessing programma uit."""
        # Pad naar de tekstbestanden, moet aangepast worden
        # als tekstbestanden verplaatst zijn.
        path_bestanden = "Data\\"
        path_bestanden_gedaan = "Data_out\\"

        bestanden = []

        # Ophalen van dagen uit bestandsnamen die beginnen met 'dag'.
        for file in os.listdir(path_bestanden):
            if file.startswith("dag"):
                bestanden.append(int(file.strip(".txt").strip("dag")))

        # sorteren van namen en opslaan in 'bestanden'
        bestanden = ['dag' + str(naam) for naam in sorted(bestanden)]

        if self.combobox1.get() == 'Aan':
            ongefilterd = False
        elif self.combobox1.get() == 'Uit':
            ongefilterd = True

        if self.combobox2.get() == 'Aan':
            spotfilt = True
        elif self.combobox2.get() == 'Uit':
            spotfilt = False

        if self.combobox3.get() == 'Aan':
            relfilt = True
        elif self.combobox3.get() == 'Uit':
            relfilt = False

        # Hoeveelheid punten voor respectievelijk a,b,c,d
        punten = [0, 1, 1, 5]

        try:
            float(self.entry1.get())
            self.answer.config(text='Processing...' + ' '*45)
            rgrens = float(self.entry1.get())

        except ValueError:
            self.answer.config(text='Ingevoerde R-Grens is geen nummer!')
            return

        # Maak een dataframe voor de uiteindenlijke waarde om naar
        # een tekstbestand geschreven te worden.
        df_rel_samen = pd.DataFrame()

        # Definieer het pad waarnaar het eindproduct geschreven moet worden.
        eind_resultaat = path_bestanden_gedaan \
            + "Relatieve expressiewaarden.txt"

        """Aanroepen functies"""

        # Een for-loop over al de tekstbestanden genoemd in het 'data'
        # tekstbestand die de hoofdacties op de data uit
        # deze bestanden uitvoert.
        for data_bestand in bestanden:

            # Definieer het pad van het huidige data bestand
            huidig_bestand = path_bestanden + data_bestand + ".txt"

            # Open het huidige databestand als dataframe
            dataframe = pd.read_csv(huidig_bestand, sep="\t", header=0)
            df_onbewerkt = dataframe.set_index('CloneID').copy()

            # Roept de hoofd functie op die de dataframe aanpast en de
            # andere functies erop laat werken.
            df_een_dag = preprocessing.Functies_aanroepen(
                df_onbewerkt, data_bestand, punten, ongefilterd, spotfilt)

            # Voeg de relatieve expressiewaarde toe en Conditie checken
            # voor ongefilterd als False voegt dan punten toe aan
            # een centraal dataframe.
            df_rel_samen['Rel exp' + ' ' +
                         data_bestand] = df_een_dag['Rel exp']
            if not ongefilterd:
                df_rel_samen['Punten' + ' ' +
                             data_bestand] = df_een_dag['Punten']

            """Dit volgende onderdeel is overbodig voor het eind programma."""

            # Definieer het pad waarnaar het huidige bewerkte dataframe
            # moet worden geschreven.
            file_uit = path_bestanden_gedaan + data_bestand + "_gedaan.txt"

            # Schrijf het dataframe naar een tekstbestand.
            df_een_dag.to_csv(path_or_buf=file_uit, sep='\t',
                              index=True, header=True)

            """Hier eindigt het overbodige onderdeel."""

            self.progressbar['value'] += 100/(len(bestanden)+1)
            root.update_idletasks()

        df_rel_eind = df_rel_samen

        # Conditie checken voor ongefilterd als False, roept dan de functie aan
        # om alle Relatieve expressiewaarden samen te voegen in 1 kolom.
        if not ongefilterd:
            df_rel_eind = preprocessing.Punten_samenvoegen(df_rel_samen)

        # Conditie checken voor ongefilterd als False en relfilt als True,
        # roept dan de functie aan om te filteren
        # op Relatieve expressiewaarden.
        if not ongefilterd and relfilt:
            df_rel_eind = preprocessing.Rel_expressie_filter(
                df_rel_eind, rgrens)

        # Verwijder GenID's die een NaN/NaT waarde hebben voor een kolom
        df_rel_eind = df_rel_eind.dropna()

        # Alle waardes in Dataframe afronden op 4 decimalen
        df_rel_eind = df_rel_eind.round(4)

        # Schrijf het eindproduct uit naar een textbestand.
        df_rel_eind.to_csv(path_or_buf=eind_resultaat,
                           sep='\t', index=True, header=False)

        self.progressbar['value'] += 100/(len(bestanden)+1)
        root.update_idletasks()

        messagebox.showinfo('Melding', 'Data is verwerkt!')
        self.progressbar['value'] = 0

        self.answer.config(text='')


root = tk.Tk()
App = Genexpressie(root)
root.mainloop()
root.mainloop()
