# -*- coding: utf-8 -*-
"""
Created on Fri Jun 4 2021.

@author: NoahOlmeijer/20203063
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os

import preprocessing
import expressie_clusters
import expressie_families
import Familie_Barchart
import cluster_frequentie


class Genexpressie:
    """Applicatie die de OGO Genexpressie fases/programma's uitvoert."""

    def __init__(self, parent):

        parent.title("OGO - Genexpressie - Groep 7 - 2020/2021")
        parent.geometry("510x310")
        parent.configure(background="white")

        self.Create_tabs()
        self.Tab_labels()
        self.Preprocessing_widgets()
        self.Interpretatie_widgets()

    def Create_tabs(self):
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
            column=0, row=0, **self.paddings, sticky='W')
        ttk.Label(self.Interpretatie,
                  text="Selecteer de relevante interpretatie programma's:") \
            .grid(column=0, row=0, **self.paddings, sticky='W')

        ttk.Button(self.Preprocessing, text='Verwerk data', width=20,
                   command=self.Preprocessing_fase).grid(
                       column=0, row=6, padx=(30, 10), pady=(0, 5), sticky='W')

    def Preprocessing_widgets(self):
        """Functie maakt widgets en labels aan."""
        self.padx = {'padx': (120, 0)}

        self.label_pp1 = ttk.Label(self.Preprocessing, text='CloneID-Filter:')
        self.label_pp1.grid(row=1, **self.padx, pady=10, sticky='W')
        self.combobox_pp1 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox_pp1.current(0)
        self.combobox_pp1.grid(column=0, row=1, padx=230, sticky='W')

        self.label_pp2 = ttk.Label(self.Preprocessing, text='Spot-Filter:')
        self.label_pp2.grid(row=2, **self.padx, pady=10, sticky='W')
        self.combobox_pp2 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox_pp2.current(0)
        self.combobox_pp2.grid(column=0, row=2, padx=230, sticky='W')

        self.label_pp3 = ttk.Label(
            self.Preprocessing, text='Expressie-Filter:')
        self.label_pp3.grid(row=3, **self.padx, pady=10, sticky='W')
        self.combobox_pp3 = ttk.Combobox(
            self.Preprocessing, values=('Aan', 'Uit'))
        self.combobox_pp3.current(0)
        self.combobox_pp3.grid(column=0, row=3, padx=230, sticky='W')

        self.label_pp4 = ttk.Label(self.Preprocessing, text='R-Grens:')
        self.label_pp4.grid(row=4, **self.padx, pady=10, sticky='W')
        self.v = tk.StringVar(value=0.7)
        self.entry_pp1 = ttk.Entry(
            self.Preprocessing, textvar=self.v, width=23)
        self.entry_pp1.grid(column=0, row=4, padx=230, sticky='W')
        self.answer = ttk.Label(self.Preprocessing, text='')
        self.answer.grid(column=0, row=5, padx=(180, 0), pady=10, sticky='W')

        self.progressbar_pp = ttk.Progressbar(self.Preprocessing, length=300)
        self.progressbar_pp.grid(column=0, row=6, padx=180,
                                 pady=(0, 5), sticky='W')

    def Preprocessing_fase(self):
        """Functie voert preprocessing programma uit."""
        self.answer.config(text='Processing...' + ' '*45)
        root.update_idletasks()

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

        if self.combobox_pp1.get() == 'Aan':
            ongefilterd = False
        elif self.combobox_pp1.get() == 'Uit':
            ongefilterd = True

        if self.combobox_pp2.get() == 'Aan':
            spotfilt = True
        elif self.combobox_pp2.get() == 'Uit':
            spotfilt = False

        if self.combobox_pp3.get() == 'Aan':
            relfilt = True
        elif self.combobox_pp3.get() == 'Uit':
            relfilt = False

        # Hoeveelheid punten voor respectievelijk a,b,c,d
        punten = [0, 1, 1, 5]

        try:
            float(self.entry_pp1.get())
            rgrens = float(self.entry_pp1.get())

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

            self.progressbar_pp['value'] += 100/(len(bestanden)+1)
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

        self.progressbar_pp['value'] += 100/(len(bestanden)+1)
        root.update_idletasks()

        messagebox.showinfo('Melding', 'Data is verwerkt!')
        self.progressbar_pp['value'] = 0

        self.answer.config(text='')

    def Interpretatie_widgets(self):
        """Functie maakt widgets en labels aan."""
        self.Frame_plots = ttk.Frame(self.Interpretatie)
        self.Frame_plots.grid(sticky='W', padx=(90, 0))
        self.Frame_plot_label = ttk.Label(
            self.Frame_plots, text="Plot programma's:")
        self.Frame_plot_label.grid(sticky='W')

        self.chk_var_ip1 = tk.IntVar(value=0)
        self.chk_ip1 = ttk.Checkbutton(
            self.Frame_plots, var=self.chk_var_ip1, text='Cluster exPlots')
        self.chk_ip1.grid(sticky='W')

        self.chk_var_ip2 = tk.IntVar(value=0)
        self.chk_ip2 = ttk.Checkbutton(
            self.Frame_plots, var=self.chk_var_ip2, text='Familie exPlots')
        self.chk_ip2.grid(sticky='W')

        self.chk_var_ip3 = tk.IntVar(value=0)
        self.chk_ip3 = ttk.Checkbutton(
            self.Frame_plots, var=self.chk_var_ip3, text='Familie barPlot')
        self.chk_ip3.grid(sticky='W')

        self.Frame_txt = ttk.Frame(self.Interpretatie)
        self.Frame_txt.grid(sticky='N', padx=(140, 0), row=1, column=0)
        self.Frame_plot_label1 = ttk.Label(
            self.Frame_txt, text="Woord programma's + Vrije analyse:")
        self.Frame_plot_label1.grid(sticky='W')

        self.chk_var_ip4 = tk.IntVar(value=0)
        self.chk_ip4 = ttk.Checkbutton(
            self.Frame_txt, var=self.chk_var_ip4, text='TelWoorden')
        self.chk_ip4.grid(sticky='W')

        self.chk_var_ip5 = tk.IntVar(value=0)
        self.chk_ip5 = ttk.Checkbutton(
            self.Frame_txt, var=self.chk_var_ip5, text='ClusterFrequentie')
        self.chk_ip5.grid(sticky='W')

        self.chk_var_ip6 = tk.IntVar(value=0)
        self.chk_ip6 = ttk.Checkbutton(
            self.Frame_txt, var=self.chk_var_ip6, text='Vrije analyse')
        self.chk_ip6.grid(sticky='W')

        self.Frame_btn = ttk.Frame(self.Interpretatie)
        self.Frame_btn.grid(sticky='W', padx=(110, 0))

        self.status_ip = ttk.Label(self.Frame_btn, text='')
        self.status_ip.grid(sticky='W', padx=(70, 0), pady=(93, 0))

        self.progressbar_ip = ttk.Progressbar(self.Frame_btn,
                                              length=300)
        self.progressbar_ip.grid(column=0, row=2, padx=(
            70, 0), pady=(0, 0), sticky='W')

        ttk.Button(self.Interpretatie, text='Genereer bestanden', width=20,
                   command=self.Expressie_cluster_plot).grid(
                       column=0, row=2,
                       padx=(30, 10), pady=(113, 0), sticky='W')

    def Expressie_cluster_plot(self):

        cluster_invoer = "Data_out/Relatieve expressiewaarden.txt"
        cluster_uitvoer = "Data_out/cluster_uitvoer.txt"
        familie_cloneID = "Data/CloneIdFamily.txt"
        gen_beschrijving = "Data/GenDescription.txt"

        self.status_ip.config(text='Processing...')
        root.update_idletasks()

        k = 5
        inc = 100/(k*self.chk_var_ip1.get()
                   + 26 * self.chk_var_ip2.get()
                   + self.chk_var_ip3.get()
                   + 2 * self.chk_var_ip5.get())

        if self.chk_var_ip1.get() == 1:
            # aanroepen van functie expressie() voor alle 6 clusters.
            cloneID_dict, cluster_invoer_data = expressie_clusters.expressie(
                cluster_invoer, cluster_uitvoer)
            for cluster in range(1, k+1):
                expressie_clusters.Plot_clusters(cloneID_dict,
                                                 cluster_invoer_data,
                                                 cluster)
                self.progressbar_ip['value'] += inc
                root.update_idletasks()

        if self.chk_var_ip2.get() == 1:
            # aanroepen van functie expressie() voor alle 26 families.
            cloneID_dict, cluster_invoer_data = expressie_families.expressie(
                cluster_invoer, familie_cloneID)
            for familie in range(1, 27):
                expressie_families.Plot_families(cloneID_dict,
                                                 cluster_invoer_data,
                                                 familie)
                self.progressbar_ip['value'] += inc
                root.update_idletasks()

        if self.chk_var_ip3.get() == 1:
            Familie_Barchart.Histogram(cluster_uitvoer, familie_cloneID, k)
            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        if self.chk_var_ip5.get() == 1:
            cluster_freq = cluster_frequentie.cluster_frequentie(
                gen_beschrijving, cluster_uitvoer)

            self.progressbar_ip['value'] += inc
            root.update_idletasks()
            cluster_frequentie.frequency_filter(cluster_freq, k)

            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        messagebox.showinfo('Melding', 'Bestanden zijn gegenereerd!')
        self.progressbar_ip['value'] = 0
        self.status_ip.config(text='')
        root.update_idletasks()


root = tk.Tk()
App = Genexpressie(root)
root.mainloop()
