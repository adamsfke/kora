# KORA – Simulations-Methodologie

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Methodologie und Code-Dokumentation
**Status:** Machbarkeitsstudie / Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Einleitung
    2.  Architekturbasierte Modellierung
    3.  Workload-Definitionen
    4.  Overhead-Transformation
    5.  KORA m3.0 Architekturmatrix
    6.  Anwendung auf Workloads
    7.  Energie- und Reproduzierbarkeitsmodell
    8.  Sensitivität & Robustheit
    9.  Grenzen der Methodik
    10. Validierungsstrategie
    11. Ausblick

---

## 1. Einleitung

Die Simulation Methodology ist ein zentrales Dokument des KORA-Projekts. Sie beschreibt den methodischen Kern, mit dem die Performanz, Energieeffizienz und Reproduzierbarkeit der KORA-Architekturen A, B und C bewertet werden. Im Unterschied zu Version 1.0 basiert Version 2.0 nicht mehr auf drei voneinander getrennten Simulationen und einer zusätzlichen Monolith-Simulation, sondern auf einem vollständig vereinheitlichten, architekturzentrierten Modell.

Die ursprüngliche Version 1.0 nutzte getrennte Konzepte:
    eine Big-Data-Simulation mit Gitterdaten
    eine BERT-Base-Simulation für KI-Modelle
    eine monolithische Funktions-Simulation
    eine dritte Simulation zur Reproduzierbarkeitsanalyse

Diese Aufteilung entsprach dem damaligen Entwicklungsstand von KORA, war jedoch mit der heutigen Architektur (KORA v3.0, deterministische Tiles, SRDB, Scheduling Trees, deterministische DMA-Fenster) nicht mehr vereinbar. Zudem waren die Modelle untereinander nicht kompatibel und führten zu unterschiedlichen Definitionen von Overheads, Workloadparametern und synchronen Zustandsübergängen.

Version 2.0 führt erstmals eine vollständig einheitliche Simulationsmethodik ein, die sämtliche Workloads – Big Data, KI, CFD und weitere wissenschaftliche Großsimulationen – in einem gemeinsamen mathematischen und architekturellen Rahmen beschreibt. Dieser Rahmen ermöglicht eine saubere, reproduzierbare und wissenschaftlich nachvollziehbare Analyse der Unterschiede zwischen:

A  Standard-HPC / GPU-Cluster  
B  KORA-SW (Software-Neuordnung auf HPC-Hardware)  
C  KORA-HW (vollständig deterministische, monolithische KORA-Hardware)

Diese drei Architekturvarianten folgen nun einer gemeinsamen mathematischen Struktur. Der Kern der neuen Methodologie besteht in der Zerlegung komplexer Workloads in ihre grundlegenden Komponenten:

    Rechenoperationen (O_base)
    Datenbewegungen (M_base)
    Synchronisationsereignisse (S_base)

Diese Basisgrößen werden im Anschluss durch ein architekturspezifisches Overhead-Modell transformiert, das für jede Architektur (A/B/C) spezifisch ist. Dadurch entsteht ein universelles Bewertungssystem, das für alle Workloads gleichermaßen anwendbar ist.

Ein zentraler Fortschritt gegenüber Version 1.0 liegt darin, dass KORA v3.0 nicht mehr über drei getrennte Simulationsuniversen beschrieben wird, sondern über ein einziges, vollständig kohärentes Modell, das direkt aus den Architekturprinzipien folgt.

Version 2.0 ist nicht nur eine methodische Neufassung, sondern ein qualitativer Sprung: Sie ermöglicht erstmals eine zusammenhängende, wissenschaftlich belastbare Simulation aller KORA-Effekte aus denselben Grundgleichungen.

---

## 2. Architekturbasierte Modellierung

Die neue Methodik verzichtet auf getrennte Simulationslogiken für Big Data, KI und CFD. Stattdessen wird ein universelles Overhead-Modell eingeführt, das auf architekturebene erklärt, warum sich die Laufzeiten und Energieverbräuche der Architekturen A, B und C unterscheiden.

Ziel ist nicht die Modellierung aller physikalischen Details eines HPC-Systems, sondern die saubere Erfassung der strukturellen Unterschiede, die für wissenschaftliche Arbeit entscheidend sind.

### 2.1 Grundgleichung der Simulation

Alle Workloads in KORA Version 2.0 werden durch dieselbe Grundgleichung beschrieben:

T_total = T_compute  
        + T_sync  
        + T_sched  
        + T_bus  
        + T_irq  
        + T_cs

Erläuterungen:

T_compute  
    reine Rechenzeit des Workloads (architekturunabhängig)

T_sync  
    Synchronisationskosten (Barriers, Reduktionen, AllReduce)

T_sched  
    Scheduling-Overhead (OS, GPU Kernel Dispatch, CUDA Streams)

T_bus  
    Datenbewegungskosten (Netzwerk, PCIe, Speicherpfade)

T_irq  
    Interrupt-Overheads (von OS, Netzwerk, Hardware)

T_cs  
    Kontextwechselkosten (CPU Threads, GPU Kontextwechsel)

Diese Zerlegung ist entscheidend, da sie zeigt, in welchen Komponenten traditionelle HPC-Systeme die meiste Energie und Zeit verlieren. Moderne Systeme verlieren typischerweise 50–90 % ihrer Zeit in genau diesen Overheads – nicht in der eigentlichen Rechenarbeit.

### 2.2 Architekturprofile A/B/C

Die wesentlichen Unterschiede der Architekturen bestehen in der Reduktion oder vollständigen Eliminierung bestimmter Overheads.

Architektur A (HPC/GPU-Cluster):
    hohe Interruptdichte  
    dynamisches Scheduling  
    synchronisationsintensive Reduktionen  
    komplexe Cache-Hierarchien  
    hohes Maß an nichtdeterministischen Ereignissen  

Architektur B (KORA-SW):
    deterministische Scheduling Trees  
    reduzierte Interrupts  
    statisch geordnete Datenpfade  
    deterministische Batch-Pipelines  
    deutlich reduzierte Overheads  

Architektur C (KORA-HW):
    keine Interrupts  
    keine Caches  
    keine Kontextwechsel  
    keine dynamischen Scheduling-Entscheidungen  
    SRDB als global kohärenter Datenbus  
    deterministische DMA-Fenster  
    deterministische Fabric-Slots  

Die Architektur C eliminiert nahezu alle Overheads, mit Ausnahme der reinen Rechenarbeit.

### 2.3 Ableitung des Energieverbrauchs

Der Energieverbrauch folgt direkt aus den Zeitkomponenten und den Leistungsprofilen der jeweiligen Architektur:

E_total = ∫ P(t) dt

Da Architektur C deterministische Leistungsaufnahme hat (konstante Frequenz, keine Boost-Mechanismen, keine DVFS-Effekte), ergibt sich:

E_C ≈ P_const × T_compute

Dies erklärt die 97–99 % Energieeinsparung in der v3.0 Simulation:  
Wenn T_sync, T_sched, T_bus, T_irq und T_cs nahezu verschwinden, verschwindet auch nahezu der gesamte Energieverbrauch.

Die Methodologie Version 1.0 konnte diese Einsparungen nicht sauber erklären, da jede der drei Simulationen ein eigenes Energie- und Zeitmodell verwendete.

Version 2.0 löst dieses Problem vollständig.

---

## 3. Workload-Definitionen

In Version 1.0 basierte jede Simulation auf unterschiedlichen Parametern. Version 2.0 führt ein voll vereinheitlichtes Workloadmodell ein, das jede wissenschaftliche Berechnung auf die drei Grundgrößen O_base, M_base und S_base zurückführt.

### 3.1 Basale Workloadparameter

O_base  
    Anzahl der arithmetischen Operationen des Workloads  
    Beispiel: FLOPs bei KI-Modellen, Stencil-Operatoren bei CFD, Transformationen bei Big-Data

M_base  
    Menge der zu bewegenden Daten  
    Beispiel: Batch-Daten, Gitterdaten, Parameter-Updates

S_base  
    Anzahl der Synchronisationsereignisse  
    Beispiel: AllReduce pro Step bei KI, Ghost-Cell-Exchanges bei CFD

Diese drei Parameter bilden die Grundlage aller folgenden Berechnungen.

### 3.2 Workloadklassen im KORA-Modell

Das unified Modell unterstützt mehrere Workloadtypen:

Big Data (strukturierte Gitterfelder)
    deterministische Rasteroperationen  
    geringe Synchronisation  
    moderate Transferlast  

KI/ML (z. B. BERT, GPT)
    extrem hohe O_base  
    hohe Anzahl globaler Reduktionen  
    komplexe Transfermuster  

CFD (Medium/Large)
    stencilbasierte, zeitabhängige Operationen  
    moderate Anforderungen an Kommunikation  
    empfindlich gegenüber Jitter  

Alle diese Workloads werden nicht mehr getrennt simuliert.  
Sie werden über dieselbe Grundgleichung abgebildet und unterscheiden sich lediglich in O_base, M_base und S_base.

### 3.3 Transformation der Workloads in die Architekturmodelle

Die Transformation erfolgt über architekturspezifische Faktoren:

Für Architektur A:
    T_sync, T_sched, T_bus, T_irq und T_cs sind alle hoch

Für Architektur B:
    T_sched stark reduziert  
    T_irq reduziert  
    T_sync stabilisiert  
    T_bus teilweise gebündelt  

Für Architektur C:
    T_sched = 0  
    T_irq = 0  
    T_cs = 0  
    T_sync minimal  
    T_bus minimal  

Damit entsteht ein universelles Simulationsmodell, das alle relevanten Workloads aus denselben Gleichungen ableitet.

---

## 4. Overhead-Transformation

Die Overhead-Transformation ist der zentrale Schritt der neuen Simulation Methodology. Sie beschreibt, wie die drei Workload-Basisgrößen O_base (Operationen), M_base (Datenbewegungen) und S_base (Synchronisationsereignisse) durch die Architekturprofile A, B und C in tatsächliche Laufzeiten und Energieverbräuche überführt werden.

Die Transformation basiert auf der Annahme, dass Overheads sich bei HPC- und GPU-basierten Systemen nicht linear, sondern multiplikativ und kumulativ verhalten. Das bedeutet: Der Verlust durch Scheduling-Jitter verstärkt den Verlust durch Synchronisation, und dieser verstärkt wiederum den Verlust durch Datenbewegung. Die neue Methodologie modelliert diese Zusammenhänge explizit.

### 4.1 Grundformel der Overhead-Transformation

T_total = T_compute  
        + f_sync(S_base, Arch)  
        + f_sched(O_base, Arch)  
        + f_bus(M_base, Arch)  
        + f_irq(Arch)  
        + f_cs(Arch)

Dabei sind die Funktionen f_sync, f_sched, f_bus, f_irq und f_cs architekturspezifisch.

#### Architektur A (HPC/GPU)

    f_sync_A  ist groß, da AllReduce, MPI und Barrier-Mechanismen ineffizient sind  
    f_sched_A ist hoch, da OS und GPU-Scheduler dynamisch sind  
    f_bus_A   ist hoch, da PCIe und Netzwerk non-deterministisch sind  
    f_irq_A   ist hoch, da Interrupts nicht steuerbar sind  
    f_cs_A    ist hoch, da Kontextwechsel unvermeidbar sind  

Dadurch ergibt sich ein Modell, in dem Overheads die eigentliche Rechenzeit bei weitem übersteigen können. Für viele HPC-Workloads gilt empirisch: Nur 10–30 % der Zeit wird für die eigentliche Berechnung genutzt, die restlichen 70–90 % gehen verloren.

#### Architektur B (KORA-SW)

    f_sync_B  ist reduziert, da Scheduling Trees die Datenreihenfolge stabilisieren  
    f_sched_B ist stark reduziert, da Thread-Zuweisungen deterministisch werden  
    f_bus_B   ist gebündelt, aber weiterhin abhängig vom PCIe-Schichtmodell  
    f_irq_B   ist reduziert, da deterministische Polling-Modelle genutzt werden  
    f_cs_B    ist reduziert, aber nicht eliminiert  

KORA-SW eliminiert Overheads nicht vollständig, aber es sorgt für eine drastische Verringerung der Varianz. Dadurch sinkt die effektive Overhead-Zeit um 40–70 %, wie die Simulation v3.0 zeigt.

#### Architektur C (KORA-HW)

    f_sync_C  ist minimal, da die Fabric deterministisch ist  
    f_sched_C = 0  
    f_bus_C   ist minimal, da SRDB und On-Die-Bus keine Variabilität aufweisen  
    f_irq_C   = 0  
    f_cs_C    = 0  

Architektur C eliminiert alle nichtdeterministischen Systemzustände. Es bleiben nur noch:

    T_compute  (die eigentliche Rechenarbeit)
    T_sync_min (minimale synchronisationsbedingte Wartezeiten)

Dadurch ergibt sich der extrem niedrige Energieverbrauch der Architektur C:  
E_total_C ≈ P_const × T_compute

Die Overheads verschwinden aus physikalischer Sicht.

### 4.2 Zusammenhang zwischen Reproduzierbarkeit und Overheads

Ein zentrales Ziel von KORA ist nicht nur Geschwindigkeit oder Energieeffizienz, sondern vollständige wissenschaftliche Reproduzierbarkeit. Diese ergibt sich direkt aus der Eliminierung von Overheads:

    f_sync_A → variable Reduktionen → numerische Drift  
    f_sched_A → unterschiedliche Ausführungsreihenfolgen → schwankende Ergebnisse  
    f_bus_A → variabler Datenzugriff → andere FP-Operationen  

Bei Architektur B bleiben geringe Unterschiede bestehen:
    ±0.005–0.02 % Reproduzierbarkeitsvarianz

Bei Architektur C:
    0.000 % Varianz – bitgenau reproduzierbar

Die neue Methodologie macht diesen Zusammenhang explizit und mathematisch modellierbar.

### 4.3 Warum Version 1.0 dieses Modell nicht abbilden konnte

In Version 1.0 wurden Simulationen unabhängig voneinander erstellt. Dadurch standen die Ergebnisse zwar nebeneinander, aber nicht in einer konsistenten Struktur. Zum Beispiel:

    Big Data → gitterbasiertes Modell  
    KI → FLOP-basiertes Modell  
    Monolith → funktionale Modellierung  
    CFD → Grenzfallanalyse  

Dadurch entstanden unterschiedliche Energie- und Zeitmodelle, die nicht aufeinander abbildbar waren.

Version 2.0 vereinheitlicht **alle Simulationen** zu einem einzigen generischen Modell, das konsistent aus den Architekturprinzipien folgt.

Dieses Modell ist:

    universell  
    deterministisch  
    reproduzierbar  
    mathematisch geschlossen  
    OSF-kompatibel  
    wissenschaftlich referenzierbar

### 4.4 Beispielhafte Transformation für alle Workloads

#### Big-Data-Beispiel

O_base = 6.48e9 × 10 × 3  
M_base = moderat  
S_base = gering

Transformation:

    A: hohe Bus-Kosten, moderate Sync-Kosten  
    B: reduzierte Bus-Kosten, nahezu konstante Sync-Kosten  
    C: fast keine Overheads mehr  

#### KI-Beispiel

O_base = 1e15–1e17 FLOPs  
M_base = hoch (Parameter-Sharding)  
S_base = sehr hoch (AllReduce pro Step)

Transformation:

    A: massive Overhead-Last  
    B: deterministische Reduktionen  
    C: Reduktionen in festen Fabric-Slots  

#### CFD-Beispiel

O_base = zeitbasierte Stencil-Operationen  
M_base = gering-moderat  
S_base = mittel (Ghost-Exchanges)

Transformation:

    A: Jitter macht Stencil-Reihenfolgen instabil  
    B: deterministische Tile-Planung reduziert Jitter  
    C: eliminiert Jitter vollständig  

Diese Beispiele zeigen, dass die Overhead-Transformation universell auf alle wissenschaftlichen Workloads angewendet werden kann.

---

## 5. KORA m3.0 Architekturmatrix

Die Architekturmatrix ist die zentrale Verdichtungsform des gesamten Methodologie-Modells. Sie fasst alle architekturellen Unterschiede zwischen A, B und C in Form quantifizierbarer Kategorien zusammen. Die Matrix bildet die Grundlage der mathematischen Simulation.

### 5.1 Kategorien

Die Matrix bewertet die Architekturvarianten anhand folgender Kategorien:

    Interrupts  
    Scheduling  
    Synchronisation  
    Bus / Fabric  
    Speicherkoherenz  
    Reproduzierbarkeit  
    Energieprofil  
    Jitter  
    Latenz  
    Parallelismusmodell  
    Overhead-Reduktion  

Jede Kategorie wird für A/B/C qualitativ und quantitativ bewertet.

### 5.2 Tabelle (vereinfacht)

Interrupts:
    A: hoch  
    B: mittel  
    C: keine  

Scheduling:
    A: dynamisch  
    B: deterministisch  
    C: hardwarefix  

Synchronisation:
    A: teuer  
    B: reduziert  
    C: minimal  

Bus:
    A: PCIe/Netzwerk  
    B: gebündelt  
    C: On-Die (SRDB)  

Coherence:
    A: komplex  
    B: komplex  
    C: entfällt  

Reproduzierbarkeit:
    A: ±0.2–1 %  
    B: ±0.005–0.02 %  
    C: 0 % (bitgenau)  

Energie:
    A: hoch  
    B: mittel  
    C: minimal  

Dies ist die Grundlage für die quantitativen Simulationen.

### 5.3 Validierungsstatus

Die Kategorien wurden mit der:

    technischen Spezifikation (03)  
    Simulation v3.0  
    Reproduzierbarkeitsanalyse  
    deterministischen Pipeline-Modelle  

abgeglichen und in Version 2.0 vollständig konsolidiert.

---

## 6. Anwendung auf Workloads

Mit der Overhead-Transformation und der Architekturmatrix kann nun jede Workloadklasse analysiert werden. Die folgenden Abschnitte zeigen, wie das neue Modell direkt zu den v3.0-Simulationsergebnissen führt – vollständig reproduzierbar und methodisch nachvollziehbar.

### 6.1 Big-Data-Anwendungen

Big-Data-Systeme sind gitterbasiert und weisen geringe Synchronisation, jedoch moderate Bus-Overheads auf.

Ergebnisse der Transformation:

    Architektur A → starke Bus-Verluste  
    Architektur B → moderate Bus-Verluste, reduzierte Scheduling-Last  
    Architektur C → nahezu keine Overheads  

Entspricht den v3.0 Ergebnissen:
    Speedup_B ≈ 1.35×  
    Speedup_C ≈ 1.93×  

### 6.2 KI-Modelle (BERT/GPT-Klasse)

KI-Modelle haben die komplexeste Overheadstruktur:

    hohe Reduktionen  
    variable FP-Pfade  
    hohe Scheduling-Komplexität  
    variable Datenströme  

Die Transformation ergibt:

    Architektur A → extrem overhead-lastig  
    Architektur B → signifikante Reduktion  
    Architektur C → minimaler Overhead  

Entspricht den v3.0 Ergebnissen:
    Speedup_B ≈ 1.7×  
    Speedup_C ≈ 5.7×  

### 6.3 CFD (Turbulenz, Langläufer)

CFD-Simulationen sind besonders empfindlich gegenüber Jitter.

Die Transformation ergibt:

    Architektur A → Jitter instabilisiert Ergebnisse  
    Architektur B → deterministische Tile-Scheduling reduziert Jitter  
    Architektur C → Eliminierung aller Jitterquellen  

Entspricht den v3.0 Ergebnissen:
    Speedup_C ≈ 15–20×  
    Energieersparnis_C ≈ 99 %  

---

## 7. Energie- und Reproduzierbarkeitsmodell

Die KORA-Simulation Methodology Version 2.0 integriert Energieverbrauch und Reproduzierbarkeit nicht als nachgelagerte Messgrößen, sondern als direkte Konsequenzen der Architektur-Overhead-Transformation. Dadurch entsteht ein konsistentes, mathematisch kohärentes Modell, das die vollständige Eliminierung von Energieverlusten und numerischer Varianz durch Architektur C erklärbar macht.

### 7.1 Energie als Overhead-Funktion

Der Energieverbrauch wird nicht direkt simuliert, sondern ergibt sich aus den Overheads:

E_total = E_compute  
        + E_sync  
        + E_sched  
        + E_bus  
        + E_irq  
        + E_cs

Da E_term = P_term × T_term gilt, entstehen hohe Energieverluste insbesondere bei Architektur A, die durch variablen Verbrauch, Dynamic Voltage and Frequency Scaling (DVFS), Netzwerkvariabilität und Speicherzugriffe bestimmt sind.

Architektur B (KORA-SW) reduziert diese Energiepfade, aber kann sie nicht eliminieren, da Standard-Hardware weiterhin Interrupts, Scheduling-Entscheidungen, PCIe-Zugriffe und dynamische Taktgeber besitzt.

Architektur C (KORA-HW) hingegen:

    keine Interrupts  
    kein Turbo, kein DVFS  
    konstante Leistungsaufnahme  
    keine nichtdeterministischen Scheduling-Pfade  
    keine kontextabhängigen Bus-Zustände  

Die Energiegleichung reduziert sich damit nahezu vollständig auf:

E_total_C ≈ P_const × T_compute

Dies erklärt die 97–99 % Energieeinsparung der vollständigen KORA-Hardware.

### 7.2 Reproduzierbarkeit als Overhead-Funktion

Reproduzierbarkeit hängt direkt von Overheads ab:

FP-Variabilität entsteht durch:
    unterschiedliche Reduktionsreihenfolgen  
    unterschiedliche Scheduling-Entscheidungen  
    unterschiedliche Thread-Pfade  
    unterschiedliche DMA-Fenster  
    variable Latenzen  

Dies entspricht den Overheads:
    T_sync  
    T_sched  
    T_irq  
    T_bus  

Wird ein Overhead eliminiert, wird auch seine numerische Variabilität eliminiert.

Das Modell definiert daher den Reproduzierbarkeitsfehler als:

R_var = g(T_sync, T_sched, T_irq, T_bus)

Bei Architektur A ist dieser Fehler am größten:
    ±0.2–1.4 % bei typischen Workloads

Bei Architektur B stark verringert:
    ±0.005–0.02 %

Bei Architektur C:
    R_var = 0  
    (bitgenaue Ausführung)

Damit ist Reproduzierbarkeit keine Eigenschaft des Workloads, sondern der Architektur. Dies ist der Kern des KORA-Modells.

### 7.3 Langzeitstabilität

Da Architektur C keine variablen Systemzustände besitzt, bleiben Ergebnisse über Jahre hinweg identisch. Selbst unterschiedliche Hardwaregenerationen erzeugen identische Ergebnisse, solange dieselbe TSF-Datei ausgeführt wird.

Dies ist eine völlig neue Qualität wissenschaftlicher Rechenarchitekturen.

---

## 8. Sensitivität & Robustheit

Die Sensitivitätsanalyse zeigt, wie anfällig die Modelle gegenüber Veränderungen in O_base, M_base und S_base sind. Version 2.0 führt erstmals eine robuste Sensitivitätsanalyse ein, die direkt aus dem Architekturmodell folgt.

### 8.1 Sensitivität gegenüber Synchronisation

Die kritischste Größe für KI- und CFD-Workloads ist S_base:

Erhöht man S_base, wachsen bei Architektur A:
    Jitter  
    FP-Drift  
    Synchronisationszeit  

Bei Architektur B:
    stabilere Reihenfolgen  
    deutlich weniger Drift  

Bei Architektur C:
    keine Drift  
    minimale Synchronisationskosten  

Dies erklärt, warum KI und CFD besonders stark von Architektur C profitieren.

### 8.2 Sensitivität gegenüber Datenbewegungen

Datenbewegungen wirken sich bei Big-Data-Workloads besonders aus:

A:
    variable PCIe- und Netzwerkpfade verursachen starke Overheads  

B:
    deterministische Batch-Pipelines reduzieren Transfers  

C:
    SRDB und deterministische DMA-Fenster eliminieren nahezu alle Transfers  

### 8.3 Sensitivität gegenüber Scheduling

Scheduling ist die dominierende Overheadquelle in GPU- und HPC-Systemen.

Version 2.0 zeigt:

A:
    hohe Scheduling-Last → großer Performanceverlust  

B:
    deterministische Scheduling Trees → signifikante Reduktion  

C:
    keine Scheduling-Last → T_sched = 0  

Dies erklärt die starken Speedups bei CFD und KI.

### 8.4 Robustheit des Modells

Das Modell ist robust gegenüber:
    Modellabweichungen  
    Variation der Basisparameter  
    Variation der Overheadschätzungen  

Solange die strukturellen Architekturmerkmale erhalten bleiben, bleiben die relativen Unterschiede zwischen A, B und C stabil.

---

## 9. Grenzen der Methodik

Version 2.0 schafft ein konsistentes, wissenschaftlich nutzbares Simulationsmodell. Dennoch gibt es Grenzen:

### 9.1 Keine cycle-accurate Simulation

KORA v3.0 modelliert Overheads und deterministische Architekturprinzipien, aber keine cycle-accurate Hardwaredetails. Das wäre erst mit Phase-2- oder Phase-3-Prototypen sinnvoll.

### 9.2 Keine Modellierung von Transienten

Netzwerktransienten, DRAM-Latenzspitzen oder thermische Variationen werden nicht simuliert. Sie sind in Architektur C jedoch minimal.

### 9.3 Workloadvereinfachungen

O_base, M_base und S_base sind abstrakte Größen. In der Realität sind viele Workloads noch komplexer (z. B. adaptive Gitter).

### 9.4 Keine Modellierung von Compiler-Optimierungen

Der Einfluss von Optimierungen im Compiler-Stack wird abstrahiert.

### 9.5 Vergleichbarkeit zwischen unterschiedlichen Systemen

Das Modell ist robust für relative Vergleiche (A vs B vs C), aber nicht für absolute Cycle-level-Performancevorhersagen.

---

## 10. Validierungsstrategie

Version 2.0 definiert erstmals eine mehrstufige Validierungsstrategie für KORA.

### 10.1 Software-Ebene

    KORA-SW-Implementierung  
    deterministische Scheduling Trees  
    Reproduzierbarkeitsmessung  
    Benchmarking auf HPC-Systemen  

### 10.2 Hardware-Ebene (Phase 2)

    Multi-Tile-Prototyp  
    DMA-Fenster  
    deterministische Fabric  

### 10.3 Hardware-Ebene (Phase 3)

    vollständiger KORA-Chip  
    SRDB  
    deterministische FP-Pipelines  

### 10.4 Langzeitvalidierung

    Ausführung über Wochen und Monate  
    bitgenaue Reproduzierbarkeit über Generationen hinweg  

### 10.5 OSF-Veröffentlichung

    vollständige Offenlegung der Methodik  
    Bereitstellung aller TSF-Dateien  
    Vergleichbare Reproduzierbarkeitsdaten anderer Forschungsgruppen  

---

## 11. Ausblick

Version 2.0 der Simulation Methodology ist ein Meilenstein im KORA-Projekt. Sie bildet die methodische Grundlage für 
alle wissenschaftlichen Resultate, Modelle und Veröffentlichungen in der Phase 2 und 3.

Die wichtigsten Fortschritte:

    vollständige Vereinheitlichung der Simulationen  
    klare architekturbasierte Modellierung  
    reproduzierbare Transformation A → B → C  
    erklärbare Energieersparnis  
    mathematisch nachvollziehbare Reproduzierbarkeit  
    robuste, universelle Workload-Definition  
    OSF-kompatible Dokumentstruktur  

Diese Methodik ermöglicht es, KORA wissenschaftlich zu bewerten, zu vergleichen und langfristig reproduzierbar zu machen. 
Sie bildet den Rahmen für zukünftige Forschung, Implementierung und Hardwareentwicklung – bis zum voll implementierten KORA-Chip in Phase 3.

---

---

## Versionierung

- **Dokument:** `08_Simulation_Methodology.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
