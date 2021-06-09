# -*- coding: utf-8 -*-
"""
Created on Fri Jun 4 2021.

@author: NoahOlmeijer/20203063
"""

# importeren van libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os

# importeren programma's
import preprocessing
import expressie_clusters
import expressie_families
import Familie_Barchart
import cluster_frequentie
import TelWoorden
import eigen_clustering
import vrije_analyse
import k_means


class Genexpressie:
    """Applicatie die de OGO Genexpressie fases/programma's kan uitvoeren."""

    def __init__(self, parent):

        # initialiseer GUI.
        parent.title("OGO - Genexpressie - Groep 7 - 2020/2021")
        parent.geometry("510x310")
        parent.minsize(510, 310)
        parent.maxsize(510, 310)

        # uitvoeren van tabblad -en widget functies.
        self.Create_tabs()
        self.Tab_labels()
        self.Preprocessing_widgets()
        self.Clustering_widgets()
        self.Interpretatie_widgets()
        self.Groep_widgets()

        # lees step variable uit 'step.txt'.
        # step waarde houd de uitvoering van de fases bij in var: self.step
        with open('step.txt', 'r') as self.fase:
            self.step = int(self.fase.read())

    def Create_tabs(self):
        """Functie maakt tabbladen aan."""
        self.tabControl = ttk.Notebook(root)

        # aanmaken van frames.
        self.Preprocessing = ttk.Frame(self.tabControl)
        self.Clustering = ttk.Frame(self.tabControl)
        self.Interpretatie = ttk.Frame(self.tabControl)
        self.Groep = ttk.Frame(self.tabControl)

        # tabbladen aanmaken van frames.
        self.tabControl.add(self.Preprocessing, text='Preprocessing')
        self.tabControl.add(self.Clustering, text='Clustering')
        self.tabControl.add(self.Interpretatie, text='Interpretatie')
        self.tabControl.add(self.Groep, text='Groep 7')

        self.tabControl.pack(expand=True, fill="both", side="top")

    def Tab_labels(self):
        """Functie maakt tabblad labels aan."""
        # **self.paddings variable aanmaken.
        self.paddings = {'padx': (120, 0), 'pady': (10, 10)}

        # toevoegen van labels in elk tabblad.
        ttk.Label(self.Preprocessing,
                  text='Schakel de filters aan of uit en stel de R-Grens in:')\
            .grid(column=0, row=0, **self.paddings, sticky='W')
        ttk.Label(self.Clustering,
                  text='Selecteer de clustermethode en k-aantal clusters:')\
            .grid(column=0, row=0, **self.paddings, sticky='W')
        ttk.Label(self.Interpretatie,
                  text="Selecteer de relevante interpretatie programma's:")\
            .grid(column=0, row=0, **self.paddings, sticky='W')

    def Preprocessing_widgets(self):
        """Functie maakt widgets en labels aan."""
        # **self.padx variable aanmaken.
        self.padx = {'padx': (120, 0)}

        # aanmaken van parameter veld widgets en labels.
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
        self.answer.grid(column=0, row=5, padx=(
            180, 0), pady=(20, 0), sticky='W')

        # aanmaken van de preprocessing verwerk knop.
        ttk.Button(self.Preprocessing, text='Verwerk data', width=20,
                   command=self.Preprocessing_fase).grid(
                       column=0, row=6,
                       padx=(30, 10), pady=(12, 0), sticky='W')

        # aanmaken van de preprocessing progress bar.
        self.progressbar_pp = ttk.Progressbar(self.Preprocessing, length=300)
        self.progressbar_pp.grid(column=0, row=6, padx=180,
                                 pady=(12, 0), sticky='W')

    def Preprocessing_fase(self):
        """Functie voert preprocessing programma uit."""
        # instellen van paths voor data invoer en uitvoer bestanden.
        path_bestanden = "Data\\"
        path_bestanden_gedaan = "Data_out\\"

        bestanden = []

        # Ophalen van dagen uit bestandsnamen die beginnen met 'dag'.
        for file in os.listdir(path_bestanden):
            if file.startswith("dag"):
                bestanden.append(int(file.strip(".txt").strip("dag")))

        # sorteren van namen en opslaan in 'bestanden'
        bestanden = ['dag' + str(naam) for naam in sorted(bestanden)]

        # functie parameters aanpassen a.h.v. de invoer parameters.
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

        # Hoeveelheid punten voor respectievelijk a, b, c en d.
        punten = [0, 1, 1, 5]

        # proberen omzetten van rgrens-string in float.
        try:
            float(self.entry_pp1.get())
            rgrens = float(self.entry_pp1.get())

        # retourneer een errorbericht wanneer dit een ValueError oplevert.
        except ValueError:
            self.answer.config(text='Ingevoerde R-Grens is geen nummer!')
            return

        # checken of het ingevoerde getal kleiner of gelijk is aan 0.
        if rgrens <= 0:
            # retourneer errorbericht als dit het geval is.
            self.answer.config(text='Ingevoerde R-Grens is ≤ 0')
            return

        # aanpassen van label naar 'Processing...'
        self.answer.config(text='Processing...' + ' '*45)
        root.update_idletasks()

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

            # update progressbar per iteratie.
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

        # laatste update progressbar.
        self.progressbar_pp['value'] += 100/(len(bestanden)+1)
        root.update_idletasks()

        # melding weergeven dat de data is verwerkt.
        messagebox.showinfo('Melding', 'Data is verwerkt!')
        self.progressbar_pp['value'] = 0

        # reset status label preprocessing.
        self.answer.config(text='')

        # step updaten en schrijven naar 'step.txt'.
        self.step = 1
        with open('step.txt', 'w') as self.fase:
            self.fase.write(str(self.step))

    def Clustering_widgets(self):
        """Functie maakt widgets en labels aan."""
        # aanmaken van parameter veld widgets en labels.
        self.Frame_clust_label1 = ttk.Label(
            self.Clustering, text="Cluster methode:")
        self.Frame_clust_label1.grid(sticky='W', padx=(120, 0))

        self.combobox_cl1 = ttk.Combobox(
            self.Clustering, values=('Eigen-Algoritme', 'K-Means'))
        self.combobox_cl1.current(0)
        self.combobox_cl1.grid(column=0, row=1, padx=230, sticky='W')

        self.Frame_clust_label2 = ttk.Label(
            self.Clustering, text="K-aantal Clusters:")
        self.Frame_clust_label2.grid(sticky='W', padx=(120, 0), pady=(0, 120))

        self.spin_var = tk.IntVar()
        self.spin_var.set(5)

        self.spinbox_cl1 = ttk.Spinbox(
            self.Clustering, from_=2, to=100, width=10,
            textvariable=self.spin_var)
        self.spinbox_cl1.grid(column=0, row=2, padx=230,
                              sticky='W', pady=(0, 120))

        # aanmaken van de clustering knop.
        ttk.Button(self.Clustering, text='Cluster data', width=20,
                   command=self.Clustering_methode).grid(
                       column=0, row=2,
                       padx=(30, 10), pady=(186, 0), sticky='W')

        # aanmaken van de clustering progress bar.
        self.progressbar_cl = ttk.Progressbar(self.Clustering,
                                              length=300)
        self.progressbar_cl.grid(column=0, row=2, padx=(
            180, 0), pady=(186, 0), sticky='W')

        self.status_cl = ttk.Label(self.Clustering, text='')
        self.status_cl.grid(sticky='W', padx=(180, 0), pady=(120, 0), row=2)

    def Clustering_methode(self):
        """Functie roept clustering methode aan."""
        cluster_invoer = "Data_out/Relatieve expressiewaarden.txt"
        # uitlezen van parameter velden.
        k = int(self.spinbox_cl1.get())
        dimensie = 8

        # check of step == 0
        if self.step == 0:
            # weergeef error message als dit True is.
            messagebox.showinfo('Warning', 'Verwerk eerst de data!')
            return

        # voer het clusterprogramma uit op basis van de combobox invoer.
        if self.combobox_cl1.get() == 'Eigen-Algoritme':

            self.status_cl.config(text='Clustering...')
            root.update_idletasks()

            eigen_clustering.formaat_omzetten(
                eigen_clustering.clusterproces(dimensie, cluster_invoer, k))

            self.progressbar_cl['value'] += 100
            root.update_idletasks()

            messagebox.showinfo('Melding', 'Data is geclusterd!')
            self.progressbar_cl['value'] = 0

            self.status_cl.config(text='')
            root.update_idletasks()

            # step updaten en schrijven naar 'step.txt'.
            self.step = 2
            with open('step.txt', 'w') as self.fase:
                self.fase.write(str(self.step))

        elif self.combobox_cl1.get() == 'K-Means':

            self.progressbar_cl['value'] += 100
            root.update_idletasks()

            optimaliseren_k_means = k_means.optimaliseren(
                cluster_invoer, k, dimensie)
            cluster_uitvoer = k_means.formaat_omzetten(optimaliseren_k_means)

            # Wegschrijven naar een tekstbestand met de CloneID's
            # en de clusternummers
            with open("Data_out/cluster_uitvoer.txt", "w") as txt:
                txt.write(cluster_uitvoer)

            self.progressbar_cl['value'] += 100
            root.update_idletasks()

            messagebox.showinfo('Melding', 'Data is geclusterd!')
            self.progressbar_cl['value'] = 0

            self.status_cl.config(text='')
            root.update_idletasks()

            # step updaten en schrijven naar 'step.txt'.
            self.step = 2
            with open('step.txt', 'w') as self.fase:
                self.fase.write(str(self.step))

    def Interpretatie_widgets(self):
        """Functie maakt widgets en labels aan."""
        # aanmaken van parameter veld widgets en labels.
        self.Frame_plots = ttk.Frame(self.Interpretatie)
        self.Frame_plots.grid(sticky='N', padx=(0, 210), row=1, column=0)
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

        self.Frame_va = ttk.Frame(self.Interpretatie)
        self.Frame_va.grid(sticky='N', padx=(0, 230),
                           pady=(100, 0), row=1, column=0)

        self.label_ip6 = ttk.Label(self.Frame_va, text='Vrije analyse:')
        self.label_ip6.grid(sticky='W')

        self.chk_var_ip6 = tk.IntVar(value=0)
        self.chk_ip6 = ttk.Checkbutton(
            self.Frame_va, var=self.chk_var_ip6, text='Entrez SE')
        self.chk_ip6.grid(sticky='W')

        self.label_ip7 = ttk.Label(self.Frame_va, text='Cluster:')
        self.label_ip7.grid(sticky='W')

        self.spin_var2 = tk.IntVar()
        self.spin_var2.set(1)

        self.spinbox_ip1 = ttk.Spinbox(
            self.Frame_va, from_=1, to=int(self.spinbox_cl1.get()), width=10,
            textvariable=self.spin_var2)
        self.spinbox_ip1.grid(pady=(0, 10), sticky='W')

        self.label_ip1 = ttk.Label(
            self.Frame_txt, text='Selecteer beschrijving:')
        self.label_ip1.grid(pady=(10, 0), sticky='W')
        self.combobox_ip1 = ttk.Combobox(
            self.Frame_txt, values=('GenDescription1', 'GenDescription2'))
        self.combobox_ip1.current(0)
        self.combobox_ip1.grid(sticky='W')

        self.Frame_se = ttk.Frame(self.Interpretatie)
        self.Frame_se.grid(sticky='N', padx=(25, 0),
                           pady=(140, 0), row=1, column=0)

        self.label_ip8 = ttk.Label(self.Frame_se, text='Zoekterm:')
        self.label_ip8.grid(padx=(0, 0), sticky='W')

        self.se = tk.StringVar()
        self.entry_ip1 = ttk.Entry(
            self.Frame_se, textvar=self.se, width=23)
        self.entry_ip1.grid(padx=(0, 0), sticky='N')

        self.Frame_btn = ttk.Frame(self.Interpretatie)
        self.Frame_btn.grid(sticky='W', padx=(110, 0))

        self.status_ip = ttk.Label(self.Frame_btn, text='')
        self.status_ip.grid(sticky='W', padx=(70, 0))

        # aanmaken van de interpretatie knop.
        ttk.Button(self.Interpretatie, text='Genereer bestanden', width=20,
                   command=self.Expressie_cluster_plot).grid(
                       column=0, row=2,
                       padx=(30, 10), sticky='W')

        # aanmaken van de interpretatie progress bar.
        self.progressbar_ip = ttk.Progressbar(self.Frame_btn,
                                              length=300)
        self.progressbar_ip.grid(column=0, row=2, padx=(
            70, 0), pady=(0, 20), sticky='W')

    def Expressie_cluster_plot(self):
        """Functie roept interpretatie programma's aan."""
        # definiëren van data invoer paths.
        cluster_invoer = "Data_out/Relatieve expressiewaarden.txt"
        cluster_uitvoer = "Data_out/cluster_uitvoer.txt"
        familie_cloneID = "Data/CloneIdFamily.txt"

        # functie parameter aanpassen a.h.v. de combobox invoer.
        if self.combobox_ip1.get() == 'GenDescription1':
            gen_beschrijving = "Data/GenDescription.txt"

        elif self.combobox_ip1.get() == 'GenDescription2':
            gen_beschrijving = "Data/GenDescription2.txt"

        # check of step != 2:
        if self.step != 2:
            # weergeef error message als dit True is.
            messagebox.showinfo('Warning', 'Cluster eerst de data!')
            return

        # uitlezen van parameter velden.
        k = int(self.spinbox_cl1.get())
        cluster_nummer = int(self.spinbox_ip1.get())
        zoekterm = str(self.entry_ip1.get())

        # check of Entrez SE is geselecteerd.
        if self.chk_var_ip6.get() == 1:
            # check of zoekterm == ''  als het vorige statement True is.
            if zoekterm == '':
                # weergeef een error message wanneer zoekterm == '', True is.
                messagebox.showinfo('Warning', 'Vul een zoekterm in!')
                return

        # bereken increments voor de progressbar.
        div = (k*self.chk_var_ip1.get()
               + 26 * self.chk_var_ip2.get()
               + self.chk_var_ip3.get()
               + self.chk_var_ip4.get()
               + 2 * self.chk_var_ip5.get()
               + 2 * self.chk_var_ip6.get())

        if div > 0:
            inc = 100/div
        else:
            # weergeef een error message als div == 0.
            messagebox.showinfo('Melding',
                                "U heeft geen programma's geselecteerd!")
            return

        # update interpretatie status label.
        self.status_ip.config(text='Processing...')
        root.update_idletasks()

        # run programma's op basis van de parameterveld invoer.
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
            # aanroepen van functie Histogram().
            Familie_Barchart.Histogram(cluster_uitvoer, familie_cloneID, k)
            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        if self.chk_var_ip4.get() == 1:
            # aanroepen van functie TelWoorden().
            TelWoorden.TelWoorden(gen_beschrijving)

            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        if self.chk_var_ip5.get() == 1:
            # aanroepen van functie cluster_frequentie()
            cluster_freq = cluster_frequentie.cluster_frequentie(
                gen_beschrijving, cluster_uitvoer)

            self.progressbar_ip['value'] += inc
            root.update_idletasks()
            cluster_frequentie.frequency_filter(cluster_freq, k)

            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        if self.chk_var_ip6.get() == 1:

            self.progressbar_ip['value'] += inc
            root.update_idletasks()

            # aanroepen van functie Entrez().
            vrije_analyse.Entrez(cluster_nummer, zoekterm)
            self.progressbar_ip['value'] += inc
            root.update_idletasks()

        # weergeef succesvolle melding.
        messagebox.showinfo('Melding', 'Bestanden zijn gegenereerd!')

        # update progressbar en statuslabel.
        self.progressbar_ip['value'] = 0
        self.status_ip.config(text='')
        root.update_idletasks()

    def Groep_widgets(self):
        """Functie voor het aanmaken van tekstwidget in groep."""
        # aanmaken van tekstveld.
        self.groeptext = tk.Text(self.Groep)
        self.groeptext.grid(row=0, column=0)

        # toevoegen van string aan tekstveld.
        self.groeptext.insert(
            tk.END, '\n'
            + ' '*24 + "Over Groep 7:\n\n"
            + ' '*24 + "Preprocessing:\n"
            + ' '*16 + "Robert van Mourik, Noach Schilt\n\n"
            + ' '*25 + "Clustering:\n"
            + ' '*14 + "Pascalle Lucassen, Joëlle Muijtens,\n"
            + ' '*25 + "Anand Rambali\n\n"
            + ' '*24 + "Interpretatie:\n"
            + ' '*16 + "Pleun Vermeegen, Noah Olmeijer,\n"
            + ' '*25 + "Lars de Haas,\n\n"
            + ' '*16 + "Teacher: Dr. ir. A.J. Markvoort\n"
            + ' '*21 + "TA: A. van der Beek")


root = tk.Tk()
App = Genexpressie(root)
root.mainloop()
