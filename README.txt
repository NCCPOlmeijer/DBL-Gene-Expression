# DBL-Gene-Expression
Groep 007
Bevat alle programma's, databestanden en versies van de interpretatiefase
(fase 3)

Vereiste libraries:
-Biopython,  latest
-Matplotlib, >=3.4.0 --> Familie_Barchart.py (datavalues attribute)
-numpy,      latest
-os,         latest
-Pandas,     latest
-random,     latest
-Tkinter,    latest

# Werking:
- Hoofdprogramma: main.py - Selecteer dit programma om de data analyse uit te 
voeren.

Note: de fases van preprocessing en clustering worden bijgehouden met de file 
'step.txt' zodat het overbodig runnen van stappen na het afsluiten van het
programma niet nodig zijn.

WARNING: pas het bestand step.txt niet handmatig aan!

Bij de uitvoering van main.py wordt er een GUI opgesteld.
Deze GUI heeft 4 tabladen voor de 3 verschillende onderdelen van het project en 
een info tab. Elk van de eerste 3 tabbladen bezit over verschillende widgets.

Preprocessing:
Het preprocessing tablad bezit over 4 verschillende opties.

- CloneID-Filter: Zet de CloneID-Filter aan of uit.
Dit is de filter die ervoor zorgt dat alleen CloneID's met expressie waardes op
elke dag behouden worden.

- Spot-Filter: Zet de SpotD-Filter aan of uit. (Aanbevolen om aan te staan)
Dit is de filter die ervoor zorgt dat de Relatieve Expressiewaardes van CloneID's,
die een te lage of te hoge spotgroote hebben op een bepaalde dag, van die dag niet 
opgeslagen worden.

- Expressie-Filter: Zet de Expressie-Filter aan of uit.
Dit is de filter die CloneID's verwijderd als deze op geen enkele dag een
relatieve expressie boven de R-Grens bevatten.

- R-Grens: Stel de R-grens in voor de Expressie-Filter.

Na het aanpassen van deze opties kan 'Verwerk Data' geselecteerd worden. Dit voert
het preprocessing programma uit door de 'Dag' bestanden in de Data bestandsmap in
te lezen. Tijdens het bewerken van de data worden er 4 figuren per 'Dag' bestand 
aangemaakt. De eerste drie zijn scatterplots van de P1Sig en P2Sig waardes van die
dag tegen elkaar uitgezet. De laatste is een histogram met een verdeling van alle
R waardes van die dag. Het programma slaat het eind resultaat op als 
'Relatieve expressiewaarden.txt' in de Data_out bestandsmap. Hiernaast slaat het 
de aangepaste 'Dag' data op als 'Dag[nummer]_gedaan' in dezelfde map.

Clustering:
Het clustering tablad bezit over 2 verschillende opties.

- Cluster methode: Deze optie verandert welke cluster methode gebruikt zal worden.
Hier is uit een eigen algoritme en K-means te kiezen.

- K-aantal Clusters: Hier is het aantal clusters dat gemaakt zullen worden te
kiezen tussen 2 en 10. Na het aanpassen van deze opties kan 'Cluster Data' 
geselecteerd worden. Dit voert een van de clustering programma's uit afhankenlijk
van welke cluster methode geselecteerd is. De programma's nemen het
'Relatieve expressiewaarden.txt' bestand uit de Data_out bestandsmap als invoer en
slaan het eindresultaat in dezelfde map op als 'cluster_uitvoer.txt'

Interpretatie:
Het preprocessing tablad bezit over 9 verschillende opties.

- Cluster exPlots: Selecteer Cluster exPlots.
Dit is het programma voor het plotten van de relatieve expressiewaarden in blauw 
en het cluster gemiddelde in rood voor elke k-aantal clusters.

- Familie exPlots: Selecteer Familie exPlots.
Dit is het programma voor het plotten van de relatieve expressiewaarden van per 
genfamilie. Het is aan te raden om de cloneID filter uit te zetten bij de
preprocessing fase i.v.m. het kleine aantal cloneIDs uit de genfamilies.

- Familie barPlot: Selecteer Familie barPlot.
Dit is het programma voor het plotten van de distributie van cloneIDs uit families
over de verschillende clusters d.m.v. een stacked barchart. Het is aan te raden om 
de cloneID filter uit te zetten bij de preprocessing fase i.v.m. het kleine aantal 
cloneIDs uit de genfamilies.

- TelWoorden: Selecteer TelWoorden.
Dit is het programma voor het bepalen van de woordfrequentie voor elk woord in de 
geselecteerde genbeschrijving: GenDescription.txt/GenDescription2.txt

- Clusterfrequentie: Selecteer Clusterfrequentie.
Dit is het programma voor het bepalen van de distributie van een woord over
k-aantal clusters. Dit programma retourneert 4 bestanden met verschillende soorten
distributies: zero, non-zero, single, multiple.

- Selecteer beschrijving: Selecteer een genbeschrijving.
Hier kan u kiezen tussen GenDescription en GenDescription2 voor het programma
Clusterfrequentie.

- Vrije analyse: Selecteer Vrije analyse.
Dit is het programma voor het opzoeken van woorden in de genen van een
geselecteerde cluster in de EMBL Mus Musculus genbank. Het programma retourneert
een tekstbestand 'Sequences.fasta' met daarin alle genen uit de geselecteerde
cluster waar de ingevulde zoekterm in voorkomt.

- Cluster: Selecteer een cluster.
U kunt kiezen in welke cluster u de zoekterm wilt opzoeken. (range 1 - k-aantal)

- Zoekterm: Vul een zoekterm in.
Hier kunt u de zoekterm invullen voor het vrije analyse programma.

Na het aanpassen van deze opties kan 'Genereer bestanden' geselecteerd worden.
De plots staan gesorteerd in de map 'Plots'; de tekstbestanden staan in de map
'Data_out'.

# Contents:
   Main directory:
     - Cluster_Plots/ 	: bevat plots gegenereerd door 'expressie_clusters.py'
     - Data/ 		: bevat alle aangeleverde databestanden in tekstformaat
     - Data_out/ 	: bevat alle gegenereerde databestanden in tekstformaat
     - cluster_frequentie.py
     - eigen_clustering.py
     - expressie_clusters.py
     - expressie_families.py
     - Familie_Barchart.py
     - k-means.py
     - main.py
     - preprocessing.py
     - TelWoorden.py
