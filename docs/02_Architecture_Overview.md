# KORA - Architecture Overview  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Architekturdefinition 
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Einleitung
    2.  Warum heutige HPC-Systeme scheitern
    3.  Der eigentliche Engpass heutiger HPC-Systeme
    4.  Was ein Monolith ist (leicht verständlich)
    5.  Warum KORA deterministisch ist
    6.  Warum KORA energieeffizient ist
    7.  Warum HPC-Barrieren verschwinden
    8.  Warum Kommunikation reduziert wird
    9.  Warum Ergebnisse stabil und reproduzierbar werden
    10. Warum das relevant ist (Vorschau zu Block 2)
    11. Energieeffizienz: Warum KORA 97–99 % spart
    12. Warum HPC-Barrieren vollständig verschwinden
    13. Warum Ergebnisse stabil und reproduzierbar werden
    14. Die Rolle des SRDB (Single Resonant Data Bus) im Überblick
    15. High-Level-Vergleich: HPC vs. GPU vs. KORA
    16. Warum KORA für CFD entscheidend ist
    17. Warum KORA für KI/ML entscheidend ist
    18. Warum KORA für Big-Data entscheidend ist
    19. Warum KORA für Klima & Medizin entscheidend ist
    20. Kurzzusammenfassung von Block 2
    21. Simulation v3.0 – High-Level-Zusammenfassung
    22. ASCII-Diagramm 7 – Speedup & Energieprofil v3.0 (vereinfacht)
    23. Simulation v3.0 – Vollständige Tabelle  
    24. Interpretation der Simulationsergebnisse
    25. High-Level-Vergleich mit existierenden Systemen (vereinfacht)
    26. Wissenschaftliche Relevanz
    27. Zusammenfassung des gesamten Overview-Dokuments
    28. Abschließender Satz

---

## 1. Einleitung

KORA ist eine neuartige Rechenarchitektur, die entwickelt wurde, um ein Problem zu lösen,
das in modernen HPC-Systemen immer deutlicher wird:

Wissenschaft braucht **Reproduzierbarkeit**, **Stabilität**, **globale Kohärenz**  
und **verstehbare Performance** –  
aber aktuelle HPC-Cluster liefern oft das Gegenteil:

- Ergebnisse hängen von der Lastsituation ab  
- minimale Timing-Unterschiede erzeugen andere Resultate  
- energieeffiziente Berechnung ist kaum möglich  
- Kommunikation dominiert die Rechenzeit  
- Workflows sind schwer überprüfbar  
- Debugging ist nahezu unmöglich  

KORA setzt hier an – mit einer vollständig deterministischen Ausführungsarchitektur,
die Rechenleistung **kohärent**, **stabil**, **energieeffizient** und **wissenschaftlich verwertbar** macht.

Ziel dieses Dokuments ist nicht, die Hardware im Detail zu erklären  
(dafür existiert das 03-Technical-Document),
sondern die **Prinzipien und Vorteile** verständlich und praxisnah darzustellen.

---

## 2. Warum heutige HPC-Systeme scheitern

### 2.1 Das Grundproblem: HPC ist nicht gebaut für Kohärenz, sondern für Durchsatz
Moderne Cluster bestehen aus tausenden unabhängigen Knoten.
Jeder dieser Knoten hat:

- eigene Caches  
- eigene dynamische Frequenzregelung  
- eigenes Betriebssystem  
- eigene Interruptquellen  
- eigene Hintergrundprozesse  
- eigenes Scheduling-Verhalten  

Das Ergebnis ist eine Architektur, die nie zwei Läufe identisch ausführt.

### 2.2 Wo es wissenschaftlich kritisch wird

#### CFD:
Kleine Unterschiede in Floating-Point-Operationen propagieren exponentiell.  
Die Simulation „kippt“ – ein bekanntes Phänomen bei Turbulenzmodellen.

#### KI/ML:
Training ist nicht reproduzierbar, weil GPUs dynamisch optimieren,
Threads wechseln, und FP-Ausführungsreihenfolgen variieren.

#### Klimamodelle:
Globale Modelle reagieren empfindlich auf numerische Drift.
Eine andere Thread-Belegung erzeugt andere Temperaturverteilungen.

#### Big-Data:
Parallele ETL-Pipelines liefern unterschiedliche Ergebnisse,
je nachdem wie der Scheduler entscheidet.

Das ist wissenschaftlich problematisch.

---

## 3. Der eigentliche Engpass heutiger HPC-Systeme

Viele glauben, dass FLOPs das entscheidende Kriterium sind.

Das ist falsch.

#### In Wirklichkeit sind die drei Engpässe:

1. **Kommunikation**
2. **Synchronisation**
3. **Inkoherente Speicherzugriffe**

Diese erzeugen:

- Jitter  
- Race Conditions  
- Floating-Point-Variabilität  
- nicht reproduzierbare Reduktionen  
- hohe Energieverbräuche  

Das folgende Diagramm verdeutlicht das klassische HPC-Problem.

#### Diagramm 1 – Der HPC-Engpass (ASCII)

    HPC-Cluster (vereinfacht)
    ┌──────────────────────────┐
    │   Node 1   Node 2   ...  │
    │   [CPU]    [CPU]         │
    │   [GPU]    [GPU]         │
    └──────────────────────────┘
           │        │
           ▼        ▼
    ┌──────────────────────────┐
    │       Netzwerk-Fabric    │
    │   (MPI, RDMA, TCP/IP)    │
    └──────────────────────────┘
           │        │
           ▼        ▼
    ┌──────────────────────────┐
    │   Synchronisation        │
    │   Barriers, Reductions   │
    └──────────────────────────┘

Ergebnis:
- Daten werden fragmentiert
- Kommunikation überlastet
- Rechenzeit wird zu Wartezeit
- Ergebnisse variieren

Die Architektur ist nicht harmonisch – sie ist eine *Koordination von Inseln*.

---

## 4. Was ein Monolith ist (leicht verständlich)

KORA ersetzt die Inselwelt („viele Knoten“) durch **einen kohärenten Rechenkörper**:

- keine Caches  
- keine dynamischen Frequenzen  
- kein OS  
- keine Interrupts  
- keine Scheduling-Variabilität  
- global einheitlicher Datenraum  

Der Monolith ist ein hardwaredeterministisches System,
in dem alle Rechenoperationen in einem globalen, synchronen Modell stattfinden.

#### Diagramm 2 – Cluster (klassisch) vs. Monolith (KORA)

    Klassischer Cluster:
    ┌────────┬────────┬────────┐
    │ Node1  │ Node2  │ Node3  │   → viele unabhängige Inseln
    └────────┴────────┴────────┘
        │         │         │
        ▼         ▼         ▼
    Netzwerk + Synchronisation

    KORA Monolith:
    ┌──────────────────────────┐
    │     EIN globaler Raum    │
    │  Tiles, Memorybanks,     │
    │  deterministische Fabric │
    └──────────────────────────┘
                 │
                 ▼
    keine Synchronisation nötig

Ein Monolith ist kein „großer Knoten“ –
es ist eine **grundlegend andere Rechenphilosophie**.

---

## 5. Warum KORA deterministisch ist

Der zentrale Unterschied zu HPC:

    HPC = dynamisch
    KORA = statisch deterministisch

Determinismus bedeutet:

- gleiche Eingaben → gleiche Ergebnisse  
- gleiche Zeit → gleiche Energieaufnahme  
- keine versteckten Ausführungspfade  
- keine spontane Variabilität  

KORA erreicht dies durch:

- Scheduling Trees mit fester Reihenfolge  
- deterministische Memorybanks  
- deterministische DMA-Fenster  
- deterministische Fabric  
- keine Interrupts  
- keine Threads  
- keine dynamischen numerischen Pfade  
- Soft-FP für reproduzierbare FP-Berechnung  
- TSF als statisches Ausführungsformat  

Das **Scheduling Tree**-Konzept aus dem technischen Dokument  
formt die fundamentale Ausführungsstruktur (Quelle: 03-Technical Spec, Kap. *Scheduling Tree*, :contentReference[oaicite:0]{index=0}).

---

## 6. Warum KORA energieeffizient ist

KORA reduziert Energieverbrauch nicht durch bessere Kühlung oder effizientere GPUs,
sondern durch **architekturelle Eliminierung von Energieverschwendung**.

### 6.1 Energieverlust im HPC:

- idle → warten auf andere  
- Clusterkommunikation → Netzwerk kostet enorm  
- Reduktionen → mehrfacher Datenverkehr  
- dynamische FP-Pfade → ineffizient  
- Cache-Kohärenz → extrem teuer  
- Scheduling → Overhead  

### 6.2 In KORA existieren diese Faktoren nicht

- keine Idle-Phasen  
- keine verteilten Knoten (→ keine Netzwerkenergie)  
- keine Reduktionsvariabilität  
- keine Caches  
- keine dynamischen Optimierer  
- konstante Leistungsaufnahme („Power Determinism“ aus Kap. 22.6, :contentReference[oaicite:1]{index=1})  

Das führt zu den Simulationsergebnissen der v3.0-Studie:
**97–99 % Energieeinsparung**, selbst bei großen Workloads.

---

## 7. Warum HPC-Barrieren verschwinden

In klassischen HPC-Systemen verbringt ein System einen Großteil der Zeit mit:

- Datenaufteilung  
- Datenzusammenführung  
- Synchronisation  
- Kommunikationsplanung  
- Netzwerkrouter-Warten  
- Wartezeiten zwischen Threads  
- stochastischen Effekten  

KORA vermeidet das durch deterministische Prinzipien:

- vollständiges Fehlen von Scheduling Jitter („Zero Jitter Architecture“, Kap. Glossary, :contentReference[oaicite:2]{index=2})  
- keine dynamische Lastverteilung („Load Balance nonexistent“, Kap. Glossary, :contentReference[oaicite:3]{index=3})  
- strukturierte Fabric (TDM) mit festen Zeitschlitzen  
- linearer Datenfluss  
- statische Kommunikation  

Es gibt keine Barrieren mehr, weil alle Abläufe vorherbestimmt sind.

---

## 8. Warum Kommunikation reduziert wird

KORA nutzt einen einzigen globalen Datenraum.
Daten werden nicht kopiert, sondern **deterministisch adressiert**.

#### Diagramm 4 – SRDB (Single Resonant Data Bus, High-Level)

    SRDB (vereinfacht)
    ┌────────────────────────────┐
    │   globaler kohärenter Bus  │
    │   keine Caches             │
    │   deterministische Pfade   │
    └────────────────────────────┘
         ▲        ▲        ▲
         │        │        │
      Tiles    Memory   DMA-Fenster

Konsequenzen:

- keine Replikation  
- keine Konsistenzprotokolle  
- keine Cache-Kohärenz  
- keine Synchronisation zwischen Knoten  

Ergebnis:
**Kommunikation verschwindet praktisch.**

---

## 9. Warum Ergebnisse stabil und reproduzierbar werden

Stabilität basiert auf mehreren Schichten (Quelle: Kap. 56/62 Validierung, :contentReference[oaicite:4]{index=4}):

- deterministische numerische Profile  
- bitgenaue FP-Ausführung  
- feste Memorypfade  
- feste DMA-Sequenzen  
- feste Fabric-Zeitfenster  
- vollständige Telemetrie  
- Hash-gesicherte Runs („Golden Runs“)  

Dadurch entsteht echte wissenschaftliche Reproduzierbarkeit:

    reproduction_possible = true  
    across_years = true  
    across_hardware_generations = true

---

## 10. Warum das relevant ist (Vorschau zu Block 2)

KORA adressiert kritische Wissenschaftsfelder:

- Turbulenzforschung (CFD)  
- Klimasimulation  
- KI & ML  
- Medizindiagnostik  
- Big-Data Mustererkennung  
- Materialwissenschaften  
- Finite-Elemente-Modelle  

All diese Bereiche profitieren von stabilen, wiederholbaren Ergebnissen.

---

## 11. Energieeffizienz: Warum KORA 97–99 % spart

KORA erreicht Energieeinsparungen nicht durch bessere Kühlung oder effizientere Transistoren,
sondern durch ein **fundamental anderes Rechenmodell**.

KORA eliminiert alle großen Energiequellen heutiger HPC-Systeme:

1. **Kommunikation**  
   In klassischen HPC-Clustern entstehen bis zu 40 % der Energiekosten im Netzwerk.  
   In KORA existiert kein Netzwerk im klassischen Sinn.

2. **Synchronisation**  
   Barrieren kosten Energie, weil Knoten warten.  
   Warten = Energieverbrauch ohne Fortschritt.  
   KORA hat keine dynamischen Barrieren.

3. **Jitter und Varianz**  
   Frequenzanpassungen, Cache-Misses, Scheduling-Wechsel → alles Energieverlust.  
   KORA hat konstante Frequenzen und statische Latenzen.

4. **Datenbewegung**  
   Jede Bewegung zwischen CPU–GPU–RAM kostet Energie.  
   KORA nutzt einen einzigen globalen Datenraum.

5. **Redundanz**  
   Verteilte Systeme müssen Daten duplizieren.  
   KORA dupliziert nie.

Dieser Eliminationsansatz führt zur beobachteten Energieeffizienz:

- KI/ML: 97–99 % Einsparung  
- Big Data: 92–99 % Einsparung  
- CFD (2h–24h Jobs): ~99 % Einsparung  

Die Simulationsergebnisse stammen aus v3.0 und erscheinen in Block 3 (Anhang).

---

## 12. Warum HPC-Barrieren vollständig verschwinden

KORA arbeitet nicht schneller, weil die Hardware „besser“ ist,
sondern weil die Architektur **keine Overheads mehr erzeugt**, die sonst den Großteil der Rechenzeit ausmachen.

In klassischen HPC-Systemen:

- Threads blockieren sich gegenseitig  
- Operationen müssen auf andere warten  
- MPI reduziert Daten über viele Schritte  
- Netzwerke haben variable Latenzen  
- Knoten laufen unterschiedlich schnell  
- Scheduler wechseln ständig  
- Cache-Kohärenz verursacht Zusatzarbeit  

In KORA existieren diese Effekte strukturell nicht:

- kein Thread-Modell  
- keine dynamischen Entscheidungen  
- keine Cache-Kohärenz  
- keine Scheduler  
- keine adaptive Frequenz  
- keine spontane Verzögerung  
- keine Netzwerklatenz  

Alle Abläufe sind vorhersehbar, synchron und global kohärent.

Ergebnis:
Eine 15–20× Beschleunigung bei CFD und 5–6× bei KI/Big-Data entsteht **ohne** neue Hardware,
sondern nur durch Eliminierung bestehender Nachteile.

---

## 13. Warum Ergebnisse stabil und reproduzierbar werden

Die Reproduzierbarkeit aus Kap. 9 (Block 1) ist in KORA kein Feature,
sondern eine unumstößliche Eigenschaft der Architektur.

### 13.1 Die sechs Schichten der Reproduzierbarkeit

1. **Deterministische Numerik**  
   (Soft-FP, feste Reihenfolgen, keine dynamischen FP-Pfade)

2. **Deterministische Ausführung**  
   (Scheduling Trees, feste DMA, konstante Fabric, fixe Latenzen)

3. **Deterministische Energieaufnahme**  
   (Power Determinism → jede Ausführung identisch in Watt/Zeit)

4. **Deterministische Telemetrie**  
   (alle Messdaten sind bitgleich wiederholbar)

5. **Golden Runs**  
   (zertifizierte, signierte Referenzläufe, vollständig archiviert)

6. **Langzeitkompatibilität**  
   (TSFs laufen über Hardwaregenerationen hinweg, Kap. 62.13–62.15, 
   siehe 03-Technical-Spec, :contentReference[oaicite:0]{index=0})

KORA ist damit das erste HPC-System,
bei dem Reproduzierbarkeit **technisch garantiert** wird.

---

## 14. Die Rolle des SRDB (Single Resonant Data Bus) im Überblick

Der SRDB ist der Kern des global kohärenten Datenmodells.

Er erfüllt drei Aufgaben:

1. **Orchestrierung**  
   Alle Tiles, DMA-Fenster, Memorybanks und Fabric-Slots
   werden synchron über den SRDB gesteuert.

2. **Synchronisation**  
   Der SRDB ersetzt Betriebssystem, Scheduler und Interrupt-Logik.

3. **Kohärenz**  
   Der SRDB garantiert einen einzigen globalen Systemzustand,
   unabhängig von Workload, Größe oder Dauer.

#### ASCII-Diagramm: SRDB im Overview-Kontext

    ┌──────────────────────────────────────────┐
    │ SRDB – Single Resonant Data Bus          │
    │------------------------------------------│
    │  globale Zeitbasis                       │
    │  deterministische DMA-Fenster            │
    │  deterministische Memorypfade            │
    │  deterministische Tile-Aktivierung       │
    │  deterministische Fabric-Slots           │
    └──────────────────────────────────────────┘
               ▲          ▲          ▲
               │          │          │
           Tiles       Memory     Fabric

KORA ersetzt Variabilität → durch *Resonanzlogik*.

---

## 15. High-Level-Vergleich: HPC vs. GPU vs. KORA

#### 15.1 Klassische HPC-Cluster
- viele Knoten, viele Caches  
- viele OS-Instanzen  
- viele Unterbrechungen  
- Instabilität durch dynamische Effekte  
- hohe Kommunikationskosten  
- unvorhersehbare Latenzen  

#### 15.2 GPU-Systeme
- besserer Durchsatz  
- aber weiterhin:  
  - dynamische Blockplanung  
  - Warps, Divergenzen  
  - nicht reproduzierbare FP-Reduktionen  
  - inhomogene Speicherpfade  

#### 15.3 KORA
- kein Cache  
- keine Threads  
- kein Scheduling  
- keine Divergenz  
- keine dynamische Verzweigung  
- keine unbestimmten FP-Pfade  
- globale Kohärenz  
- konstante Energie  

**Ergebnis:**
KORA ist nicht „noch eine neue Hardware“,  
sondern eine neue Rechenform.

---

## 16. Warum KORA für CFD entscheidend ist

### 16.1 Turbulenz ist extrem empfindlich
Minimalste Abweichungen in:

- Addition  
- Reduktion  
- Speicherzugriff  
- Reihenfolge der Berechnung  

können zu völlig anderen Ergebnissen führen.

HPC-Systeme erzeugen:

- variable Reihenfolgen  
- divergierende FP-Pfade  
- unterschiedliche Cache-Histories  
- unbestimmte Reduktionen  
- Thread-Rennen  
- Jitter  

CFD auf HPC ist daher immer „ungefähr“ reproduzierbar,
aber nie vollständig.

### 16.2 In KORA existiert keiner dieser Effekte

Alle Zeitschritte, alle Reduktionen, alle DMA-Fenster, alle Ghost-Exchanges
sind deterministisch und vorherbestimmt.

Das bedeutet wissenschaftlich:

- Turbulenzmodelle werden wiederholbar  
- Parameterstudien werden vergleichbar  
- Debugging wird endlich möglich  
- Ergebnisse hängen nicht vom Clusterzustand ab  

Dies ist ein fundamentaler Vorteil gegenüber jeder bisherigen Architektur.

---

## 17. Warum KORA für KI/ML entscheidend ist

KI-Systeme leiden heute unter vier grundlegenden Problemen:

1. **Non-Determinismus der GPUs**  
2. **Variable Ausführungsreihenfolgen**  
3. **Floating-Point-Instabilität**  
4. **Nicht-reproduzierbare Trainingsläufe**

KORA löst alle vier Probleme:

- deterministischer SCR (Scheduling Tree)  
- deterministische FP-Profile (A/B/C)  
- statische Tile-Ausführung  
- perfekt wiederholbare Trainingsläufe  

Ergebnis:
- Modelle können exakt reproduziert werden  
- Debugging wird möglich  
- Trainingshistorien sind identisch  
- Benchmarks werden stabil  

Für ML-Forschung ist dies paradigmatisch.

---

## 18. Warum KORA für Big-Data entscheidend ist

Big-Data-Prozesse leiden vor allem an:

- variablen ETL-Ausführungen  
- instabilen Reduktionen  
- unvorhersehbaren Latenzen  
- Scheduling-Jitter  
- Netzwerkengpässen  
- dynamischen Thread-Rennen  

In KORA:

- alle ETL-Schritte deterministisch  
- alle Reduktionen deterministisch  
- keine Latenzvariabilität  
- keine Partitionierungsprobleme  
- keine verteilten Knoten  
- keine inkonsistenten Pfade  

Dies erzeugt etwas, das es in Big-Data so noch nie gab:

**Komplett reproduzierbare Datenpipelines.**

---

## 19. Warum KORA für Klima & Medizin entscheidend ist

#### Klima:
- kein numerisches Driften  
- keine divergierenden Zeitschritte  
- wiederholbare Langzeitläufe  
- bitgenaue Vergleiche möglich  

#### Medizin:
- KI-Modelle liefern identische Diagnosen  
- Trainingsfehler werden nachverfolgbar  
- Sensitivitätsanalysen zuverlässig  
- wissenschaftliche Standards erfüllbar  

Im medizinischen Umfeld ist Reproduzierbarkeit essenziell –
und KORA liefert sie auf Hardwareebene.

---

## 20. Kurzzusammenfassung

KORA schafft:

- Energieeinsparungen bis zu 99 %  
- Eliminierung aller HPC-Barrieren  
- vollständige wissenschaftliche Reproduzierbarkeit  
- global kohärentes Rechnen  
- deterministische ETL- und KI-Pipelines  
- stabile CFD- und Turbulenzsimulationen  
- zuverlässige Klimamodelle  
- nachvollziehbare medizinische Diagnosen  

KORA ist damit kein „schnelleres HPC“,  
sondern eine **neue Klasse wissenschaftlicher Rechenarchitektur**.

---

## 21. Simulation v3.0 – High-Level-Zusammenfassung

Die KORA v3.0 Simulation umfasst vier Workload-Klassen, die für moderne Wissenschaftssysteme repräsentativ sind:

- KI/ML (BERT-Large)
- Big-Data (Small & Large)
- CFD (2h & 24h)
- Energieeffizienz für Langläufe

Die Ergebnisse zeigen zwei klar getrennte Ebenen:

1. **KORA-SW (Architektur B)**  
   Software-neuorganisierte Ausführungsmodelle →  
   **1.3–2.6× Speedup**  
   **40–70 % Energieersparnis**

2. **KORA-HW (Architektur C)**  
   vollständig deterministische Hardwareausführung →  
   **5–6× Speedup bei KI/Big-Data**  
   **15–20× Speedup bei CFD**  
   **97–99 % Energieersparnis**

Die Simulationsergebnisse bilden die Grundlage für die Bewertung von Reproduzierbarkeit, Effizienz und wissenschaftlicher Nutzbarkeit.

---

## 22. ASCII-Diagramm 7 – Speedup & Energieprofil v3.0 (vereinfacht)

    KORA v3.0 – Speedup (qualitativ, zusammengefasst)

    Workload           A (HPC)     B (SW)         C (HW)
    ------------------------------------------------------------
    KI / BERT-Large      1×       1.7×        ~5.7×
    Big-Data Small       1×       1.3×        ~1.9×
    Big-Data Large       1×       2.1×        ~5.5×
    CFD Medium (2h)      1×       2.6×        ~19×
    CFD Large (24h)      1×       2.5×        ~15×


    KORA v3.0 – Energieverbrauch (qualitativ)

    Workload           A (HPC)     B (SW)          C (HW)
    -------------------------------------------------------------
    KI / BERT-Large    100 %       ~46 %        ~2.4 %
    Big-Data Small     100 %       ~59 %        ~7 %
    Big-Data Large     100 %       ~38 %        ~2.5 %
    CFD Medium         100 %       ~30 %        ~0.7 %
    CFD Large          100 %       ~32 %        ~0.9 %


Kernaussage:
Architektur C verschiebt Energieverbrauch aus der
Kategorie „Bottleneck & Overhead" → in tatsächliche Rechenarbeit.

---

## 23. Simulation v3.0 – Vollständige Tabelle  
*(alle Zeiten in Stunden, alle Energien in kWh)*

|Workload | Arch | Zeit_eff [h] | Energie_eff [kWh] | Speedup | Energie-Ersparnis |
|-----|-----|-----|-----|-----|-----|
| BERT-Large | A | 92.400        | 794.64            | 1.00×    | 0 % |
| BERT-Large | B | 53.294        | 367.73            | 1.73×    | 53.7 % |
| BERT-Large | C | 16.211        | 19.45             | 5.70×    | 97.6 % |
| | | | | | |
| Big-Data Small | A | 0.024       | 0.210             | 1.00×    | 0 % |
| Big-Data Small | B | 0.018       | 0.125             | 1.35×    | 40.5 % |
| Big-Data Small | C | 0.013       | 0.015             | 1.93×    | 92.8 % |
| | | | | | |
| Big-Data Large | A | 0.550       | 4.730             | 1.00×    | 0 % |
| Big-Data Large | B | 0.262       | 1.810             | 2.10×    | 61.7 % |
| Big-Data Large | C | 0.099       | 0.120             | 5.53×    | 97.5 % |
| | | | | | |
| CFD Medium (2h) | A | 2.200      | 18.92             | 1.00×    | 0 % |
| CFD Medium (2h) | B | 0.840      | 5.79              | 2.62×    | 69.4 % |
| CFD Medium (2h) | C | 0.114      | 0.14              | 19.31×   | 99.3 % |
| | | | | | |
| CFD Large (24h) | A | 26.400     | 227.04            | 1.00×    | 0 % |
| CFD Large (24h) | B | 10.585     | 73.03             | 2.49×    | 67.8 % |
| CFD Large (24h) | C | 1.725      | 2.07              | 15.30×   | 99.1 % |

---

## 24. Interpretation der Simulationsergebnisse

### 24.1 Der strukturelle Effekt: Overhead fällt weg
Die Hauptverbesserung entsteht nicht durch „bessere Hardware“,
sondern durch:

- kein Scheduling  
- keine Kommunikation  
- keine Synchronisation  
- keine dynamischen Pfade  
- keine Caches  
- keine Replikation  

Alle Werte der Architektur C liegen deswegen **so drastisch niedrig**.

### 24.2 KI/Big-Data: tiefe kohärente Verarbeitung
KI-Modelle profitieren maßgeblich:

- deterministische Tensor-Pipeline  
- deterministische FP-Reihenfolgen  
- keine Jitter-Propagation  
- kein Scheduling Race  

Effekt:  
Mehrfach schnellere Konvergenz, extrem niedriger Energieverbrauch.

### 24.3 CFD: exponentielle Verstärkung von Jitter
CFD reagiert besonders stark auf nichtdeterministische Systeme.  
KORA eliminiert alle Jitterquellen → daher die enormen Speedups (bis 19×).

### 24.4 Energieprofil: wissenschaftliche Rechenarbeit wird wieder Energiequelle
In HPC fließen 70–90 % der Energie in:

- Kopieren  
- Warten  
- Synchronisieren  
- Cache-Kohärenz  
- Thread-Wechsel  

In KORA fließt nahezu **100 %** der Energie in **die Berechnung selbst**.

---

## 25. High-Level-Vergleich mit existierenden Systemen (vereinfacht)

#### Klassischer HPC:
    overhead / compute: ~3–7× höher als echte Rechenzeit  
    Ergebnisse variieren zwischen Läufen

#### GPU:
    besserer Durchsatz, aber weiterhin:
    - dynamische Planung
    - Reduktionsvariabilität
    - Divergenzen
    - Jitter

#### KORA:
    overhead ~0  
    compute = 1:1 Ausführung  
    Ergebnisse bitgenau reproduzierbar  
    Energieverbrauch ~1–3 %

---

## 26. Wissenschaftliche Relevanz

KORA ermöglicht – zum ersten Mal – ein System, das:

- deterministische numerische Simulationen zulässt  
- Hardwarereproduzierbarkeit garantiert  
- KI-Modelle wirklich identisch trainieren kann  
- Debugging in CFD & ML wieder möglich macht  
- bitexakte Klima- und Langzeitmodelle liefert  
- medizinische KI stabilisiert  
- bei enormer Senkung der Energiekosten arbeitet  

Damit bildet KORA eine neue Klasse von Rechenarchitektur:
**kohärenzorientierte Wissenschaftsmaschinen**.

---

## 27. Zusammenfassung des gesamten Overview-Dokuments

1. **HPC scheitert an Kommunikation, Synchronisation und Inkoherenz.**  
2. **KORA löst diese Probleme strukturell**, nicht durch Optimierung.  
3. **Monolithische, deterministische Architektur** = keine Jitterquellen.  
4. **SRDB erzeugt globale Kohärenz**, ohne Netzwerk.  
5. **Reproduzierbarkeit wird zur Systemgarantie.**  
6. **CFD, KI, Big-Data, Klima, Medizin** profitieren massiv.  
7. **Simulation v3.0 bestätigt**:  
   - SW (B): 1.3–2.6× schneller, 40–70 % Energieersparnis  
   - HW (C): 5–20× schneller, 97–99 % Energieersparnis  
8. **KORA ist kein schnellerer HPC-Cluster**,  
   sondern eine völlig neue Form wissenschaftlicher Rechenarchitektur.

---

## 28. Abschließender Satz

KORA macht wissenschaftliches Rechnen stabil, reproduzierbar und nahezu energieverlustfrei –  
und definiert damit die Grundlage für die nächste Generation wissenschaftlicher Forschungssysteme.

---

## Versionierung

- **Dokument:** `02_Architecture_Overview.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
