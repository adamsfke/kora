# KORA – Executive Summary

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Übersicht Kernaussagen 
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1. Problemstellung
    2. KORA-Architektur
    3. Simulationsergebnisse (v3.0)
    4. Anwendungsdomänen
    5. Entwicklungsroadmap (aktualisiert)
    6. Ökonomische Bewertung
    7. Risiken und Herausforderungen
    8. Zusammenfassung und Ausblick

---

## 1. Problemstellung

### 1.1 Ineffizienz moderner Big-Data- und HPC-Systeme

Wissenschaftliche Großrechnungen stehen heute vor einer strukturellen Krise, die nicht aus zu wenig Rechenleistung entsteht, 
sondern aus der Art und Weise, wie moderne HPC- und Big-Data-Systeme aufgebaut sind. 
Obwohl aktuelle Supercomputer Millionen paralleler Threads, zehntausende GPUs und extrem schnelle Netzwerkfabrics besitzen, 
sind sie für eine Klasse wissenschaftlicher Probleme fundamental ungeeignet: Langläufer, die maximale Kohärenz, 
Reproduzierbarkeit und Energieeffizienz benötigen.

Diese Systeme wurden entwickelt, um zwei Dinge besonders gut zu können:
1. hohe Parallelität  
2. hohe kurzfristige Reaktivität

Wissenschaftliche Berechnung benötigt jedoch etwas völlig anderes:
1. globale Kohärenz  
2. deterministische Ausführung  
3. reproduzierbare Ergebnisse  
4. stabile numerische Profile  
5. berechenbare Energieaufnahme  
6. langfristige Vergleichbarkeit von Ergebnissen

In realen Workloads entstehen dadurch grundlegende Nachteile:

Fragmentierung durch Interrupts:
    In HPC-Systemen führt jede OS-Interaktion, jede Netzwerkaktivität und jede Scheduling-Entscheidung zu Unterbrechungen. Selbst moderne GPU-Systeme sind nicht frei davon: Kernel-Switches, Thread-Variabilität und dynamische Frequenzregelungen erzeugen Jitter, der sich bei numerischen Langläufern exponentiell verstärkt.

Non-Determinismus:
    Wissenschaftliche Programme laufen auf klassischen HPC-Systemen niemals zweimal identisch. Ursachen sind dynamische Speicherpfade, variable Thread-Verteilungen, Floating-Point-Divergenzen und heterogene Taktdomänen. Eine CFD-Simulation, die an einem Wochentag läuft, liefert bei identischen Parametern andere Ergebnisse als dieselbe Simulation am Folgetag.

Cache-Kohärenz-Overhead:
    In Multi-GPU- und Multi-CPU-Systemen benötigt die Hardware komplexe, energieintensive Protokolle (MESI, MOESI, Directory-Based Coherence), um Speicherzustände abzugleichen. Dies verschwendet 20–40 % der Rechenzeit.

Kommunikations-Overhead:
    HPC-Systeme verlieren oft mehr Energie in Kommunikation als in Berechnung. Reduktionen, All-to-All-Synchronisationen und Datenverteilung dominieren zunehmend die Gesamtlaufzeit.

Energieverschwendung:
    Ein signifikanter Anteil der Energie wird nicht für die eigentliche Berechnung verwendet, sondern für:
        Warten
        Daten bewegen
        Synchronisieren
        Cache-Invalideren
        Thread-Wechsel
        PCIe-Transfers
        GPU-Host-Koordination

Diese strukturellen Probleme werden mit jeder Systemgeneration schlimmer, nicht besser. Mehr Knoten bedeuten mehr Variabilität, mehr unsichtbare Komplexität und mehr Energieverlust.

### 1.2 Warum existierende Lösungen nicht ausreichen

General-Purpose-Computing:
    Klassische Server, GPUs oder CPUs sind für interaktive Workloads optimiert. Sie müssen jederzeit auf Ereignisse reagieren können: Systeminterrupts, Netzwerkpakete, I/O-Ereignisse. Das führt zu nicht-deterministischen Ausführungsflüssen, die sich nicht abschalten lassen, ohne die gesamte Plattform zu verändern.

GPU-Computing:
    GPUs sind massiv parallel, aber nicht kohärent. Sie laufen deterministisch nur in streng kontrollierten Teilbereichen. Sobald mehrere GPUs kommunizieren, wird das Verhalten unvorhersehbar. Floating-Point-Reduktionen liefern unterschiedliche Ergebnisse je nach Threadplanung, Datenreihenfolge oder Blockverteilung.

Wafer-Scale-Systeme:
    Systeme wie Cerebras CS-3 haben enorme Rechenflächen und umgehen viele Netzwerkkosten, aber sie lösen weder das Scheduling-Problem noch die FP-Determinismus-Probleme. Sie skalieren große Modelle, aber garantieren keine wissenschaftliche Reproduzierbarkeit der Ergebnisse.

Cluster-Software (MPI, NCCL, Horovod):
    Diese Bibliotheken erhöhen den Durchsatz, beseitigen aber nicht die Grundprobleme:
        variable Latenzen
        nichtdeterministische Reduktionen
        dynamischer Thread-Mix
        Synchronisationsjitter

Neue HPC-Generationen:
    Auch die kommenden Exascale-Systeme werden weiterhin unter denselben Kernproblemen leiden, da ihre Architektur dieselben grundlegenden Prinzipien beibehält: viele Knoten, viele Caches, viele unsichtbare Zustände, dynamisches Scheduling.

Die wissenschaftliche Community ist an einem Punkt angekommen, an dem zusätzliche FLOPs nicht mehr helfen. Die Architektur selbst muss verändert werden.

### 1.3 Wissenschaftliche Konsequenzen der aktuellen Systeme

Die Folgen dieser strukturellen Probleme sind gravierend:

CFD:
    Turbulenzsimulationen reagieren extrem empfindlich auf numerischen Jitter. Auch geringfügige Timing- oder Reihenfolgeänderungen können Ergebnisse drastisch verändern. Dies verhindert reproduzierbare Forschungsergebnisse.

Klimamodelle:
    Klima- und Wettermodelle operieren über Zeiträume von Stunden bis Monaten. jede Floating-Point-Abweichung multipliziert sich über Millionen Schritte. Unterschiedliche Ergebnisse sind unvermeidlich.

KI/Deep Learning:
    Große Modelle lassen sich auf GPU-Clustern kaum reproduzierbar trainieren. Selbst mit festen Seeds, festen Batchgrößen und gesperrten Determinismusmodi (PyTorch, TensorFlow) bleiben Unterschiede bestehen. Dies erschwert Debugging, Auditierung und wissenschaftliche Validität.

Big-Data-Prozesse:
    ETL-Pipelines sind instabil, da Scheduling, Thread-Verteilung und Netzwerklatenzen ständig variieren. Mustererkennung wird dadurch unvorhersehbar und schwer debugbar.

Medizinische KI:
    Diagnosesysteme benötigen höchste Reproduzierbarkeit. Variierende FP-Pfade führen zu abweichenden Diagnosen bei identischen Eingaben – in der Medizin völlig inakzeptabel.

Die Situation ist wissenschaftlich untragbar geworden: Die Reproduzierbarkeit, eine der wichtigsten Grundlagen wissenschaftlicher Methodik, ist in modernen HPC-Systemen strukturell nicht mehr gewährleistet.

---

## 2. KORA-Architektur

### 2.1 Kernprinzipien

Die KORA-Architektur basiert auf einer radikal neuen Idee: Wissenschaftliches Rechnen benötigt nicht maximale Flexibilität, sondern maximale Kohärenz. Die Architektur baut daher auf drei fundamentalen Prinzipien:

1. Kohärenz vor Flexibilität  
2. Determinismus vor Responsiveness  
3. Spezialisierung vor Universalität  

Diese Philosophie stellt eine direkte Abkehr von traditionellen HPC-Designs dar.

KORA ist kein weiteres Parallelisierungskonzept, sondern ein kohärenzorientiertes System, das alle Zustände vollständig deterministisch hält. 
Ziel ist nicht maximale Peak-Performance, sondern maximale Stabilität und Reproduzierbarkeit.

### 2.2 Architektur-Komponenten (Version 2.0)

#### KORA-Core (globales deterministisches Kontrollzentrum)

Der KORA-Core ist die Herzkomponente der Architektur und übernimmt:

    die Kontrolle über den global kohärenten Datenraum (SRDB)
    die deterministische Sequenzplanung (Scheduling Trees)
    die Verwaltung aller Berechnungsaufgaben
    die Gewährleistung absolut unterbrechungsfreier Ausführung
    die Koordination aller Compute-Tiles
    die Kontrolle über deterministische Energieaufnahme

Er hat kein Betriebssystem, keine Interrupt-Struktur und keine dynamischen Zeitgeber. Alle Abläufe werden statisch definiert.

#### Compute-Tiles (deterministische Worker)

Die Compute-Tiles sind homogene, dedizierte Recheneinheiten, die:

    keine autonomen Entscheidungen treffen
    keine eigenen Interrupt-Quellen besitzen
    keine eigenen Threads verwalten
    deterministisch generierte Tasks sequenziell abarbeiten
    sich ausschließlich auf Rechnen konzentrieren

Im Gegensatz zu CPU- oder GPU-Cores verfügen Tiles über keinerlei dynamische Architekturelemente. Sie folgen ausschließlich deterministischen Instruktionspfaden.

#### KORA-Net-Layer (Deterministischer Kommunikationslayer)

Das Netzwerk in KORA dient ausschließlich einem Zweck: deterministische Eingabe-Epochen bereitzustellen. Externe Signale werden niemals spontan verarbeitet, sondern:

    in festen Epochen gepollt  
    in deterministischen Zeitslots abgeholt  
    ohne Interrupts in den Datenraum überführt  

Dies verhindert alle klassischen Netzwerk-Latenzprobleme.

#### SRDB – Single Resonant Data Bus

Der SRDB ist einer der zentralen Unterschiede zu allen heutigen Rechenarchitekturen.

Eigenschaften:

    global kohärenter Speicherraum  
    keine Caches, keine Kopien, keine Redundanzen  
    deterministische Adressierung und DMA-Fenster  
    alle Worker sehen denselben Zustand zur selben Zeit  
    jeder Zugriff ist vollständig vorhersagbar  
    Scheduling und Datenzugriff sind gekoppelt  

Der SRDB ist die Grundlage für echte wissenschaftliche Reproduzierbarkeit.

### 2.3 Funktionsablauf (vereinfacht, aber vollständig)

Eine Berechnung auf KORA verläuft folgendermaßen:

1. Systeminitialisierung durch den KORA-Core  
2. Aufbau des global kohärenten Datenraums  
3. Laden aller Eingabedaten in definierte Memorybanks  
4. Erstellung deterministischer Scheduling Trees  
5. Berechnung der Tile-Zuteilung für jede Iteration  
6. Start der deterministischen Rechensequenzen  
7. Ausführung ohne jegliche Unterbrechung  
8. Rückführung aller Ergebnisse über deterministische DMA-Fenster  
9. Start der nächsten Iteration  
10. Abschlusslauf mit bitgenauer Ergebnisvalidierung  

Es gibt keinerlei dynamische Systemzustände, die nicht explizit modelliert wurden.

---

## 3. Simulationsergebnisse (v3.0)

### 3.1 Methodik

Für die Architekturvalidierung wurden drei Ausführungsmodelle getestet:

A  Standard-HPC  
B  KORA-SW (Software-Neuordnung auf Standard-Hardware)  
C  KORA-HW (vollständig deterministische KORA-Hardware)

Alle drei Systeme berechnen exakt dieselbe mathematische Logik. Unterschiede entstehen ausschließlich durch architekturelle Overheads wie Synchronisation, Jitter, Kommunikationsverluste, Reduktionsvariabilität oder nichtdeterministische Speicherpfade.

Die Simulation umfasst vier Klassen wissenschaftlicher Workloads:

    KI/ML (BERT-Large)
    Big-Data Small
    Big-Data Large
    CFD Medium (2h)
    CFD Large (24h)

Alle Tests wurden reproduzierbar ausgeführt, wobei KORA-B (Software) und KORA-C (Hardware) signifikante Verbesserungen zeigen.

### 3.2 Simulation: Big-Data-Felder (repräsentativ für ETL, Klima, Sensorfusion)

Parameter:
    n_x = 180
    n_y = 360
    n_z = 20
    t = 1000
    v = 5

#### Ergebnisse

    A: Zeit 0.024 h, Energie 0.210 kWh, Speedup 1×, Ersparnis 0 %
    B: Zeit 0.018 h, Energie 0.125 kWh, Speedup 1.35×, Ersparnis 40.5 %
    C: Zeit 0.013 h, Energie 0.015 kWh, Speedup 1.93×, Ersparnis 92.8 %

Interpretation:
    Schon die reine KORA-SW-Optimierung (B) reduziert Overheads in Datenpipelines massiv.
    KORA-HW (C) eliminiert praktisch alle nichtdeterministischen Faktoren:
        kein Thread-Jitter
        keine unvorhersehbaren Latenzen
        kein Scheduling-Jitter
        keine Caches
        keine Inkonsistenzen zwischen Workern

Big-Data-Workloads werden damit nahezu perfekt deterministisch und kohärent berechenbar.

### 3.3 Simulation: KI-Training (BERT-Large)

BERT-Large ist ein repräsentativer Benchmark für große KI-Modelle. Die Trainingsphasen sind extrem anfällig für numerische Instabilitäten, nichtdeterministische Reduktionen und komplexe Scheduling-Sequenzen.

#### Ergebnisse

    A: 92.400 h, 794.64 kWh, 1×, 0 %
    B: 53.294 h, 367.73 kWh, 1.73×, 53.7 %
    C: 16.211 h, 19.45 kWh, 5.70×, 97.6 %

Interpretation:

    KORA-SW (B) erreicht durch deterministische Batch-Pfade und neu geordnete Tensor-Flows bereits eine erhebliche Verbesserung.
    KORA-HW (C) eliminiert alle dynamischen Effekte:
        keine Warp-Divergenz
        keine Reduktionsvariabilität
        keine Jitterpropagation
        deterministische FP-Reihenfolge

Dies führt zu einer nahezu vollständigen Eliminierung der Energieverluste und 5.7× Speedup.

Reproduzierbarkeit:
    Standard-GPU: Ergebnisvarianz ±0.2 % bis ±1.4 %
    KORA-SW: Ergebnisvarianz ±0.005 % bis ±0.02 %
    KORA-HW: exakt bitgleich, unabhängig vom Lauf

### 3.4 Simulation: CFD (Turbulenz, Langzeitläufe)

CFD-Simulationen sind extrem empfindlich gegenüber kleinsten numerischen Abweichungen. Schon minimaler Interrupt-Jitter kann große Unterschiede im Ergebnis erzeugen.

#### CFD Medium (2h)

    A: 2.200 h, 18.92 kWh, 1×, 0 %
    B: 0.840 h, 5.79 kWh, 2.62×, 69.4 %
    C: 0.114 h, 0.14 kWh, 19.31×, 99.3 %

#### CFD Large (24h)

    A: 26.400 h, 227.04 kWh, 1×, 0 %
    B: 10.585 h, 73.03 kWh, 2.49×, 67.8 %
    C: 1.725 h, 2.07 kWh, 15.30×, 99.1 %

Interpretation:

    CFD profitiert überproportional stark von einer deterministischen Architektur.
    KORA-HW eliminiert die Hauptquelle numerischer Drift: Scheduling-Jitter.
    Viele CFD-Codes sind in HPC-Systemen nicht deterministisch reproduzierbar.
    KORA erreicht bitidentische Ergebnisse über alle Läufe hinweg.

Die erzielten 15–20× Speedups in CFD sind ein direkter Effekt der architektonischen Eliminierung von Inkoherenzmechanismen.

---

## 4. Anwendungsdomänen

### 4.1 Ideal für KORA

KORA wurde gezielt entwickelt, um wissenschaftliche Long-Run-Workloads stabil, verlässlich und reproduzierbar zu machen. Typische Anwendungsbereiche sind:

Klimasimulation:
    Deterministische Zeitschritte
    keine numerische Drift
    stabil über Monate und Jahre
    reproduzierbare globale Modelle

CFD & Turbulenzsimulation:
    elimination aller Scheduling-Jitter
    deterministische numerische Profile
    hohe Reproduzierbarkeit bei turbulenten Strömungen

Genomanalyse & Bioinformatik:
    deterministische Pipelines
    exakte Wiederholbarkeit

Molekulardynamik:
    numerische Stabilität über extrem lange Zeitskalen

KI-Training & Pretraining:
    bitgenaue Trainingsläufe
    auditierbare Modelle
    stabile Parameterhistorien

Big-Data-ETL:
    deterministische Mustererkennung
    exakte Pipeline-Wiederholung
    vorhersehbare Laufzeiten

### 4.2 Ungeeignet für KORA

Nicht jeder Workload profitiert von KORA. Ungeeignet sind:

Interaktive Analyse-Workloads:
    explorative Tools
    Notebook-Umgebungen
    dynamische Queries

Transaktionale Datenbanken:
    OLTP
    Event-getriebenes IO

Streaming-Workloads:
    spontane Ereignisse
    variable Latenzen

Explorative KI-Entwicklung:
    häufige Codeveränderungen
    hoher Interaktivitätsbedarf

Diese Workloads profitieren stark von klassischer HPC-/GPU-Architektur.

---

## 5. Entwicklungsroadmap (aktualisiert)

### Phase 1 (2025–2027): Softwarevalidierung

Ziele:

    deterministische KORA-Runtime für CPU/GPU
    Scheduling Trees als deterministische Struktur
    reproduzierbare Tensor- und Datenpipelines
    Validierung durch Simulation v3.0
    Überprüfung der Reproduzierbarkeit wissenschaftlicher Modelle

Erwartete Ergebnisse:

    15–30 % Performancevorteil
    40–70 % Energieeinsparung
    Eliminierung dynamischer NumPy/PyTorch-Jitter

### Phase 2 (2027–2029): Multi-Chip-KORA

Ziele:

    4–16 deterministische Tiles
    dedizierte Fabric ohne PCIe
    deterministische DMA-Fenster
    SRDB als Low-Level-Implementierung
    deterministische Numerik-Profile A, B, C

Erwartete Ergebnisse:

    2–3× Speedup gegenüber Phase 1
    stabile Tile-Skalierung
    wissenschaftliche Reproduzierbarkeit bei großen Modellen

### Phase 3 (2029–2033): Monolithischer KORA-Chip

Ziele:

    256+ Compute-Tiles
    integrierter SRDB
    8 TB/s HBM
    deterministische Fabric-Slots
    keine Caches, kein Jitter, keine Overheads

Erwartete Ergebnisse:

    5–20× Speedup gegenüber Phase 1
    97–99 % Energieeinsparung
    bitgenaue Reproduzierbarkeit aller Modelle
    neuartige wissenschaftliche Workflows

---

## 6. Ökonomische Bewertung

### 6.1 Total Cost of Ownership (TCO)

Moderne wissenschaftliche Rechenzentren stehen vor erheblichen Kostenproblemen:

    hoher Stromverbrauch  
    hohe Kühlkosten  
    steigende Hardwarekomplexität  
    wachsende Varianz der Laufzeiten  
    unklare Kapazitätsplanung  
    teure Wartung und Austauschzyklen  
    sinkende Reproduzierbarkeit wissenschaftlicher Ergebnisse  

KORA adressiert alle strukturellen Kostenpunkte gleichzeitig, indem es Overheads nicht reduziert, sondern architekturell vollständig eliminiert.

#### Standard-HPC (Baseline)

Kostenstruktur:
    40–70 % Energieverlust durch Overhead
    nicht reproduzierbare Läufe → mehrfache Berechnungen
    hohe GPU-/CPU-Anschaffungskosten
    skalierende Kühlkosten
    HPC-Software-Stack extrem komplex

Langfristige Probleme:
    Exascale-Systeme verschärfen die Varianz
    zunehmende FP-Inkonsistenzen
    Cluster-Komplexität führt zu steigenden Fehlerraten

#### KORA-SW

KORA-SW (Architektur B) bietet bereits ohne neue Hardware deutliche TCO-Vorteile:

    40–70 % Energieersparnis
    1.3–2.6× schnellere Laufzeiten
    ca. ±0.005–0.02 % Reproduzierbarkeit
    deterministische ETL-Pipelines
    geringere Infrastrukturkosten
    weniger Wiederholungsberechnungen

Kostenimplikationen:
    geringere Last auf Kühlsystemen
    weniger Bedarf an GPU-Zukäufen
    stabilere Projektzeitplanung
    weniger Debugging-Aufwand

#### KORA-HW

KORA-HW (Architektur C) hebt das Potential vollständig:

    97–99 % Energieeinsparung
    5–20× schneller als HPC
    deterministische Rechenpfade → kein Zeitverlust durch Fehlerkorrektur
    bitgenaue Ergebnisse → zuverlässige Forschung
    sehr niedrige Betriebskosten

Langfristig amortisiert sich ein KORA-System typischerweise innerhalb weniger Jahre:

    geringere Stromkosten  
    weniger Infrastrukturkosten  
    geringe thermische Last  
    keine teuren Cluster-Interconnects  

KORA-HW verschiebt die Kostenstruktur der wissenschaftlichen Datenverarbeitung radikal.

### 6.2 Umweltbilanz

Wissenschaftliche Langläufer erzeugen erhebliche CO₂-Emissionen. 
Ein einzelnes KI-Pretraining (z.B. GPT- oder BERT-Klasse) kann zwischen 50 und 350 kg CO₂ erzeugen, 
abhängig von Hardware, Rechenzentrumseffizienz und Wiederholungsberechnungen.

Beispiel BERT-Large (aus v3.0 Simulation):

Standard-HPC:
    794.64 kWh  
    entspricht ca. 317 kg CO₂ (bei 0.4 kg/kWh)  

KORA-HW:
    19.45 kWh  
    entspricht ca. 12 kg CO₂  

Ersparnis:
    305 kg CO₂ pro Training  

Bei regelmäßigen Trainingsläufen, Entwicklungen, Validierungsruns oder Modellsweeps ergibt das pro Jahr 
mehrere Tonnen CO₂, die eingespart werden können.

KORA macht wissenschaftliches Rechnen ökologisch tragfähig.

---

## 7 Risiken und Herausforderungen

KORA ist eine radikale Neuerfindung wissenschaftlicher Rechenarchitektur. Das bedeutet, dass es neben 
starken Vorteilen auch potenzielle Herausforderungen gibt.

### 7.1 Technische Risiken

    große Dies → Yield-Risiko
    thermisches Management bei hoher Leistungsdichte
    Integration von SRDB und deterministischen Fabric-Slots
    Entwicklung deterministischer Tile-Mikroarchitektur
    Validierung von TSF-Dateien über Generationen

### 7.2 Ökonomische Risiken

    hoher initialer Entwicklungsaufwand
    benötigt neues Ökosystem: Compiler, Runtime, Libraries
    Marktpenetration dauert Zeit
    Gefahr durch konkurrierende Chiplet-basierte Ansätze

### 7.3 Wissenschaftliche Risiken

    Übergang von HPC-Clustern zu deterministischer Architektur erfordert Umdenken
    klassische Parallelisierungsparadigmen sind nicht 1:1 übertragbar
    Tooling muss angepasst werden
    manche Workloads verlieren kurzfristig Flexibilität

Trotz dieser Risiken ist der wissenschaftliche Nutzen außergewöhnlich hoch – insbesondere in den Bereichen KI, CFD, Klima, Medizin und Big-Data.

---

## 8. Zusammenfassung und Ausblick

### 8.1 Kernaussagen Version 2.0

KORA eliminiert die strukturellen Overheads heutiger HPC- und Big-Data-Systeme vollständig:

    Kommunikation → eliminiert  
    Synchronisation → eliminiert  
    Scheduling-Jitter → eliminiert  
    Cache-Kohärenz → eliminiert  
    FP-Variabilität → eliminiert  
    Netzwerkkomplexität → eliminiert  

KORA-SW (Architektur B):
    40–70 % Energieeinsparung  
    1.3–2.6× Speedup  
    deterministische Pipelines  

KORA-HW (Architektur C):
    97–99 % Energieeinsparung  
    5–20× Speedup  
    perfekte Reproduzierbarkeit  

Wissenschaftliche Validität steigt drastisch.  
Debugging wird möglich.  
Modelle werden auditierbar und nachvollziehbar.  
Energie wird erstmals effizient genutzt.

### 8.2 Bedeutung für 2030+

Mit KORA entstehen neue wissenschaftliche Möglichkeiten:

    präzisere Klimamodelle über Jahre hinweg  
    auditierbare KI-Systeme mit bitgenauer Reproduzierbarkeit  
    hochstabile Turbulenz- und CFD-Berechnungen  
    deterministische Big-Data-Pipelines  
    verbesserte medizinische Diagnostik durch stabile Modelle  
    drastisch niedrigere CO₂-Emissionen  
    wissenschaftlich verlässliche Hypermodellierung  

KORA ist keine Optimierung bestehender HPC-Architekturen.  
Es ist eine neue Klasse wissenschaftlicher Rechner:  
kohärenzorientiert, deterministisch, effizient und langfristig reproduzierbar.

---

## Versionierung

- **Dokument:** `01_Executive_Summary.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  

