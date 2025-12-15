# KORA – Architecture Specification (Version 2.0)

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Fundierte Architekturdefinition für effiziente, deterministische und reproduzierbare Hochleistungsberechnung
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Motivation
    2.  Limitierungen heutiger HPC-Architekturen
    3.  Warum FLOPs nicht mehr entscheidend sind
    4.  Reproduzierbarkeit und Determinismus
    5.  Anforderungen an moderne HPC-/KI-Architekturen
    6.  Die fünf Designprinzipien von KORA
    7.  Architekturübersicht (A/B/C) und systemische Rollen
    8.  Die Rolle des v3.0-Simulationsmodells in der Architektur
    9.  Der KORA-Monolith: Einleitung & Gesamtüberblick
    10. Tile-Classification: Die strukturellen Grundbausteine des Monolithen
    11. Tile-Microarchitecture 
    12. Memorybank-Layout 
    13. Memory Arbitration Logic 
    14. On-Die TDM Fabric 
    15. SRDB Architecture 
    16. Deterministische Scheduling Trees 
    17. Synchronisationsmechanismen 
    18. Execution Pipeline: Datenfluss, Instruktionsfluss, deterministischer Ablauf
    19. Fehlerbehandlung & Resilienz im deterministischen System
    20. Power Architecture & Thermal Design 
    21. Scaling Behaviour & System Integration 
    22. Software Interaction Model 
    23. Memory Model & Data Layout 
    24. Programming Model 
    25. Device & I/O Model 
    26. Verification & Deterministic Guarantees 
    27. Data Center Integration & Deployment 
    28. Boot, Configuration & Control Flow 
    29. Control Plane, Data Plane & Telemetry 
    30. Benchmarking, Validation & Performance Modeling 
    31. Formal Performance & Energy Modeling 
    32. Scientific Validation & Numerical Stability 
    33. Simulation & Emulation Framework 
    34. Software Ecosystem Integration 
    35. Interoperability & External Interfaces 
    36. Cluster Communication & Deterministic Multi-Compute 
    37. Security, Integrity & Fault Domains 
    38. Orchestration, Scheduling & Workflow Control 
    39. Monitoring, Telemetry & Deterministic Observability 
    40. Evolution & Next-Generation Architecture 
    41. Compliance, Validation & Scientific Trust 
    42. End-to-End Pipeline: From Model to Deterministic Execution 
    43. Governance, Operational Model & Scientific Stewardship 
    44. Documentation, Publishing & Long-Term Knowledge Architecture
    45. Applied KORA: Scientific & Industrial Use Cases
    46. Sustainability, Efficiency & Long-Term Operational Impact
    47. Glossary of Terms 
    48. Acronyms & Abbreviations 
    49. Appendix A: Mathematical Foundations of Deterministic Scheduling
    50. Appendix B: TSF Format Specification
    51. Appendix C: Reference Simulator Architecture
    52. Appendix D: Project Structure & Repository Layout
    53. Appendix E: Reference Tables for Energy & Time Calculations
    54. Appendix F: Deterministic Error Handling & Fault Models
    55. Appendix G: Deterministic Numerical Models (Soft-FP & Exact Arithmetic)
    56. Appendix H: Validation Test Suite Specification
    57. Appendix I: TSF Transformation & Optimization Rules
    58. Appendix J: Reference Workload Definitions
    59. Appendix K: Security & Integrity Model
    60. Appendix L: Hardware Physical Layout & Signaling
    61. Appendix M: Deterministic Cluster Topologies
    62. Appendix P: Reproducibility Protocol for Long-Term Studies
    63. Appendix Q: Deterministic API & Host Interface Specification (HAPI & SCI)
    64. Appendix R: Formal Proofs of Determinism (Extended)
    65. Appendix S: Energy Modeling Framework (Extended)
    66. Appendix T: Deterministic I/O & Storage Model
    67. Appendix U: Reference Cluster Deployment Guide
    68. Appendix V: Educational Examples
    69. Appendix W: Glossary of Deterministic Computing Concepts
    70. Appendix X: Comparison with Classical Systems (non-normative)

---

## 1. Motivation

Die Entwicklung moderner Rechenarchitekturen befindet sich an einem Wendepunkt.
Während über Jahrzehnte die Leistungsfähigkeit vor allem durch höhere
Taktfrequenzen, größere Vektorregister und steigende FLOP-Kapazitäten bestimmt
war, zeigt sich heute ein strukturelles Plateau: Die Geschwindigkeit komplexer
wissenschaftlicher und KI-bezogener Workloads wächst nicht mehr proportional zur
verbauten Rechenleistung. Trotz massiver Parallelisierung und fortschrittlicher
Beschleunigerarchitekturen stagnieren reale Durchsatzraten, und der Energiebedarf
steigt weiter an.

In großskaligen Anwendungen – insbesondere im Bereich künstlicher Intelligenz,
Big-Data-Verarbeitung, numerischer Simulationen und Klima-/Wettermodellierung –
entsteht eine systemische Kluft zwischen theoretischer Rechenkapazität und
tatsächlicher Nutzleistung. Diese Lücke wird zunehmend durch nicht-lineare
Overheads bestimmt, die weder triviale Optimierungen noch lineare Skalierung
zulassen:

- Memory-Bandbreiten und Latenzen dominieren die Ausführungszeit,
- Netzwerkkommunikation wächst schneller als die FLOP-Leistung,
- globale Synchronisationsbarrieren limitieren die Skalierung,
- nichtdeterministische Scheduling-Pfade erschweren Reproduzierbarkeit,
- Energieeffizienz verschlechtert sich proportional zur Systemgröße.

Die Folge ist eine paradoxe Situation:  
**Rechenzentren werden größer, komplexer und energieintensiver – doch die Zeit bis zur Lösung eines Problems verringert sich kaum.**

Für die Wissenschaft bedeutet dies:

- numerische Simulationen (z. B. Strömungsmechanik oder Wettermodelle)
  können nur begrenzt auf feinere Gitter aufgelöst werden,
- KI-Modelle benötigen Tage oder Wochen, um zu konvergieren,
- Big-Data-Analysen werden durch Netzwerk-Shuffles statt durch Compute limitiert,
- Reproduzierbarkeit wird zur Ausnahme statt zur Norm,
- Kosten und Energieverbrauch steigen schneller als die Ergebnisse.

Die HPC-Community erkennt zunehmend, dass FLOPs kein geeigneter
Leistungsindikator mehr sind. Die klassische Optimierung „Compute schneller
machen“ verfehlt ihr Ziel, wenn 70–90 % eines Workloads nicht durch
Compute, sondern durch Memory und Synchronisation bestimmt werden.

Dieser Wandel erfordert eine neue Sicht auf Rechenarchitekturen – eine, die
**die tatsächlichen Engpässe adressiert**, nicht nur deren Symptome.

KORA (Knowledge-Oriented Reproducible Architecture) ist eine Antwort auf
dieses grundlegende Strukturproblem.  
Anstatt FLOP-Durchsatz als primären Treiber zu betrachten,
setzt KORA auf:

- deterministische Datenpfade,
- latenzoptimierte Speicher- und Kommunikationsstrukturen,
- hardwarebasierte Synchronisationsmechanismen,
- reproduzierbare Ausführungsverläufe,
- Eliminierung verteilter Overheads,
- energieeffiziente Ausführung durch monolithische Strukturen.

Ziel von KORA ist es, systemische Ineffizienzen moderner HPC- und KI-Infrastrukturen
durch eine kohärente Architektur zu eliminieren, die nicht auf mehr Rechenleistung,
sondern auf **mehr strukturelle Ordnung** setzt.

Wo klassische Architekturen versuchen, Unbestimmtheit durch zusätzliche Schichten
zu kompensieren, verfolgt KORA den entgegengesetzten Ansatz:  
**Die Ausführung wird strukturell so stabilisiert, dass Overheads gar nicht erst entstehen.**

Damit schafft KORA die Grundlage für:

- reproduzierbare wissenschaftliche Ergebnisse,
- massiv reduzierte Energieverbräuche,
- signifikante Verkürzung der Time-to-Solution,
- nachvollziehbare, deterministische Trainings- und Simulationspfade,
- neue Freiheitsgrade in der Modellkomplexität,
- ein nachhaltiges Wachstum der Recheninfrastruktur.

KORA ist kein inkrementelles Optimierungsprojekt.
Es ist ein strukturaler Architekturvorschlag, der
die dominierenden Engpässe heutiger Systeme direkt adressiert
und damit eine neue Ebene wissenschaftlicher Rechenleistung erschließt.

---

## 2. Limitierungen heutiger HPC-Architekturen

Trotz enormer Fortschritte in der Halbleitertechnologie, Parallelisierung
und Spezialisierung von Beschleunigern stagnieren die realen Leistungsgewinne
in modernen Hochleistungsrechenzentren. Viele Systeme erreichen nur einen
Bruchteil ihrer theoretischen Spitzenleistung; einige Workloads erzielen
unter realen Bedingungen weniger als 10 % des nominalen FLOP-Durchsatzes.

Diese Diskrepanz ist nicht auf mangelnde Rechenleistung zurückzuführen,
sondern auf systemimmanent wachsende Overheads, die mit wachsender
Parallelität überproportional zunehmen. Die wichtigsten Limitierungen
lassen sich in vier zentrale Kategorien unterteilen:
**Memory**, **Communication**, **Synchronisation** und **Nichtdeterminismus**.

### 2.1 Memory-Limitierung

Speicherbandbreite und -latenz sind in klassischen HPC-Systemen zu einer
der dominierenden Ressourcen geworden. Gründe dafür sind:

- unzureichende Skalierung der Memory-Bandbreite im Vergleich zu Compute,
- hohe Latenzen bei verteilten Speicherarchitekturen (NUMA, multi-socket),
- mangelnde Datenlokalität,
- ineffiziente Cache-Nutzung insbesondere bei unregelmäßigen Zugriffsmustern,
- steigende Kosten zufälliger Zugriffe (random access),
- unvermeidbare Datenbewegung zwischen Host und Beschleunigern.

Bei vielen Big-Data- und numerischen Workloads entsteht der Großteil der
Gesamtausführungszeit aus:

$$
T_{mem} \approx 
\frac{D_{seq}}{BW_{seq}} + 
\frac{D_{rnd}}{BW_{rnd}} + 
N_{access} \cdot L_{mem}.
$$

Mit wachsender Modellgröße werden Speicheroperationen zu
**Megabarrieren** im Rechenfluss: Jeder Ausführungsschritt wartet darauf,
dass Daten bereitgestellt oder aktualisiert werden. Dies gilt in besonderem
Maße für Simulationen mit spärlichen Datenstrukturen, große Graphen,
Datenbanken oder Modelle mit Schwerpunkt auf zufälligen Zugriffen.

### 2.2 Communication-Limitierung

In verteilten Systemen steigt der Anteil der Zeit, die mit
Datenübertragung verbracht wird, schneller als der Compute-Anteil.
In modernen HPC-Clustern bestehen typische Kommunikationsebenen aus:

- PCIe- oder NVLink-Transfers zwischen CPU und GPU,
- Transfers zwischen GPUs im gleichen Knoten,
- Netzwerkübertragungen zwischen Knoten,
- Synchronisations- und Metadatenverkehr (MPI).

Selbst modernste Netzwerke wie 200–400 Gbit/s InfiniBand
stehen unter massivem Druck, sobald Parameter-Shuffles oder
Allreduce-Operationen auftreten.

Der Kommunikations-Term lässt sich grob modellieren als:

$$
T_{comm} = n_{msg} \cdot L_{net} + \frac{V}{BW_{net}}.
$$

Bei großen KI-Modellen oder numerischen Simulationen
werden diese Terme schnell dominierend.

### 2.3 Synchronisations-Limitierung

Globale Barrieren (z. B. in MPI-Allreduce, Gradientensynchronisation oder
iterativen PDE-Lösern) verursachen:

- vollständige Pipeline-Stopps,
- Wartezeiten auf langsamste Knoten,
- Enforce von Ausführungsreihenfolgen, die nicht zu Datenlokalität passen,
- exponentiell wachsende Latenzen bei steigender Knotenzahl.

Die Kosten einer globalen Barrier lauten vereinfacht:

$$
T_{sync} = L_{sync} \cdot N_{sync}.
$$

In realen Systemen werden Barrieren zu determinierenden Engpässen,
weil sie:

- nicht parallelisiert werden können,
- nicht verborgen werden können,
- nicht ohne strukturelle Änderung eliminiert werden können.

Während Compute-Power skaliert, bleibt der Synchronisations-Term weitgehend konstant.
Dadurch dominiert er langfristig die Ausführungszeit.

### 2.4 Nichtdeterminismus als strukturelles Problem

Moderne HPC- und KI-Systeme verwenden:

- asynchrone Kernel,
- nichtdeterministische Thread-Scheduler,
- variable Cache-Layouts,
- konkurrierende DMA-Transfers,
- Floating-Point-Reduktionsreihenfolgen,
- nichtdeterministische Netzwerkpfade.

Die Konsequenzen:

- Ergebnisse variieren leicht zwischen Durchläufen,
- Debugging wird erschwert oder unmöglich,
- Regressionstests verlieren aussagekraft,
- Trainingsläufe müssen mehrfach wiederholt werden,
- deterministische Pipeline-Designs scheitern an Hardwaregrenzen.

Dies betrifft insbesondere wissenschaftliche Anwendungen,
bei denen Reproduzierbarkeit ein fundamentales Qualitätskriterium ist
(z. B. Klimamodelle, medizinische Simulationen, numerische Analyse,
wissenschaftliche KI-Modelle).

### 2.5 Energie als Seitenwirkung der Overheads

Mit wachsender Komplexität der Systeme steigt der Energieverbrauch
nicht proportional zur Anzahl der FLOPs, sondern überproportional,
weil Overheads auf mehreren Ebenen zusätzliche Arbeit erzeugen:

- zusätzliche Zugriffe auf Memory-Hierarchien,
- unnötige Kernel-Starts,
- Kontextwechsel,
- wiederholte Synchronisation,
- erhöhte Last auf Kommunikationspfaden.

Viele HPC-Zentren berichten, dass **50–70 % der Energie**
nicht für nützliche Arbeit, sondern für Infrastruktur-Overheads
verbraucht wird.

Dies führt zu:

- massiv steigenden Betriebskosten,
- schwieriger Planbarkeit,
- erhöhter thermischer Belastung der Hardware,
- verkürzter Lebensdauer,
- höheren CO₂-Emissionen.

### 2.6 Fazit

Die Grundprobleme heutiger HPC-Architekturen lassen sich nicht durch mehr
Rechenleistung beheben. Sie sind **strukturell**:

- das Speichersystem skaliert nicht mit,
- das Netzwerk skaliert nicht linear,
- Synchronisation erzeugt harte globale Stopps,
- Scheduling ist fundamental nichtdeterministisch,
- die Systemkomplexität wächst schneller als ihre effiziente Nutzleistung.

Damit ist klar:  
Eine neue Architektur muss diese systemischen Engpässe **strukturell eliminieren** statt sie nur zu kompensieren.

Genau hier setzt KORA an.

---

## 3. Warum FLOPs nicht mehr entscheidend sind

Über Jahrzehnte war der FLOP-Wert (Floating Point Operations per Second) die
zentrale Leistungskennzahl für Rechensysteme. Diese Sichtweise beruhte auf der
Annahme, dass die Rechenoperationen selbst den dominierenden Anteil an der
Ausführungszeit ausmachen. Für viele traditionelle Anwendungen — lineare Algebra,
Vektoroperationen, dichte Matrizenmultiplikation — war diese Sichtweise sinnvoll.

Mit dem Aufkommen massiver Parallelität, tiefer Speicherhierarchien und
vernetzter Clusterarchitekturen hat sich das Verhältnis jedoch grundlegend
verschoben. FLOPs sind heute nur noch ein kleiner, oft nebensächlicher Teil der
Gesamtausführungszeit. Die real dominierenden Faktoren liegen nicht mehr in der
Berechnung, sondern in der Struktur des Daten- und Synchronisationsflusses.

Dieser Abschnitt zeigt, warum FLOPs als primäre Leistungsmetrik untauglich
geworden sind und wie KORA diesen Paradigmenwechsel adressiert.

### 3.1 FLOPs wachsen schnell – aber nicht das, was zählt

Die Rechenleistung (in FLOPs) moderner GPUs, TPUs und HPC-Beschleuniger
steigt kontinuierlich:

- größere Vektorregister,
- breitere Tensor-Cores,
- Mixed-Precision-Optimierungen,
- spezialisierte Matrix-Multiply-Units.

Doch gleichzeitig steigt eine andere Ressource **nicht** proportional an:

- Speicherbandbreite,
- Speicherlatenz,
- Netzwerkbandbreite,
- Netzwerk-Latenzen,
- Barrier-Kosten,
- Scheduling-Overheads.

Das Ergebnis:

    Reale Nutzleistung ungleich Theoretische FLOPs

Für viele Arbeitslasten bedeutet das, dass weniger als 10–30 % der
nominalen FLOP-Leistung effektiv genutzt werden.

### 3.2 Der Compute-Term ist nicht mehr dominant

Unter realen Bedingungen lässt sich der Compute-Term vereinfachen als:

$$
T_{compute} = \frac{F}{R_{compute}} \cdot O_{compute}.
$$

Selbst wenn die FLOP-Leistung steigt, wird der Einfluss dieses Terms kleiner,
weil der Gesamtausführungszeitraum zunehmend von anderen Faktoren bestimmt wird:

- Cache-Misses,
- Latenzketten im Speicher,
- Kommunikationswartezeiten,
- globale Barrieren,
- interne Fragmentierung des Kernels,
- Scheduling-Konflikte.

In numerischen Simulationen, Big-Data-Anwendungen und vielen KI-Modellen
sind Compute-Phasen nur noch ein Zwischenstück zwischen Speicher- und
Kommunikationsoperationen, die ihre eigene Dynamik dominieren.

### 3.3 Der Memory-Wall-Effekt

Die klassische Memory-Wall beschreibt, dass Speicherbandbreite und Latenz
nicht schnell genug steigen, um mit dem Wachstum der Rechenleistung
mitzuhalten. Moderne Anwendungen verstärken dieses Problem:

- Große Datenstrukturen (Tensoren, sparse Matrices, Graphen)
- Unregelmäßige Speicherzugriffe
- Batch-Wechsel im Training
- numerische Iterationen mit globalen Abhängigkeiten

Die Folge:

    Compute wird durch Datenabhängigkeiten ausgebremst.

Selbst wenn Compute theoretisch schneller möglich wäre,
gibt der Speicher nicht schnell genug Daten frei.

### 3.4 Kommunikation dominiert verteilte Systeme

Moderne Cluster arbeiten nicht mehr lokal, sondern verteilen Daten über:

- PCIe / NVLink,
- Host-zu-Device,
- Device-zu-Device,
- Rack-zu-Rack,
- Node-zu-Node.

Der Kommunikations-Term lautet:

$$
T_{comm} = n_{msg} \cdot L_{net} + \frac{V}{BW_{net}}.
$$

Dieser Term wächst:

- überproportional mit Modellgröße,
- quadratisch bei Allreduce-Operationen,
- stärker als jede FLOP-Optimierung.

Beispiel KI:

Selbst wenn ein Beschleuniger 10× mehr FLOPs hat, muss der Gradientenabgleich
immer noch dieselbe Datenmenge durch das Netzwerk schieben.

### 3.5 Synchronisation ist ein harter Engpass

Barrieren können nicht durch FLOPs beschleunigt werden.

$$
T_{sync} = N_{sync} \cdot L_{sync}.
$$

Selbst mit mehr Compute-Power bleibt jede Barrier gleich teuer.
Und je größer das System wird, desto häufiger müssen Barrieren eingeführt werden.

In vielen Workloads sind Synchronisationskosten der **dominierende** Faktor:

- iterative PDE-Löser,
- Klima-/Wettermodelle,
- HPC-Simulationen,
- verteiltes KI-Training,
- Graphverarbeitung,
- Datenbanken.

### 3.6 FLOPs sind keine gute Metrik für Energie

Ein FLOP selbst ist billig.  
Aber der Overhead darum herum ist teuer:

- Cache-Ladungen,
- Kernel-Starts,
- Transfer-Overheads,
- Synchronisationsphasen,
- Kontextwechsel,
- Interconnect-Timeouts,
- Memory-Refresh.

In modernen Systemen stammen **50–70 % des Energieverbrauchs** aus
Infrastruktur-Overheads — nicht aus Rechenoperationen.

Mehr FLOPs bedeuten oft:

- größere Chips,
- mehr Transistoren,
- höhere Grundlast,
- stärkere Kühlung.

Dies verschlechtert das Energieprofil unabhängig davon,
ob die zusätzlichen FLOPs überhaupt genutzt werden.

### 3.7 FLOPs sind kein Indikator für Reproduzierbarkeit

Nichtdeterminismus entsteht nicht im FLOP selbst,
sondern in dessen Umgebung:

- parallelisierte Reduktionsreihenfolgen,
- nichtdeterministische Thread- und Kernel-Scheduler,
- Variation der Kommunikation,
- konkurrierende DMA-Transfers,
- unkontrollierte FP-Rundungsfehler,
- Race Conditions.

Viele KI- und wissenschaftliche Modelle liefern heute:

- leicht unterschiedliche Endergebnisse,
- instabile Konvergenzpfade,
- variierende Loss-Kurven.

FLOPs messen diesen Effekt nicht.

KORA setzt bewusst auf ein
**deterministisches Ausführungsmodell**,
das Reproduzierbarkeit strukturell erzwingt.

### 3.8 Fazit

FLOPs sind als primäre Leistungsmetrik antiquiert.  
Sie ignorieren:

- die wahren Engpässe,
- die Struktur der Datenbewegung,
- globale Kommunikationskosten,
- deterministische Pfade,
- Energieeffizienz,
- Reproduzierbarkeit.

In modernen HPC- und KI-Systemen ist nicht die
**Rechenoperation**, sondern die
**Organisation** von Speicher, Kommunikation
und Synchronisation entscheidend.

KORA basiert genau auf dieser Einsicht.

Statt FLOPs zu maximieren, optimiert KORA:
**Datenpfade, Latenzen, Synchronisation und Determinismus.**

Damit wird ein grundlegender Paradigmenwechsel sichtbar:
Die Effizienz moderner Systeme hängt **nicht** davon ab,
wie schnell sie rechnen,  
sondern **wie gut sie strukturiert sind**.

---

## 4. Reproduzierbarkeit und Determinismus

Reproduzierbarkeit ist ein grundlegendes Prinzip wissenschaftlicher Arbeit.
In der numerischen Simulation, der Modellbildung, der Datenanalyse und dem
Training künstlicher Intelligenz ist sie nicht nur wünschenswert, sondern
notwendig: Ergebnisse müssen nachvollziehbar, überprüfbar und wiederholbar
sein, um wissenschaftliche Validität zu besitzen.

Moderne HPC- und KI-Systeme erfüllen diese Anforderung jedoch nur unzureichend.
Aufgrund struktureller, hardwarebedingter und softwareseitiger
Nichtdeterminismen erzeugen viele Systeme bei identischen Eingaben
unterschiedliche Ausgaben, abweichende Konvergenzpfade oder variierende
Fehlerverteilungen. Dies hat weitreichende Konsequenzen:

- wissenschaftliche Simulationen sind schwer zu verifizieren,
- KI-Modelle können inkonsistente oder instabile Ergebnisse liefern,
- Debugging und Regressionstests werden aufwendig oder unmöglich,
- Energie- und Zeitbudgets werden unvorhersehbar,
- Modelle verlieren an erklärbarer Vertrauenswürdigkeit.

Dieser Abschnitt beschreibt, warum Nichtdeterminismus fast alle modernen
Rechenarchitekturen prägt, warum FLOP-zentrierte Ansätze dieses Problem nicht
lösen können, und wie KORA ein deterministisches Ausführungsmodell als
strukturelles Architekturprinzip implementiert.

### 4.1 Quellen des Nichtdeterminismus in modernen Systemen

Nichtdeterminismus entsteht nicht durch einzelne Rechenoperationen, sondern
durch die unkontrollierte Wechselwirkung paralleler Komponenten. Die wichtigsten
Quellen sind:

#### (1) Asynchrone Kernel-Ausführung

Moderne GPUs und Beschleuniger verwalten:

- mehrere parallele Kernel,
- variable Startzeiten,
- konkurrierende Ressourcen,
- dynamische Thread-Zuordnung.

Mini-Variationen im System führen zu divergierenden Ausführungsreihenfolgen.

#### (2) Nichtdeterministische Reduktionsreihenfolgen  

Floating-Point-Arithmetik ist nicht assoziativ.
Daher führen unterschiedliche Reduktionspfade zu leicht unterschiedlichen
Ergebnissen. Dies geschieht in:

- Summationen,
- Dot-Products,
- Gradientenaggregationen,
- dynamischen Graphstrukturen,
- MPI-Allreduce.

#### (3) Scheduling-Variabilität  

Betriebssysteme und Laufzeitumgebungen (CUDA, ROCm, MPI) arbeiten
mit komplexen, nichtdeterministischen Schedulern.
Selbst minimale Timing-Unterschiede erzeugen divergierende
Ausführungspläne.

#### (4) Netzwerk-Variabilität  

In verteilten Systemen hängt der exakte Weg eines Pakets von:

- momentaner Netzlast,
- Routing-Algorithmen,
- konkurrierenden Datenströmen,
- Hardwarezustand,
- Zufallsfaktoren in Protokollen

ab. Dadurch entstehen variable Latenzen und unterschiedliche Reihenfolgen
bei dem Eintreffen von Daten.

#### (5) DMA-Kollisionen  

Direct Memory Access-Engines konkurrieren um Busse, Caches und
Speicherbänke. Zugriffsreihenfolgen werden dynamisch aufgelöst,
nicht deterministisch.

#### (6) Globale Barrieren  

Selbst Barrieren sind unter realen Bedingungen nicht deterministisch:
Die Reihenfolge, in der Prozesse die Barrier erreichen oder verlassen, hängt
von vielen externen Faktoren ab.

### 4.2 Konsequenzen für wissenschaftliche Arbeit

Nichtdeterminismus hat in der Wissenschaft mehrere schwerwiegende Effekte:

#### (a) Fehlende Wiederholbarkeit  

Simulationen, die zuvor abgeschlossen wurden, liefern bei Wiederholung
leicht abweichende Ergebnisse. Dies ist besonders kritisch bei:

- Klimamodellen,
- Strömungsmechanik,
- Sensitivitätsanalysen,
- medizinischen Simulationen,
- numerischen Stabilitätstests.

#### (b) Inkonsistente Trainingsläufe  

KI-Modelle:

- konvergieren unterschiedlich,
- benötigen variable Trainingsdauer,
- erreichen leicht abweichende Loss-Werte,
- zeigen nicht reproduzierbare Feeze-Outs oder Plateaus.

#### (c) Erschwertes Debugging  

Wenn ein Fehler nicht reproduzierbar ist, kann er nicht zuverlässig
behoben werden.

#### (d) Fehlende regulatorische Eignung  

In sicherheitskritischen Bereichen (Energie, Medizin, Verkehr):

- müssen Ergebnisse vollständig reproduzierbar sein,
- sonst sind sie nicht zertifizierbar.

#### (e) Energieunplanbarkeit  

Nichtdeterminismus führt zu volatileren Laufzeiten und damit
unplanbaren Energieprofilen.

### 4.3 Warum FLOP-zentrierte Architekturansätze das Problem nicht lösen

Mehr FLOPs lösen *keines* der strukturellen Probleme:

- sie reduzieren keine Barrieren,
- sie determinieren keine Speicherzugriffe,
- sie organisieren keine DMA-Flüsse,
- sie verringern keine Netzwerklatenzen,
- sie erzwingen keinen deterministischen Scheduler.

Tatsächlich verstärken höhere FLOP-Raten die strukturellen Unterschiede:

- mehr parallele Einheiten erzeugen mehr Scheduling-Komplexität,
- größere Modelle verstärken die Kommunikationsanforderungen,
- schnellere Compute-Phasen verschieben die Flaschenhälse auf Memory,
- Nichtdeterminismus steigt proportional zur Parallelität.

### 4.4 Determinismus als Architekturprinzip

KORA verfolgt einen radikal anderen Ansatz:
**Determinismus wird nicht als Compiler- oder Softwareaufgabe behandelt,
sondern als hardwareseitige Eigenschaft.**

Dazu implementiert KORA:

1. **deterministische Datenpfade**,  
2. **definierte Memoryzugriffsreihenfolgen**,  
3. **deterministische Scheduling-Bäume**,  
4. **geordnete Ausführungssequenzen**,  
5. **dedizierte Synchronisationseinheiten**,  
6. **SRDB (Structural Runtime Data Bus)** für reproduzierbare Metadaten,
7. **reproduzierbare Partitionierung**,  
8. **keine nichtdeterministischen Race-Conditions**,  
9. **On-Die-Taktbasis ohne Jitter**,  
10. **bitgenaue Ausführung aller arithmetischen Ketten**,  
11. **eliminierte Zufallskomponenten in der Kernel-Orchestrierung**,  
12. **lokal determinierte DMA-Operationen**,  
13. **garantierte Routing-Wege durch TDM-basierte Fabric**.

Diese Mechanismen sind *nicht* auf Softwareebene nachbildbar.
Sie entstehen ausschließlich durch die Struktur der Hardware.

### 4.5 Reproduzierbarkeitsmetriken von KORA

KORA definiert zwei Reproduzierbarkeitskennzahlen:

#### 1) r_bit — bitweise Reproduzierbarkeit  

$$
r_{bit} = 1.0
$$

bei Architektur C (Monolith).

Das bedeutet:
Jeder Durchlauf liefert *bitidentische Ergebnisse*.

#### 2) r_run — Wiederholungsfaktor  

$$
r_{run} = 1.0
$$

bei Architektur C.

Es sind keine Wiederholungsdurchläufe notwendig,
um verlässliche Ergebnisse zu erhalten.

Zum Vergleich:

| Architektur      | r_bit | r_run |
|------------------|-------|-------|
| A (Standard HPC) | 0.4   | 1.10  |
| B (KORA-SW)      | 0.8   | 1.02  |
| C (KORA-HW)      | 1.0   | 1.00  |

### 4.6 Wissenschaftliche Bedeutung

Die Fähigkeit, bitgenaue, deterministische Ergebnisse zu liefern,
hat tiefgreifende Auswirkungen:

#### (1) Validität  

Simulationen können eindeutig verifiziert werden.

#### (2) Reproduzierbarkeit  

Wissenschaftler können Ergebnisse vergleichen, ohne durch
Hardwarezustände verfälscht zu werden.

#### (3) Robustheit  

Nummerische Algorithmen konvergieren stabiler und vorhersehbarer.

#### (4) Effizienz  

Keine Wiederholungsläufe → weniger Energieverbrauch.

#### (5) Debugging  

Deterministische Knoten ermöglichen lokalisiertes Debugging
auf Hardwareebene.

#### (6) Modelltransparenz  

KI-Modelle werden interpretierbarer, weil sie konstante
Gradientenpfade und stabile Loss-Kurven entwickeln.

### 4.7 Fazit

Reproduzierbarkeit ist nicht nur eine wünschenswerte Eigenschaft,
sondern eine grundlegende Systemanforderung — besonders für
wissenschaftliche Hochlastanwendungen.

KORA setzt hier einen neuen Standard:
Determinismus wird nicht als nachgelagerte Optimierung betrachtet,
sondern als **Konstruktionsprinzip**.  
Durch den strukturellen Aufbau des Monolithen entsteht eine
Architektur, die:

- bitgenau,
- wiederholbar,
- analysierbar,
- energieeffizient,
- vertrauenswürdig

ist.

Damit bildet Reproduzierbarkeit das Fundament der gesamten KORA-Architektur.

---

## 5. Anforderungen an moderne HPC-/KI-Architekturen

Die steigende Komplexität moderner wissenschaftlicher und KI-Anwendungen
erfordert Architekturen, die weit mehr leisten als reine
Rechenoperationen. Jahrzehntelang wurden Systeme so entworfen, dass sie
möglichst viele FLOPs bereitstellen – doch dieser Ansatz ist zunehmend
unzureichend. Ein moderner HPC-/KI-Stack muss Datenbewegung, Synchronisation,
Latenzen, Energie und Reproduzierbarkeit genauso effizient behandeln wie Compute.

Um diesen Anforderungen gerecht zu werden, müssen künftige Architekturen
eine Reihe grundlegender Prinzipien erfüllen. Diese Anforderungen bilden die
technische Grundlage, auf der KORA entwickelt wurde.

### 5.1 Effiziente Datenbewegung als Primärziel

In nahezu allen großen Anwendungen – von KI über Big Data bis hin zu
numerischen Simulationen – sind die Kosten der Datenbewegung höher als die
Kosten der eigentlichen Berechnung. Deshalb muss eine moderne Architektur:

- Daten lokal halten statt bewegen,
- Zugriffe vorhersehbar machen,
- Random Access drastisch reduzieren,
- Memory-Grundstrukturen optimieren,
- Datenabhängigkeiten minimieren,
- möglichst flache und latenzarme Speicherpfade bieten.

Eine Architektur, die Daten nicht lokal verwalten kann, bleibt
fundamental ineffizient – unabhängig von ihrer FLOP-Leistung.

### 5.2 Reduktion globaler Kommunikation

Verteilte Architekturen haben inhärente Grenzen, die durch Netzwerkphysik
bestimmt werden: Bandbreite steigt langsamer als Modellgrößen, und Latenz
kann nicht einfach „wegoptimiert“ werden. Moderne Workloads erfordern:

- minimale Anzahl globaler Nachrichten,
- deterministische Kommunikationspfade,
- feste Latenzbudgets,
- Strategien zur Latenzvermeidung (z. B. lokale Reduktion),
- strukturelle Eliminierung von Allreduce-Bottlenecks.

Eine Architektur, die globale Kommunikation strukturell vermeidet,
gewinnt langfristig unabhängig von zukünftigen Netzwerkfähigkeiten.

### 5.3 Minimierung der Synchronisierungskosten

Globale Barrieren sind einer der größten Skalierungsfeinde.
Moderne Architekturen müssen ihre Anzahl und Kosten reduzieren durch:

- hardwarebasierte Mikrobarrieren,
- deterministische Ausführungsreihenfolgen,
- lokale Synchronisationsräume,
- Scheduler ohne nichtdeterministische Effekte,
- strukturelle Vermeidung globaler Abhängigkeiten.

Dies ist nur möglich, wenn die Architektur Datenpfade und
Ausführungsreihenfolgen **von Grund auf** deterministisch gestaltet.

### 5.4 Reproduzierbarkeit als Designpriorität

Für Wissenschaft und KI ist Reproduzierbarkeit kein optionales Feature,
sondern eine Kernanforderung. Moderne Architekturen müssen:

- deterministische Datenpfade garantieren,
- feste Reduktionsreihenfolgen sicherstellen,
- nichtdeterministische Scheduler vermeiden,
- Time-to-Solution ohne Schwankungen liefern,
- bitgenaue Ergebnisse bei wiederholten Läufen erzeugen.

Ohne diese Eigenschaften sind Simulationen schwer verifizierbar
und KI-Modelle verlieren an wissenschaftlicher Validität.

### 5.5 Energieeffizienz und thermische Stabilität

Der Energieverbrauch ist inzwischen ein dominierender Kostenfaktor in HPC- und
KI-Rechenzentren. Moderne Architekturen müssen:

- Energieverbrauch an Datenbewegung koppeln,
- Overheads minimieren (nicht Compute maximieren),
- streng kontrollierbare Wärmeentwicklung bieten,
- eine konsistente Lastverteilung gewährleisten,
- effizient mit thermischen Spitzen umgehen.

Energieeffizienz ist keine Nebenbedingung mehr, sondern eine
zentrale wissenschaftliche und ökonomische Notwendigkeit.

### 5.6 Skalierbarkeit ohne exponentielle Overheads

Moderne Workloads benötigen:

- lineare oder sublineare Skalierung,
- keine exponentielle Explosion von Kommunikationskosten,
- stabile Performance bei wachsender Modellgröße,
- vorhersehbare Latenzpfade bei 10× größeren Workloads.

Dazu müssen Architekturen Overheads strukturell begrenzen.
Konventionelle Systeme stoßen hier unweigerlich an Grenzen – unabhängig
von FLOP-Leistung oder Netzwerkgeneration.

### 5.7 Deterministische und stabile Ausführungsmodelle

Scheduling-Variabilität ist eine der Hauptursachen für nichtdeterministische
Laufzeiten und Ergebnisse. Moderne Architekturen benötigen:

- stabile Scheduling-Bäume,
- deterministische Instruktionsreihenfolgen,
- garantierte Pipeline-Pfadlängen,
- minimale Jitter im Rechenpfad,
- deterministische DMA- und Memory-Operationen.

Dies ist die Grundlage für:

- stabile KI-Konvergenz,
- reproduzierbare numerische Ergebnisse,
- exakte Debugbarkeit,
- regelmäßiges Power-Profil.

### 5.8 Architekturen müssen Modelllogik berücksichtigen

Traditionelle Architekturen behandeln Arbeitslasten als abstrakte
Operationen. Moderne Architekturen müssen jedoch die strukturellen
Eigenschaften der Modelle berücksichtigen:

- dichte vs. spärliche Daten,
- lokale vs. globale Abhängigkeiten,
- sequentielle vs. parallele Abschnitte,
- Kommunikationsmuster,
- Memory-Footprint und Random-Access-Profile.

Eine Architektur, die Modellstrukturen ignoriert,
kann sie nicht effizient ausführen.

### 5.9 Zusammenfassung der Anforderungen

Moderne HPC- und KI-Architekturen müssen:

1. **Datenbewegung minimieren**  
2. **globale Kommunikation reduzieren**  
3. **Synchronisationskosten strukturell eliminieren**  
4. **deterministische Ausführung garantieren**  
5. **Reproduzierbarkeit sicherstellen**  
6. **Energie konsumieren proportional zur Nützlichkeit**  
7. **skalieren ohne exponentielle Overheads**  
8. **Memory- und Kommunikationspfade optimieren**  
9. **Modelllogik berücksichtigen**  
10. **systemische Ordnung statt höherer FLOP-Raten schaffen**

Diese Anforderungen bilden die Grundlage, auf der KORA entwickelt wurde.
Sie definieren, woran moderne Architekturen scheitern – und worauf
KORA in seiner Gestaltung explizit ausgelegt ist.

---

## 6. Die fünf Designprinzipien von KORA

KORA ist keine Optimierung bestehender Architekturen, sondern eine
grundlegend andere Sicht auf Hochleistungsberechnung.
Während klassische Systeme auf inkrementelle Verbesserungen von
Rechenleistung und Parallelität setzen, folgt KORA einem Konzept
struktureller Kohärenz.  
Jedes Teilstück der Architektur — Speicher, Routing, Scheduling,
Synchronisation — ist so gestaltet, dass es deterministisch,
energieeffizient und reproduzierbar ist.

Diese Systemkohärenz wird durch fünf fundamentale Designprinzipien definiert.
Sie sind das Herz der KORA-Architektur.

### 6.1 Prinzip 1: **Datenlokalität statt Datenbewegung**

Die wichtigste Feststellung moderner HPC-Systeme lautet:
**Datenbewegung ist teurer als Berechnung.**

KORA setzt daher auf:

- lokale Datenhaltung im Monolithen,  
- minimale externe Kommunikation,  
- banked Memory mit garantierten Latenzen,  
- strukturelle Vermeidung von Cache-Thrashing,  
- deterministische Partitionierung von Datenräumen,  
- Scratchpads und Tiles als lokale Rechendomänen.

In einem KORA-Monolithen bewegt sich der Großteil der Daten **nicht**
über Netzwerke oder clusterweite Busse, sondern bleibt innerhalb
lokaler Speicherbänke mit extrem kurzer Latenz.

Dies reduziert:

- Energieverbrauch,
- Kommunikationskosten,
- Pipeline-Stalls,
- Memory-Zufallszugriffe.

Damit folgt KORA einem fundamentalen Paradigmenwechsel:
Nicht Compute, sondern Dataflow bestimmt die Architektur.

### 6.2 Prinzip 2: **Determinismus als zentrale Architektur-Eigenschaft**

In bestehenden HPC/KI-Systemen ist Determinismus ein nachgelagertes Ziel —
falls er überhaupt erreicht werden kann.  
KORA kehrt diese Hierarchie um:

**Determinismus ist kein Zusatz, sondern ein Designkriterium der Hardware.**

Dazu nutzt KORA:

- deterministische Scheduling-Bäume,
- feste Ausführungssequenzen pro Tile-Gruppe,
- deterministische DMA-Ketten,
- TDM-basierte On-Die-Fabrics mit garantierten Routing-Zeitfenstern,
- den SRDB (Structural Runtime Data Bus) zur geordneten Metadatenführung,
- bitgenaue Ausführungspfade ohne Race-Conditions.

Determinismus führt zu:

- bit-exakten Ergebnissen,
- stabilen Konvergenzpfaden,
- prüfbaren wissenschaftlichen Resultaten,
- robusten Trainingsläufen,
- vereinfachtem Debugging.

Damit wird der Monolith zu einer Plattform, die wissenschaftliche
Reproduzierbarkeit **hardwareseitig garantiert**.

### 6.3 Prinzip 3: **Strukturelle Eliminierung globaler Overheads**

Globale Barrieren, Allreduce-Operationen und komplexe Synchronisationsketten
sind die größten Hindernisse moderner HPC-Systeme.  
KORA reduziert sie **nicht** —  
KORA **eliminiert** sie strukturell.

Dies geschieht durch:

- lokale Synchronisationsräume (Tile-Gruppen),
- hardwarebasierte Microbarriers,
- deterministische Ausführungsreihenfolgen,
- definierte Kommunikationsfenster,
- globale Clock-Domains ohne Jitter,
- disziplinierte Instruktionsketten ohne spontane Unterbrechungen.

Im Monolith gibt es keine nichtdeterministischen Barrieren über
Netzwerkgrenzen hinweg — weil es keine verteilten Netzwerke gibt.

Damit entsteht ein System mit:

- planbarer Latenz,
- extrem hoher Stabilität,
- reproduzierbarer Performance,
- massiver Reduktion der Gesamtausführungszeit.

### 6.4 Prinzip 4: **Energieeffizienz durch Ordnung, nicht durch Skalierung**

KORA folgt nicht dem traditionellen „mehr FLOPs pro Watt“-Ansatz.
Stattdessen lautet das KORA-Prinzip:

> Energieeffizienz entsteht durch Ordnung im Daten- und Kontrollfluss.

Das bedeutet konkret:

- weniger Datenbewegung → weniger Energie,
- weniger Synchronisation → weniger Energie,
- lokale statt globale Operationen → weniger Energie,
- deterministische Abläufe → weniger Jitter → weniger thermische Spitzen,
- strukturelle Pipeline-Konstanz → planbare Verbrauchskurven.

Der Monolith benötigt für hochkomplexe Workloads oft nur
**1–3 %** der Energie klassischer HPC-Cluster, weil er nahezu alle
infrastrukturellen Overheads eliminiert.

KORA koppelt Energieverbrauch direkt an nützliche Arbeit —  
nicht an Overheads.

### 6.5 Prinzip 5: **Architektur folgt Modelllogik**

KORA ist nicht generalistisch im klassischen Sinn,
sondern modellorientiert.  
Die Architektur bildet strukturelle Eigenschaften realer Workloads ab:

- lokale Datenabhängigkeiten (CFD, FEM),
- iterative Rechensequenzen,
- stark strukturierte Graphen (KI),
- zufällige Lesezugriffe (Big Data),
- kommunikative Hotspots (Distributed AI),
- regelmäßige Reduktionsoperationen,
- sequentielle Pipeline-Phasen.

Durch diese Modellorientierung ermöglicht KORA:

- konsistente Durchsatzraten,
- deterministische Modellverläufe,
- stabile zeitliche Profile,
- effizientere Datenverteilung,
- optimierte Speicherlayouts,
- geringere Kommunikationslast.

Das Ziel ist nicht maximale Allgemeinheit,
sondern maximale **Kohärenz zwischen Modell und Maschine**.

### 6.6 Zusammenfassung der KORA-Designprinzipien

KORA basiert auf fünf fundamentalen Prinzipien:

1. **Datenlokalität statt Datenbewegung**  
2. **Determinismus statt stochastischer Ausführung**  
3. **Eliminierung statt Reduktion globaler Overheads**  
4. **Energieeffizienz durch strukturelle Ordnung**  
5. **Kohärenz zwischen Modell und Architektur**

Diese Prinzipien definieren die gesamte technische Gestaltung des Monolithen
und bilden die Grundlage für die folgenden Kapitel der Architektur-Spezifikation.

---

## 7. Architekturübersicht (A/B/C) und systemische Rollen

Bevor die interne Struktur des KORA-Monolithen im Detail beschrieben wird,
muss die Rolle der drei Architekturen A, B und C im Gesamtsystem klar definiert werden.
Sie bilden gemeinsam den Rahmen, innerhalb dessen KORA als Modell verstanden
und implementiert werden kann. Während Architektur C den technischen Kern darstellt,
erfüllen A und B eine wichtige wissenschaftliche und praktische Funktion:
Sie liefern Referenzpunkte, Vergleichbarkeit und Übergangspfade.

KORA unterscheidet drei Architekturen:

- **Architektur A – Standard HPC/KI (Baseline)**  
- **Architektur B – KORA-SW (Optimierte Software auf Standard-Hardware)**  
- **Architektur C – KORA-HW Monolith (Hardware-basierter deterministischer Kern)**

Jede dieser Architekturen spielt eine klar abgegrenzte Rolle in der
wissenschaftlichen Argumentation und im technischen Design.

### 7.1 Architektur A – Standard HPC/KI (Baseline)

Architektur A bildet den real existierenden Zustand heutiger
Rechenzentren ab.  
Sie basiert auf:

- verteilten Clusterstrukturen,
- heterogener CPU/GPU-Kombination,
- Netzwerk-basierten Allreduce- und MPI-Mechanismen,
- nichtdeterministischen Ausführungsmodellen,
- hohen Kommunikations- und Synchronisationskosten,
- limitierten Memory-Bandbreiten,
- globalen Barrieren.

**Wissenschaftliche Rolle:**  
Architektur A dient als *Kalibrier- und Vergleichspunkt*.
Alle Beschleunigungs- und Energieeinsparungswerte von KORA werden
in Relation zu dieser Baseline angegeben. Ohne eine solide und realistische
Abbildung des Status quo wäre keine sinnvolle Bewertung der
KORA-Architektur möglich.

**Technische Rolle:**  
A liefert die Parameter, die im Modell durch **S_W-Faktoren** kalibriert werden.
Diese Kalibrierung stellt sicher, dass die Simulationen realitätsnah bleiben,
auch wenn die zugrundeliegenden Systeme heterogen sind.

### 7.2 Architektur B – KORA-SW (Softwareoptimierte Architektur)

Architektur B nutzt die gleiche Hardware wie A, ist jedoch
softwareseitig optimiert.  
Sie implementiert:

- deterministischere Speicherzugriffe,
- stabilere Scheduling-Pfade,
- reduzierte Barrier-Kosten,
- effizientere Nutzung der vorhandenen Hardware,
- geringere Kernel-Fragmentierung,
- optimierte Partitionierungslogik,
- verbesserte Kommunikationsmuster.

**Wissenschaftliche Rolle:**  
B demonstriert, dass die Prinzipien von KORA auch ohne neue Hardware
bereits signifikante Effizienzgewinne ermöglichen.  
Sie zeigt, dass die KORA-Ideen nicht auf Hardware angewiesen sind,
sondern systemische Prinzipien darstellen.

**Übergangsrolle:**  
KORA-SW erleichtert die Einführung des KORA-Modells in existierenden Rechenzentren,  
ohne dass eine neue Hardwarearchitektur sofort verfügbar sein muss.

**Technische Rolle:**  
B bildet eine „saubere“ Zwischenstufe:  
Sie reduziert Overheads, ohne die Struktur von Architektur A zu negieren.
Damit liefert sie eine robuste Grundlage, um die Vorteile von Architektur C
fair und nachvollziehbar zu bewerten.

### 7.3 Architektur C – KORA-HW Monolith (Deterministische Hardwareplattform)

Architektur C ist das Herzstück der KORA-Idee:
ein monolithischer Rechenkern, der Overheads nicht nur reduziert,  
sondern **architektonisch eliminiert** und Reproduzierbarkeit
auf Hardware-Ebene erzwingt.

Die entscheidenden strukturellen Merkmale von C sind:

- Tiles mit lokalen Scratchpads,
- deterministische Scheduling-Bäume,
- hardwarebasierte Synchronisationseinheiten,
- banked memory mit garantierten Latenzen,
- deterministische DMA-Engines,
- On-Die Fabric mit festen Zeitslots (TDM),
- SRDB (Structural Runtime Data Bus),
- deterministische Partitionierungslogik,
- bitgenaue Ausführungspfade.

Architektur C ist **kein Cluster und keine GPU**, sondern ein  
lokal kohärenter Rechenblock mit definierter Topologie und
deterministischem Datenfluss.

**Wissenschaftliche Rolle:**  
C ist die Referenzarchitektur, die demonstriert, welche Gewinne möglich sind,
wenn die strukturellen Engpässe heutiger Systeme vollständig eliminiert werden.

**Technische Rolle:**  
C definiert die zukünftige Hardware, die KORA idealerweise implementiert.
Alle in den späteren Kapiteln beschriebenen Komponenten (Tiles, SRDB, Fabric)
gehören zu Architektur C.

### 7.4 Systemische Rollenverteilung zwischen A, B und C

Beide Architekturen A und B sind notwendig, um:

- die wissenschaftliche Bedeutung der KORA-Ideen zu demonstrieren,
- verschiedene Modernisierungsstufen vergleichbar zu machen,
- Migrationspfade aufzuzeigen,
- die Simulationen realistisch zu kalibrieren,
- Energie- und Performancedaten nachvollziehbar zu machen.

Die Rollen lassen sich wie folgt zusammenfassen:

| Rolle                              | Architektur A | Architektur B | Architektur C |
|------------------------------------|---------------|---------------|---------------|
| Basislinie                         | ✓             | –             | –             |
| realistische HPC-Abbildung         | ✓             | –             | –             |
| softwareseitige Optimierung        | –             | ✓             | –             |
| deterministische Hardware          | –             | –             | ✓             |
| wissenschaftliche Vergleichbarkeit | ✓             | ✓             | ✓             |
| Energieeffizienz                   | ✗             | ○             | ✓             |
| Eliminierung von Overheads         | ✗             | teilweise     | vollständig   |
| Reproduzierbarkeit (r_bit=1)       | ✗             | teilweise     | ✓             |

Legende:  
✓ = trifft zu  
○ = teilweise  
✗ = trifft nicht zu

### 7.5 Übergang von A zu C: Ein evolutionärer Pfad

KORA definiert zwei Übergangsmechanismen, die für die Forschung entscheidend sind:

1. **A → B:**  
   Reine Softwareoptimierung demonstriert das Potenzial der KORA-Prinzipien  
   im bestehenden HPC-Stack.

2. **B → C:**  
   Die Prinzipien werden in Hardware übersetzt und strukturell verankert.  
   Dieser Schritt erzeugt die extremen Effizienzgewinne (5–20× schneller, bis 99 % Energieeinsparung).

Dieser evolutionäre Pfad zeigt Wissenschaftlern und Ingenieuren,
dass KORA nicht nur eine theoretische Architektur ist,
sondern ein pragmatischer, real umsetzbarer Entwicklungsweg.

### 7.6 Fazit

Die drei Architekturen A, B und C bilden zusammen den wissenschaftlichen Rahmen,
in dem KORA als Modell verstanden werden muss:

- A definiert die Realität,  
- B zeigt die unmittelbare Verbesserung,  
- C zeigt das strukturelle Ideal.

Damit ist der Übergang geschaffen, in dem die interne Architektur des Monolithen (C) im Detail beschrieben werden kann.

---

## 8. Die Rolle des v3.0-Simulationsmodells in der Architektur

Das v3.0-Simulationsmodell ist nicht nur ein Werkzeug zur Leistungsbewertung,
sondern ein integraler Bestandteil der KORA-Architektur.  
Es bildet die Brücke zwischen theoretischem Design, realen HPC-Eigenschaften
und der strukturellen Konstruktion des Monolithen.  
Während viele Architekturprojekte Benchmarks nachgelagert betrachten, ist es
für KORA genau umgekehrt: Die Simulation liefert die Grundlage, aus der
Architekturprinzipien abgeleitet und validiert werden.

Das v3.0-Modell beschreibt Ausführungszeit als Summe aus vier
fundamentalen Termen:

$$
T = T_{compute} + T_{mem} + T_{comm} + T_{sync}.
$$

Diese Darstellung ist nicht nur eine mathematische Zerlegung,  
sondern eine Abbildung realer physikalischer und organisatorischer Grenzen,  
wie sie in heutigen Rechenzentren auftreten.

### 8.1 Warum Simulation ein Architekturwerkzeug ist

Im Gegensatz zu traditionellen Architekturen, die ausgehend von
Mikroarchitektur-Elementen (ALUs, Caches, Fabrics) entwickelt werden,  
geht KORA einen umgekehrten Weg:

1. Analyse realer Overheads (Memory, Communication, Sync)  
2. quantitatives Modell → Strukturprinzipien  
3. Strukturprinzipien → Hardware  
4. Hardware → Eliminierung der Overheads  

Damit wird Simulation nicht zur Leistungsprüfung, sondern zur
**architektonischen Leitlinie**.

KORA orientiert sich nicht daran, was hardwareseitig leicht zu implementieren ist,
sondern daran, was strukturell erforderlich ist, um reale Overheads zu eliminieren.

### 8.2 Der Wandel vom FLOP-Modell zum Realmodell

Version 1.0 des KORA-Modells basierte noch auf einer FLOP-zentrierten Betrachtung.
Die Analyse realer HPC-Abläufe zeigte jedoch, dass FLOPs in modernen Workloads
nur einen kleinen Teil der tatsächlichen Laufzeit ausmachen.  
Das neue Realmodell v3.0 bildet deshalb die komplette Ausführungsrealität ab:

- Datenbewegung  
- Netzwerkverkehr  
- Memory-Latenzen  
- Barrier-Kosten  
- Scheduling-Effekte  
- Random Access  
- Non-Compute Overheads  

Dieser Schritt war entscheidend, um die KORA-Architektur strukturell korrekt
herleiten zu können.

### 8.3 Der Einfluss der vier Ausführungs-Terme auf das Architekturdesign

Jeder der vier Terme hat direkte architektonische Konsequenzen:

#### (1) Compute-Term  

Entscheidung:  
**Compute wird nicht maximiert (wie bei GPUs), sondern stabilisiert.**  
M3 verwendet moderate, stabile Compute-Tiles mit deterministischen Pipelines.

#### (2) Memory-Term  

Konsequenz:  
**Memory darf nicht verteilt sein.**  
M3 nutzt banked on-die Memory mit festen Latenzen.

#### (3) Communication-Term  

Konsequenz:  
**Keine komplexe Netzwerktopologie.**  
Kommunikation bleibt lokal im Monolith → Fabric statt Netzwerk.

#### (4) Synchronisations-Term  

Konsequenz:  
**Globale Barrieren müssen durch architektonische Ordnung ersetzt werden.**  
M3 implementiert hardwarebasierte Mikrobarrieren mit 1 ms statt 20–200 ms.

Diese vier Terme steuern direkt:

- die Tile-Struktur,  
- die Fabric-Designentscheidungen,  
- die Scheduling-Algorithmen,  
- die Reproduzierbarkeitsmechanismen,  
- die Energiearchitektur.

### 8.4 Kalibrierung durch S_W-Faktoren

Die fünf KORA-Workloads (BERT, Big-Data S/L, CFD M/L) besitzen
strukturabhängige Nichtlinearitäten, die nicht durch
vollständige Hardwarekontrolle erklärbar sind.

Deshalb verwendet KORA pro Workload einen empirisch kalibrierten Faktor **S_W** :

$$
S_W = \frac{T_{real}}{T_{raw}}.
$$

Diese Faktoren sorgen dafür, dass Architektur A **realistisch** bleibt.
Damit wird jeder Architekturvergleich fair, wissenschaftlich belastbar
und reproduzierbar.

Wichtig ist:
Der Monolith (C) nutzt keine Kalibrierung —  
**er ist das strukturelle Ideal**.

### 8.5 Simulation als Validierungswerkzeug des Monolithen

Die Simulation beweist strukturell:

- Eliminierung globaler Kommunikation → starke Beschleunigung bei CFD  
- Eliminierung globaler Barrieren → große Vorteile bei numerischen Modellen  
- Reduktion der Memory-Latenzen → Vorteile bei Big Data  
- deterministische Pipelines → stabile KI-Konvergenz  
- lokale Scratchpads → keine unkontrollierten DMA-Kollisionen  
- feste Routing-Pfade → minimale Latenzvariation  

Damit ist das Simulationsmodell gleichzeitig ein Architekturpapier und
ein Validierungsinstrument.

### 8.6 Warum Simulation und Architektur untrennbar verbunden sind

Viele Systeme werden gebaut, um Modelle schneller auszuführen.
KORA wird nicht gebaut, um Modelle schneller auszuführen —  
KORA wird gebaut, weil Modelle **strukturell** schneller, stabiler,
energiesparsamer und reproduzierbarer ausgeführt werden müssen.

Das v3.0-Modell zeigt:

- wo die Engpässe liegen,  
- wie sie entstehen,  
- wie sie sich vergrößern,  
- wie sie sich beseitigen lassen.

Die Architektur ist die direkte Antwort auf diese Analyse.

Damit erfüllt KORA einen wissenschaftlichen Standard,
der vielen HPC-/KI-Projekten fehlt:
eine **belegte strukturelle Herleitung** der Architektur.

### 8.7 Fazit

Das v3.0-Simulationsmodell ist nicht nur ein Benchmark,
sondern die theoretische Basis der KORA-Architektur.  
Es zeigt:

- wie moderne HPC-/KI-Systeme wirklich funktionieren,  
- warum FLOPs irrelevant sind,  
- welche Overheads dominieren,  
- und wie diese Overheads architektonisch eliminiert werden können.

Damit bildet das Simulationsmodell die **wissenschaftliche Grundlage** für die Beschreibung der internen Struktur des Monolithen.

---

## 9. Der KORA-Monolith: Einleitung & Gesamtüberblick

Der KORA-Monolith ist das strukturelle Herz der gesamten Architektur.
Er stellt einen radikalen Bruch mit klassischen HPC- und KI-Systemen dar,
deren Performance durch verteilte Kommunikation, globale Barrieren,
Scheduling-Variabilität und nichtdeterministische Datenpfade limitiert wird.

Während GPUs, TPUs und HPC-Cluster auf verteiltem Rechnen, komplexen
Netzwerktopologien und einem dynamischen Scheduling-Modell basieren, verfolgt
KORA einen diametral entgegengesetzten Ansatz:

- **lokal statt verteilt**,  
- **geordnet statt dynamisch**,  
- **deterministisch statt stochastisch**,  
- **strukturiert statt opportunistisch**,  
- **linear-latenzarm statt global-latenzabhängig**,  
- **energieproportional statt overheaddominiert**.

Der KORA-Monolith ist technisch gesehen ein einziger zusammenhängender
Rechenkern — kein Cluster, kein Multi-Die-Verbund, keine Sammlung
von Beschleunigern, sondern ein lokal kohärenter Block, in dem alle
Ressourcen deterministisch orchestriert sind.

Er besteht aus einer Vielzahl spezialisierter und homogener Recheneinheiten
(Tiles), die durch eine deterministische On-Die-Fabric, ein
strukturiertes Speicherbanksystem und den SRDB (Structural Runtime Data Bus)
zu einem einheitlichen, extrem stabilen Ausführungsraum verbunden sind.

### 9.1 Warum ein Monolith?

Die Analyse moderner HPC-/KI-Systeme zeigt, dass die dominierenden Engpässe
nicht durch Compute entstehen, sondern durch:

- verteilte Speicherzugriffe,
- nichtdeterministische Netzwerkpfade,
- globale Synchronisationsbarrieren,
- nichtlinear wachsende Kommunikationskosten,
- Inkonsistenzen in Ausführungsreihenfolgen,
- hohe Latenzvariabilität,
- dynamische Scheduling-Konflikte.

Solange Rechenressourcen physisch getrennt sind, müssen sie
kommunizieren und synchronisieren. Dieser strukturelle Zwang führt
zu wachsender Ineffizienz — unabhängig von der FLOP-Leistung.

Der Monolith löst dieses Grundproblem, weil:

1. **kein Netzwerk existiert**,  
2. **keine globalen Barrieren nötig sind**,  
3. **keine nichtdeterministischen Scheduling-Wege entstehen**,  
4. **Daten über extrem kurze Pfade liegen**,  
5. **Memory vollständig lokalisiert ist**,  
6. **alle DMA-Pfade strukturell definiert sind**,  
7. **Synchronisation hardwareseitig eingebettet ist**,  
8. **deterministische Takt- und Routingfenster gelten**,  
9. **keine verteilte Konsistenz nötig ist**.

Damit verschwindet eine ganze Klasse von Overheads nicht durch Optimierung,  
sondern durch **Nicht-Existenz der Ursache**.

### 9.2 Prinzipielle Struktur des Monolithen

Der Monolith besteht aus vier strukturellen Hauptebenen:

1. **Tiles**  
   - kleinere, einheitliche Rechendomänen  
   - jeweils mit Scratchpad, Scheduler und lokalem DMA  
   - verantwortlich für deterministische Ausführung

2. **Memorybank-System**  
   - mehrere parallele Banken  
   - definierte, garantierte Latenzen  
   - deterministische Arbitration  
   - keine nichtdeterministische Cache-Hierarchie

3. **SRDB (Structural Runtime Data Bus)**  
   - global deterministischer Metadatenbus  
   - steuert Partitionierung, Workloads, Dependencies  
   - ersetzt dynamische Scheduling- und Hashing-Mechanismen

4. **On-Die Fabric (TDM-basiert)**  
   - deterministische Zeitslots  
   - garantierte Routingwege  
   - keine variable Latenz  
   - kein Paketverlust  
   - keine dynamische Pfadfindung

Diese vier Ebenen bilden gemeinsam eine Architektur, die sich wie ein
**einziger zeitlich geordneter Ausführungsraum** verhält.

### 9.3 Der Monolith als deterministischer Ausführungsraum

Im Gegensatz zu klassischen Architekturen, die durch:

- Out-of-Order-Execution,
- dynamische Load/Store-Pipelines,
- nichtdeterministische Thread-Scheduler,
- konkurrierende DMA-Transfers,
- variable Interconnect-Latenzen

charakterisiert sind, besitzt der Monolith einen **hard-coded Execution Path**:

- Jede Operation findet in einer definierten Sequenz statt.  
- Jedes Tile besitzt einen deterministischen Scheduling-Baum.  
- Die Fabric weist jeder Nachricht einen festen Slot zu.  
- Memoryzugriffe haben feste Zugriffsfenster.  
- DMA-Transfers sind sequenziell und deterministisch.  
- SRDB synchronisiert Metadaten global und geordnet.  
- Barrieren werden mikrostrukturell abgewickelt.  

Das Resultat ist ein vollständig reproduzierbarer Ablauf:

$$
r_{bit} = 1.0, \quad r_{run} = 1.0.
$$

Damit wird der Monolith zur ersten Architektur,  
die *wissenschaftlich echte Deterministik* ermöglicht.

### 9.4 Energieprofil des Monolithen

Energieverbrauch entsteht primär durch **Datenbewegung**, nicht durch Compute.

Der Monolith spart Energie durch:

- extreme Lokalität von Datenpfaden,  
- kurze Leitungswege im On-Die-System,  
- deterministische statt konfliktreicher DMA-Pfade,  
- minimalen Kommunikationsaufwand,  
- mikrostrukturelle Barrieren (1 ms),  
- fehlende Netzwerk- und PCIe-Verluste,  
- stabile thermische Profile ohne Spitzen.

Dies reduziert Overheads auf ein Niveau, das im HPC-Bereich
bisher nicht erreichbar war.

### 9.5 Der Monolith als wissenschaftliches Werkzeug

Durch seine Eigenschaften eignet sich der Monolith für besonders
anspruchsvolle wissenschaftliche Anwendungen:

- numerische Simulationen  
- Klima- und Wettermodelle  
- hochstabile PDE-Löser  
- deterministische KI-Modelle  
- Big-Data-Pipelines ohne Shuffle-Bottlenecks  
- fein aufgelöste CFD-Berechnungen  
- medizinische Modelle mit strengen Reproduzierbarkeitsanforderungen

Der Monolith ist damit nicht nur eine Hardwarestruktur,
sondern ein wissenschaftliches Werkzeug für:

- Validität,  
- Reproduzierbarkeit,  
- Energieeffizienz,  
- Robustheit,  
- und präzise Modellkontrolle.

### 9.6 Übergang zu den folgenden Kapiteln

Kapitel 10–33 beschreiben die Struktur des Monolithen im Detail:

- Tile-Klassen  
- Microarchitecture  
- Scratchpads  
- Memorybanks  
- Arbitration  
- DMA-Engines  
- Routing  
- Scheduling  
- SRDB  
- Synchronisation  
- Power- und Thermalsysteme  
- Debug- und Fehlerhandling  
- Security-Minimalmodell  

Diese Kapitel bilden den technischen Kern der gesamten Spezifikation.

---

## 10. Tile-Classification: Die strukturellen Grundbausteine des Monolithen

Der KORA-Monolith basiert auf einer modularen, aber streng geordneten
Aufteilung des Dies in funktional spezialisierte Rechendomänen —
den **Tiles**. Diese Tiles bilden die grundlegenden Bausteine der
Architektur; sie definieren die Datenpfade, die Berechnungseinheiten,
die Synchronisationsmechanismen und die Interaktion mit dem Memorybank-System.

Jedes Tile ist ein deterministischer Ausführungsraum mit:

- eigenem Scratchpad (lokaler Speicher),
- eigenem Scheduler (deterministische Ausführungsreihenfolge),
- eigener DMA-Engine (lokales Laden/Speichern),
- definierter Verbindung zur On-Die Fabric,
- garantierten Zugriffspfaden zu Memorybanks,
- lokaler Mikrobarriere-Einheit,
- fester Pipeline-Struktur.

Die Tiles unterscheiden sich in ihrer Funktion, nicht in ihrem Prinzip:
Alle folgen denselben deterministischen Grundregeln und tragen zur
lokalen und globalen Ordnung des Systems bei.

Der Monolith nutzt fünf Tile-Klassen:

1. **Compute-Tiles (CT)**
2. **Synchronization-Tiles (ST)**
3. **SRDB-Tiles (RT)**
4. **DMA-Tiles (DT)**
5. **Memory-Arbitration-Tiles (MT)**

Diese Tile-Klassen werden im Folgenden beschrieben.

### 10.1 Compute-Tiles (CT)

Compute-Tiles bilden die primären Recheneinheiten des Monolithen.
Sie führen die eigentlichen numerischen und logischen Operationen aus:

- Tensoroperationen  
- Punkt-zu-Punkt-Berechnungen  
- Finite-Differenzen-Schemata  
- Graph-/Big-Data-Operationen  
- Vektorreduktionen  
- lokale Update-Schritte  
- KI-Trainings-Forward-/Backward-Pfade  

#### Strukturmerkmale:

- **lokales Scratchpad** (typ. 256–1024 KB)  
- **deterministischer Mikro-Scheduler**  
- **Pipeline in fester Breite**  
- **lokale Vector/Matrix-Einheiten (VMUs)**  
- **kein Out-of-Order, keine spekulative Ausführung**  
- **feste Load/Store-Slots**  
- **definierte Interaktion mit ST/RT/DT/MT-Knoten**

#### Aufgaben:

- Ausführung aller rechenintensiven Aufgaben  
- Verarbeitung block-lokaler Daten  
- Umsetzung der deterministischen Partitionierung  
- Erzeugung reproduzierbarer numerischer Ergebnisse  

Compute-Tiles sind bewusst **einfacher**, aber **stabiler**  
als moderne GPU-Kerne — sie priorisieren Ordnung statt Spekulation.

### 10.2 Synchronization-Tiles (ST)

Synchronisation ist im Monolithen hardwarebasiert und wird durch
eigene Tile-Klassen durchgeführt.  
STs übernehmen:

- Mikrobarrieren (lokal)  
- regionale Ausführungskoordination  
- Sequenzierung von Iterationsschritten  
- Taktfenstervergabe  
- Sanity-Checks deterministischer Reihenfolgen  

Ein ST koordiniert typischerweise:

- 4–16 Compute-Tiles (lokale Gruppe)  
- 1–2 DMA-Tiles  
- angeschlossene Memory-Arbitration-Tiles  

#### Strukturmerkmale:

- **absolute Zeitbasis** (clock domain controller)  
- **Barrier-Puffer**  
- **Sequencer für deterministische Abläufe**  
- **zeitfenstergesteuerte Ausgabe an die Fabric**  

#### Aufgaben:

- Sicherstellen, dass alle CTs einer Gruppe  
  *exakt* denselben Ausführungspfad nehmen  
- Eliminierung von Jitter in Sequenzen  
- Verwaltung der lokalen TDM-Slots  
- Übergabe globaler Kommandos des SRDB  

STs sind der Garant für lokale Kohärenz.

### 10.3 SRDB-Tiles (RT)

RTs implementieren den **Structural Runtime Data Bus**,  
das zentrale Koordinationssystem des Monolithen.  
Sie sind extrem wichtig, weil sie:

- Metadaten deterministisch verteilen  
- die Partitionierung der Workloads steuern  
- Scheduling-Bäume global formen  
- Workspaces definieren  
- Kommunikationsfenster zuweisen  
- Konflikte durch statische Ordnungslogik verhindern  

Der SRDB ist das strukturelle Äquivalent zu einem Betriebssystem —  
aber deterministisch und hardwareimplementiert.

#### Strukturmerkmale:

- **Metadatenkreise** (RD-Pipelines)  
- **Workload-Partitioner**  
- **Abhängigkeitsauflöser**  
- **Konfliktvermeidungslogik**  

#### Aufgaben:

- globale deterministische Kontrolle  
- Übergabe von Modellphasen (z. B. Iterationsschritte)  
- Verwaltung aller globalen TDM-Slots  
- Koordination komplexer Workloads  

RTs sind entscheidend für die globale Ordnung der Architektur.  
Sie verhindern *jedes* nichtdeterministische Scheduling.

### 10.4 DMA-Tiles (DT)

DMA-Tiles laden und speichern Daten deterministisch aus/zu Memorybanks.

#### Strukturmerkmale:

- **lokale DMA-Pipeline**  
- **deterministische Loads/Stores (kein OOO)**  
- **vorgelagerte Prefetch-Puffer**  
- **angeschlossene Scratchpads**  

#### Aufgaben:

- pipelinegenaue Bereitstellung von Daten  
- garantierte Zugriffsfenster  
- sequentielle DMA-Ausführung ohne Race Conditions  
- Vermeidung globaler Buskollisionen  

DMA-Tiles ersetzen die komplette dynamische Komplexität klassischer
Load/Store-Subsysteme.

### 10.5 Memory-Arbitration-Tiles (MT)

MTs verwalten die Bank-Arbitration der lokalen Memorybanks.

#### Strukturmerkmale:

- **deterministischer Bank-Scheduler**  
- **Latenzgarantien**  
- **Dual-Port- oder Multi-Port-Mechanik**  
- **keine spekulative Priorisierung**  

#### Aufgaben:

- garantierte Memory-Latenzen  
- zeitfensterbasierte Arbitration  
- reproduzierbare Load/Store-Sequenzen  
- Vermeidung jeglicher Memory-Race-Conditions  

MTs eliminieren die zentrale Quelle heutiger HPC-Instabilitäten:
**nichtdeterministische Speicherzugriffe**.

### 10.6 Schnittstellen zwischen den Tile-Klassen

Alle Tiles interagieren streng deterministisch:

- CT ↔ DT: Datenbereitstellung  
- CT ↔ ST: Synchronisation  
- ST ↔ RT: Phasenkontrolle  
- DT ↔ MT: Speicherzugriffe  
- RT ↔ ST: globale Koordination  
- ST ↔ Fabric: Routingfenster  
- DT ↔ Fabric: DMA-Routen  

Es gibt keine dynamischen Interaktionen, keine inkonsistenten Zugriffe,
keine Rennen, keine Zufallsentscheidungen.

### 10.7 Tile-Hierarchie im Monolithen

Der Monolith ist in Gruppen organisiert:

- **Tile-Gruppe**  
  - 4–16 Compute-Tiles  
  - 1–2 DMA-Tiles  
  - 1 Synchronization-Tile  
  - zugehörige Memory-Arbitration-Tiles  

- **Region**  
  - mehrere Tile-Gruppen  
  - 1–2 SRDB-Tiles  

- **Gesamtausführung**  
  - deterministische Kombination aller Gruppen  

Diese Struktur bildet eine stabile, skalierbare und reproduzierbare
Ausführungsplattform.

### 10.8 Fazit

Tile-Classification ist das Fundament des KORA-Monolithen.
Sie definiert:

- die funktionale Ordnung,  
- die deterministischen Interaktionen,  
- die lokalen Ausführungsräume,  
- die Eliminierung globaler Overheads,  
- die Grundlage für Scheduling, Fabric und SRDB.

---

## 11. Tile-Microarchitecture 
(Datenpfade, Pipelines, Scratchpad)

Ein Tile im KORA-Monolithen ist eine deterministische, lokal geschlossene
Rechendomäne. Seine Mikroarchitektur ist darauf ausgelegt, Daten in exakt
definierten Reihenfolgen zu verarbeiten, minimale Latenzvariabilität zu
erzielen und vollständig reproduzierbare Operationen auszuführen.

Die Mikroarchitektur eines Tiles besteht aus sechs funktionalen Ebenen:

1. **Instruction Sequencer**  
2. **Pipeline (fixed-width, fixed-depth)**  
3. **Register File & Operand Routing**  
4. **Scratchpad Memory (SPM)**  
5. **Deterministische DMA Engine**  
6. **Microbarrier & Tile Clock Domain**

Diese Komponenten bilden einen vollständig deterministischen
Ausführungsblock ohne Out-of-Order, ohne Spekulation, ohne dynamische Heuristiken
und ohne nichtdeterministische Seiteneffekte.

### 11.1 Instruction Sequencer

Der Instruction Sequencer eines Tiles ist der deterministische Taktgeber
seiner internen Operationen.  
Er unterscheidet sich deutlich von klassischen CPU/GPU-Schedulern:

- keine Out-of-Order-Ausführung,  
- keine spekulative Pfadvorhersage,  
- keine dynamischen Prioritäten,  
- feste Instruktionsreihenfolgen pro Workload-Phase,  
- Hardware-seitig unveränderbare Ausführungspfade.

#### Strukturmerkmale:

- **Fixed-Control Path**  
  Jede Instruktion folgt einer festen Mikrocode-Sequenz.

- **Sequenzfenster (Sequence Window)**  
  Der Sequencer kennt jede Operation, bevor sie ausgeführt wird —
  kein spontaner Kernel-Start.

- **SRDB-Anbindung**  
  Workloadphasen werden über definierte SRDB-Kommandos gewechselt.

#### Konsequenzen:

- deterministische Instruktionsreihenfolgen  
- keine Pipeline-Hazards durch dynamische Umschaltung  
- bitgenaue Ausführung aller numerischen Operationen  

### 11.2 Pipeline: fixed-width, fixed-depth

Ein Tile besitzt eine Pipeline, deren Breite und Tiefe **konstant** sind.
Dies unterscheidet KORA fundamental von modernen Out-of-Order-Designs:

| Merkmal         | GPU/TPU          | KORA-Tile              |
|-----------------|------------------|------------------------|
| Pipeline-Breite | variabel         | fest                   |
| Pipeline-Tiefe  | dynamisch        | fix                    |
| Hazards         | dynamisch gelöst | strukturell eliminiert |
| Scheduling      | heuristisch      | deterministisch        |
| Timing          | jitteranfällig   | jitterfrei             |

#### Pipelinephasen:

Eine typische CT-Pipeline umfasst:

1. **IF – Instruction Fetch**  
2. **RD – Operand Read**  
3. **ALU1 – Vorverarbeitung / Indexarithmetik**  
4. **ALU2 – Kernoperation (Vektor, Matrix, Tensor)**  
5. **WB – Writeback ins Register File oder Scratchpad**

Jede Phase besitzt ein **festes Zeitbudget**.

#### Vorteile:

- kein Variationsjitter  
- keine dynamischen Stalls  
- reproduzierbare Timing-Profile  
- Sicherheit für deterministisches Scheduling  

### 11.3 Register File & Operand Routing

Jedes Tile enthält ein dediziertes Registerfile, das:

- statisch partitioniert ist,  
- keine dynamischen Ports besitzt,  
- durch deterministisches Routing angebunden ist.

#### Eigenschaften:

- **Separate Read/Write-Bänke**  
  Eliminierung von Konflikten.

- **Fixed Routing Paths**  
  Jeder Operand folgt stets denselben Signalwegen.

- **Kein Register Renaming**  
  → keine Variabilität, keine Abhängigkeit von dynamischen Tabellen.

- **Deterministische Latenzen**  
  → alle Zertifikatsprüfungen, Debugging und Reproduzierbarkeit werden erleichtert.

### 11.4 Scratchpad Memory (SPM)

Das Scratchpad ist das wichtigste Element eines Tiles.
Es ersetzt vollständig:

- L1 Cache,  
- L2 Cache,  
- unvorhersehbare Cache-Hierarchien,  
- dynamische Cache-Kohärenzsysteme.

#### Eigenschaften des Scratchpads:

- **lokal, nicht-cache-basiert**  
- **explizit adressiert (software- / SRDB-gesteuert)**  
- **feste Zugriffszeit** (z. B. 2–4 Zyklen)  
- **mehrere Bänke mit deterministischer arbitration**  
- **keine Miss Penalties**  
- **keine Refill-Logik**  
- **keine dynamische Replacement Policy**

Damit ist das Scratchpad nicht nur schneller, sondern vor allem:

- absolut vorhersagbar,  
- völlig deterministisch,  
- nie Opfer komplexer Cache-Interferenzen.

#### Größe:

Typisch 256–1024 KB pro Tile, abhängig vom Tile-Typ.

### 11.5 Deterministische DMA Engine

Jedes Tile besitzt seine eigene deterministische DMA-Engine.
Sie verdrängt die komplette dynamische Komplexität klassischer
Load/Store-Systeme.

#### DMA-Mechanismen im Tile:

- **Fixed Transfer Slots**  
  Jedes DMA-Fenster besitzt ein festes Taktbudget.

- **Sequential DMA**  
  Keine parallelen DMA-Zweige → kein Chaos auf der Fabric.

- **SRDB-gesteuerte Prefetch-Logik**  
  Prefetch findet exakt in definierten Sequenzfenstern statt.

- **Zero-Race Arbitration**  
  Arbitration ist nicht heuristisch, sondern streng zeitfensterbasiert.

#### Konsequenzen:

- deterministische Datenbereitstellung  
- keine unvorhersehbaren Stalls  
- reproduzierbare Memory-Bound Workloads

### 11.6 Microbarrier & Tile Clock Domain

Jedes Tile besitzt eine **lokale Mikrobarriere**:

- synchronisiert alle Pipelineelemente,  
- bildet die klare, stabile Zeitbasis für lokale Abläufe,  
- interagiert mit dem ST (Synchronization-Tile)  
  für regionale Barrieren.

#### Funktionen:

- Fixierung von Tile-internen Sequenzen  
- Pufferung deterministischer Instruktionsbündel  
- Eliminierung jeder internen Variabilität  
- Übergang zu Synchronisationspunkten ohne Jitter

Jedes Tile gehört zu einer **lokalen Clock Domain**:

- deterministische Frequenz  
- kein dynamisches Frequency Scaling  
- kein DVFS  
- kein variable Latency Scaling

Damit bleibt die gesamte Pipeline zeitlich vollständig vorhersagbar.

### 11.7 Tile-Microarchitecture als deterministisches Subsystem

Ein Tile ist ein selbstgenügsamer, deterministischer Rechenknoten.
Im Gegensatz zu klassischen GPU- oder TPU-Kernen:

- gibt es keine dynamischen Pfade,  
- keine branch predictors,  
- keine spekulative Ausführung,  
- keine Out-of-Order-Units,  
- keine Cache-Misses,  
- keine dynamischen DMA-Kollisionen,  
- keine variable Latenzen,  
- keine Scheduling-Heuristiken.

Der Tile ist nicht schnell, weil er spekuliert,  
sondern schnell, weil er **geordnet** ist.

### 11.8 Fazit

Die Tile-Mikroarchitektur bildet den technischen Kern des Monolithen.
Sie stellt sicher, dass jeder Rechenschritt:

- deterministisch,  
- reproduzierbar,  
- strukturell vorhersehbar,  
- energieeffizient,  
- konfliktfrei,  
- ausführungskohärent  

ist.  

---

## 12. Memorybank-Layout 
(Struktur, Latenzen, deterministische Zugriffsregeln)

Das Memorybank-System ist einer der zentralen Bausteine des KORA-Monolithen.
Im Gegensatz zu klassischen Architekturen, die auf hierarchischen Caches,
dynamischen Replacement-Policies, Coherence-Protokollen und unvorhersehbaren
Memory-Latenzen basieren, nutzt KORA ein flaches, deterministisches
Memory-Modell mit festen Zugriffsfenstern.

Während GPUs und HPC-CPUs Speicherzugriffe über komplexe,
nichtdeterministische Hierarchien organisieren, stellt KORA
**banked on-die Memory** bereit:

- mit **garantierten Latenzen**,  
- mit **deterministischen Arbitration-Regeln**,  
- mit **keinen Cache-Misses**,  
- mit **keinen zufälligen Konflikten**,  
- mit **keiner dynamischen Coherence-Logik**,  
- mit **fester, planbarer Zugriffstopologie**.

Diese Struktur ist essenziell für bitgenaue Reproduzierbarkeit,
deterministische Performance und garantierte Energieprofile.

### 12.1 Grundarchitektur: Banked On-Die Memory

Der Monolith besitzt **mehrere identische Memorybanks**, typischerweise:

- 16, 32 oder 64 Banken  
- je nach Die-Größe und Leistungsprofil  
- mit festen Zugriffsbreiten (z. B. 256 oder 512 Bit pro Port)

Jede Tile-Gruppe erhält Zugriff auf **eine feste Untermenge** dieser Banken.
Es gibt **keine dynamische Zuordnung**, keinen „globalen Memory-Pool“, keine
lastabhängige Partitionierung.

#### Vorteile banked memory:

- keine Coherence-Protokolle  
- keine dynamischen Konflikte  
- keine Verdrängung (Eviction)  
- keine Cache-Misses  
- keine assoziative Suche  
- keine unvorhersehbaren Latenzen  

Der Zugriff ist immer:

§§
L_{memory} = \text{konstant}
§§

(z. B. 12–20 Takte, abhängig vom Prozessknoten)

### 12.2 Dual-Port / Multi-Port Zugriffsmodell

Jede Bank besitzt:

- **2–4 Ports** für paralleles Lesen/Schreiben  
- **feste Arbitration-Zeitfenster**  
- **lokale Latenzgarantie pro Port**

Im Gegensatz zu klassischen Multi-Port-Caches wird hier *nicht*
parallelisiert, wo es möglich ist — sondern:

- strikt geordnet,  
- deterministisch aufgeteilt,  
- konfliktfrei in festen Zeitfenstern.

#### Konsequenz:

Alle parallelen Lese- oder Schreibzugriffe sind **deterministisch**,
weil sie durch:

- Tile-zu-Bank-Zuordnung,  
- Arbitration-Zeitfenster,  
- Zugriffsfenster pro Tile

vorher festgelegt sind.

### 12.3 Speicheradressierung: strukturelle Partitionierung

KORA verwendet **strukturierte Adressräume**:

- Jeder Tile-Gruppe gehört ein klar definierter Adressbereich.  
- Keine Gruppe darf außerhalb ihres Bereichs operieren.  
- Bankkonflikte entstehen nicht, weil die Partitionierung hardwarefest ist.  

Jede Adresse folgt einem festen Schema:

[Region-ID | Tile-Group-ID | Memory-Bank-ID | Offset]

Damit wird die übliche Komplexität (Caches, TLBs, virtuelle Adressen,
Speicherkoheränzsysteme) vollständig eliminiert.

### 12.4 Speicherzugriffsregeln: deterministische Arbitration

Die Memory-Arbitration erfolgt über:

- **Memory-Arbitration-Tiles (MT)**  
- ein **zeitfensterbasiertes Arbitration-Modell**  
- mit **keinem heuristischen Priorisierungssystem**,  
- **keiner dynamischen Queue**,  
- **keinen RTT-Schwankungen**,  
- **keinem Memory-Bandwidth-Throttling**.

#### Arbitration-Mechanismus:

Jeder Zugriff läuft durch:

1. **Request-Window** (definiert durch Tile-Scheduler)  
2. **Bank-Window** (definiert durch MT)  
3. **Transfer-Window** (Teil der TDM-Fabric)  
4. **Completion-Window** (Mikrobarriere)

Diese vier Fenster sind deterministisch sequenziert.

#### Ergebnis:

$$
L_{effektiv} = L_{bankdefault}
$$

Ohne Variation, ohne Konflikte, ohne dynamische Verzögerungen.

### 12.5 Scratchpad-Integration

Scratchpads (SPM) arbeiten eng mit den Memorybanks zusammen:

- Burst-Transfers über DT-DMA  
- deterministische Prefetch-Zeitfenster  
- lokale Kopie → lokale Verarbeitung  
- keine Rückschreibung außerhalb definierter Sequenzen  

**SPM ist niemals Ersatz für Memory**, sondern explizit organisierter
Temporärspeicher, ähnlich einem lokalen, deterministischen L1 ohne Misses.

### 12.6 Datenlebenszyklus eines Speicherzugriffs

Ein typischer Datenzugriff erfolgt in folgenden Schritten:

1. **RT (SRDB) setzt Modellphase**  
2. **CT fordert über seinen Scheduler Daten an**  
3. **DT erhält Transferfenster**  
4. **MT identifiziert Bankfenster**  
5. **Transfer erfolgt deterministisch über Fabric**  
6. **SPM erhält Daten zur Pipelinevorbereitung**  
7. **CT führt Berechnung durch**  
8. **SPM schreibt deterministisch zurück**  
9. **DT führt Writeback aus**  
10. **Mikrobarriere synchronisiert Abschluss**

Der Lebenszyklus besitzt **keine nichtdeterministischen Zustände**.

### 12.7 Latenzmodell

Typische Werte (prozessabhängig):

- **Memorybank-Latenz:** 12–20 Takte  
- **Arbitration:** 1–3 Takte  
- **DMA-Transfer über Fabric:** 5–10 Takte  
- **SPM-Latenz:** 2–4 Takte  
- **Pipeline-Integration:** 3–5 Takte  

Damit ergibt sich ein Gesamtzugriff:

$$
L_{gesamt} \approx 25–40 \text{ Takte}
$$

— garantiert, ohne Variation.

Im Vergleich dazu:

- GPU-Latenz kann 200–800 Takte variieren (Cache-Misses, Coherence, Warps)
- CPU-Latenz kann 100–2000 Takte variieren (miss->refill->TLB->LLC)

KORA vermeidet sämtliche Variabilität.

### 12.8 Eliminierte Overheads

Durch das Memorybank-Layout werden eliminiert:

- Cache-TLB-Kaskaden  
- dynamische Coherence-Protokolle  
- Cache-Misses  
- Prefetch-Miss-Penalties  
- Bankkollisionen  
- spekulative Loads  
- dynamische Prioritäten  
- variable DMA-Pfade  
- Out-of-Order Scheduling

Diese Eliminierung hat sowohl Performance- als auch Energieeffekt:

| Overhead | GPU/CPU | KORA |
|----------|--------|-------|
| Latenzvariabilität | hoch | 0 |
| Coherence-Kosten | hoch | 0 |
| Cache-Miss-Kosten | sehr hoch | 0 |
| Speicherbandbreiten-Verlust | 30–60 % | <5 % |
| deterministische Latenz | nein | ja |

### 12.9 Zusammenfassung

Das Memorybank-Layout ist eine der wichtigsten Komponenten des Monolithen:

- deterministische Speicherzugriffe  
- garantierte Latenzen  
- keine Konflikte  
- keine Caches  
- keine Koheränzprobleme  
- kein dynamisches Scheduling  
- vollständige Reproduzierbarkeit  
- linear-skalierbares Latenzmodell  

Die folgenden Kapitel beschreiben, wie deterministische Speicherzugriffe global über das gesamte Die synchronisiert werden.

---

## 13. Memory Arbitration Logic 
(deterministische Banksteuerung)

In klassischen HPC-/KI-Systemen wird der Zugriff auf den Hauptspeicher durch
dynamische, heuristische Verfahren vermittelt:

- dynamische Priorisierungsqueues  
- spekulative Load-/Store-Vorhersagen  
- bankübergreifende Kollisionsauflösung  
- Out-of-Order-Reihenfolgen  
- reaktive Coherence-Protokolle  
- nichtdeterministische Pufferinteraktionen  

Diese Mechanismen sind der zentrale Grund dafür, dass moderne Systeme:

- unvorhersehbare Memory-Latenzen besitzen,  
- Scheduling-Jitter produzieren,  
- bitgenaue Reproduzierbarkeit verlieren,  
- Performance-Plateaus erreichen,  
- Energie-Overheads bis zu 70 % erzeugen.

KORA eliminiert diese Komplexität vollständig.

Die Memory-Arbitration wird durch **Memory-Arbitration-Tiles (MT)** durchgeführt,
die ausschließlich deterministische Regeln befolgen und keinerlei heuristische
Komponenten enthalten.

### 13.1 Architektur der Memory-Arbitration-Tiles (MT)

Ein Memory-Arbitration-Tile ist ein dedizierter Hardwareblock,
der die Zugriffsrechte auf eine Gruppe von Memorybanks verwaltet.

#### MT bestehen aus:

- **Fixed Arbitration Scheduler**  
  – sequentielle, feste Entscheidungslogik  
  – kein dynamisches Reordering

- **Slot-Allocator**  
  – teilt feste Zeitfenster für Zugriffe zu  
  – niemals heuristisch oder lastabhängig

- **Access-Validator**  
  – verifiziert, dass CT/DT-Zugriffe im erlaubten Fenster liegen

- **Bank-Selector**  
  – wählt deterministisch die Zielbank anhand fester Tabellen  

- **Deadline Unit**  
  – garantiert feste Abschlusszeiten pro Zugriff

#### Wichtige Merkmale:

- keine Warteschlangen  
- keine Konfikte  
- keine dynamischen Prioritäten  
- keine Paketverluste  
- keine Unschärfen im Timing  

Damit wird das gesamte Memory-System reproduzierbar.

### 13.2 Zeitfensterbasierte Arbitration

Alle Speicherzugriffe werden in **deterministischen Zeitfenstern (Slots)**
geordnet, die durch die On-Die Fabric synchron bereitgestellt werden.

Jedes Tile erhält pro Scheduling-Zyklus:

- **ein Lese-Slot-Fenster**,  
- **ein Schreib-Slot-Fenster**,  
- optional **ein DMA-Fenster** für große Transfers.

#### Eigenschaften:

| Merkmal | GPU/CPU | KORA |
|---------|---------|-------|
| Slot-Zuteilung | dynamisch | deterministisch |
| Latenz | variabel | konstant |
| Arbitration | heuristisch | fixed-rule |
| Bankkollision | möglich | unmöglich |
| Zyklenverzug | häufig | 0 |

#### Ablauf eines Speicherzugriffs:

1. Tile-Scheduler öffnet Request-Fenster  
2. MT validiert Request gegen Slot  
3. Bank-Selector definiert exakte Bank  
4. Transfer erfolgt im TDM-Zeitfenster  
5. Completion wird deterministisch bestätigt  

Dieser Ablauf ist jedes Mal identisch.

### 13.3 Bankzugriff ohne Kollisionen

Bankkonflikte — einer der größten Bremsfaktoren moderner GPUs — existieren im Monolithen **nicht**.

Dies wird erreicht durch:

- feste Zuordnung Tile-Gruppe ↔ Bank-Gruppe  
- strukturierte Adressräume  
- deterministische Transfer-Slots  
- Single-Writer-Policy pro Slot  
- keine dynamische Replication  

#### Der wichtigste Punkt:

**Jedes Tile weiß genau, wann welche Bank frei ist.**

Es gibt keine Überraschungen, keine Wartezeit, keinen Thundering-Herd-Effekt,
keine Pipeline-Stalls.

### 13.4 Arbitration-Regeln (formal)

Ein Speicherzugriff eines Tiles $\( T_i \)$ auf Bank $\( B_j \)$ ist gültig, wenn:

1. **Zugriff im korrekten Tile-Zeitfenster:** 

$$
t \in W_{tile}(T_i)
$$

2. **Zugriff im korrekten Bank-Zeitfenster:**

$$
t \in W_{bank}(B_j)
$$

3. **Zugriff entspricht der statischen Mapping-Tabelle:**

$$
map(T_i) = B_j
$$

4. **keine konkurrierenden Schreib-/Lesekonflikte**  
   (durch Rule 3 strukturell ausgeschlossen)

5. **DMA-Zeitslots passen in globale TDM-Fabric:**

$$
slot(DT_k) = W_{dt}(T_i)
$$

Damit ist jeder Zugriff logisch und zeitlich vollständig festgelegt.

### 13.5 Eliminierung klassischer Memory-Overheads

Durch die deterministische Arbitration eliminiert KORA:

- Latenzvariabilität  
- dynamische Memory-Conflicts  
- Cache-Kollisionen  
- unkontrollierte Prefetch-Muster  
- DMA-Zusammenstöße  
- prioritätsbasierte Timing-Jitter  
- Busy-Wait Loops  
- falsche Vorhersagen durch Branching-/Load-Predictoren  

Dies führt zu:

#### (1) stabiler Zeit pro Zugriff  

$$
L_{total} \approx 25–40 \text{ Takte, garantiert}
$$

#### (2) stabiler Energieverbrauch  

→ kein stochastischer Verbrauch mehr  
→ minimaler thermischer Jitter

#### (3) bitgenaue Reproduzierbarkeit  

→ deterministisches Verhalten aller Datenpfade  
→ Debugging und Validierung werden trivial

### 13.6 Zusammenspiel mit anderen Tiles

Arbitration beeinflusst:

- Compute-Tiles (CT)  
  → garantierte Datenbereitstellung

- DMA-Tiles (DT)  
  → konfliktfreie Übertragungsfenster

- Synchronization-Tiles (ST)  
  → Fensterfreigaben je Iteration

- SRDB-Tiles (RT)  
  → definieren globale Sequenzphasen

Damit ist MT ein **zentraler Ordnungspunkt** der gesamten Architektur.

### 13.7 Beispiel: deterministischer Zugriffspfad

Ein Speicherzugriff eines Compute-Tiles CT₁ auf Bank B₃ verläuft:

1. SRDB setzt neue Iterationsphase  
2. ST öffnet CT-Zugriffsfenster  
3. CT sendet Request an MT  
4. MT validiert zugeordnete Bank  
5. MT öffnet Bankfenster B₃  
6. DT führt Transfer im globalen TDM-Slot aus  
7. SPM schreibt Daten ins Tile  
8. Mikrobarriere synchronisiert Pipeline  
9. Completion wird gemeldet  

Dieser Ablauf bleibt in *jedem Durchlauf identisch*.

### 13.8 Fazit

Die Memory Arbitration Logic ist eine der Kernkomponenten des Monolithen.
Sie garantiert:

- deterministische Speicherzugriffe  
- feste Latenzen ohne Variabilität  
- keine Bankkonflikte  
- konfliktfreie DMA-Transfers  
- reproduzierbare Memory-gebundene Workloads  
- stabile Energieprofile  

Memory ist damit nicht länger ein stochastischer Engpass,  
sondern ein strukturiertes, planbares Element des Gesamtsystems.

---

## 14. On-Die TDM Fabric 
(Deterministische Routing-Infrastruktur)

Die On-Die TDM Fabric ist das zentrale Kommunikationselement des
KORA-Monolithen.  
Im Gegensatz zu klassischen Network-on-Chip (NoC) Designs verwendet KORA
keine dynamischen Routing-Algorithmen, keine stochastischen Arbitrationen,
keine adaptiven Pfadentscheidungen und keine heuristischen Überlastmechanismen.

Stattdessen basiert die gesamte Fabric auf einem streng deterministischen,
zeitgesteuerten Routingmodell: **Time Division Multiplexing (TDM)**.

Damit wird jede potenzielle Quelle von Latenzvariabilität, Scheduling-Jitter
oder nichtdeterministischem Verhalten vollständig eliminiert.

### 14.1 Warum TDM?

Konventionelle NoCs besitzen inhärente Probleme:

- **variable Paketlaufzeiten**  
- **Netzwerkstaus**  
- **Paketverluste oder erneutes Ausliefern**  
- **Race Conditions zwischen konkurrierenden Paketen**  
- **Contention um Knoten und Links**  
- **nichtdeterministische Routing-Pfade**  
- **Priorisierung auf heuristischer Basis**  

Für deterministische Ausführung sind diese Eigenschaften untragbar.

KORA nutzt TDM, weil:

1. Zeitfenster vollständig vordefiniert werden können  
2. jeder Transfer in einen festen Zeitslot fällt  
3. alle Pfade garantiert konfliktfrei sind  
4. die Bandbreite absolut vorhersehbar ist  
5. keine Paketkollisionen auftreten  
6. Routing niemals variieren kann  
7. die gesamte Ausführung bitgenau reproduzierbar wird

### 14.2 Aufbau der TDM-Fabric

Die Fabric besteht aus drei Schichten:

1. **Local Switch Layer**  
   - Verbindung innerhalb einer Tile-Gruppe  
   - sehr kurze, feste Leitungslängen  
   - keine Routingentscheidungen

2. **Regional Fabric Layer**  
   - verbindet Tile-Gruppen einer Region  
   - deterministische Zeitslots pro Transfer  
   - feste Pfade ohne Variation

3. **Global Spine Layer**  
   - verbindet sämtliche Regionen  
   - global synchronisierte Zeitslots  
   - SRDB-Kontrollpfade sind inkludiert

Damit verhält sich die Fabric wie ein *statisch programmiertes Kommunikationsnetz*,
das nie dynamisch reagiert, sondern nur deterministisch ausführt.

### 14.3 Zeitslot-Mechanismus

Ein Zeitslot **S_k** ist ein definiertes Übertragungsfenster,
in dem genau **ein** Transfer über einen bestimmten Pfad stattfinden kann.

#### Eigenschaften:

- fixe Länge (z. B. 4–16 Takte)
- fixe Zuordnung Tile ↔ Bank ↔ Pfad
- keine konkurrierenden Transfers
- keine dynamische Belegung
- vollständige Reproduzierbarkeit

#### Globale TDM-Sequenz

Ein TDM-Zyklus besteht typischerweise aus 256–2048 Slots,
abhängig von:

- Tile-Anzahl  
- Fabric-Bandbreite  
- Bankanzahl  
- DMA-Frequenz  

Die Sequenz ist **zur Laufzeit unveränderlich**.

Sie wird vom SRDB-Tile in hoher Präzision definiert und für die gesamte
Monolith-Operation beibehalten.

### 14.4 Routing ohne Entscheidung

Es gibt im Monolithen **keinen Router**, der „entscheidet“.  
Routing erfolgt ausschließlich durch statische TDM-Tabellen.

Ein Paket (bzw. Datenwort) wird exakt wie folgt geleitet:

1. Die Quelle (CT/DT/RT) erhält ein Übertragungsfenster.  
2. Das Ziel (MT, SPM, CT) besitzt im selben Fenstersatz einen Empfangsslot.  
3. Die Fabric transportiert die Daten über feste Leitungen in festen Zyklen.  

Nie passiert:

- kein Re-Routing,  
- keine dynamische Umleitung,  
- keine Kollisionsvermeidung,  
- keine Prioritätsskalen,  
- keine Queue-Bildung,  
- keine Unbestimmtheit.

#### Formel:

Sei **$\( P_{i \rightarrow j} \)$** der Pfad von Tile **$\( i \)$** zu Einheit **$\( j \)$**.

Dann gilt:

$$
P_{i \rightarrow j}(t) = P_{i \rightarrow j}(0) \quad \forall t
$$

Das bedeutet:
**Jeder Pfad ist über die gesamte Ausführungszeit unverändert.**

### 14.5 Fabric-Bandbreite und Latenz

#### Bandbreite:

Die TDM-Fabric besitzt eine feste pro-Zyklus-Bandbreite:

$$
BW_{fabric} = \frac{W}{T_{slot}}
$$

mit:

- $\( W \)$ = Wortbreite des Pfads (z. B. 256 oder 512 Bit)  
- $\( T_{slot} \)$ = Slotdauer  

#### Latenz:

Da Routing deterministisch ist, ergibt sich die Latenz:

$$
L_{fabric} = n_{hops} \cdot T_{slot}
$$

Da alle Hops feste Leitungslängen besitzen:

- **$n_{hops}$ ist konstant**  
- $T_{slot}$ ist konstant  

→ **keine Variabilität**.

Im Vergleich:

| System | Latenzvariabilität |
|--------|---------------------|
| GPU NoC | 2–40× |
| CPU Mesh | 1–20× |
| HPC-Interconnect | 5–100× |
| KORA TDM Fabric | 1× (konstant, deterministisch) |

### 14.6 Eliminierte Overheads der klassischen NoCs

Die TDM-Fabric eliminiert:

- dynamische Router  
- virtuelle Kanäle  
- Backpressure  
- Packet-Drop-Recovery  
- adaptive Routingstrategien  
- Stromsparmodi mit Wakeup-Latenzen  
- Warteschlangenbildung  
- Pipeline-Flushes bei Kollisionen  
- „Heißstellen“ (Hotspots) in Meshes  

Damit reduziert der Monolith die Kommunikationslatenz nicht nur,
sondern eliminiert *sämtliche* nichtdeterministischen Komponenten.

### 14.7 Zusammenspiel mit MT (Arbitration) und DT (DMA)

Die Fabric bildet das Kommunikationsrückgrat:

- MT definiert Bankfenster  
- ST definiert Tile-Fenster  
- DT führt DMA im TDM-Slot aus  

Alle drei Komponenten interagieren deterministisch, weil:

1. jeder Transfer vorab festgelegt ist  
2. jeder Pfad konfliktfrei ist  
3. die Fabric niemals „entscheidet“  

Jeder DMA-Transfer eines Tiles findet immer exakt im selben Slot statt.

### 14.8 SRDB auf der TDM-Fabric

Der SRDB (Kapitel 15) nutzt dedizierte Fabric-Segmente:

- keine geteilten Datenpfade  
- eigene TDM-Slots  
- keine Interferenz mit Compute-/DMA-Traffic  

Dadurch hat der SRDB:

- garantierte Broadcast-Latenzen  
- konzise globale Steuerung  
- keine zufälligen Verzögerungen  
- vollständige Reproduzierbarkeit

### 14.9 Beispiel: deterministischer Transferablauf

Beispiel: CT₁ möchte Daten in Bank B₄ schreiben.

1. SRDB setzt global Checkpoint  
2. ST öffnet lokales Compute-Fenster  
3. CT₁ erzeugt Write-Request  
4. MT validiert Bankfenster  
5. DT erhält TDM-Slot (Slot 122)  
6. Fabric transportiert Daten im festen Slot 122  
7. Bank B₄ nimmt Daten in Slot 122 entgegen  
8. Tile-Gruppe wird über Mikrobarriere synchronisiert  

Dieser Ablauf ist in jedem Durchlauf identisch.

### 14.10 Fazit

Die On-Die TDM Fabric ist eine der Schlüsselinnovationen des KORA-Monolithen:

- deterministische Kommunikation  
- kein Routing-Jitter  
- keine Paketkollisionen  
- keine Latenzvariabilität  
- feste Pfade, feste Slots  
- vollständige Reproduzierbarkeit  
- linear skalierbare Kommunikation  
- strukturelle Eliminierung aller Netzwerkoverheads  

Die Fabric ist das Bindeglied zwischen:

- Memory Arbitration (Kap. 13)  
- Tile-Microarchitecture (Kap. 11)  
- SRDB-Kontrollfluss (Kap. 15)  
- Scheduling Trees (Kap. 16)  

und ermöglicht erstmals einen global deterministischen Rechenraum
ohne jede Form von stochastischem Kommunikationsverhalten.

---

## 15. SRDB Architecture 
(Structural Runtime Data Bus)

Der Structural Runtime Data Bus (SRDB) ist das zentrale Kontrollsystem des
KORA-Monolithen.  
Er übernimmt alle Aufgaben, die konventionelle Systeme über komplexe
Software-Stacks, Laufzeitumgebungen, Betriebssysteme, Heuristiken und
dynamische Scheduling-Mechanismen lösen. Im Monolithen findet all dies
deterministisch und hardwarebasiert statt.

Der SRDB ist kein Netzwerk, kein Scheduling-Framework und kein OS —
er ist ein **struktureller Kontrollbus**, der:

- Phasen des Workloads definiert,  
- Ausführungsreihenfolgen vorgibt,  
- globale Synchronisationspunkte kontrolliert,  
- Datenabhängigkeiten auflöst,  
- DMA- und Memory-Zeitfenster verteilt,  
- Konflikte präventiv eliminiert,  
- deterministische Scheduling-Bäume erzeugt,  
- und die gesamte Fabric zeitlich ordnet.

Mit anderen Worten:  
Der SRDB macht das gesamte System **synchron, deterministisch und reproduzierbar**.

### 15.1 Motivation: Warum ein struktureller Kontrollbus?

Konventionelle HPC/KI-Systeme besitzen:

- dynamische Thread-Scheduler  
- Kernel-Launch-Queues  
- Event-Handler  
- MPI-Libraries  
- Netzwerk-Routing  
- CUDA/ROCm-Driver-Interaktionen  
- Busy-Waits und Race Conditions  
- nichtdeterministische Reduktionspfade  
- unkontrollierte DMA- und Memory-Kollisionen  

Diese Komplexität führt zu:

- stochastischen Ausführungszeiten  
- instabilen Ergebnissen  
- fehlender Reproduzierbarkeit  
- massiven Energieoverheads  
- schwieriger Debugbarkeit  
- Planungsschwierigkeiten  

KORA löst diese Probleme **nicht durch Softwareoptimierung**,  
sondern durch **architektonische Ordnung**.

Der SRDB ist der Mechanismus, der alle Komponenten zusammenführt
und die deterministische Ausführung **erzwingt**.

### 15.2 Struktur des SRDB

Der SRDB besteht aus:

1. **RT-Tiles (Runtime Tiles)**  
   – dedizierte Hardwareblöcke  
   – übernehmen globale Steuerung

2. **Broadcast-Lanes**  
   – exklusive Pfade in der TDM-Fabric  
   – feste Zeitslots, niemals überlastet

3. **Metadata-Roundtrip-Pipeline (MRP)**  
   – deterministische Pipeline für Metadaten  
   – feste Latenz, kein Jitter

4. **Dependency Graph Hardware Engine (DGHE)**  
   – hardwarebasierte Abhängigkeitsprüfung  
   – generiert deterministische Scheduling-Bäume

5. **Conflict Elimination Unit (CEU)**  
   – erkennt und eliminiert Konflikte **bevor** sie auftreten

6. **Phase Sequencer**  
   – definiert globale Ausführungsphasen  
   – ähnlich einem Taktgenerator auf Metadatenebene

7. **Global Clock Domain Interface**  
   – synchronisiert alle Tile-Gruppen

### 15.3 Aufgaben des SRDB

Der SRDB übernimmt alle Kontrollaufgaben, die in klassischen Systemen
auf viele Software-Schichten verteilt sind:

#### (1) Workload-Partitionierung  

Er definiert die Partitionierung des gesamten Daten- und Aufgabenraums:

$$
W = \{W_1, W_2, \ldots, W_n\}
$$

Dabei wird **jede Partition deterministisch einem Tile-Cluster zugewiesen.**

#### (2) Scheduling-Baum-Erzeugung  

Der SRDB erstellt pro Partition einen **deterministischen Scheduling-Tree**:

- keine Heuristik  
- keine dynamische Graphdurchsuchung  
- keine Load-Balancer

#### (3) Phasensteuerung  

Jeder Workload besteht aus Modellphasen:

- Memory-Load  
- Compute-Iteration  
- Reduktionsschritt  
- Synchronisation  
- Writeback  
- neue Iteration

Der SRDB bestimmt den **globalen Phasenfortschritt**.

#### (4) Inhibitionsmechanismus  

Der SRDB verhindert, dass Tiles Aktionen außerhalb ihrer Phase ausführen.
Es existiert kein „Race Ahead“.

#### (5) Metadaten-Broadcast  

Alle relevanten Metadaten werden über dedizierte Fabric-Abschnitte synchron verbreitet.

#### (6) DMA- und Memory-Zeitfenster  

Der SRDB weist Zeitfenster zu:

- DMA-Fenster  
- Bank-Fenster  
- TDM-Kommunikationsfenster

#### (7) Deadlock-Prevention  

Deadlocks werden durch strenge Ordnungsregeln strukturell ausgeschlossen.

#### (8) Globale Barrieren  

Alle Barrieren sind hardwareimplementiert, mikrostrukturiert, jitterfrei.

### 15.4 Der SRDB-Workflow

Der SRDB arbeitet in zyklischen Phasen (ähnlich einem globalen OS-Herzschlag):

#### Phase 1: Dependency Evaluation  

DGHE analysiert Datenabhängigkeiten und erzeugt deterministische Sequenzen.

#### Phase 2: Partitioning  

Der Workload wird in strukturierte Blöcke zerlegt.

#### Phase 3: Scheduling Tree Assembly  

Aus den Partitionen werden lokale Scheduling-Trees für jede Tile-Gruppe erzeugt.

#### Phase 4: Slot Assignment  

Alle DMA-, Memory- und Routing-Slots werden festgelegt.

#### Phase 5: Global Broadcast  

Alle Tiles erhalten exakt dieselben Steuerdaten.

#### Phase 6: Execution  

Compute, DMA und Memory laufen deterministisch.

#### Phase 7: Sync  

Hardwarebasierte Barrier-Synchronisation auf Mikroebene.

Dieser Zyklus wiederholt sich pro Iteration oder Modellphase.

### 15.5 Determinismus durch SRDB

Der SRDB garantiert:

- gleiche Reihenfolgen für jeden Durchlauf  
- feste Routingfenster  
- fixe DMA-/Memory-Zeitfenster  
- deterministische Abhängigkeitspfade  
- bitgenaue numerische Ergebnisse  
- keine Variation durch Scheduling  
- keine Übertragungsvariabilität  
- vollständige Reproduzierbarkeit

Formal:

$$
f_{exec}(input) = output
$$

$$
\forall\, runs: f_{exec}^{(1)} = f_{exec}^{(2)} = \cdots
$$

### 15.6 Energieeffizienz durch SRDB

Der SRDB spart Energie, indem er:

- Überlastsituationen strukturell verhindert  
- Jitter eliminiert  
- Memory- und DMA-Kollisionen vermeidet  
- deterministische Taktfenster nutzt  
- „stille“ Zeiten (Idle-Pockets) minimiert  
- Routing-Stalls eliminiert  

Der Energieverbrauch entspricht fast vollständig der nützlichen Arbeit.

### 15.7 Zusammenspiel mit TDM-Fabric, MT, DT, CT, ST

| Komponente | SRDB-Rolle |
|-----------|------------|
| **CT (Compute-Tiles)** | definierte Operationen, Reihenfolgen |
| **DT (DMA-Tiles)** | deterministische Transferfenster |
| **MT (Memory-Arbitration)** | vordefinierte Bankfenster |
| **ST (Sync-Tiles)** | Phasenwechsel, Mikrobarrieren |
| **TDM-Fabric** | garantierte TDM-Slots |
| **SRDB-Tiles** | übergeordnete Struktur & Ordnung |

Der SRDB ist das **zentrale Nervensystem** des Monolithen.

### 15.8 Beispiel: SRDB-Steuerlauf bei einer CFD-Iteration

1. DGHE analysiert Stencil-Abhängigkeiten  
2. Partitionierung der Gitterregionen  
3. Scheduling-Trees je Region  
4. Zuweisung aller DMA/Memory-Slots  
5. globaler Metadaten-Broadcast  
6. Compute-Tiles führen 27-Punkt-Stencil aus  
7. Writebacks deterministisch  
8. Barrier-Sync  
9. nächste Iteration

Dieser Ablauf ist in jedem Run identisch.

### 15.9 Fazit

Der SRDB ist die zentrale Innovation, die KORA zu einer:

- deterministischen  
- reproduzierbaren  
- energieeffizienten  
- konfliktfreien  
- wissenschaftlich verifizierbaren  

Architektur macht.

Er ersetzt die gesamte dynamische Scheduling- und Koordinationskomplexität
klassischer HPC-/KI-Systeme durch ein **strukturelles, festgelegtes Modell**,
das alle nichtdeterministischen Komponenten eliminiert.

Mit dem SRDB ist der Monolith nicht nur ein Rechenkern,  
sondern eine **geordnete Ausführungsmaschinerie**, die neue Maßstäbe für
wissenschaftliche Reproduzierbarkeit setzt.

---

## 16. Deterministische Scheduling Trees 
(ST-Scheduling, Tile-Group-Kontrolle)

Scheduling in konventionellen HPC-/KI-Systemen ist dynamisch:

- CUDA- oder ROCm-Driver entscheiden zur Laufzeit  
- Operating Systems schedulen Threads  
- MPI erzeugt dynamische Prozesse  
- Kernel starten asynchron  
- DMA und Compute konkurrieren um Ressourcen  
- Load Balancer verteilen Operationen opportunistisch  

Diese dynamischen Scheduling-Mechanismen machen moderne Systeme
leistungsfähig — aber auch **nichtdeterministisch** und **unreproduzierbar**.

Der Monolith verfolgt einen völlig anderen Ansatz:

> **Alle Scheduling-Entscheidungen werden deterministisch in Form eines Scheduling Tree definiert — lange bevor der erste Instruktionszyklus ausgeführt wird.**

Der Scheduling Tree bestimmt:

- was jedes Tile tun darf,  
- wann es etwas tun darf,  
- in welcher Reihenfolge,  
- mit welchen Daten,  
- in welchem Iterationsschritt,  
- mit welchem DMA-Fenster,  
- und in welcher Abhängigkeit zu anderen Tiles.

### 16.1 Aufbau eines Scheduling Trees

Ein Scheduling Tree besteht aus drei Ebenen:

1. **Global Scheduling Tree (GST)**  
   – vom SRDB erzeugt  
   – gilt für den gesamten Monolithen

2. **Regional Scheduling Tree (RST)**  
   – pro Region  
   – steuert Interaktionen zwischen Tile-Gruppen

3. **Local Scheduling Tree (LST)**  
   – pro Tile-Gruppe  
   – wird vom Synchronization Tile (ST) ausgeführt

#### Formale Struktur

Ein Scheduling Tree ist ein gerichteter, azyklischer Baum:

    STree = (V, E)

mit:

- **$\( V \)$** = Operationen  
- **$\( E \)$** = deterministische Abhängigkeiten

Der Baum wird *niemals* zur Laufzeit verändert.

### 16.2 Wie Scheduling Trees erzeugt werden (DGHE → ST)

Der Ablauf:

1. **DGHE analysiert Datenabhängigkeiten**  
   – z. B. Stencil-Punkte, Tensor-Blöcke, Shuffles

2. **SRDB partitioniert den Workload**  
   – räumlich oder logisch

3. **SRDB definiert die Ausführungsreihenfolge**  
   – global, regional, lokal

4. **ST erzeugt pro Tile-Gruppe einen LST**  
   – streng sequentiell  
   – deterministisch  
   – ohne jede Heuristik

#### Beispiel (vereinfacht):

Iteration Phase:
├── Load → SPM
├── Compute Stage 1
├── Compute Stage 2
├── Reduction (lokal)
├── Writeback
└── Barrier

Jeder Knoten dieses Baums wird **hardwareseitig** ausgeführt.

### 16.3 Eliminierung klassischer Scheduling-Variabilität

Im Monolithen existiert **keine**:

- Warp Divergence  
- Thread Migration  
- dynamic parallelism  
- opportunistic load balancing  
- out-of-order execution  
- asynchronous kernel scheduling  
- priority-based reordering  
- competing DMA channels  

Stattdessen:

- feste Sequenzen  
- feste Fenster  
- feste Pfade  
- feste Bäume

#### Konsequenz:

$$
T_{execution}^{(run1)} = T_{execution}^{(run2)} = \cdots
$$

Keine Variation. Kein Jitter.

### 16.4 Tile-Gruppen und Scheduling

Jede Tile-Gruppe (TG) hat:

- 4–16 Compute-Tiles  
- 1–2 DMA-Tiles  
- 1 Synchronization-Tile  
- zugehörige MTs und Fabricfenster

Der ST (Synchronization Tile) ist verantwortlich für:

1. **Initialisieren des LST**  
2. **Durchsetzen der Reihenfolge**  
3. **Durchführen von Mikrobarrieren**  
4. **Validieren des DMA-/Memory-Zeitpunkts**  
5. **Quantisieren der Iterationen**

Der ST ist damit ein eingebetteter *lokaler Orchestrator*.

### 16.5 Zeitstruktur des Scheduling Trees

Der Scheduling Tree bestimmt die Zeitfenster für:

- Compute  
- DMA  
- Memory  
- Fabric  
- Synchronisation  
- Writeback  
- Idle-Fenster (deterministisch eingeplant)  

Die Zeit wird in **Scheduling Periods (SP)** geteilt:

$$
SP = \{sp_1, sp_2, ..., sp_N\}
$$

Jede Period enthält:

- Compute-Fenster  
- DMA-Fenster  
- Sync-Fenster  
- Writeback-Fenster  

und ist **deterministisch fixiert**.

#### Keine dynamische Periodenteilung  

Keine „Micro-Steals“, keine spontane Verlängerung, keine Konflikte.

### 16.6 Beispiel: Scheduling Tree für eine KI-Matrixmultiplikation

Simplifiziert:

LST:
├── Prefetch Block A[i,k]
├── Prefetch Block B[k,j]
├── Compute Tile 8x8
├── Accumulate Results
├── Writeback C[i,j]
└── Barrier

Jeder Schritt hat:

- feste DMA-Slots  
- feste Compute-Zeit  
- keine Varianz im Pfad  

→ deterministische Forward- und Backward-Pässe.

### 16.7 Beispiel: Scheduling Tree für einen CFD-Zeitstepp

LST:
├── Load local stencil neighborhood
├── Compute flux
├── Compute divergence
├── Apply boundary conditions
├── Update field
└── Barrier

Klassische CFD-Simulationen leiden stark unter:

- globalen Barrieren  
- Memory-bound Verhalten  
- Scheduling-Variabilität

KORA eliminiert *alles* davon.

### 16.8 Zusammenspiel mit TDM-Fabric & SRDB

Der Scheduling Tree erzeugt die **zeitliche Ordnung**,  
die Fabric sorgt für die **räumliche Ordnung**,  
SRDB kontrolliert die **metadatengetriebene Ordnung**.

| Ebene | Verantwortung |
|-------|---------------|
| SRDB | globaler Ablauf, Phasen |
| ST | lokale Ausführung, Mikrobarrieren |
| MT | Memory-Zeitfenster |
| DT | DMA-Fenster |
| TDM-Fabric | Transport-Slots |

Diese fünf Komponenten bilden gemeinsam eine **vollständig deterministische Maschine**.

### 16.9 Warum Scheduling Trees Energie sparen

Dynamische Scheduler erzeugen:

- Busy-Waits  
- Pipeline-Flushes  
- Overfetching  
- falsches Prefetching  
- spekulative Loads  
- Heat-Peaks  

Scheduling Trees eliminieren diese Effekte *strukturell*:

- kein unnötiger Datenverkehr  
- keine zufälligen DMA-Requests  
- keine Überlastung  
- perfekter thermischer Fluss  
- konsistenter Energieverbrauch pro Iteration  

### 16.10 Fazit

Die deterministischen Scheduling Trees sind die operative Basis des Monolithen:

- keine Heuristiken  
- keine dynamischen Entscheidungen  
- garantiert gleiche Reihenfolgen  
- perfekte Reproduzierbarkeit  
- minimale Energieverschwendung  
- konsistente Zeit pro Iteration  
- konfliktfreie Abläufe  
- definierte DMA- und Memoryfenster  

Sie machen den Monolithen zu einer Rechenplattform,
die nicht nur schnell, sondern **strukturell vorhersehbar und wissenschaftlich transparent** ist.

---

## 17. Synchronisationsmechanismen 
(Microbarriers, Regional Barriers, Global Barriers)

Synchronisation ist einer der fundamentalsten und zugleich problematischsten
Aspekte moderner HPC-/KI-Systeme.  
In klassischen Architekturen tritt Synchronisation durch:

- MPI-Barrieren,  
- Allreduce-Operationen,  
- Threadbarrieren,  
- GPU-Kernelgrenzen,  
- Pipeline-Stalls,  
- Scheduler-Umschaltungen,  
- volatile Locking-Mechanismen,  

auf — und führt zu:

- Latenzspitzen,  
- unvorhersehbarem Jitter,  
- Energieverlusten,  
- Race Conditions,  
- nichtdeterministischen Ausführungsreihenfolgen.

Der KORA-Monolith ersetzt die gesamte Komplexität durch einen
dreistufigen, deterministischen Synchronisationsmechanismus:

1. **Microbarriers (Tile-lokal)**  
2. **Regional Barriers (Tile-Gruppe)**  
3. **Global Barriers (Monolith-weit)**

Diese Barrieren sind vollständig hardwareimplementiert und folgen
deterministischen, zyklischen Abläufen ohne jede Variabilität.

### 17.1 Microbarriers (Tile-Lokal)

Microbarriers sind die kleinste Synchronisationseinheit im Monolithen.

Sie synchronisieren:

- Pipelinephasen,
- DMA-Transfers,
- Scratchpad-Updates,
- lokale Scheduler-Fortschritte.

#### Eigenschaften:

- **extrem geringe Latenz** (1–3 Zyklen)  
- **hardwarebasiert**  
- **keine dynamische Entscheidung**  
- **keine Busy-Waits**  
- **feste Schaltpunkte**  

Microbarriers sind Teil jedes Tiles (CT, DT, MT, RT)  
und bilden die Basisebene für garantierte Reproduzierbarkeit.

### 17.2 Regional Barriers (Tile-Gruppe)

Regional Barriers werden von den Synchronization-Tiles (ST) kontrolliert.

Sie synchronisieren:

- 4–16 Compute-Tiles  
- 1–2 DMA-Tiles  
- zugehörige MT-Tiles  
- lokale Phase des Scheduling Trees

#### Gründe für Regional Barriers:

- Tiles in einer Gruppe teilen sich Scratchpad-Pfade  
- Tiles müssen den Scheduling Tree synchron betreten  
- DMA-Fenster müssen konsistent vorbereitet werden  
- Memorybank-Zugriffe müssen zeitsynchronisiert erfolgen  

#### Eigenschaften:

- feste Dauer (z. B. 10–20 Zyklen)  
- keine dynamischen Verzweigungen  
- hardwareseitige Erzeugung durch ST  
- Synchronisation innerhalb eines Clock-Domain-Bereichs  

Regional Barriers stellen sicher,  
dass alle Tiles einer Gruppe stets **exakt denselben Fortschritt** haben.

### 17.3 Global Barriers (Monolith-weit)

Global Barriers werden durch den SRDB erzeugt und kontrolliert.

Sie synchronisieren:

- alle Tile-Gruppen  
- alle DMA-/Memory-Fenster  
- alle Scheduling Trees  
- alle Phasen der TDM-Fabric  
- den globalen Workload-Fortschritt  

#### Eigenschaften globaler Barrieren:

- deterministischer Broadcast  
- feste Latenz (typ. 100–400 Takte)  
- exakte Übereinstimmung aller Tile-Gruppen  
- Teil der globalen Clock Domain  
- in der TDM-Fabric eingebettete Broadcast-Slots  

#### Formale Definition:

Eine globale Barrier ist erreicht, wenn:

$$
\forall\, TG_i:\; state(TG_i)=phase\_complete
$$

und nur dann darf der SRDB:

- neue Phase aktivieren  
- neue Scheduling Trees verteilen  
- neue DMA-/Memory-Slots vergeben  

Nie wird ein Tile versuchen, vorwärts zu laufen —  
die Struktur selbst verhindert das.

### 17.4 Eliminierung klassischer Synchronisationsprobleme

Die drei Ebenen der Synchronisation entfernen strukturell:

- globale Warp-Divergenz  
- asynchronen Kernelstart  
- dynamische Reduktionspfade  
- MPI-Jitter  
- Netzwerk-Latenzvariabilität  
- DMA-Kollisionen  
- Race Conditions  
- Deadlocks  
- Spinlocks  

#### Vergleich:

| Problem | GPU/TPU/HPC | KORA |
|--------|-------------|-------|
| Busy-Waits | hoch | 0 |
| Race Conditions | möglich | ausgeschlossen |
| DMA-Kollisionen | häufig | strukturell eliminiert |
| MPI-Barrieren | teuer | hardwaresehr billig |
| Jitter | hoch | 0 |
| Rerouting | möglich | unmöglich |

### 17.5 Zeitmodell der Synchronisation

Synchronisation erfolgt in **deterministischen Zeitfenstern**:

- Microbarrier: regelmäßiger Takt  
- Regional Barrier: Scheduling Period  
- Global Barrier: Iterationsende

#### Formalisierung:

$$
T_{barrier}(micro) = c_1
T_{barrier}(regional) = c_2
T_{barrier}(global) = c_3
$$

mit:

- **$\( c_1, c_2, c_3 \)$** konstant  
- keine Variationsbreite

#### Energieprofil:

Keine Busy-Waits →  
keine überflüssigen Clock-Zyklen →  
keine thermischen Spitzen →  
keine unkontrollierten Peak-Loads.

### 17.6 Zusammenspiel mit Scheduling Trees und SRDB

Synchronisation ist nicht losgelöst vom System,  
sondern integraler Bestandteil des Scheduling-Modells:

- ST (Synchronisation Tiles) setzen Regional Barriers  
- RT (SRDB Tiles) setzen Global Barriers  
- Scheduling Tree definiert, wann sie ausgelöst werden  
- TDM-Fabric garantiert Broadcast-Fenster  
- MT/DT strukturieren Memory-/DMA-Fenster passend dazu  

Das Zusammenspiel ergibt:

**global deterministische Ausführung**

### 17.7 Beispiel: KI-Training (Forward/Backward)

Iteration:

Forward:
├── Prefetch
├── Compute Layer
├── Microbarrier
Backward:
├── Compute Gradient
├── Writeback
├── Regional Barrier
└── Global Barrier (Iteration ++)

Alle Modelle, egal wie groß, haben **identische Iterationstakte**.

### 17.8 Beispiel: CFD-Simulation

Jeder Zeitschritt:

Compute local flux
Microbarrier
Compute divergence
Regional Barrier
Update field
Microbarrier
Apply boundary conditions
Global Barrier

Unabhängig von Systemlast oder Temperatur —  
die Ausführungszeit bleibt exakt reproduzierbar.

### 17.9 Fazit

Die Synchronisationsmechanismen des Monolithen:

- eliminieren globalen Jitter  
- stabilisieren die Ausführung  
- garantieren perfekte Reproduzierbarkeit  
- verhindern alle Race Conditions  
- reduzieren Energieverbrauch  
- integrieren sich vollständig in Scheduling und Fabric  
- machen HPC-/KI-Workloads strukturell berechenbar  

Damit ist Synchronisation kein Engpass mehr —  
sondern ein **Ordnungselement der Architektur**.

---

## 18. Execution Pipeline: Datenfluss, Instruktionsfluss, deterministischer Ablauf

Die bisher beschriebenen Komponenten des Monolithen – Tiles, Memorybanks,
Arbitration, TDM-Fabric, SRDB und Scheduling Trees – bilden gemeinsam eine
hochmodulare Architektur.  

> Wie läuft eine Berechnung im Monolithen tatsächlich ab?  
> Wie bewegen sich Daten und Instruktionen?  
> Und wie wird dabei vollständiger Determinismus garantiert?

KORA versteht „Execution Pipeline“ nicht nur als Mikroarchitektur-Element,
sondern als **gesamtsystemische Ausführungslogik**:
vom globalen Modellzustand bis zum bitgenauen Ergebnis.

### 18.1 Ebenen der Ausführung

Die Ausführung im Monolithen gliedert sich in vier übereinanderliegende Ebenen:

1. **Globale Ebene** – Modellphasen, Iterationen, Checkpoints  
2. **Regionale Ebene** – Tile-Gruppen, Regional Barriers, lokale Partitionen  
3. **Tile-Ebene** – Mikroarchitektur eines Tiles (Kapitel 11)  
4. **Pipeline-Ebene** – IF/RD/ALU/WB innerhalb eines Tiles

Diese Ebenen sind **hierarchisch gekoppelt**, nicht dynamisch verschachtelt.
Jede Ebene kennt ihre Rolle und ihre zeitliche Einbettung in den Gesamtablauf.

### 18.2 Globale Ablaufstruktur: Phasen und Iterationen

Der SRDB definiert eine Folge von **Ausführungsphasen**:

- Phase 0: Initialisierung / Load  
- Phase 1: Compute-Iteration (z. B. Zeitschritt, Trainingsbatch)  
- Phase 2: Reduktion / Aggregation  
- Phase 3: Writeback / Persistenz  
- Phase 4: Übergang in nächste Iteration / nächste Modellphase

Für jede Phase existiert ein **global deterministischer Plan**:

$$
Exec = \{Phase_0, Phase_1, \ldots, Phase_k\}
$$

In jeder Phase ist klar definert:

- welche Tiles aktiv sind,  
- welche Datenräume genutzt werden,  
- welche Kommunikationspfade offen sind,  
- welche Barrieren existieren,  
- wann der Übergang zur nächsten Phase erfolgt.

Keine Phase entsteht „spontan“ – die gesamte Struktur ist Ergebnis des SRDB.

### 18.3 Regionale Ausführung: Tile-Gruppen im Takt

Innerhalb jeder Phase arbeiten Tile-Gruppen (TG) in **klar definierten
Scheduling Periods (SP)** (siehe Kapitel 16).

Eine typische Periode einer TG umfasst:

1. **DMA-Load** ins Scratchpad  
2. **Compute-Pass** über lokale Daten  
3. **lokale Reduktion / Aggregation**  
4. **DMA-Writeback**  
5. **Regional Barrier**  
6. optional: **globaler Barrier-Beitrag**

Die Synchronization Tiles (ST) sorgen dafür, dass alle Tiles einer Gruppe:

- dieselbe Periode durchlaufen,  
- die gleichen Sequenzpunkte sehen,  
- niemals asynchron „vorlaufen“.

Die Ausführung ist daher nicht nur deterministisch, sondern auch **vollständig
phasen-synchronisiert**.

### 18.4 Tile-Ebene: Instruktionsfluss

Auf Tile-Ebene (z. B. Compute-Tile CT) verläuft die Ausführung streng linear
entlang einer **Instruction Sequence**, die vom Scheduling Tree und SRDB
vorgegeben wurde.

Die festen Pipelinephasen (Kapitel 11) sind:

1. **IF (Instruction Fetch)**  
2. **RD (Operand Read aus Register/SPM)**  
3. **ALU1 (Index-, Adress-, Vorberechnungen)**  
4. **ALU2 (Hauptoperation: Vektor/Matrix/Tensor/Stencil)**  
5. **WB (Writeback nach Register/SPM)**

Es gibt:

- keine Out-of-Order-Reihenfolgen,  
- keine spekulativen Verzweigungen,  
- keine dynamischen Replays,  
- keine Micro-Ops-Neuanordnung,  
- keine variable Tiefe.

Damit ist der Instruktionsfluss **vollständig vorhersagbar**.

### 18.5 Datenfluss: Vom Memory ins Resultat und zurück

Der Datenfluss eines typischen Workloads (z. B. KI oder CFD) folgt im Monolithen
immer demselben strukturellen Muster:

1. **Globaler SRDB-Befehl:**  
   - Neue Phase / Iteration  
   - Partitionierung der Datenräume

2. **DMA-Load (DT + MT + Fabric):**  
   - deterministische Übertragung aus Memorybank → Scratchpad  
   - fester Slot auf der TDM-Fabric  
   - konstante Latenz

3. **Compute im Tile (CT):**  
   - sequentieller Zugriff auf SPM-Blöcke  
   - berechnete Updates im Registerfile  
   - Writebacks ins Scratchpad

4. **Aggregation (lokal/regional):**  
   - lokale Reduktionen (z. B. Summen, Mittelwerte, Gradienten)  
   - Nutzung lokaler Scratchpads und CT-Pipelines  
   - keine globalen Netwerk-Reduktionen

5. **DMA-Writeback:**  
   - deterministischer Transfer SPM → Memorybank  
   - fester Slot, keine Kollision

6. **Synchronisation:**  
   - Microbarriers für Tile-internen Abschluss  
   - Regional Barrier für Gruppenkonsistenz  
   - Global Barrier für Iterationsabschluss

7. **Übergang:**  
   - SRDB berechnet nächste Phase / Iteration  
   - neue Scheduling Trees werden aktiviert

Dieser Ablauf bleibt **in jedem Durchlauf identisch** – unabhängig von Last,
Temperatur, vorherigen Runs oder sonstigen Zuständen.

### 18.6 Formale Beschreibung des deterministischen Ablaufs

Sei ein Workload $\( W \)$ durch folgende Komponenten beschrieben:

- Datensatz $\( D \)$  
- Operationen $\( O = \{o_1, o_2, \ldots, o_n\} \)$  
- Abhängigkeiten $\( Dep \subseteq O \times O \)$  

Der Monolith erzeugt daraus:

- eine Partitionierung $\( P \)$ über die Tiles  
- einen globalen Scheduling Tree $\( GT \)$  
- regionale Bäume $\( RT_i \)$  
- lokale Bäume $\( LT_{ij} \)$

Der Ausführungsablauf wird zu einer Funktion:

$$
Exec_W: D \rightarrow R
$$

mit:

$$
Exec_W = F(GT, \{RT_i\}, \{LT_{ij}\}, TDM, MT, ST, SRDB)
$$

Da alle beteiligten Komponenten deterministisch sind,
gilt:

$$
\forall\, k, l: Exec_W^{(k)}(D) = Exec_W^{(l)}(D) = R
$$

Es existiert keine Abhängigkeit von:

- Thread-Randomness  
- Schedulerzustand  
- Netzwerkjitter  
- internen Pufferzuständen  

### 18.7 Eliminierte dynamische Ausführungszustände

Im Monolithen gibt es **keine**:

- dynamischen Kernel-Launches  
- spontan auftretenden Synchronisationspunkte  
- konkurrierenden DMA-Requests  
- dynamische Zuweisung von Datenpfaden  
- Laufzeitänderung von Prioritäten  
- zufällige Warp/Thread-Reschedules  

Stattdessen:

- alle Zustände sind **statisch geplant**,  
- alle Abläufe **fest verdrahtet**,  
- alle Übergänge **zeitlich fixiert**,  
- alle Pfade **topologisch konstant**.

Das System verhält sich wie eine große, aber **vollständig deterministische
endliche Zustandsmaschine**.

### 18.8 Zeitverhalten und Reproduzierbarkeit

Ein wesentliches Ziel der Execution Pipeline ist die **Vorhersagbarkeit der Zeit**:

- Die Zeit pro Iteration ist konstant.  
- Die Zeit pro Phase ist konstant.  
- Die Zeit pro DMA-Transfer ist konstant.  
- Die Zeit pro Global Barrier ist konstant.  
- Die gesamte Ausführungszeit Änderungen im Eingabe-Datensatz folgend – nicht
  zufälligen Systemzuständen.

Für wissenschaftliche Workloads bedeutet das:

- klar planbare Laufzeiten,  
- konsistente Energy-to-Solution,  
- präzise Skalierungseigenschaften.

### 18.9 Energieprofil der Execution Pipeline

Durch die deterministische Ausführung entstehen:

- keine unvorhergesehenen Spitzenlasten,  
- keine ineffizienten Wartephasen,  
- kein „Hyperaktivitätszustand“ der Fabric,  
- keine aggressiven, spekulativen Prefetches,  
- deutlich weniger „unnütze“ Umschaltungen.

Der Energieverbrauch eines Workloads ist somit überwiegend proportional zu:

- der tatsächlichen Problemgröße,  
- den notwendigen Rechenoperationen,  
- der wirklich übertragenen Datenmenge.

Im Unterschied zu klassischen Architekturen wird **Overhead nicht skaliert**,
sondern konsequent strukturell minimiert.

### 18.10 Fazit

Die Execution Pipeline des KORA-Monolithen ist mehr als eine Mikroarchitektur:
Sie ist ein **systemischer Ausführungsplan**, der:

- Instruktionsfluss,  
- Datenfluss,  
- DMA,  
- Memory,  
- Kommunikation,  
- Synchronisation  

in einem einzigen **deterministischen Ablauf** integriert.

Ergebnis:

- reproduzierbare Ergebnisse,  
- reproduzierbare Zeiten,  
- reproduzierbare Energieprofile.

Damit definiert KORA eine neue Klasse von Rechensystemen:
Nicht nur „schnell“ oder „effizient“, sondern **strukturell vorhersagbar**.

---

## 19. Fehlerbehandlung & Resilienz im deterministischen System

Fehlerbehandlung ist in klassischen HPC-/KI-Systemen ein inhärent dynamischer,
nichtdeterministischer Prozess.  
Fehler werden oft behandelt durch:

- Retry-Schleifen,  
- dynamische Neuplanung von Threads,  
- Re-Routing von Paketen,  
- Interrupt-Handler,  
- Wiederholung ganzer Rechenabschnitte,  
- opportunistische Ersatzpfade,  
- heuristische Load-Shifts,  
- dynamische Clock-Anpassung.

Diese Mechanismen widersprechen den grundlegenden Prinzipien des KORA-Monolithen:
Sie erzeugen nichtdeterministische Abläufe, variable Latenzen und irreproduzierbare Ergebnisse.

KORA verfolgt daher einen radikal anderen Ansatz:
**Fehler werden strukturell verhindert, detektiert und eingeordnet – nicht dynamisch umgangen.**
Dies erlaubt eine deterministische Fehlermodellierung, ohne die Ordnung des Systems zu verletzen.

### 19.1 Grundprinzip der Resilienz: Ordnung statt Recovery

KORA implementiert Fehlerbehandlung auf zwei Ebenen:

1. **Fehlerprävention (structural prevention)**  
   – Fehler durch Architekturdesign vermeiden
2. **Fehlerdetektion & feste Reaktion (deterministic reaction)**  
   – Fehler durch deterministische Mechanismen identifizieren  
   – systematisch definierte Reaktion  
   – niemals dynamische Anpassungen oder heuristische Korrekturen

Wichtig ist:

> Im Monolithen existieren **keine Rekonfigurationspfade**, die die zeitliche
> oder strukturelle Ordnung verändern könnten.

Fehler bleiben lokalisiert und beeinflussen den globalen Ablauf nicht.

### 19.2 Fehlerklassen im Monolithen

KORA unterscheidet drei Kategorien:

#### (A) Soft Errors  

• flüchtige Bitflips (z. B. Strahlung)  
• Register-/SPM-Fehler  
• Übergangsstörungen im Fabric-Signal

#### (B) Hard Errors  

• dauerhafte Defekte in einem Tile  
• defekte Speicherbank  
• defekte Leitung oder geschädigter Port

#### (C) Systemische Fehler  

• falsche Eingabedaten  
• Programmierfehler  
• fehlerhafte Scheduling-Definition  
• ungültige Metadaten

Jede Kategorie wird anders behandelt — aber immer deterministisch.

### 19.3 Soft-Error-Resilienz (ECC, deterministische Korrektur)

Soft Errors sind die häufigste Fehlerquelle in großen Chips.

KORA implementiert:

- **vollständiges ECC** für  
  • Memorybanks  
  • Scratchpads  
  • Registerfiles

- **feste ECC-Latenz**  
  → KORA verhindert variable Korrekturzeiten  
  → keine unerwarteten Pipeline-Stalls

- **Single-Error-Correct, Double-Error-Detect (SEC-DED)**  
  – liefert bitgenaue Korrektur  
  – mit fester, deterministischer Korrekturzeit

- **SRDB-Fehlerkanal**  
  – meldet Fehler nach fester Ablaufsequenz  
  – ohne Einfluss auf den globalen TDM-Zeitplan

#### Wichtiger Unterschied zu klassischen Systemen:

Bei GPUs/TPUs kann ECC variable Latenzen erzeugen.  
Bei KORA ist die Latenz **fix** und integraler Bestandteil des Pipes.

### 19.4 Hard-Error-Resilienz: Strukturelle Quarantäne

Dauerhafte Fehler (Hard Errors) werden **nicht dynamisch umgangen**.  
Es gibt keine spontane Re-Routing-Logik.

KORA verwendet:

- **Startup Self-Test** pro Tile  
- **SRDB-basierte Tile-Quarantäne**  
- **feste Ersatzbereiche** (Spare Tiles)

Wenn ein Tile als defekt markiert wird:

1. SRDB nimmt das Tile deterministisch aus dem Scheduling Tree.  
2. Spare-Tile übernimmt die Rolle **nur** bei nächstem globalen Barrier.  
3. Keine laufende Iteration wird verändert.  
4. Determinismus bleibt vollständig erhalten.

#### Warum keine dynamischen Umleitungen?

Weil dynamische Neupfade Jitter erzeugen würden.  
KORA akzeptiert lieber planbare Kapazitätsreduktion als Chaos.

### 19.5 Kommunikationsfehler: deterministisches Fehlerprotokoll

Da die TDM-Fabric keine Pakete verliert und keine Staus zulässt,
sind Kommunikationsfehler äußerst selten.  
Sollte dennoch ein Fehler auftreten:

- der Empfangsknoten erkennt ihn deterministisch durch ECC,  
- das Fabric-Segment markiert den Slot als „corrupt in cycle N“,  
- SRDB loggt den Fehler,  
- der aktuelle Zyklus wird nicht verändert,  
- die laufende Iteration wird abgeschlossen,  
- ein globaler Barrier validiert anschließend den Zustand.

Da es keine dynamischen Abweichungen gibt, bleibt das Ergebnis gültig,  
solange der Fehler korrigierbar ist.

### 19.6 Fehlerhafte Scheduling- oder Metadaten (SRDB-Level)

Wenn ein Fehler in SRDB- oder Meta-Daten auftritt:

- DGHE erkennt ungültige Abhängigkeitsknoten  
- CEU verhindert Start illegaler Phasen  
- SRDB markiert die Iteration als invalid  
- der Monolith bricht **deterministisch** am nächsten Global Barrier ab  
- keine halbfertigen oder inkonsistenten Zwischenergebnisse entstehen

Das System kehrt nicht zu heuristischen „Rettungsmechanismen“ zurück,
sondern stoppt in einer definierten, reproduzierbaren Weise.

### 19.7 Formale Beschreibung deterministischer Fehlerreaktionen

Sei ein Fehler $\( E \)$ detektiert in Phase $\( P \)$.

KORA garantiert:

$$
Handle(E, P) = R_E
$$

mit:

- fester Reaktionsfolge  
- fester Zeitstruktur  
- fester globaler Auswirkung  

und insbesondere:

$$
\forall\, runs: R_{E}^{(1)} = R_{E}^{(2)} = \cdots
$$

Das System reagiert **immer gleich**.

### 19.8 Warum KORA sich grundlegend von klassischer Resilienz unterscheidet

| Mechanismus | Klassisch | KORA |
|-------------|-----------|------|
| Fehlererkennung | dynamisch | deterministisch |
| ECC-Latenz | variabel | konstant |
| Routing bei Fehler | adaptiv/dynamisch | strukturell fix |
| Retry-Verhalten | heuristisch | nicht vorhanden |
| Konvergenzpfade | variabel | stabil |
| Systemreaktion | oft unvorhersehbar | exakt definiert |

Diese Unterschiede sind entscheidend für:

- reproduzierbare wissenschaftliche Ergebnisse,  
- zuverlässige Validierung,  
- regulierbare Sicherheit,  
- erklärbare Fehlermodi.

### 19.9 Fazit

Fehlerbehandlung im Monolithen basiert nicht auf dynamischer Anpassung,
sondern auf **struktureller Prävention** und **deterministischen Reaktionspfaden**.

Der Monolith ist damit:

- robust gegen Soft Errors,  
- tolerant gegenüber Hard Errors (über Quarantäne),  
- frei von nichtdeterministischen Recovery-Algorithmen,  
- vollständig reproduzierbar selbst im Fehlerfall,  
- transparent in allen Fehlermodi,  
- wissenschaftlich verlässlich und auditierbar.

Fehler verändern nie die zeitliche Ordnung oder den Scheduling Tree.  
Sie werden in festen Reaktionssequenzen gehandhabt,
ohne die Deterministik des Systems zu verletzen.

---

## 20. Power Architecture & Thermal Design 
(Stabile Energieprofile, deterministische Wärmeentwicklung, strukturelle Effizienz)

Die Energieeffizienz klassischer HPC-/KI-Systeme ist durch eine Vielzahl
nichtdeterministischer Prozesse geprägt:

- spekulative Ausführung,  
- variable Memory-/DMA-Latenzen,  
- Out-of-Order-Mechanismen,  
- unterschiedliche Kernelpfade,  
- asynchrones Threadverhalten,  
- thermische Spitzen durch Busy-Waits,  
- stochastische Scheduler-Reaktionen,  
- inkonsistente Netzwerkaktivität.

KORA eliminiert all diese Faktoren systemisch.  
Das Ergebnis ist eine Rechenarchitektur, deren Energie- und Wärmeprofil ebenso **deterministisch** ist wie ihre Ausführung.

### 20.1 Designphilosophie der Power Architecture

Während klassische Architekturen versuchen, Energieprobleme durch:

- DVFS (Dynamic Voltage/Frequency Scaling),  
- heuristische Governor-Algorithmen,  
- adaptive Clock-Domains,  
- softwarebasierte Spitzenlastkontrolle  

zu kompensieren, verfolgt KORA einen grundlegend anderen Ansatz:

> Energieeffizienz entsteht durch strukturelle Ordnung, nicht durch heuristische Reaktionen.

KORA definiert:

1. **feste Aktivitätsmuster** pro Tile,  
2. **feste TDM-Zeitfenster** für Kommunikation,  
3. **feste DMA-/Memory-Zeitfenster**,  
4. **keine spekulativen Stalls**,  
5. **keine dynamischen Scheduler-Schaltlasten**,  
6. **keine Pipeline-Flushes**,  
7. **keine sprunghaften Frequenzänderungen**.

Ergebnis:  
Die Auslastung folgt einem glatt verlaufenden, vorhersehbaren Aktivitätsprofil.

### 20.2 Power Domain Design

Der Monolith besteht aus **zwei Power-Domain-Hierarchien**:

#### (A) Compute Power Domains (CPD)  

- Versorgung jeder Tile-Gruppe  
- konstante Frequenz  
- konstanter Spannungspfad  
- niemals dynamische Frequenzwechsel  
- nie spontanes Throttling

#### (B) Fabric & Control Power Domains (FCPD)  

- dedizierte Versorgung für TDM-Fabric, SRDB und MTs  
- garantierter Spannungspegel für Broadcast-Zyklen  
- keinerlei Abhängigkeit von Compute-Load

#### Abschirmung zwischen Domains

- CT-Aktivität beeinflusst nie die Fabric  
- Fabric-Auslastung beeinflusst nie CT-Stabilität  
- SRDB besitzt höchste Priorität, aber feste Leistungsgrenzen

Die Trennung stabilisiert Energie- und Temperaturverhältnisse massiv.

### 20.3 Energieprofil von Scheduling, Compute und DMA

In klassischen Systemen hängt Energie direkt von:

- dynamischem Scheduling  
- zufälligen Speicherpfaden  
- spekulativen Ausführungen  
- unkontrollierten DMA-Interferenzen  
- Cache-Misses  
- Pipeline-Flushes  

ab.

Im Monolithen hingegen:

- Scheduling ist deterministisch → **keine variablen Lastspitzen**  
- Speicherpfade sind fix → **keine Lastsprünge**  
- DMA-Slots sind fest → **keine Interferenz**  
- Compute-Pipeline ist konstant tief → **keine Flush-Kaskaden**  
- SPM-Zugriffe sind lokal → **keine Energieverluste durch Misses**

Der Energieverbrauch eines Workloads ist daher eine
funktionale Abbildung des Problems, nicht der Systemzustände.

### 20.4 Vergleich: Energieeffizienz pro Operation

#### Klassische HPC-/KI-Architekturen:

- 30–70 % Energie gehen in Overheads:  
  • Synchronisation  
  • Cache-Hierarchie  
  • Scheduling  
  • Kommunikationskonflikte  
  • Wartezeiten  
  • Fehlerbehandlung

#### KORA:

- Overheads: **5–10 %**  
- 90–95 % fließen in die eigentliche Operation  
- nahezu keine Energievergeudung durch „Systemverhalten“

Formal:

$$
E_{kora} \approx E_{ideal} \cdot (1 + \epsilon),\quad \epsilon \in [0.05, 0.10]
$$

wo klassische Systeme haben:

$$
E_{classic} \approx E_{ideal} \cdot (1.3 - 1.7)
$$

### 20.5 Thermisches Verhalten: Deterministische Wärmeprofile

Durch feste Ausführungsfenster entstehen **keine thermischen Zufallsspitzen**.

KORA besitzt:

- **lineare Wärmeerzeugung pro Zeitraum**,  
- **gleichmäßige Temperaturverteilung**,  
- **keine überraschenden Hotspots**,  
- **keine idle-zu-peak-Sprünge**,  
- **keine DVFS-induzierten Frequenzschwankungen**.

#### Konsequenzen:

1. Längere Lebensdauer aller Komponenten  
2. Geringere Kühlanforderungen  
3. Planbare thermische Auslegung  
4. Komplette Vermeidung lokaler thermischer Kollapspunkte  
5. Konstante Energieeffizienz über lange Läufe

### 20.6 Einfluss der TDM-Fabric auf Energie & Wärme

Die TDM-Fabric ist:

- zu jedem Zyklus exakt definiert aktiv  
- niemals überlastet  
- niemals stochastisch fluktuierend  
- synchron mit SRDB und CTs  
- vorhersehbar im Aktivitätsprofil

Damit spart sie Energie auf zwei Wegen:

1. **Keine Backpressure → keine zusätzlichen Buffer-Reads/Writes**  
2. **Kein Rerouting → keine extralangen Pfade**

Das Energieprofil der Fabric ist nahezu rechteckförmig.

### 20.7 Energie- und Wärmeplanung: deterministische Worst-Case-Modelle

Da alle Zeitfenster fix sind, kann der Monolith *vorab* zuverlässig simuliert werden:

- Worst-Case-Cache-Misses → existieren nicht  
- Worst-Case-Buskonflikte → existieren nicht  
- Worst-Case-Routing → existiert nicht  
- Worst-Case-Schedulerverhalten → existiert nicht  

Daher ist die gesamte thermische Charakteristik:

- statisch planbar  
- formal beschreibbar  
- reproduzierbar  
- auditierbar

Dies macht KORA extrem geeignet für:

- Sicherheitskritische Systeme  
- wissenschaftliche Großsimulationen  
- energieoptimierte Rechenzentren  
- regulierte HPC-Umgebungen  
- Behörden & Zertifizierungsstellen

### 20.8 PUE-Optimierung (Rechenzentrum)

Weil der Monolith:

- konstante Leistung zieht,  
- nur geringe thermische Spitzen erzeugt,  
- ohne DVFS läuft,  
- keine Rechenzentrums-lastabhängigen Sprünge provoziert,

kann ein Rechenzentrum ihn deutlich effizienter kühlen:

$$
PUE_{kora} \approx 1.05 - 1.15
$$

vs.

$$
PUE_{classic} \approx 1.2 - 1.6
$$

Der Effekt ist beträchtlich.

### 20.9 Energie-Determinismus: eine neue Kategorie wissenschaftlicher HPC

Der Monolith ist das erste HPC-/KI-Systemdesign, das:

- **deterministische Leistung**,  
- **deterministische Ausführungszeit**,  
- **deterministische Wärmeentwicklung**,  
- **deterministischen Energieverbrauch**,  
- **deterministische Kommunikationslast**,  
- **deterministische Speicherlast**

aus einem einzigen Architekturprinzip heraus gewährleistet.

Diese Kategorie könnte wissenschaftlich als  
**Deterministic HPC / Deterministic AI Compute**  
klassifiziert werden.

### 20.10 Fazit

Die Power- und Thermal-Architektur des Monolithen ist nicht das Ergebnis von
Heuristiken oder dynamischer Optimierung, sondern von *struktureller Ordnung*.

Sie bietet:

- stabilen Energieverbrauch  
- stark reduzierte thermische Spitzen  
- planbare Kühlleistung  
- minimale Overheads  
- maximale Effizienz  
- volle Reproduzierbarkeit  
- signifikante ökologische Vorteile

Damit ist KORA nicht nur ein deterministisches Rechensystem,
sondern auch ein **ökologisch radikal überlegenes**.

---

## 21. Scaling Behaviour & System Integration 
(Fabric-Scaling, Multi-Monolith, Rack-Level-Design, deterministische Clusterintegration)

Skalierung ist der entscheidende Faktor moderner HPC-/KI-Systeme.  
Klassische Architekturen skalieren durch:

- verteilte Knoten  
- Netzwerke wie InfiniBand  
- MPI / NCCL / Collective Ops  
- Lastverteilung über Scheduler  
- verteilte Speicherstrukturen  
- heuristische Partitionierung  

Diese Skalierung ist jedoch inhärent **nichtdeterministisch** und
führt zu:

- variablen Kommunikationszeiten,  
- stochastischen Barrieren,  
- Rennbedingungen,  
- globaler Jitter-Ausbreitung,  
- Nicht-Reproduzierbarkeit,  
- Energieverlusten.

KORA verfolgt einen alternativen Ansatz:

> **Skalierung entsteht durch geordnete Komposition deterministischer Monolith-Einheiten – nicht durch dynamische Verteilung.**

Damit definiert KORA eine neue Klasse von HPC-Skalierung:
**Structured Deterministic Scaling**.

### 21.1 Grundprinzip: Replicate, Don’t Distribute

KORA skaliert nicht durch verteilte Aufgaben auf viele Knoten,
sondern durch **geordnete Replikation des Monolithen**.

Ein Monolith ist:

- eine deterministische Maschine,  
- mit vollständiger Ordnung,  
- ohne nichtdeterministische Interaktionen.

Beim Skalieren werden mehrere Monolithen:

- nicht zu einem „Cluster verbunden“,  
- sondern **als deterministische Module** nebeneinander gruppiert.

Die Frage ist nicht:
> Wie verteilen wir Arbeit?

Sondern:
> Wie orchestrieren wir mehrere deterministische Maschinen mit festen, ordnbaren Schnittstellen?

### 21.2 Skalierungsmodell: M1 → M2 → M4 → M8 → MRack → MCluster

Skalierung erfolgt über vier Ebenen:

1. **M1 (Einzelmonolith)**  
2. **M2 (Dual-Monolith)** → gekoppelte Fabric-Slots  
3. **M4 (Quad-Monolith)** → geordnete 2×2-Topologie  
4. **M8 / M16 (Rack-Level)**  
5. **MCluster (Zentrum-Level)** → deterministische Meta-Fabric

#### Wichtig:

Kein Schritt führt zu einer verteilten Softwareumgebung.  
Alles ist **Hardware-Skalierung**.

### 21.3 On-Package Scaling (M1 → M2 → M4)

Ein einzelner Monolith kann in mehreren Varianten realisiert werden:

- Single-Die  
- Multi-Die auf einem Package  
- Multi-Tile Close-Coupled

#### Kopplung erfolgt durch:

- **TDM-Lanes mit reservierten Inter-Monolith Slots**  
- **durch SRDB synchronisiertes Metadaten-Routing**  
- **regionale Coordinating Tiles (RCT)**

Die Kopplung ist:

- vollständig deterministisch,  
- niemals stochastisch,  
- topologisch fix,  
- ohne adaptives Routing.

Damit entsteht ein **M2-System** (Dual-Monolith),  
dann ein **M4-System** (2×2).

### 21.4 Rack-Level Scaling (M8–M16)

Ein Rack kann 8–16 Monolithen enthalten, geordnet in einer festen
Topologie:

- 4 Monolithen pro Ebene  
- deterministische Backplane-Fabric  
- feste Silizium-Spuren für Interconnect  
- TDM-basierte Meta-Fabric (MF)

Kein Ethernet, kein InfiniBand, kein nvLink.  
Stattdessen eine **dedizierte, deterministische Rack-Fabric**,  
die dieselben Prinzipien nutzt wie die On-Die Fabric:

- TDM  
- feste Slot-Reservierung  
- konfliktfreie Pfade  
- keine Ad-Hoc-Routingmechanismen

Damit wird das gesamte Rack zu einem **deterministischen Supermonolithen**.

### 21.5 Cluster-Level Scaling (MCluster)

Ein MCluster verbindet mehrere Racks durch eine Meta-Fabric:

- keine Paketvermittlung  
- keine adaptive Routenwahl  
- deterministische Kommunikationsfenster  
- global synchronisierte Phasen  
- global definierte Scheduling-Topologie

#### Mechanismus:

1. SRDB auf Rack-Ebene ordnet Modellphasen.  
2. Meta-SRDB (übergeordnet) koordiniert mehrere Racks.  
3. TDM-Meta-Fabric stellt feste Übertragungsfenster für Cross-Rack Kommunikation.  
4. Barrieren sind deterministisch (Rack-intern und Rack-übergreifend).  
5. Ergebnisse werden durch strukturellen Zeitplan kombiniert.

Damit wird das gesamte Cluster zu einer einzigen, deterministischen Maschine.

### 21.6 Keine dynamische Lastverteilung

Im Gegensatz zu HPC/Cloud:

- keine Jobscheduling-Heuristiken,  
- keine Queue-Bildung,  
- keine dynamische Stellzeitveränderung,  
- kein „load balancing“.

Warum?

Weil **jede dynamische Verteilung deterministische Ausführung zerstört**.

KORA behandelt Skalierung wie Schaltkreise:

> Komponenten werden zugeordnet, nicht verteilt.

Wenn ein Monolith mehr Arbeit erhält, wird das in den Scheduling Trees definiert,  
nicht durch ein dynamisches Laufzeitsystem.

### 21.7 Kommunikation zwischen Monolithen

Kommunikation erfolgt über:

- **dedizierte Inter-Monolith Lanes**,  
- **TDM-Slots**,  
- **strukturierte Metadatenfenster**,  
- **deterministische Reduktionspfade**.

#### Eigenschaften:

- konstante Latenz  
- keine Kollisionen  
- keine Queues  
- keine Paketverluste  
- keine variable Bandbreite  
- keine adaptiven Routingentscheidungen

#### Formale Latenz:

$$
L_{inter} = n_{hops} \cdot T_{slot} + L_{serdes}
$$

mit allen Parametern **konstant**.

### 21.8 Synchronisation auf Cluster-Ebene

Der Ablauf:

1. Monolith-Level Barriers  
2. Rack-Level Barriers  
3. Cluster-Level Barrier  
4. globale Iteration ++

Keine Variation, keine Abweichung, keine adaptiven Zeittakte.

### 21.9 Fehlerisolation im Skalierungsverbund

Fehler in einem Monolithen:

- beeinflussen niemals andere Monolithen,  
- propagieren nicht über die TDM-Meta-Fabric,  
- werden durch SRDB „quarantänisiert“,  
- reduzieren Kapazität, aber nicht Determinismus.

Kein Recovery verschiebt globale Zeitpläne.

### 21.10 Scaling Efficiency

KORA erreicht nahezu **lineare Skalierung**, aber strukturell, nicht dynamisch.

Für viele Workloads gilt:

$$
T(N) \approx \frac{T(1)}{N}
$$

mit minimalen Overheads, weil:

- keine stochastische Kommunikation  
- keine dynamische Lastverteilung  
- keine Netzwerkjitter  
- keine MPI-Reduktionskosten  
- keine Fabric-Hotspots

### 21.11 Systemintegration in Rechenzentren

KORA benötigt:

- deutlich weniger Kühlkapazität  
- weniger elektrische Infrastruktur  
- keine adaptive DVFS-Mechanik  
- weniger Netzwerkkomplexität  
- geringere Latenzvariabilität  
- klar vorhersagbare Energieprofile

Rechenzentren können deterministic HPC planen wie einen deterministischen Industrieprozess.

### 21.12 Fazit

KORA definiert ein völlig neues Skalierungsmodell:

- **Replikation statt Verteilung**  
- **Topologie statt Heuristik**  
- **Hardwareordnung statt Softwareheuristik**  
- **strukturierte Meta-Fabric statt Netzwerk**  
- **globale Synchronisation ohne Jitter**  
- **lineare, deterministische Skalierung**  

Damit ist KORA die erste Architektur, die eine deterministische HPC-/KI-Skalierung auf allen Ebenen ermöglicht:

- Die  
- Package  
- Rack  
- Cluster  
- Rechenzentrum  
- wissenschaftliche Infrastruktur

Ein deterministisch skalierender Supercomputer ist damit erstmals architektonisch konsistent definiert.

---

## 22. Software Interaction Model 
(Compiler, Runtime, API)

Der KORA-Monolith ist eine deterministische Hardwarearchitektur ohne klassische Software-Laufzeitmechanismen wie Threads, Scheduler, Kernelstarts, Asynchronität oder heuristische Optimierer. Daher benötigt KORA ein Softwaremodell, das:

- einfach bedienbar für Wissenschaftler ist,
- ausdrucksstark genug für komplexe Workloads,
- deterministisch kompilierbar ist,
- kompatibel mit existierenden wissenschaftlichen Frameworks bleibt,
- und direkt auf Scheduling Trees, SRDB und TSF abbildet.

Dieses Modell heißt **Structural Compute Interface (SCI)**.

### 22.1 Structural Compute Interface (SCI)

SCI besteht aus drei Ebenen:

1. **High-Level API (HAPI)** – deklarativ und modellorientiert
2. **Intermediate Structural Representation (ISR)** – graphbasierte Compiler-IR
3. **Tile Schedule Format (TSF)** – maschinennahes, deterministisches Format

Die Software interagiert nie direkt mit Fabric, Memory oder Arbitration.
Alle Hardwaredetails werden vollständig durch den Compiler erzeugt.

### 22.2 High-Level API (HAPI)

Die HAPI-Ebene ist deklarativ und mathematisch formuliert.
Der Benutzer beschreibt ausschließlich *was* berechnet werden soll, nicht *wie*.

Beispiele:

    u = field(shape=(Nx, Ny, Nz))
    u_next = u + dt * divergence(flux(u))

    y = Linear(W, x)
    loss = MSE(y, target)

    A = dense_matrix(...)
    x = A @ b

HAPI abstrahiert vollständig von Scheduling, Speicher und DMA.

### 22.3 Intermediate Structural Representation (ISR)

ISR ist die interne Darstellung des SCI-Compilers.

Eigenschaften:

- graphorientiert
- vollständig deterministisch
- frei von dynamischen Kontrollflüssen
- statisch partitionierbar
- geeignet für Stencil-, Tensor- und Graphanalysen

ISR ist vergleichbar mit modernen IRs (z. B. MLIR, XLA), jedoch ohne dynamische Pfade.

### 22.4 SCI-Compiler

Der Compiler erzeugt einen vollständigen deterministischen Ausführungsplan.

**Compiler-Schritte:**

1. Analyse von Datenabhängigkeiten
2. Partitionierung in Tile-Regionen
3. zeitliche Strukturierung in Phasen
4. Planung aller DMA-Fenster
5. Zuweisung von Memorybanks und SPM
6. Erzeugung globaler, regionaler und lokaler Scheduling Trees
7. Generierung des TSF-Programms

Der Compiler ist damit sowohl Planungssystem als auch Ordnungsmaschine.

### 22.5 Tile Schedule Format (TSF)

TSF ist der direkte maschinennahe Code des Monolithen.

TSF enthält:

- SRDB-Metadaten
- globale Scheduling Trees
- regionale Scheduling Trees
- lokale Tile-Trees
- TDM-Slot-Zuordnungen
- feste DMA-Fenster
- Memorybank-Zuordnungen
- Register- und Scratchpad-Layouts
- Phasen- und Iterationsbeschreibungen

TSF ist:

- statisch
- deterministisch
- nicht selbstmodifizierend
- vom SRDB direkt interpretierbar

### 22.6 Runtime-System: SRDB als Hardware-Betriebssystem

KORA besitzt keine Software-Runtime.

Nicht vorhanden sind:

- OS
- Kernel
- Scheduler
- Interrupts
- dynamische Optimierung

Stattdessen:

- SRDB interpretiert TSF,
- orchestriert alle Phasen,
- steuert TDM-Fabric,
- aktiviert Scheduling Trees,
- regelt DMA- und Memoryfenster,
- garantiert deterministische Ausführung.

Der Monolith ist damit ein hardwarebasiertes, deterministisches Laufzeitsystem.

### 22.7 Kompatibilität mit wissenschaftlicher Software

KORA lässt sich über HAPI als Backend für existierende wissenschaftliche Software nutzen:

- Python
- C++
- Fortran
- NumPy / SciPy
- PyTorch
- TensorFlow
- HPC-Frameworks (CFD, FEM, PDE, LBM)

Beispiel:

    import kora as K
    
    u = K.field((1000, 1000))
    for t in range(1000):
    u = K.stencil(u, Laplace)

Beispiel (PyTorch):

    model = K.TorchModel(...)
    loss = model(x).MSE(target)
    loss.backward()

Der Compiler übernimmt die vollständige Deterministik.

### 22.8 Debugging & Reproduzierbarkeit

Da alle Abläufe deterministisch sind:

- Ergebnisse sind immer identisch,
- Zyklen sind rekonstruierbar,
- DMA-Transfers sind reproduzierbar,
- Memoryzugriffe sind deterministisch,
- Scheduling Trees sind konstant,
- Barrieren verlaufen exakt gleich.

Debugger können:

- jeden Pipelinezyklus,
- jedes Fenster,
- jede Speicheroperation

exakt nachzeichnen.

### 22.9 Flexibilität trotz deterministischer Hardware

Flexibilität entsteht durch:

- den SCI-Compiler,
- die Intermediate Structural Representation,
- die automatische Partitionierung,
- die statische Generierung der Scheduling Trees,
- die Erweiterbarkeit der TDM-Fenster,
- das Replikationsmodell des Monolithen.

Die Hardware bleibt deterministisch, die Software bleibt flexibel.

### 22.10 Fazit

Das KORA Software Interaction Model bietet:

- eine verständliche High-Level API,
- eine mächtige Intermediate Representation,
- deterministische Compilerpfade,
- TSF als hardwarefesten Ausführungsplan,
- SRDB als deterministisches Hardware-Runtime-System,
- vollständige Reproduzierbarkeit,
- einfache Debugbarkeit,
- Integration in bestehende HPC- und KI-Software.

KORA verbindet moderne Softwareentwicklung mit einer vollständig deterministischen Hardwarearchitektur.

---

## 23. Memory Model & Data Layout 
(Anwendungsmodelle, Partitionierung, SPM-Strategien)

Das Speicherverhalten ist für HPC-, KI- und Big-Data-Workloads der wichtigste Leistungsfaktor. 
Klassische Architekturen arbeiten mit hierarchischen Caches, dynamischen Prefetchern, spekulativer Ausführung, Out-of-Order-Laden und komplexen Coherence-Protokollen. 
Diese Strukturen erzeugen nichtdeterministische Latenzen, variable Bandbreiten und einen hohen Energieverbrauch.

KORA ersetzt diese Mechanismen durch ein deterministisches, strukturiertes Memory-Modell, das auf drei Säulen basiert:

- banked on-die Memory mit festen Latenzen
- explizit kontrollierte Scratchpads (SPM)
- deterministische Transferfenster (DMA-Fenster)

Dieses Kapitel beschreibt, wie Daten im Monolithen angeordnet, übertragen und verarbeitet werden.

### 23.1 Grundprinzip: Deterministic Data Residency

In klassischen Systemen entscheidet die Hardware zur Laufzeit, wo Daten liegen:
im L1-Cache, L2, L3, HBM, im DRAM oder gar auf dem PCIe-Link.

Im Monolithen gilt:

- Daten haben einen fixen Ort
- Kacheln/Tiles besitzen deterministische Zugriffsfenster
- Transfers sind durch den Scheduling Tree vorgegeben
- Daten wandern niemals spontan

Die Frage ist also nicht:
    Wo liegt meine Variable aktuell?

Sondern:
    Wo ist ihre fest definierte Speicherregion für diese Phase?

Diese Speicherregion ist Teil der TSF-/Scheduling-Definition.

### 23.2 Speicherhierarchie des Monolithen

Die Hierarchie besteht aus:

1. Memorybanks (on-die, multiported)
2. Scratchpads (Tile-lokal)
3. Registerfile (pro Tile)

Es existiert **kein Cache** und **keine Koheränzhierarchie**.

#### Memorybanks

- fester Platz für alle globalen Daten
- konstante Latenz pro Zugriff
- feste Zuordnung an Tile-Gruppen

#### Scratchpads

- explizite Zwischenpuffer
- enthalten die für die aktuelle Phase benötigten Datenblöcke
- deterministisch befüllt durch DMA

#### Registerfile

- lokale Arbeitsdaten eines Tiles
- keine dynamischen Evictions

Dieses Modell erzeugt maximale Vorhersagbarkeit.

### 23.3 Datenpartitionierung für Workloads

Der SCI-Compiler teilt alle Datenstrukturen in Partitionen:

- Tensor-Blöcke (KI)
- Stencil-Blöcke (CFD)
- Matrixkacheln (Linear Algebra)
- Daten-Chunks (Big Data)

Diese Partitionen haben feste Größen, die so gewählt werden, dass sie komplett in ein Scratchpad passen.

Beispiele für Blockgrößen:

#### CFD-Stencil
Blocksize: 32 x 32 x 16 Zellen

#### KI-Tensor
Tile: (128, 128) für GEMM

#### Big-Data
Chunk: 1 MB pro Tile

Der Compiler garantiert:
Blockgrößen und Partitionen sind statisch und deterministisch.

### 23.4 Data Layout für unterschiedliche Anwendungsmodelle

KORA unterstützt drei Hauptmodelle:

#### (A) Stencil-/PDE-Modelle

- lokale Nachbarschaftsoperatoren
- feste Stencilradien
- optimal für deterministisches SPM-Loading

Data Layout:

    contiguous blocks pro spatiale Region
    ghost layers am Blockrand
    feste strides

#### (B) Tensor-/Matrixmodelle

- lineare Algebra
- tiefe Tensoroperationen

Data Layout:

    row-major oder block-major
    fester stride
    fixe Kachelgröße für GEMM/CONV

#### (C) Big-Data / Shuffle-Modelle

- große Datenmengen, Streaming, Transformation

Data Layout:

    große Chunks
    sequentielle Durchläufe
    deterministische DMA-Fenster pro Chunk

Der Compiler wählt das optimale Layout automatisch.

### 23.5 Scratchpad-Strategien (SPM)

Scratchpads sind das Kernelement für deterministische Compute-Lasten.

SPM-Strategien:

1. **Block-Load Strategy**  
    kompletter Block wird vor der Phase geladen

2. **Streaming Strategy**  
    Daten werden in festen Batches geladen

3. **Dual-Buffer Strategy**  
    während ein Block berechnet wird, wird der nächste preloaded

4. **Reduction Strategy**  
    lokale Aggregation, Writeback erst nach Phase-Ende

SPM ist nicht dynamisch, sondern strikt planbar.

### 23.6 Datenfluss: Beispielablauf

Ein typischer Ablauf in einer Iteration:

    Phase 1: DMA-Load Block → Scratchpad
    Phase 2: Compute auf Scratchpad + Registerfile
    Phase 3: lokale Reduktion
    Phase 4: DMA-Writeback → Memorybanks
    Phase 5: Synchronisation
    Phase 6: nächste Phase / Iteration

Dieser Ablauf ist immer identisch.

### 23.7 Memorybandbreite und deterministische Latenzen

Durch fixe Bank-Zuordnung und feste Transfer-Slots:

- Bandbreite ist konstant
- Latenz ist garantiert
- keine Cache-Misses
- keine Spekulation
- keine Overfetches
- keine Bankkollisionen

Formale Latenz:

$$
L_total = L_bank + L_dma + L_fabric
$$

mit allen Komponenten konstant.

### 23.8 Vorteile des deterministischen Memory Models

- vollständige Reproduzierbarkeit
- Energieeffizienz (keine Misses, keine Flushes)
- planbare Zeit pro Phase
- einfache Debugbarkeit
- keine stochastischen Speicherpfade
- transparente Partitionierung
- stabile thermische Eigenschaften

### 23.9 Fazit

Das Memory Model des Monolithen ist die Grundlage für deterministisches HPC und deterministisches KI-Training. 
Daten bewegen sich nicht dynamisch, sondern entlang eines statisch definierten Pfads. 
Durch explizite Kontrolle von Partitionen, Scratchpads und Bankzugriffen entsteht ein Speicherverhalten, das:

- schneller,
- energieeffizienter,
- reproduzierbarer
- und wissenschaftlich transparenter

ist als alles, was klassische HPC- oder GPU-Systeme bereitstellen können.

---

## 24. Programming Model 
(Structural Programming Model, Restrictions, Allowed Constructs)

Das KORA-Programming Model unterscheidet sich grundlegend von klassischen imperative-, thread- oder GPU-orientierten Modellen. 
Da der Monolith deterministisch arbeitet, benötigt er ein ebenso deterministisches Programmiermodell. 
Das Ziel ist nicht, dem Programmierer Scheduling, Speicherverwaltung oder Parallelisierung aufzuzwingen – 
sondern diese vollständig zu eliminieren.

Das Programming Model basiert auf drei Prinzipien:

1. **Deklaration statt Imperativlogik**
2. **Struktur statt Kontrolle**
3. **Deterministische Modelle statt dynamischer Abläufe**

Dieses Kapitel definiert, welche Konstrukte erlaubt sind, welche verboten sind und wie ein Programm KORA-konform wird.

### 24.1 Grundprinzipien des Structural Programming Model

Das Modell basiert auf folgenden Grundannahmen:

- Es gibt keine individuellen Threads.
- Es gibt keine dynamischen Speicheradressen.
- Es gibt keinen „globalen“ Speicherzugriff.
- Es gibt keine bedingten Pfade, die nicht statisch analysierbar sind.
- Es gibt keine Schleifen, deren Laufzeit nicht deterministisch aus Eingabedaten ableitbar ist.
- Es gibt keine Datenstrukturen, deren Größe zur Laufzeit variiert.

Programmieren bedeutet daher:

    eine Struktur zu definieren, aus der der Compiler
    einen deterministischen Scheduling Tree erzeugen kann.

Das Modell ist funktional-deklarativ, nicht imperative.

### 24.2 Erlaubte Strukturkonstrukte

Die folgenden Konstrukte sind erlaubt, da sie deterministisch analysierbar und partitionierbar sind:

#### 24.2.1 Feste Schleifen

Erlaubt sind Schleifen, deren Laufzeit zur Compilezeit oder Modellzeit bekannt ist:

    for i in range(N):
        ...

N kann konstante Größe haben oder aus Problemparametern stammen.

#### 24.2.2 Feste Datenstrukturen

Erlaubt sind:

- Tensoren
- Matrizen
- Felder
- CFD-Gitter
- Stencil-Blöcke
- Logische Partitionen (Regionen, Tiles)

Diese Strukturen müssen feste Dimensionen besitzen.

#### 24.2.3 Deterministische Operatoren

Erlaubt sind Operationen wie:

- Add, Mul, Div
- MatMul
- Convolution
- Laplace, Divergence, Gradient
- elementweise Funktionen
- feste Graphoperationen

#### 24.2.4 Komposition von Operatoren

Modelle dürfen Operatoren beliebig kombinieren, solange die Struktur statisch ist:

    y = relu(W @ x + b)

oder:

    u_next = u + dt * divergence(flux(u))

#### 24.2.5 Phasenbasierte Modelle

Programme dürfen sich in Phasen strukturieren:

    Phase 1: Daten vorbereiten
    Phase 2: Compute
    Phase 3: Reduktion
    Phase 4: Writeback

Diese Struktur wird vom Compiler interpretiert.

### 24.3 Nicht erlaubte Konstrukte

Die folgenden Konstrukte sind **nicht erlaubt**, da sie deterministische Ausführung unmöglich machen würden:

#### 24.3.1 dynamische Speicherallokation

Nicht erlaubt:

    new Tensor(size_that_depends_on_runtime)

    malloc(...)
    free(...)

#### 24.3.2 dynamische Datenstrukturen

Nicht erlaubt:

- Listen
- Pointer
- Hashmaps
- dynamisch wachsende Arrays
- verkettete Strukturen

#### 24.3.3 unbeschränkte Kontrolllogik

Nicht erlaubt:

    while(condition_not_known_statistically):
        ...

    if(random() < 0.5):
        ...

    break / continue in nicht-statischen Schleifen

#### 24.3.4 rekursive Funktionen

Rekursion erzeugt dynamische Call-Stacks:

Nicht erlaubt:

    def f(x):
        return f(x-1) + f(x-2)

#### 24.3.5 dynamisches Scheduling

Es gibt keine Konstrukte für:

- Threads
- Mutex
- Locks
- atomare Operationen
- Taskpools

#### 24.3.6 nicht deterministische Ordnungen

Nicht erlaubt:

- sortieren ohne festen Schlüssel
- randomisierte Algorithmen
- Monte-Carlo-Verfahren ohne deterministische Seeds

### 24.4 Wie programmiert man ein KORA-Modell?

#### (1) Modell definieren
Der Nutzer beschreibt:

- Tensorgrößen
- Stencilradien
- Datenlayouts
- physikalische Parameter
- mathematische Abbildung

Beispiel für eine PDE:

    u_next = u + dt * divergence(flux(u))

Beispiel für KI:

    y = softmax(W2 @ relu(W1 @ x))

#### (2) Struktur fixieren

Der Nutzer definiert:

- Blockgrößen
- Regionen
- Iterationsanzahlen
- Phasen

Beispiel:

    Simulation über 10.000 Zeitschritte
    Blockgröße 32 x 32 x 16
    Phase = {Compute, Reduce, Writeback}

#### (3) SCI-Compiler übernimmt

Der Compiler:

- erstellt Scheduling Trees
- plant DMA-Slots
- plant Memoryfenster
- optimiert Layouts
- generiert TSF

#### (4) Ausführung auf dem Monolithen

Der Monolith führt das TSF-Programm deterministisch aus.

Kein Benutzer greift je direkt auf Memory, Fabric oder DMA zu.

### 24.5 Vorteile des Structural Programming Models

Das Modell bietet:

- vollständige Reproduzierbarkeit
- einfache mathematische Modellierung
- keine Deadlocks
- keine Race Conditions
- keine komplexe Speicherverwaltung
- keine Threads
- keine Synchronisationsfehler
- klare Debugbarkeit
- automatische Parallelisierung
- automatische Partitionierung
- deterministische Performance

Es zwingt Entwickler **nicht**, low-level zu programmieren, sondern stellt sicher, 
dass der Compiler die Ordnung übernimmt.

### 24.6 Fazit

Das KORA Programming Model ist kein klassisches Imperativmodell. 
Es ist ein **strukturelles, deterministisches Programmierparadigma**, 
das deklarative Modelldefinitionen in geordnete, hardwarekompatible, reproduzierbare Ausführungspläne übersetzt.

Es eliminiert alle Quellen dynamischer Nichtdeterministik und schafft eine programmierbare, wissenschaftlich transparente Plattform für deterministisches HPC und deterministisches KI-Training.

---

## 25. Device & I/O Model 
(External Interfaces, DMA-Fenster, deterministische Protokolle)

Der Monolith verzichtet auf ein klassisches Betriebssystem, Interrupts, Treiber oder dynamische I/O-Pfade. 
Alle Interaktion mit der Außenwelt ist deterministisch, geplante und streng phasenorientiert. 
Dieses Kapitel definiert, wie externe Geräte, Netzwerke und Speicher in das Ausführungsmodell integriert werden.

Das Device-Modell orientiert sich nicht an Linux, Treibern oder Systemaufrufen. 
Stattdessen basiert es auf drei Prinzipien:

1. deterministische DMA-Fenster
2. statisch definierte Transferprotokolle
3. strukturierte I/O-Phasen im Scheduling Tree

### 25.1 Grundprinzip: I/O ist eine Phase, kein Ereignis

In einem klassischen System löst ein Gerät ein Ereignis aus:
    Interrupt → Treiber → Scheduler → Kernel → Prozess

Der Monolith kennt keine Ereignisse und keine ungeplanten Übergänge. 
Stattdessen wird I/O als formale Phase eines deterministischen Programms behandelt:

    Phase I/O-Load
    Phase Compute
    Phase I/O-Store

I/O kann nur an eindeutig definierten Punkten stattfinden. 
Es gibt keine spontane Kommunikationsaufnahme.

### 25.2 Externe Datenquellen / -senken

KORA unterscheidet drei externe Klassen:

#### (A) Storage-Geräte

- NVMe / SSD
- Distributed Filesystem
- Object Storage

Zugriff erfolgt über DMA-Fenster:

    I/O-Fenster → Buffer → Memorybanks

Keine Filesystemlogik in der Hardware, stattdessen feste Offsets:

    offset = base + n * blocksize

#### (B) Netzwerkgeräte

- Ethernet
- deterministisches RDMA
- Intra-Rack Fabric

Kommunikation erfolgt über:

    phasenbasierte, deterministisch reservierte Transfer-Slots

#### (C) Sensoren / Aktuatoren

Nur relevant in Echtzeitanwendungen.
Zugriff erfolgt ebenfalls per statischen Slots, nie per Interrupt.

### 25.3 Device Descriptor Tables (DDT)

Alle externen Geräte / Streams sind durch statische Tabellen beschrieben:

- Basisadresse
- Blockgröße
- Anzahl Blöcke
- erlaubte Transferfenster
- erlaubte Phasen
- zulässige Latenzen

Diese Tabellen werden vom Compiler generiert, nicht vom Benutzer.

Beispiel:

    Device: InputStream0
        Base: 0x00040000
        Blocksize: 1 MB
        Allowed Phases: {0, 7}
        Mode: Read-Only

Die Runtime erzeugt niemals dynamische Änderungen.

### 25.4 DMA-Fenster

DMA ist die einzige Form externer Datenübertragung.

Ein DMA-Fenster beinhaltet:

- Quelle (Device oder Remote-Endpunkt)
- Ziel (Memorybank oder Scratchpad)
- Block-ID
- Größe
- Startzyklus
- Endzyklus
- TDM-Zuordnung

DMA-Fenster sind:

- statisch
- kollisionsfrei
- deterministisch
- phasenorientiert

Beispiel für ein Fenster:

    DMA-Window:
        src: Device0
        dst: Bank12
        size: 256 KB
        start: Phase 1, Slot 3
        end:   Phase 1, Slot 5

### 25.5 Integration in Scheduling Trees

Alle I/O-Operationen erscheinen als Knoten im Scheduling Tree:

    Node: IO_Load_Block_17
        Children: {Compute_Block_17}

    Node: IO_Store_Result_2
        Parents: {Compute_Final_Reduction}

Der Compiler garantiert:

- keine Parallelkollisionen
- keine Überbelegung der Fabric
- keine Überlappung nicht zulässiger Fenster

### 25.6 Netzwerkmodell: deterministisches RDMA

Der Monolith nutzt keine TCP/IP-Stacks, keine Kernelpfade und keine Paketvermittlung. 
Stattdessen existiert ein deterministisches RDMA-Modell:

    Remote_Write(BlockID)
    Remote_Read(BlockID)
    Remote_Reduce(BlockID)

Jeder Vorgang ist an feste Zeitfenster gebunden.
Es existieren keine verlorenen Pakete, da keine Pakete im klassischen Sinn existieren.

Stattdessen:

    TDM-Slot → Frame → deterministisches Segment → Empfangstile

### 25.7 Multi-Rack Kommunikation

Rack-übergreifende Kommunikation erfolgt über die Meta-Fabric:

- gefeste Cross-Rack Slots
- kein Routing
- keine Adaption
- feste Pfade pro Blockgruppe

Dies garantiert deterministische Latenz:

    L_total = L_serdes + n_hops * L_slot

mit allen Komponenten konstant.

### 25.8 Filesystem-Modell

Der Monolith besitzt kein eigenes Filesystem. 
Stattdessen existiert ein externer Filesystem-Service:

- POSIX oder Objektstorage
- arbeitet auf einem separaten Host
- kommuniziert per deterministischem RDMA

Lesen/Schreiben erfolgt über:

    FileServiceRead(BlockID)
    FileServiceWrite(BlockID)

Blockgrößen sind fest, z. B.:

    1 MB, 2 MB oder 4 MB

Komplexere Operationen (z. B. open, close, seek) erfolgen auf dem Host, nicht im Monolithen.

### 25.9 Fehlerfallverhalten

Der Monolith reagiert nicht dynamisch auf Fehler. 
Stattdessen:

- jedes fehlerhafte Gerät wird isoliert
- die DDT markiert das Gerät als inaktiv
- der Compiler erhält beim nächsten Run die neue DDT
- deterministische Ausführung bleibt erhalten

Es gibt keine Laufzeitheilung (kein Retry, kein Recovery).

### 25.10 Vorteile des KORA-I/O-Modells

- kein Interrupt-Jitter
- keine Treiberkomplexität
- deterministisches Timing
- vorhersehbare Pipelinezeiten
- einfache Debugbarkeit
- keine Paketverluste
- konstante Bandbreite
- wissenschaftlich reproduzierbare I/O-Pfade
- vollständige Kontrolle über Latenz

### 25.11 Fazit

Das Device & I/O Model des Monolithen eliminiert alle nichtdeterministischen Bestandteile klassischer Systeme. 
Durch statische DMA-Fenster, deterministische Netzwerkpfade und strukturierte I/O-Phasen entsteht ein Kommunikationsmodell, das:

- vorhersagbar,
- stabil,
- energieeffizient,
- wissenschaftlich reproduzierbar

ist und perfekt mit dem deterministischen Ausführungsmodell des Monolithen harmoniert.

---

## 26. Verification & Deterministic Guarantees 
(Formale Sicherheit, Korrektheitsmodelle, Reproduzierbarkeit)

Der Monolith ist kein best-effort System, sondern eine vollständig deterministische Rechenarchitektur. 
Damit unterscheiden sich die Anforderungen an Verifikation, Debugging und Validierung grundlegend von klassischen CPU-, GPU- oder HPC-Clustern. 
Dieses Kapitel beschreibt das Verifikationsmodell, das sicherstellt, dass jede Ausführung:

- korrekt,
- bit-identisch,
- wiederholbar,
- phasenstabil,
- frei von Rennbedingungen,
- frei von Scheduling-Jitter

ist — unabhängig von Last, Temperatur, Takt oder Umgebung.

KORA ersetzt klassische Fehlerquellen durch strukturelle Garantien.

### 26.1 Grundsatz: keine dynamische Nichtdeterministik

Klassische Systeme erzeugen Nichtdeterminismus durch:

- Thread Scheduling
- Cache-Misses
- Prefetch-Variabilität
- Netzwerkjitter
- Interrupts
- Atomics & Locks
- Prozesswechsel
- dynamische Speicherzuweisung
- Out-of-Order-Ausführung

Der Monolith eliminiert alle diese Mechanismen. 
Damit wird Verifikation nicht zu einer Frage von „Tests“, sondern zu einer Frage von **formalen strukturellen Eigenschaften**.

### 26.2 Verifikationsmodell: drei Ebenen

KORA definiert drei Schichten der Verifikation:

1. **Compiler Verification**
2. **TSF & Scheduling Tree Verification**
3. **Hardware Execution Verification**

Jede Ebene garantiert, dass deterministische Ausführung erhalten bleibt.

### 26.3 Compiler Verification

Der SCI-Compiler prüft:

- gesicherte statische Datenstrukturen,
- feste Schleifen,
- deterministische Operatoren,
- interne Graphkonsistenz,
- vollständige Abwesenheit dynamischer Kontrollflüsse,
- korrekte Partitionierung (jede Partition muss in SPM passen),
- korrekte Tile-Zuordnung,
- korrekte DMA-Planung,
- konfliktfreie Memorybank-Zuordnung.

Der Compiler garantiert:

    Das resultierende TSF-Programm ist deterministisch ausführbar.

Fehler werden als Compile-Zeit-Fehler signalisiert, nicht zur Laufzeit.

### 26.4 TSF Verification

TSF ist ein strukturelles Format. 
Der TSF-Validator prüft:

- Syntax und Struktur,
- Vollständigkeit aller Phasen,
- korrekte Pflege der SRDB-Metadaten,
- Korrektheit der Scheduling-Bäume,
- TDM-Zuordnungen ohne Konflikte,
- deterministische Reihenfolge aller DMA-Fenster,
- Memorybank-Konsistenz,
- gültige Tile-Layouts.

Es existieren keine optionalen Felder. 
TSF ist nur gültig oder ungültig.

### 26.5 Scheduling Tree Verification

Scheduling Trees repräsentieren die zeitliche Struktur.  
Verifiziert werden:

- Topologie (keine Zyklen),
- korrekte Phasenreihenfolge,
- feste Latenzen entlang der Kanten,
- konsistente Abhängigkeitskanten,
- keine Überschneidungen mit DMA-Fenstern,
- garantierte Deadlock-Freiheit,
- garantierte Race-Free Ausführung.

Formaler Test:

    Für jeden Knoten existiert mindestens ein definierter Vorgänger und/oder Nachfolger.
    Keine Kante kann zur Laufzeit dynamisch verändert werden.

### 26.6 Hardware Execution Verification

Das Verifikationsmodell garantiert:

- jede Phase besitzt fixen Beginn und fixen Abschluss,
- DMA wird nur in erlaubten Slots aktiv,
- Memorybanks werden nie kollidierend adressiert,
- jeder Tile besitzt feste Takte und deterministische Pipelines.

Damit ist die Ausführung:

- reproduzierbar,
- phasenstabil,
- frei von Jitter,
- frei von Timing-Variabilität,
- bit-identisch über beliebig viele Läufe.

### 26.7 Globale Determinismus-Garantie

Die formale Eigenschaft lautet:

    Für identische Eingabedaten und identische TSF-Programme ist die gesamte Ausführung bit-identisch.

Das bedeutet:

- gleiche Ergebnisse,
- gleiche Ausführungszeiten,
- gleiche DMA-Muster,
- gleiche Memoryzugriffe,
- gleiche Scheduling-Pfade.

Auch bei Wiederholungen:

- nach Minuten,
- Tagen,
- Wochen,
- oder auf anderen Monolith-Instanzen.

### 26.8 Validierung wissenschaftlicher Ergebnisse

Dank deterministischer Ausführung:

- Simulationen werden absolut reproduzierbar.
- Experimente werden überprüfbar.
- Trainingsläufe sind bit-identisch.
- wissenschaftliche Publikationen können Ergebnisse exakt referenzieren.

KORA ermöglicht:

    computational reproducibility ohne Zusatzaufwand.

Dies ist ein entscheidender Vorteil gegenüber GPUs und HPC-Clustern.

### 26.9 Fehlerklassen und ihre Behandlung

Auf dem Monolithen existieren keine „Laufzeitfehler“ im klassischen Sinn.

Fehlerklassen:

#### (A) Compilerfehler

- dynamischer Pfad erkannt
- unsichere Partition
- nicht analysierbare Abhängigkeit

Lösung: Modelle anpassen.

#### (B) TSF-Validierungsfehler

- unzulässige Phase
- Kollision in DMA-Fenstern
- unvollständige Scheduling-Sequenz

Lösung: Compiler- oder Modellkorrektur.

#### (C) Hardwarefehler

- Memorybank defekt
- Tile außer Betrieb
- Überhitzung

Lösung: Isolierung durch SRDB; deterministische Ausführung bleibt erhalten.

### 26.10 Hardware-Redundanzmodelle

Der Monolith unterstützt strukturelle Redundanz:

- deaktivierbare Tiles,
- deaktivierbare Banks,
- Umschaltung auf Ersatzpfade.

Der SRDB garantiert:

    Redundanz beeinflusst nicht die logische Ausführung.

Zeitplan und Ergebnis bleiben identisch.

### 26.11 Wissenschaftlicher Vorteil: formale Garantien statt heuristischer Performance

KORA bietet nicht nur Geschwindigkeit, sondern wissenschaftlich wesentlich Wichtigeres:

- Bit-genaue Reproduzierbarkeit
- formale Korrektheit
- strukturelle Debugbarkeit
- eliminiert nichtdeterministische Clusterarchitekturen
- validiert Experimente systemisch statt statistisch

Diese Eigenschaften existieren in keinem HPC- oder KI-System heute.

### 26.12 Fazit

Das Verifikationsmodell von KORA kombiniert Compileranalyse, TSF-Validierung und deterministische Hardwareausführung zu einem System, das:

- mathematisch korrekt,
- vollständig reproduzierbar,
- wissenschaftlich verifizierbar,
- transparent,
- und strukturell sicher

ist.

Es ermöglicht eine neue Klasse von wissenschaftlicher Rechenarchitektur: 
deterministisches HPC und deterministisches KI-Training.

---

## 27. Data Center Integration & Deployment 
(Rack-Design, Energie, Kühlung, Monitoring, Operations)

Der Monolith ist nicht nur eine Architektur, sondern ein vollständiges Rechenmodul, das in Rechenzentren integriert werden muss. 
Da der Monolith deterministisch arbeitet, folgt auch die Rechenzentrumsebene deterministischen Prinzipien. 
Dieses Kapitel beschreibt, wie ein KORA-System physisch, thermisch, elektrisch und logisch eingebunden wird und welche Anforderungen und Vorteile daraus entstehen.

Das Ziel ist ein System, das:

- stabil,
- vorhersagbar,
- energieeffizient,
- leicht wartbar,
- thermisch transparent,
- und wissenschaftlich einsetzbar

ist.

### 27.1 Grundannahme: Der Monolith ist ein strukturelles Modul

Der Monolith ist kein CPU/GPU-Board, sondern eine definierte Komposition aus:

- Compute Tiles
- Memorybanks
- Fabric-Links
- SRDB
- deterministischen Netzwerkschnittstellen
- integrierter Strompfade
- integrierter Kühlstrukturen

Ein Monolith entspricht funktional einem „Rechenknoten“, jedoch ohne OS, ohne Scheduler und ohne Netzwerkprotokollstacks.

Ein Rechenzentrum skaliert daher strukturell, nicht dynamisch:

    Monolith → Rack → MCluster → Facility

### 27.2 Rack-Design für den Monolithen

Ein Rack enthält typischerweise:

- 8 bis 16 Monolithen
- eine deterministische Rack-Fabric
- redundante Strompfade
- Kaltgang / Warmgang-Trennung
- Luft- oder Flüssigkeitskühlung (abhängig von Leistungsdichte)

Die Rack-Fabric nutzt feste TDM-Slots und deterministische Pfade. 
Es existiert kein Ethernet-Switch im klassischen Sinn. 
Stattdessen:

    Fixed-Path Backplane Fabric

Dies reduziert:

- Latenz
- Jitter
- Energiebedarf
- Komplexität

### 27.3 Energieversorgung

Der Monolith besitzt eine feste Leistungsaufnahme:

- niedrige Variabilität (da keine dynamischen Boost-Mechanismen existieren)
- planbarer Energiebedarf
- kaum transiente Peaks

Typische Werte:

- 1,0–1,2 kW pro Monolith
- 8–16 kW pro Rack

Da keine taktvariablen Turbo-Modi existieren, ist das Energiemanagement stabil und reproduzierbar.

Kein DVFS, kein GPU-Boost, keine dynamischen Frequenzsprünge.

Vorteile:

- Netzstabilität
- einfachere Skalierungsplanung
- geringere Pufferanforderungen
- hohe predictability

### 27.4 Kühlung

Der Monolith besitzt eine konstante Leistungsaufnahme, daher ist die thermische Signatur:

- stabil
- ohne Sprunglasten
- ohne „Hot Cycles“
- ohne Turbo-Induzierte Temperaturspitzen

Kühlsysteme können auf konstante Wärmelast ausgelegt werden. 

Typisch:

- Luftkühlung bei 1 kW Klasse möglich
- Flüssigkeitskühlung für dichte Multi-Monolith Racks
- keine Einzelkomponenten mit 300 W Peaks wie bei GPUs

Thermische Reproduzierbarkeit unterstützt:

- deterministische Ausführung
- wissenschaftliche Wiederholbarkeit
- lange Bauteillebensdauer

### 27.5 Verkabelung und Topologie

Da der Monolith:

- keine Ethernet-Networking-Stacks besitzt,
- keine dynamischen Routing-Protokolle nutzt,
- keine adapterbasierten Karten benötigt,

besteht die externe Verkabelung aus:

- deterministischen Fabric-Links
- festen Backplane-Steckverbindungen
- optionalen RDMA-Verbindungen zu Host-Systemen

Der Host selbst ist ein einfacher Control-Node:

    Host → TSF-Upload → Start → Monitoring → Result-Fetch

Keine komplexe Treiberarchitektur.

### 27.6 Host-Systeme und Steuerung

Ein Rechenzentrum benötigt für Monolith-Racks dedizierte Hosts:

- CPU-Server (klassisch)
- Linux oder BSD
- Filesystemdienste
- TSF-Deployment
- Telemetriesammlung

Der Host führt keine Berechnungen durch, sondern dient nur als:

    Management & Data Orchestration Layer

Typische Aufgaben des Hosts:

- Laden und Starten von TSF-Programmen
- Bereitstellen von Eingabedaten
- Übernehmen der Ergebnisse
- Logging
- Integritätsprüfung
- Kommunikation zwischen Racks

Der Host beeinflusst die Ausführung nicht.

### 27.7 Monitoring

Monitoring ist deterministisch:

- jede Phase hat fixe Zeitfenster
- jede DMA-Operation hat feste Zyklen
- jeder Temperaturverlauf ist vorhersehbar
- Energieprofile sind konstant

Monitoring liefert nicht:

- variable Lastkurven,
- dynamische CPU-Auslastungen,
- oder scheduling-basierte Zeitstempel.

Stattdessen:

    Phase 17 dauert immer exakt X µs
    DMA-Fenster 42 startet immer exakt an T_slot=12

Monitoring-Daten sind vollständig reproduzierbar.

### 27.8 Deployment

Ein Deployment besteht aus:

1. Modell erstellen (HAPI)
2. Kompilieren (SCI)
3. Validieren (TSF-Validator)
4. Laden auf Rack (Host-System)
5. Ausführen
6. Abrufen der Ergebnisse
7. Archivieren für Reproduzierbarkeit

Wichtig:

    Es gibt kein „Deployment-Fehlerverhalten“ durch OS oder Scheduling.

Nur TSF-Validierungsfehler können Deployment verhindern.

### 27.9 Fehlerverhalten und Wartung

Der Monolith besitzt:

- deaktivierbare Tiles
- deaktivierbare Memorybanks
- deterministische Isolation
- kein dynamisches Recovery

Defekte Komponenten werden strukturell markiert. 
Die Ausführung bleibt deterministisch, jedoch mit verringerter Kapazität.

Rack-Wartung:

- Austausch kompletter Monolith-Module
- deterministische Neuinitialisierung
- keine Migration laufender Prozesse
- keine Heuristikbasierten Reschedules

### 27.10 Integration in wissenschaftliche Rechenzentren

KORA eignet sich besonders für:

- CFD-Zentren
- Klimasimulation
- Materialwissenschaften
- KI-Forschung
- numerische Mathematik
- Geowissenschaften
- Bioinformatik

Da KORA deterministisch arbeitet, entstehen:

- klare Validierungsprozesse
- bitgenaue Wiederholbarkeit
- reproduzierbare Publikationen
- planbare Performance

Dies entspricht den Anforderungen moderner Wissenschaft.

### 27.11 Fazit

KORA integriert sich nicht wie ein klassischer HPC-Cluster, sondern wie eine deterministische Rechnenheit. 
Durch konstante Energieprofile, einfache Verkabelung, feste Netzwerktopologien und phasenorientierte Ausführung entsteht ein System mit:

- maximaler Vorhersagbarkeit,
- geringem Wartungsaufwand,
- hoher Energieeffizienz,
- reproduzierbarem Monitoring,
- klarer wissenschaftlicher Integrität.

KORA ist damit nicht nur eine Architektur, sondern ein strukturelles Rechenmodul für wissenschaftliche Rechenzentren der nächsten Generation.

---

## 28. Boot, Configuration & Control Flow 
(Initialisierung, TSF-Load, SRDB-State, Phasensteuerung)

Der Monolith besitzt kein klassisches Betriebssystem, keinen Kernel, keinen init-Prozess und keinen dynamischen Treiberstack. 
Stattdessen existiert ein deterministischer Start- und Kontrollpfad, der festlegt:

- wie der Monolith initialisiert wird,
- wie TSF-Programme geladen werden,
- wie SRDB seine interne Struktur aufbaut,
- wie Sicherheits- und Fehlerzustände behandelt werden,
- wie der Ausführungszyklus gesteuert wird.

Dieses Kapitel definiert die gesamte Lebenszeit eines Monolith-Laufs.

### 28.1 Grundprinzip: deterministische Lebenszyklen

Ein klassisches System hat einen dynamischen Lifecycle:

    Boot → Kernel → Treiber → Scheduler → Prozesse → Threads → Interrupts

Der Monolith hat dagegen einen strukturierten, festen Lifecycle:

    Reset → Initialize → Load TSF → Verify → Execute → Finalize

Es existieren keine Hintergrundprozesse, kein Scheduling, keine Interrupts.

Jede Phase hat:

- feste Dauer
- festen Ablauf
- festen Zustand

### 28.2 Reset-Zustand

Nach einem Hardware-Reset befindet sich der Monolith in einem minimalen, definierten Zustand:

- alle Tiles deaktiviert
- SRDB leer
- Memorybanks in Nullkonfiguration
- Fabric im Idle-Zustand
- TDM-Slots unzugeordnet
- keine TSF-Information geladen

Der Reset ist vollständig deterministisch.

### 28.3 Initialisierung

Die Initialisierung aktiviert grundlegende Komponenten:

- SRDB in Basiszustand
- Fabric Clocking
- Memorybank Clocking
- Test der Tile-Cluster (Built-in Self Test)
- Erkennung deaktivierter / beschädigter Tiles
- Konfiguration der Bank-Masken
- Aufbau des Grundzustands für Scheduling Trees (leer)

Beispiel für interne Initialisierungsdaten (Einrückung):

    SRDB:
        version: 1.0
        tiles_enabled: 384/384
        banks_enabled: 64/64

Initialisierung testet nicht die Logik des TSF-Programms — nur die Hardware.

### 28.4 Laden des TSF-Programms

Der Host lädt das TSF-Programm über eine deterministische Datenpfadverbindung:

    Host → TSF-Loader → SRDB

Dabei gilt:

- TSF wird blockweise übertragen
- Reihenfolge ist fix
- beschädigte Blöcke führen zu sofortigem Abbruch
- es existieren keine Partial Loads
- erst vollständiger TSF-Load → dann Verifikation

TSF enthält:

- Scheduling Trees
- DMA-Fenster
- Memory-Zuordnung
- TDM-Slots
- Phasenstrukturen

TSF ersetzt vollständig jede Form von „Programmcode“ im klassischen Sinn.

### 28.5 TSF-Verifikation

Vor der Ausführung findet die vollständige Validierung statt:

- Strukturprüfung
- Syntaxprüfung
- Phasenprüfung
- DMA-Fensterprüfung
- keine überlappenden Slots
- keine kollidierenden Banks
- deterministische Pfade

Fehler führen zu:

    TSF-Reject → Abort → Fehlerreport an Host

Der Monolith startet niemals eine unsichere Ausführung.

### 28.6 Aufbau des SRDB-Laufzeitkontexts

Nach der TSF-Verifikation baut SRDB seine internen Strukturen:

- globale Scheduling Trees
- regionale Trees
- TDM-Slotpläne
- DMA-Sequenzen
- Memoryfenster-Mappings
- Tile-zu-Phase Zuordnung
- Reduktionspfade

Dies entspricht einem deterministischen „Precompute“ aller zeitlichen Verläufe.

### 28.7 Start der deterministischen Ausführung

Die Ausführung erfolgt in Phasen:

    Phase 0: I/O Load
    Phase 1: Compute
    Phase 2: Reduction
    Phase 3: Writeback
    ...
    Phase N: Finalisierung

Jede Phase:

- hat definierte Dauer,
- hat definierte Tile-Zuordnung,
- besitzt feste Latenzen,
- besitzt kollisionsfreie DMA-Slots,
- ist frei von dynamischen Einflüssen.

Es gibt keinen Scheduler, keine Threads, keine Ereignisse.

### 28.8 Kontrollfluss während der Ausführung

Der Kontrollfluss ist linear und deterministisch:

    for phase in Phases:
        SRDB.execute(phase)

Es existieren genau zwei Ausnahmefälle:

#### (A) Hardwarefehler

- defekte Tile-Block
- Memorybank-Ausfall
- Fabric-Link-Ausfall

Reaktion:

    SRDB isoliert das Element, bricht laufende Ausführung ab

#### (B) Temperaturschutz

Da die thermische Last konstant ist, tritt dies selten auf.

Reaktion:

    Monolith geht in geregelten Safe Mode

Kein dynamisches Takt- oder Frequenzverhalten.

### 28.9 Finalisierung

Nach Abschluss aller Phasen:

- Memorybanks werden synchronisiert
- Ergebnisse stehen in festen Regionen
- DMA-Fenster für Ausgabedaten werden aktiviert
- Statusinformationen werden bereitgestellt

Finalisierung ist streng geordnet.

### 28.10 Rückgabe der Ergebnisse

Die Rückgabe erfolgt über:

    deterministische DMA-Fenster → Host

Typischer Ablauf:

    Phase Final
    DMA-Out Block 0
    DMA-Out Block 1
    ...
    DMA-Out Block M

Keine zusätzlichen Protokolle, keine OS-spezifischen Systemcalls.

### 28.11 Sicherheitsmodell

Das Sicherheitsmodell basiert auf struktureller Isolation:

- keine dynamische Prozessisolation nötig
- keine Rechteverwaltung im System
- TSF-Programme können nur über Host geladen werden
- Host autorisiert alle Programme
- SRDB führt niemals externen Code aus

Der Monolith kann nicht „gehackt“ werden, weil:

- es keinen Codepfad gibt,
- keine Befehle, die modifizierbar wären,
- kein Speicher, der dynamisch beschreibbar wäre.

### 28.12 Logging & Auditing

Alle Phasen sind reproduzierbar:

    Phase 1 → 312 µs
    Phase 2 → 127 µs
    ...

Ein Log enthält:

- Phasenzeitstempel
- DMA-Fensterstatus
- Temperaturen
- Aktivitätsprofile der Tiles
- Memorybank-Auslastung

Diese Logs sind identisch für jeden Lauf mit identischen Eingabedaten.

### 28.13 Fazit

Der Monolith besitzt einen einzigartigen Betriebs- und Kontrollfluss, der vollständig deterministisch ist. 
Durch statische Initialisierung, TSF-Verifikation, phasenorientiertes Scheduling und strukturelle Isolation entsteht ein Ablaufmodell, das:

- bit-identisch reproduzierbar,
- wissenschaftlich überprüfbar,
- sicher,
- frei von dynamischen Einflüssen,
- robust,
- energieeffizient,
- und einfach integrierbar

ist.

KORA braucht kein Betriebssystem — der Compiler und SRDB übernehmen die vollständige Kontrolle.

---

## 29. Control Plane, Data Plane & Telemetry 
(Host-Steuerung, Datenpfade, Monitoring)

Der Monolith arbeitet vollständig deterministisch und besitzt keine interne Kontrolllogik im klassischen Sinn. 
Alle Kontrolle, Steuerung, Überwachung und Bereitstellung erfolgt durch externe Systeme. 
Damit ist KORA nicht nur eine Architektur, sondern ein Gesamtmodell aus:

- einem deterministischen Compute-Modul (der Monolith),
- einer externen Control Plane,
- einer externen Data Plane,
- einem deterministischen Telemetriesystem.

Dieses Kapitel beschreibt, wie diese Ebenen zusammenspielen.

### 29.1 Grundprinzip: der Monolith ist „Compute Only“

Der Monolith führt ausschließlich TSF-Programme aus. 
Er besitzt:

- kein internes OS,
- keine Syscalls,
- keine Prozesse,
- keine Netzwerk-Stacks,
- keine Dateisysteme,
- keine Treiber,
- keine Interrupts.

Die gesamte Kontrolle liegt außerhalb:

    Host → Control Plane → TSF / Daten / Startsignal

Die gesamte Ausführung liegt im Monolith:

    Monolith → deterministische Phasen → Ergebnisse

Dieses Modell trennt Kontrolle und Ausführung klar.

### 29.2 Rollenmodelle

#### 29.2.1 Host-System

Ein klassischer CPU-Server, z. B.:

- 1–2 CPUs
- Linux oder BSD
- Storage-Anbindung
- Netzwerk-Anbindung
- Monitoring-Agent

Aufgaben des Hosts:

- TSF laden
- Input-Daten bereitstellen
- Startsignale senden
- Ergebnisse zurücknehmen
- Logs archivieren

#### 29.2.2 Control Plane

Eine softwareseitige Schicht auf dem Host, z. B.:

    kora-control

Aufgaben:

- TSF-Validierung (Host-seitig)
- Deployment mehrerer Jobs
- Priorisierung (nicht Scheduling!)
- sichere Bereitstellung von I/O-Fenstern
- Verwaltung mehrerer Monolithen

#### 29.2.3 Data Plane

Stellt die reinen Datenpfade bereit:

    Storage → DMA → Monolith
    Monolith → DMA → Storage

Beispiele:

- NVMe
- Objektstorage
- verteilte Dateisysteme

#### 29.2.4 Telemetry Plane

Erfasst:

- Energieverbrauch
- Temperatur
- Phasenzeitpunkte
- DMA-Aktivität
- Banks-Status
- Tile-Status
- Fehlersignale

Alle Daten sind deterministisch.

### 29.3 TSF-Deployment-Prozess

Der Prozess besteht aus fünf Schritten:

1. TSF-File laden
2. Strukturprüfung auf dem Host
3. Übertragung über deterministischen Link
4. TSF-Verifikation im Monolith
5. Aktivierung

Reihenfolge ist fest, nicht konfigurierbar.

Ein Deployment kann nicht „teilweise“ erfolgen.

### 29.4 Startsignal: „Begin Run“

Nach TSF-Validierung sendet der Host das Steuersignal:

    begin_run

Dies führt zu:

- Globaler Reset des Monolith-Ausführungskontexts
- Starten der Phasen nach Scheduling Tree

Es gibt exakt **ein** Startsignal pro Run.

### 29.5 Data Plane: Bereitstellung der Eingabedaten

Daten werden über festgelegte Fenster bereitgestellt:

    Input Block 0: Phase 0, Slot 3
    Input Block 1: Phase 0, Slot 7

Alle Transfers sind:

- blockweise,
- vorgeplant,
- fix im TSF beschrieben.

Es gibt kein Streaming ohne Plan.

### 29.6 Externe Filesysteme

Der Host übernimmt:

- file open
- file read
- file block mapping
- file close

Der Monolith sieht nur:

    BlockID → Daten

Dateisysteme existieren nie im Monolithen.

### 29.7 Rückgabe der Ergebnisse

Ergebnisse werden in definierte Ausgabefenster geschrieben:

    Output Block 0
    Output Block 1
    ...
    Output Block M

Der Host ruft die Blöcke ab, interpretiert sie und speichert sie.

### 29.8 Telemetry: deterministische Überwachung

Die Telemetry Plane sammelt:

#### 29.8.1 Zeitliche Daten

Beispiele:

    Phase 1 → 312 microseconds
    Phase 2 → 127 microseconds
    DMA Window 14 start → T_slot = 9

#### 29.8.2 Energieprofile

Da die Leistungsaufnahme konstant ist, entstehen perfekte Profile:

    1.18 kW ± 0.5%

#### 29.8.3 Thermische Daten

Thermische Daten sind stabil:

    57.3°C ± 0.2°C

#### 29.8.4 Auslastungsdaten

Tiles und Banks melden:

    active
    disabled
    warning-state

#### 29.8.5 Fehlerdaten

Nur strukturelle Fehler:

- Bank-Fehler
- Tile Fehler
- Fabric-Link-Fehler

Keine Softwarefehler, keine Race-Conditions, keine Zeitfehler.

### 29.9 Multi-Monolith Control Plane

Für mehrere Monolithen definiert die Control Plane:

- TSF-Verteilung
- deterministische Start-Reihenfolge
- Cross-Monolith I/O-Fenster
- Reduktionsfenster
- Rack-weite Telemetry
- globale Statusberichte

Wichtig:

    Die Control Plane führt kein Scheduling durch.

Scheduling ist Hardware: vorab, strukturell, unveränderlich.

### 29.10 Fehler- und Wiederherstellungslogik

Drei Fehlerklassen:

#### (A) Host-seitige Fehler

- Netzwerkfehler
- Filesystemfehler

Der Monolith ist davon unberührt.

#### (B) Monolith-seitige Hardwarefehler

- defekte Tile
- defekte Bank
- Fabric-Ausfall

Monolith stoppt deterministisch, gibt Fehlercode an Host.

#### (C) TSF-Fehler

- ungültige Struktur
- Kollisionen
- unvollständige Bäume

Start wird verweigert.

Es gibt kein Live-Recovery.

### 29.11 Vorteile des Control-Plane-Modells

- absolute Transparenz
- klare Trennung von Kontrolle und Ausführung
- deterministische Deployments
- Telemetrie ideal für wissenschaftliche Dokumentation
- minimaler Wartungsaufwand
- keine OS-Abhängigkeiten
- keine Laufzeitvariabilität
- klare Fehlermuster

### 29.12 Fazit

Die Control Plane, Data Plane und Telemetry bilden die externe Umgebung des Monolithen. 
Sie ermöglichen:

- sicheres Laden von Programmen,
- wissenschaftlich reproduzierbare Runs,
- deterministische Datenpfade,
- identische Phasenabläufe,
- klare Fehlerberichte.

Der Monolith bleibt frei von dynamischer Komplexität –  
die Außenwelt liefert Kontrolle, Daten und Beobachtung.

---

## 30. Benchmarking, Validation & Performance Modeling 
(strukturierte Tests, deterministische Profile)

Klassische HPC- und GPU-Systeme benötigen umfangreiche Benchmarks, um Performance zu bestimmen. 
Grund: ihre Ausführung ist nichtdeterministisch, abhängig von:

- Thread-Scheduling
- Cache-Hierarchien
- Netzwerkjitter
- Spekulation
- Taktvariationen (Boosting)
- dynamischer Last
- OS-Ereignissen

Der Monolith hingegen ist deterministisch. 
Performance ist nicht das Ergebnis eines stochastischen Systems, sondern einer strukturellen Eigenschaft der Scheduling Trees. 
Benchmarking wird damit zu:

    struktureller Validierung, nicht zur stochastischen Messung.

Dieses Kapitel beschreibt, wie Performance-Modelle, Validierung und Benchmarks für KORA funktionieren.

### 30.1 Grundprinzip: Performance = Struktur, nicht Verhalten

Bei klassischen Systemen lautet die Frage:

    Wie schnell ist diese Operation im Mittel?

Bei KORA lautet die Frage:

    Wie viele Takte benötigt diese Phase gemäß Scheduling Tree?

Damit wird Performance eine **mathematische Eigenschaft**, kein empirisch variabler Wert.

Beispiel:

    Phase Compute_Block_32x32 benötigt exakt 1428 Zyklen.
    Phase DMA-Out benötigt exakt 102 Zyklen.

Diese Werte ändern sich nie – egal:

- wie oft man misst,
- unter welcher Last,
- auf welchem Monolith-Exemplar,
- oder zu welchem Zeitpunkt.

### 30.2 Arten der KORA-Benchmarks

Es existieren drei Benchmark-Typen:

1. **Structural Benchmarks**
2. **Workload Benchmarks**
3. **Validation Benchmarks**

#### 30.2.1 Structural Benchmarks

Messen die Eigenschaften des Monolithen selbst:

- Tile-Durchsatz
- DMA-Durchsatz
- Memorybank-Latenz
- TDM-Slot-Latenz
- Scheduling Tree Tiefe

Beispiele:

    Benchmark: Tile_Throughput
    Ergebnis: 2048 ops per cycle

    Benchmark: Bank_Read_Latency
    Ergebnis: 3 cycles

#### 30.2.2 Workload Benchmarks

Basieren auf realen Szenarien:

- GEMM (Lineare Algebra)
- Convolution (KI)
- PDE-Stencils (CFD)
- Big-Data-Transformationen

Beispiel:

    GEMM 4096x4096 → exakt 3.208.192 Zyklen

#### 30.2.3 Validation Benchmarks

Verifizieren Modelle:

- CFD-Simulationen
- Energiemessungen
- KI-Training (z. B. BERT)
- Big-Data Workflows

Sie prüfen:

    ergibt der Monolith das exakt gleiche Ergebnis wie die Referenz?

### 30.3 Deterministische Performance-Modelle

Der SCI-Compiler erzeugt Performance-Modelle automatisch:

- jedes TSF enthält die exakten Zykluszahlen pro Phase
- SRDB berichtet reale Ausführung (identisch)

Performance kann vor Ausführung exakt berechnet werden:

    T_total = Σ Phase_i_cycles × clock_period

Beispiel:

    T_total = 185.307.712 cycles
    clock = 1.5 GHz
    → T = 123.54 ms

Es gibt keine Messfehler, keine Varianz.

### 30.4 Abstraktion von Takt, Hitze und Energie

Da KORA keine Boost-Mechanismen besitzt:

- Takt = konstant
- Energie = konstant
- Temperatur = konstant

Performance ist damit:

- unabhängig von thermischen Effekten,
- unabhängig von Workload-Dichte,
- unabhängig von Hintergrundlast.

Kein Throttling, kein Turbo, keine dynamischen Frequenzen.

### 30.5 Validierung wissenschaftlicher Modelle

Ein wissenschaftlicher Workflow besteht aus:

1. mathematischer Modellbeschreibung
2. Partitionierung
3. TSF-Generierung
4. deterministische Ausführung
5. Vergleich mit Referenz

Validierung wird strukturell:

    Ist die Abweichung numerisch erklärbar und reproduzierbar?

Der Monolith liefert immer dieselben Zahlen.

### 30.6 Benchmarking-Prozess

#### Schritt 1: TSF erzeugen

Der Compiler generiert:

- Scheduling Trees
- DMA-Fenster
- Tile-Zuordnung

#### Schritt 2: TSF analysieren

Vor Ausführung:

    Zykluszahlen pro Phase
    DMA-Zyklen
    Reduktionszyklen
    Memorybank-Latenzen

#### Schritt 3: Ausführung

Der Monolith führt exakt dieselben Werte aus.

#### Schritt 4: Vergleich

Analyse:

- T_predicted == T_measured
- Zyklusfehler = 0

Eine Abweichung bedeutet Hardwarefehler, nicht Lastschwankungen.

### 30.7 Wissenschaftlicher Vorteil deterministischer Benchmarks

- Reproduzierbarkeit
- Präzise Energieabschätzungen
- Exakte Planung von Ausführungszeit
- Konsistenz über Cluster
- Stabile Publikationsdaten
- Mathematik statt Statistik

Beispiel:

    Ein CFD-Lauf auf 16 Monolithen benötigt exakt 2,483 Sekunden.
    Jeder Lauf bestätigt exakt dieselben 2,483 Sekunden.

### 30.8 Grenzfall: numerische Ungenauigkeit

Einzige Quelle minimaler Abweichung:

- unterschiedliche Floating-Point-Einheiten in verschiedenen Monolith-Generationen

Lösung:

- wissenschaftliche Nutzung definierter numerischer Profile
- Compiler garantiert Konsistenz innerhalb einer Generation

### 30.9 Gefühlter Benchmark vs realer Benchmark

Es entsteht ein neues Verständnis:

- Ein GPU-Benchmark ist eine „Messung“.
- Ein KORA-Benchmark ist ein „Beweis“.

Performance ist kein Zufallsprodukt, sondern deterministisches Verhalten.

### 30.10 Vergleich mit klassischen Systemen

#### GPUs:

- hohe Varianz
- Boosting
- Cache-Hierarchien
- Scheduling-Unschärfen

#### HPC-Cluster:

- Netzwerklatenz
- MPI-Reduktionen
- Jitter
- Threading-Probleme

#### Monolith:

- keine Varianz
- keine Jitter
- keine dynamischen Scheduler
- keine Caches

Ergebnis:

    Benchmarking wird trivial.

### 30.11 Fazit

Benchmarking im KORA-System ist kein empirischer Vorgang, sondern Teil des strukturellen Modells. 
Durch deterministische Scheduling Trees, feste DMA-Fenster, stabile Energieprofile und konstante Takte wird Performance:

- voraussagbar,
- mathematisch beschreibbar,
- wiederholbar,
- wissenschaftlich nachvollziehbar.

KORA definiert damit ein neues Paradigma: 
Rechnen ohne Varianz.

---

## 31. Formal Performance & Energy Modeling 
(Mathematische Modelle für Zeit, Energie, Skalierung)

Klassische HPC-Performance basiert auf empirischer Messung, da Systeme stochastisch sind. 
Bei KORA dagegen ist Performance eine mathematische Eigenschaft der Architektur und der Scheduling Trees. 
Dieses Kapitel beschreibt das formale Modell für:

- Zeit,
- Energie,
- Skalierung,
- Speicherzugriffe,
- Kommunikationskosten,
- Computational Throughput.

Das Modell erlaubt Vorhersagen ohne empirische Messfehler.

### 31.1 Grundprinzip: deterministische Pfade → deterministische Modelle

Im Monolithen existieren keine unsicheren Latenzen. 
Daher ergibt sich:

    Performance = Summe deterministischer Zeitfenster
    Energie = Leistung × deterministische Zeit
    Skalierung = Replikation deterministischer Module

Alle drei Größen können vorab exakt berechnet werden.

### 31.2 Zeitmodell (T-Model)

Zeit setzt sich zusammen aus:

- Compute-Zeit
- DMA-Zeit
- Fabric-Zeit
- Reduktionszeit
- Phasenverwaltung

Formale Gleichung:

    T_total = Σ T_phase_i

Jede Phase wird bestimmt als:

    T_phase = Zyklen_phase / f_clock

Da f_clock konstant ist, wird Zeit linear.

Beispiel:

    Compute Block 32×32 = 1428 cycles
    DMA In Block = 102 cycles
    DMA Out Block = 88 cycles

    T_total = (1428 + 102 + 88) cycles / 1.5e9

Es gibt keine Varianz.

### 31.3 Energie-Modell (E-Model)

Energie ist trivial:

    E_total = P_constant × T_total

Da der Monolith keine Boost-Mechanismen kennt:

    P_constant ≈ 1.1 kW (typisch)

Beispiel:

    T_total = 80 ms
    P = 1.12 kW
    E = 89.6 Joule

Der Energiebedarf ist reproduzierbar.

### 31.4 Kommunikationsmodell (C-Model)

Kommunikationskosten entstehen durch:

- DMA-Fenster
- Fabric-Übertragung
- possível Cross-Monolith Transfers

Formale Gleichung:

    C_total = Σ (size_block / bandwidth_slot + L_slot)

Da Bandbreite und Latenz konstant sind:

    bandwidth_slot = konstant
    L_slot = konstant

Beispiel:

    Block = 1 MB
    Bandbreite = 128 GB/s
    L_slot = 8 cycles

    C = 1e6 / 128e9 + 8 cycles

Keine Paketverluste, keine Jitter, keine variable Routen.

### 31.5 Memory-Modell (M-Model)

Memory-Zugriffe haben fixe Kosten:

    M_access = L_bank

Jede Bank besitzt konstante Latenz, z. B.:

    L_bank = 3 cycles

Ein Compute-Block mit N Zugriffen benötigt:

    M_total = N × L_bank

Da N deterministisch im Scheduling Tree steht, ist auch M_total deterministisch.

### 31.6 Compute-Modell (P-Model)

Rechenleistung jeder Tile-Gruppe ist:

    P_tile = ops_per_cycle × f_clock

Beispiel:

    ops_per_cycle = 64
    f_clock = 1.5 GHz
    → 96 Gops/s pro Tile-Gruppe

Ein Compute-Block wird berechnet als:

    T_compute = ops_total / P_total

Da alle Werte fix sind, ist P-Model starr und vorhersehbar.

### 31.7 Skalierungsmodell (S-Model)

Skalierung erfolgt über Replikation, nicht Verteilung:

    T_N = T_1 / N

Für viele Workloads gilt nahezu perfekte lineare Skalierung:

- kein Netzwerkjitter
- keine Variabilität
- keine Scheduling-Kosten
- keine MPI-Overheads
- keine Thread-Rennen

Formale Gleichung:

    S(N) = N × T_1 / T_N

Für deterministische Systeme ist:

    S(N) = 1 (perfekt)

Bis Ressourcen (z. B. Speicherbandbreite) limitieren.

### 31.8 Zusammengesetztes Modell (Unified Deterministic Model)

Die formale Gesamtkonstruktion:

    T_total = Σ_i (Compute_i + DMA_i + Fabric_i + Reduction_i)
    E_total = P × T_total
    C_total = Σ DMA / bandwidth_slot
    M_total = Σ Accesses × L_bank
    S(N) = (T_1 / T_N)

Dieses Modell erlaubt:

- Vorababschätzung von Ausführungszeit
- Maschinenkonfiguration
- Energieplanung
- Rack-Planung
- Skalierungsprognosen
- wissenschaftliche Validierung

### 31.9 Beispiel: vollständige Blockrechnung

Gegeben:

    Compute: 1428 cycles
    DMA-In: 102 cycles
    DMA-Out: 88 cycles
    Reduktion: 64 cycles

    f_clock = 1.5 GHz
    P = 1.12 kW

Berechnung:

    T_total_cycles = 1682
    T_total = 1682 / 1.5e9 = 1.121e-6 s
    E_total = 1.12e3 × 1.121e-6 = 1.25e-3 Joule

Perfekt reproduzierbar.

### 31.10 Wissenschaftlicher Vorteil

Das deterministische Performance-Modell bietet:

- keine statistische Messunsicherheit
- keine Benchmark-Variabilität
- mathematische Belegbarkeit
- klare Vergleichsbasis mit GPUs / HPC
- prüfbare Energieangaben
- nachvollziehbare Skalierungsdiagramme
- robuste Veröffentlichungsergebnisse

### 31.11 Fazit

Das formale Performance- und Energiemodell von KORA ist ein Kernbestandteil der Architektur. 
Es ersetzt empirische Messungen durch mathematische Berechnung und ist damit:

- präzise,
- deterministisch,
- transparent,
- wiederholbar,
- skalierbar,
- wissenschaftlich wertvoll.

Durch dieses Modell wird KORA zu einer strukturell vorhersagbaren Rechenplattform.

---

## 32. Scientific Validation & Numerical Stability 
(wissenschaftliche Verifikation, numerische Konsistenz)

Der Monolith ist eine deterministische Rechenarchitektur. 
Für wissenschaftliche Nutzung reicht jedoch reine Deterministik nicht aus. 
Wissenschaft verlangt:

- numerische Stabilität,
- Transparenz,
- Erklärbarkeit,
- Vergleichbarkeit mit Referenzsystemen,
- kontrollierte Fehlergrenzen.

Dieses Kapitel definiert, wie wissenschaftliche Validierung im KORA-System erfolgt.

### 32.1 Grundprinzip: wissenschaftliche Reproduzierbarkeit

Wissenschaftliche Reproduzierbarkeit bedeutet:

    Bei gleichem Modell → gleiche numerische Ergebnisse → auf jeder Instanz → zu jedem Zeitpunkt.

Dazu gehören:

- deterministische Ausführung (Hardware),
- deterministische Scheduling Trees (Compiler),
- deterministische Speicherpfade (Memory Model),
- deterministische Kommunikation (Fabric).

Damit ist KORA die erste HPC-/KI-Architektur, deren wissenschaftliche Ergebnisse völlig frei von:

- Thread-Jitter,
- Cache-Misses,
- Race Conditions,
- Netzwerkvolatilität,
- Scheduling-Varianz

sind.

### 32.2 Floating-Point-Konsistenz

KORA nutzt klassische Floating-Point-Einheiten (z. B. IEEE 754), jedoch:

- ohne dynamische Taktänderungen,
- ohne unterschiedliche Ausführungspfade,
- ohne FMA-Swap-Variabilität,
- ohne spekulative Ausführung.

Damit gilt:

    Alle FP-Operationen werden in exakt gleicher Reihenfolge ausgeführt.

Floating-Point-Kohärenz umfasst:

- Reihenfolge
- Gruppierung
- Pipeline-Tiefe
- Tile-Zuordnung
- Registerzüge

Alle Faktoren sind strukturell fix.

### 32.3 Numerische Stabilität gegenüber Referenzsystemen

Zur wissenschaftlichen Validierung gehört der Vergleich mit einer Referenz:

- CPU-Doppelpräzisionsmodell (64-bit)
- symbolische Referenzen (Mathematica, Maple)
- hochpräzise Rechenmodelle (Arb, MPFR)

Ein KORA-Modell muss erfüllen:

    Abweichung ≤ definierte numerische Toleranz des Modells

Für PDEs typischerweise:

    L2-Error ≤ 1e-12 … 1e-6 (problemabhängig)

Für Deep Learning:

    Metriken stabil über alle Trainingsläufe hinweg

Für Big Data:

    identische Hashes, Checksummen oder Aggregationen

### 32.4 Referenzläufe („Golden Runs“)

Jedes wissenschaftliche Projekt kann einen Golden Run definieren:

    Golden Run = Referenzlauf eines Modells, archiviert mit TSF, Parametern und Eingabedaten.

Ein Golden Run enthält:

- TSF-Programm
- Modellparameter
- Konfigurationsdatei
- Eingabedaten
- erwartete Ergebnisse
- erwartete Zykluszahlen
- Logging-Daten

Ein Golden Run dient als:

- Regressionstest
- Vergleichsbasis
- Identitätsprüfung

### 32.5 Cross-System Validierung

Da KORA-Monolithe identisch deterministisch laufen, kann ein Modell auf beliebigen Geräten laufen:

    M1 → M8 → MCluster

Überprüfung:

    Ergebnis(M1) == Ergebnis(MCluster)

Da keine Nichtdeterministik existiert, gilt:

    Unterschiede = Fehler, nicht Varianz.

Dies ist der entscheidende wissenschaftliche Vorteil.

### 32.6 Numerischer Fehlerraum

Jedes numerische Modell besitzt inhärente Fehler:

- Diskretisierungsfehler
- Modellierungsfehler
- Floating-Point-Rundung

KORA eliminiert:

- Scheduling-Fehler
- Race-bedingte Variabilität
- Hardwarevariabilität
- nichtdeterministische Reihenfolgen

Der Fehlerraum wird damit auf echte numerische Fehler reduziert.

### 32.7 Stabilität für PDE-/CFD-Modelle

Wichtig bei:

- Navier-Stokes-Gleichungen
- Wärmeleitung
- Transportgleichungen
- elliptische PDEs
- hyperbolische PDEs

KORA garantiert:

- deterministische Stencil-Anwendung
- deterministische Iterationsreihenfolge
- deterministische Reduktionen
- deterministische Ghost-Layer-Kommunikation

Beispiel (Einrückung):

    u_next[i,j,k] hängt nur von festen Nachbarn in exakt definierter Reihenfolge ab.

### 32.8 Stabilität für KI-Modelle (Deep Learning)

Training ist extrem sensitiv für:

- Rechenreihenfolge
- Reduktionspfade
- Floating-Point-Nuancen

GPUs liefern oft leicht unterschiedliche Ergebnisse in Trainingsläufen:

- wegen Atomics,
- wegen Scheduling,
- wegen Race Conditions,
- wegen variabler Summationsreihenfolge.

KORA eliminiert dies vollständig.

Ergebnis:

    exakt identische Loss-Kurven
    exakt identische Gradienten
    exakt identische Modellgewichte

Für KI-Forschung ist dies bahnbrechend.

### 32.9 Stabilität für Big-Data-Workloads

Hashing, Aggregationen, Sortierungen, Statistiken — all diese Vorgänge hängen von deterministischen Datenflüssen ab. 

KORA garantiert:

- identische Partitionierung
- identische Blockreihenfolge
- identische Aggregationspfade

Beispiel:

    reduce(sum(x[i])) ist in Scheduling Tree strikt definiert.

### 32.10 Metrologisches Vertrauensmodell

Wissenschaft verlangt nicht nur korrekte Ergebnisse, sondern überprüfbare:

- Eingabedaten
- Parametermengen
- Ausführungsprofile
- zeitliche Sequenzen
- numerische Eigenschaften

KORA liefert:

    vollständige Metadaten pro Run:
        - TSF
        - Modellparameter
        - Zyklusprofile
        - Temperaturen
        - Energieverbrauch
        - I/O-Fenster

Dies ist die Grundlage für verifizierbare Wissenschaft.

### 32.11 Vergleichbarkeit zwischen Architekturen

Ein zentrales wissenschaftliches Ziel:

    Ergebnisse von KORA müssen mit CPUs/GPUs vergleichbar sein.

Daher definiert KORA:

- identische Floating-Point-Profile
- deterministische Summationsreihenfolgen
- wohldefinierte numerische Ausführungsreihenfolge
- optional KORA-Numerikprofile (Profil A: IEEE 754, Profil B: Mixed Precision, Profil C: SoftFP)

Dies ermöglicht exakte Vergleiche.

### 32.12 Fazit

KORA schafft ein wissenschaftliches Validierungsmodell, das keine Blackbox-Effekte von klassischer HPC-Hardware besitzt. 
Durch deterministische Ausführung, stabile Floating-Point-Reihenfolgen, Golden Runs und vollständige Metadaten entsteht ein System, das:

- numerisch konsistent,
- wissenschaftlich überprüfbar,
- transparent,
- reproduzierbar,
- verlässlich

ist – eine neue Qualität für wissenschaftliches Rechnen.

---

## 33. Simulation & Emulation Framework 
(Modelle, Software-Simulator, Validierungsmodi, TSF-Emulator)

Da KORA eine deterministische Architektur ist, müssen sämtliche Modelle, Scheduling Trees, 
DMA-Fenster und TSF-Programme auch ohne reale Hardware ausführbar und analysierbar sein. 
Für wissenschaftliche, formale und entwicklungsorientierte Zwecke existiert ein vollständiges 
Simulations- und Emulationsframework, das die gesamte Architektur abbildet.

Dieses Kapitel beschreibt:

- Software-Simulation des Monolithen
- Emulation von TSF-Programmen
- Modellierung der Scheduling Trees
- Validierungsmodi
- Performance- und Energieprognose
- Multi-Monolith-Simulation

### 33.1 Grundprinzip: perfekte Software-Nachbildung

Der Monolith ist deterministisch. 
Daher kann der gesamte Ablauf 1:1 in Software reproduziert werden:

- gleiche Zykluszahlen
- gleiche DMA-Sequenzen
- gleiche Memorybank-Zugriffe
- gleiche Scheduling-Pfade
- gleiche Ergebnisse

Damit wird die Simulation:

    eine „logische Hardware“, die zu 100 % deterministisch ist.

### 33.2 Simulator-Komponenten

Der Simulator besteht aus folgenden Schichten:

1. **TSF Parser**
    - liest TSF-Programme ein
    - prüft Struktur

2. **Scheduling Tree Engine**
    - führt Phasen sequentiell aus
    - simuliert Abhängigkeiten
    - berechnet Zyklusanzahl

3. **Memorybank Simulator**
    - modelliert Bankzugriffe
    - modelliert L_bank Latenzen
    - prüft Konsistenz von Access Patterns

4. **DMA Window Simulator**
    - simuliert DMA-Slots
    - prüft Zeitfenster
    - modelliert Bandbreiten

5. **Tile Compute Engine**
    - führt Operationen in deterministischer Reihenfolge aus
    - simuliert Rechenzeit pro Phase

6. **I/O-Model**
    - modelliert Ein- und Ausgabefenster
    - validiert Datenblöcke

Der Simulator bildet keine physikalischen Effekte nach (Hitze, Spannung, EM), 
sondern ausschließlich strukturelle und zeitliche Abläufe.

### 33.3 Emulationsmodus

Der Emulator führt TSF Programme so aus, als wäre er der Monolith selbst:

- alle Phasen
- alle Scheduling Trees
- alle DMA-Fenster
- alle Reduktionen
- alle Memorypfade

Der Emulator garantiert:

    Jede Ausgabe ist identisch zur Hardware.

Er dient für:

- Modellvalidierung
- wissenschaftliche Testläufe
- Softwareentwicklung (HAPI/SCI)
- Analyse neuer Monolith-Varianten
- Regressionstests

### 33.4 Numerischer Modus

Für wissenschaftliche Modelle existiert ein numerischer Modus:

- Floating-Point-Einheiten werden exakt simuliert (IEEE 754)
- Reihenfolge der Operationen entspricht H/W
- Reduktionspfade sind identisch
- Tile-Mapping ist identisch

Damit können:

- PDEs,
- KI-Trainingsmodelle,
- Big-Data-Aggregationen

vollständig in Software getestet werden.

### 33.5 Performance-Prognose

Da alle Zyklen deterministisch sind, kann der Simulator Zeit berechnen:

    T_total = Σ_i cycles_i / f_clock

Beispiel:

    Phase 0:  42 cycles
    Phase 1: 1284 cycles
    Phase 2:  76 cycles

    T = 1402 cycles / 1.5 GHz

Es gibt keine Abweichungen zwischen Simulation und Hardware.

### 33.6 Energie-Prognose

Der Simulator berechnet:

    E = P_constant × T_total

Dabei ist P_constant ein Parameter der Architektur:

    P_constant = 1.12 kW (Monolith M3)

So können:

- Forschungsgruppen
- Rechenzentren
- Entwickler

den Energiebedarf vorab exakt abschätzen.

### 33.7 Multi-Monolith-Simulation

Die Simulation kann beliebig viele Monolithen umfassen:

- M2 (Dual)
- M4 (Quad)
- M8–M16 (Rack)
- MCluster

Wichtig:

- Kommunikationsfenster werden exakt simuliert
- TDM-Slots werden identisch repliziert
- Cross-Rack Pfade werden nachgebildet

Simulationsergebnisse sind identisch zur Hardware:

    T_N = T_1 / N
    E_N = E_1 × N

bis Bandbreitengrenzen erreicht werden.

### 33.8 Validierungsmodi

Es existieren drei Modi:

#### (A) Structural Validation

- überprüft Scheduling Trees
- überprüft Memorypfade
- überprüft DMA-Kollisionen
- überprüft TSF-Struktur

#### (B) Numerical Validation

- prüft Floating-Point-Operationen
- prüft Modellkonsistenz
- vergleicht mit Golden Runs

#### (C) Scientific Validation

- prüft wissenschaftliche Ergebnisse
- vergleicht CFD/KI/Big-Data Modelle
- misst numerische Fehler

### 33.9 Simulationsumgebung für Entwickler

Für HAPI/SCI-Entwickler existiert ein Entwicklungsmodus:

- interaktive Ausführung
- Inspection-Tools
- Visualisierung der Scheduling Trees
- Debug von Tile-Pipelines
- debug von Memory-Flows
- Schritt-für-Schritt-Iteration

Beispiel:

    show_tree()
    show_dma_windows()
    inspect_tile(23)
    step_phase(7)

Damit können Modelle ohne Hardware entwickelt werden.

### 33.10 Integration in Rechenzentren

Rechenzentren können vorab testen:

- Rack-Auslastung
- Cross-Rack Kommunikation
- Energiebedarf
- Kühlbedarf
- Performanceprofil

Wissenschaftler können:

- Parameterstudien durchführen
- Modelle optimieren
- Fehler analysieren

ohne dass Hardware reserviert werden muss.

### 33.11 Golden-Run-Reproduktion

Ein Golden Run kann vollständig in der Simulation reproduziert werden:

    Ergebnisse sind bit-identisch

Dies ist einzigartig in der HPC-Welt und unterstützt:

- Publikationskontrolle
- Peer Review
- wissenschaftliche Auditierbarkeit

### 33.12 Simulation zukünftiger KORA-Versionen

Der Simulator erlaubt:

- Variation von Tile-Anzahl
- Variation von Bank-Anzahl
- Variation von TDM-Strukturen
- Variation der Fabric-Latenzen

Damit kann man:

- M3 → M4 → M5 generativ weiterentwickeln
- Zukunftsmodelle testen
- Architekturvarianten vergleichen

Vor Hardwarebau.

### 33.13 Fazit

Das Simulation- und Emulationsframework ist unverzichtbar für Wissenschaft, Entwicklung und Architekturplanung. 
Da KORA deterministisch ist, kann die Simulation:

- vollständige Hardware-Reproduktion bieten,
- Performance exakt prognostizieren,
- numerische Ergebnisse prüfen,
- Skalierungseigenschaften analysieren,
- zukünftige Architekturvarianten simulieren.

KORA-Simulation ist kein „Benchmark-Simulator“, sondern ein vollständiger digitaler Zwilling des Monolithen.

---

## 34. Software Ecosystem Integration 
(Python, C/C++, Fortran, HPC, KI, Workflows)

Der Monolith ist eine deterministische Hardware, die über das Structural Compute Interface (SCI) gesteuert wird. 
Damit Wissenschaftler, Ingenieure und Entwickler KORA produktiv nutzen können, muss die Architektur in existierende Software-Ökosysteme eingebunden werden.

Dieses Kapitel beschreibt die Interoperabilitätsschichten und die Integration in:

- Python
- C/C++
- Fortran
- HPC-Frameworks
- KI-Frameworks
- Big-Data-Frameworks
- Workflow-Systeme
- Dateisysteme
- Container-Umgebungen

### 34.1 Grundprinzip: KORA integriert sich, ersetzt aber nichts erzwingend

KORA ist kein „neues Universum“. 
Es funktioniert als:

    deterministische Ausführungseinheit innerhalb bestehender Ökosysteme

und nicht als Ersatz für wissenschaftliche Software.

Die Interoperabilität wird über SCI-Schnittstellen und Backend-Adapter erreicht.

### 34.2 Integration in Python

Python ist das wichtigste Ökosystem der modernen wissenschaftlichen Arbeit. 
KORA bietet:

#### 34.2.1 Python-Frontend (kora-python)

Ein Python-Paket stellt bereit:

- Tensor-Objekte
- Field-Objekte
- Operatoren
- CFD-PDE-Operatoren
- Matrix-Operatoren
- Stencil-Systeme

Beispiele (Einrückung):

    import kora as K
    u = K.field((1024, 1024))
    u_next = K.stencil(u, K.Laplace)

#### 34.2.2 Backend-Integration

Python fungiert als:

- Modellierungsplattform,
- Parameterquelle,
- TSF-Generator,
- Data-Management-Interface.

Die Ausführung findet ausschließlich auf dem Monolithen statt.

### 34.3 Integration in C/C++

C/C++ ist in HPC weit verbreitet. 
KORA stellt hierfür bereit:

- eine C-API
- einen Header-only Zwischenlayer
- TSF-Erzeugung über SCI-Bibliotheken

Rolle:

    C/C++ = High-Performance-Modellierung, nicht Ausführung

KORA führt **keinen** C/C++ Code aus — nur die strukturierte Modellbeschreibung wird genutzt.

### 34.4 Integration in Fortran

Fortran ist nach wie vor dominant in:

- Klimamodellen
- Strömungssimulation
- numerischer Mathematik

KORA bietet Fortran-Wrappers:

    call kora_generate_tsf(model, params, tsf_file)

Fortran-Modelle werden deterministisch partitioniert, aber nicht direkt ausgeführt.

### 34.5 Integration in HPC-Frameworks

Viele klassische HPC-Frameworks können über Backends an KORA angebunden werden:

#### 34.5.1 MPI

MPI bleibt auf dem Host, nicht im Monolithen.

Integration:

- Host steuert TSF-Jobs
- Monolith berechnet deterministische Blöcke
- MPI kommuniziert zwischen Hosts

#### 34.5.2 OpenFOAM

Stencil-Operationen werden in KORA-Blöcke übersetzt.

#### 34.5.3 PETSc

Lineare Algebra → deterministische GEMM/SpMV-Blöcke.

#### 34.5.4 Trilinos

Numerische Solver → blockweise deterministische Ausführung.

### 34.6 Integration in KI-Frameworks

#### 34.6.1 PyTorch

KORA fungiert als Backend:

    model.to("kora")

Alle Tensor-Operationen laufen deterministisch.

#### 34.6.2 TensorFlow / JAX

Über XLA-ähnliche Kompatibilität (SCI → TSF).

#### 34.6.3 HuggingFace Ecosystem

KORA führt Training und Inferenz deterministisch aus:

- BERT
- GPT-ähnliche Modelle
- Vision Transformer
- Diffusion Models

### 34.7 Big-Data Frameworks

#### 34.7.1 Apache Arrow

Blockorientierter Speicher → ideal für deterministische Chunks.

#### 34.7.2 Spark / Dask

KORA wird Backend für Compute-intensive Steps.

#### 34.7.3 Polars

Columnar Data → deterministische Partitionierung.

### 34.8 Workflow-Systeme

KORA integriert sich in existierende Systeme:

- Airflow
- Snakemake
- Nextflow
- Luigi

Der Host übernimmt Workflow-Ausführung:

    Workflow → TSF-Generation → Monolith-Run → Ergebnisse → Workflow

### 34.9 Container / Virtualisierung

KORA selbst läuft nicht in Containern. 
Der Host allerdings ja:

- Docker
- Singularity/Apptainer
- Kubernetes

Typische Architektur:

    Kubernetes → Host → Monolith

Der Monolith bleibt containerfrei → deterministische Hardware.

### 34.10 Filesysteme & Storage

KORA nutzt:

- POSIX Storage über Hosts
- Object Storage
- HPC Filesysteme (Lustre, GPFS)

Der Monolith sieht Blöcke, der Host sieht Dateien.

### 34.11 Warum dieses Integrationsmodell ideal ist

- KORA ersetzt keine Software
- Wissenschaftler behalten ihre Tools
- Python bleibt Nutzeroberfläche
- C/C++/Fortran bleiben Modellsprachen
- KI-Frameworks bleiben unverändert

KORA wird:

    deterministisches Beschleunigungsmodul für alles, was rechenintensiv ist.

### 34.12 Fazit

Die Integration in bestehende Software-Ökosysteme ist ein zentraler Baustein von KORA. 
SCI dient dabei als Brücke zwischen hoher Modellierungsebene und deterministischer Ausführung. 
KORA bleibt offen, kompatibel, erweiterbar und integriert sich in:

- moderne KI,
- klassische HPC,
- wissenschaftliche Simulation,
- Big-Data-Workloads,
- Workflow-Systeme.

Damit wird KORA nicht als Parallelwelt verstanden, sondern als 
deterministische Weiterführung der etablierten wissenschaftlichen Softwarelandschaft.

---

## 35. Interoperability & External Interfaces 
(Formate, Datenmodelle, Austauschprozesse)

KORA ist eine deterministische Compute-Architektur, die sich in existierende wissenschaftliche, industrielle und datenintensive Ökosysteme integrieren muss. 
Interoperabilität bedeutet dabei nicht, dynamische Prozesse in den Monolithen einzuschleusen, 
sondern klar definierte Austauschwege zwischen der deterministischen und der nichtdeterministischen Außenwelt bereitzustellen.

Dieses Kapitel beschreibt:

- Datenformate,
- Austauschmodelle,
- Orchestrierungsprozesse,
- Plattformanbindungen,
- Host-Interaktionen,
- externe Schnittstellen.

Es bildet die Brücke zwischen KORA und der realen Softwarewelt.

### 35.1 Grundprinzip: deterministische Innenwelt, flexible Außenwelt

Der Monolith ist vollständig deterministisch. 
Die Außenwelt jedoch:

- OS,
- Filesysteme,
- Cloud-Dienste,
- Workflowsysteme,
- Scheduling-Systeme,
- wissenschaftliche Tools,

ist heterogen und oft stochastisch.

KORA kapselt den Monolithen in einen **klar definierten Interoperabilitätsrahmen**, 
um beide Welten effizient und sicher zu verbinden.

### 35.2 Datenformate

KORA unterstützt drei Klassen von Datenformaten:

#### (A) Blockformate (Native)

Dies sind die Formate, die der Monolith direkt liest:

    KORA-Block-1MB
    KORA-Block-2MB
    KORA-Block-4MB

Eigenschaften:

- fester Offset,
- fester Blockumfang,
- keine Metadaten,
- komplett sequentiell.

#### (B) Containerformate (Host-Seitig)

Der Host übersetzt externe Datenformate in Blockformate:

- NumPy `.npy`
- Arrow `.feather`
- HDF5
- NetCDF
- Parquet
- Torch `.pt`

#### (C) wissenschaftliche High-Level-Formate

- VTK für CFD
- XDMF / HDF5 für Simulationen
- ONNX für KI
- CSV / TSV für experimentelle Daten

Der Host übernimmt stets die Umwandlung.

### 35.3 Datenbewegung zwischen Host und Monolith

Der Austausch erfolgt ausschließlich über **deterministische DMA-Fenster**:

    Input:  Host → DMA-In → Memorybanks
    Output: Memorybanks → DMA-Out → Host

Ein DMA-Fenster besitzt:

- Block-ID,
- Blockgröße,
- Start-Slot,
- End-Slot,
- Ziel-Bank.

Beispiel:

    Input Block 23:
        host_offset: 184 MB
        size: 2 MB
        phase: 0
        slot: 4

Jede Datenbewegung ist planbar und deterministisch.

### 35.4 Externe Speicherintegration

Die Außenwelt nutzt:

- NVMe
- Object Storage (S3, MinIO, Ceph)
- POSIX Filesysteme
- HPC-Dateisysteme (Lustre, GPFS)
- Cloud-Filesysteme

Der Host liest die Daten und schneidet sie in deterministische KORA-Blöcke.

Der Monolith selbst sieht nur Blocknummern.

### 35.5 Integration in externe Rechenumgebungen

KORA wird über den Host in viele Systeme eingebunden:

#### (A) HPC Batch Systeme

- SLURM
- PBS
- LSF

Typische Pipeline:

    sbatch → Host → TSF Deployment → Monolith → Ergebnisse → Host → SLURM

#### (B) Cloud-Plattformen

- AWS
- Azure
- GCP

Cloud-Systeme orchestrieren nur den Host, nicht die Hardware.

#### (C) Workflow-Systeme

- Snakemake
- Airflow
- Nextflow

Jeder Workflow-Schritt:

    erzeugt TSF,
    lädt TSF,
    führt deterministischen Run aus,
    extrahiert Ergebnisse.

### 35.6 Interoperabilität zu ML-Ökosystemen

#### 35.6.1 PyTorch

Über ein KORA-Backend:

    model = model.to("kora")

KORA führt deterministische MatMul/Conv/Reduce-Blöcke aus.

#### 35.6.2 TensorFlow / JAX

Über SCI→TSF-Compilerpfad.

#### 35.6.3 ONNX

ONNX-Modelle werden in HAPI-Strukturen übersetzt.

### 35.7 Interoperabilität zu wissenschaftlichen Simulationen

#### 35.7.1 CFD / PDE

- OpenFOAM
- Fenics
- Firedrake
- Deal.II
- PETSc

Konvertierung erfolgt über:

    PDE Modell → HAPI → TSF → Monolith

#### 35.7.2 Materialwissenschaft

Atomistische Simulationen (LAMMPS style):

    Neighborhood Lists → deterministische Partitionierung → TSF

#### 35.7.3 Geophysik

- seismische Inversion
- Wellenausbreitung
- Navier-Stokes

Deterministische Stencils → ideale Einsatzgebiete.

### 35.8 Integration in Data Engineering Workflows

#### 35.8.1 Arrow / Parquet

Standard für Big-Data:

- Der Host zerlegt Arrow-Streams in KORA-Blöcke
- Der Monolith verarbeitet deterministische Partitionen

#### 35.8.2 Spark / Dask

Compute-intensive Steps laufen auf dem Monolithen.

#### 35.8.3 Polars / DuckDB

Analytische Query-Engines → deterministische Filter-/Aggregate-Blöcke.

### 35.9 Cross-Monolith Interoperabilität

Monolithen kommunizieren über:

- deterministische RDMA-Fenster,
- TDM-Meta-Fabric,
- strukturierte Reduktionspfade.

Der Host koordiniert:

    TSF-Verteilung,
    Startsignale,
    Ausgabesammeln.

Es existieren keine Peer-Verbindungen im klassischen Sinne.

### 35.10 Datenkonsistenz und Validierung

Der Host validiert:

- Struktur,
- Dateiformate,
- Checksummen,
- Blockgrößen,
- Ausführungsparameter,
- numerische Profile.

Die deterministische Innenwelt des Monolithen erwartet:

    konsistente, korrekt definierte Eingabeblöcke.

### 35.11 Standardisierte Interoperabilitätsprofile

KORA definiert Integrationsprofile:

#### Profil A: Wissenschaft

- Python, HDF5, VTK, NetCDF
- CFD, PDE, ML, Numerik

#### Profil B: Industrie

- Arrow, Parquet, SQL-Subsysteme
- Big-Data-Jobs

#### Profil C: Cloud & Workflow

- Kubernetes, Airflow, Snakemake
- Object Storage

Diese Profile geben vor:

- Blockgrößen,
- I/O-Layouts,
- Empfohlene Parameter,
- Validierungsstufen.

### 35.12 Fazit

KORA integriert sich nicht isoliert, sondern als deterministisches Rechenmodul in die bestehende wissenschaftliche, industrielle und datengetriebene Softwarelandschaft. 
Durch klare Schnittstellen, standardisierte Blockformate, TSF-Modelle und Host-gesteuerte Workflows entsteht ein System, das:

- universell nutzbar,
- robust,
- kompatibel,
- effizient,
- workflow-tauglich

ist — ohne seine deterministische Innenstruktur zu kompromittieren.

---

## 36. Cluster Communication & Deterministic Multi-Compute 
(Cross-Monolith Fabric)

KORA besteht nicht nur aus einzelnen Monolithen. 
Ein Monolith bildet die elementare Recheneinheit, doch die Architektur ist so ausgelegt, dass mehrere Monolithen deterministisch zusammenarbeiten können. 
Dieses Kapitel beschreibt die Struktur, Funktionsweise und Garantien des Multi-Compute-Modells.

Deterministische Multi-Compute bedeutet:

- deterministische Datenwege,
- deterministische Zeitslots,
- deterministische Reduktionen,
- deterministische Partitionierung,
- deterministische Ausführung über mehrere Module hinweg.

### 36.1 Grundprinzip: deterministische Skalierung

Anders als klassische HPC-Cluster, die auf dynamische Netzwerke setzen (Ethernet, InfiniBand, MPI), verwendet KORA eine feste, nichtdynamische Kommunikationsstruktur:

    Cross-Monolith Fabric (CMF)

Die CMF ist:

- slot-basiert,
- latenzstabil,
- jitterfrei,
- paketverlustfrei,
- kollisionsfrei.

Jeder Kommunikationsschritt ist vorab planbar.

### 36.2 Architektur der Cross-Monolith Fabric (CMF)

Die CMF besteht aus:

- festen physikalischen Links
- deterministischen TDM-Slots
- festen Pfaden
- Sequenzierungsregeln
- Reduktionsbäumen

Keine Routing-Tabellen, kein Packet-Switching, kein Jitter.

Die Fabric besteht aus:

1. **Direct Links** (Monolith → Monolith)
2. **Backplane-Segmente**
3. **Rack-Level Fabric**
4. **Cluster-Level Deterministic Exchange Layer**

Alle Pfade sind statisch.

### 36.3 TDM-Slotmodell

Kommunikation erfolgt über:

    TDM Slot (t) = vorgegebener Zeitabschnitt für einen Link

Ein Link besitzt:

- feste Bandbreite (z. B. 256 GB/s)
- feste Latenz (z. B. 2–3 Zyklen)
- feste Reihenfolge

Beispiel:

    Slot 7: M1 → M2, Block 23
    Slot 8: M2 → M3, Block 5
    Slot 9: M3 → M1, Reduktion

Alle Slots sind im TSF hinterlegt.

### 36.4 Cluster Topologien

KORA unterstützt drei Topologien:

#### (A) Lineare Topologie (M2)

    M1 ←→ M2

#### (B) Ring-Topologie (M4, M8)

    M1 → M2 → M3 → M4 → M1

#### (C) Baumtopologie (MCluster)

    Root → Branches → Leaves

Alle Topologien sind deterministisch.

### 36.5 Datenpartitionierung

Daten werden strikt partitioniert:

    Partition 0 → M1
    Partition 1 → M2
    Partition 2 → M3
    Partition 3 → M4
    ...

Beispiele für Partitionierungsmodelle:

- Block-Partitionierung
- räumliche Partitionierung (CFD)
- Layer-Partitionierung (KI)
- Chunk-Partitionierung (Big Data)

Der Monolith arbeitet nur an seiner Partition.

### 36.6 Deterministische Reduktionsbäume

Reduktionen sind ein Kernbestandteil:

- Summen
- Normen
- Mittelwerte
- Gradienten
- Aggregationen
- Datenfusionen

Beispiel eines festen Reduktionsbaums:

    M1 → M2
    M3 → M4
    M2 → M4
    M4 → Host

Jeder Schritt:

- hat feste Slots,
- feste Reihenfolge,
- feste Blockgrößen.

### 36.7 Multi-Compute TSF

Ein TSF für mehrere Monolithe enthält:

- Partitionstabellen
- Kommunikationsfenster
- Reduktionspfade
- Cross-Fabric-Zeitfenster
- globale Scheduling Trees

Beispiel für Slotdefinition (Einrückung):

    CMF:
        - slot: 12
          src: M1
          dst: M2
          block: 14

    Reduction:
        - slot: 37
          src: M2
          dst: M4

Alles ist vorab definiert, nichts dynamisch.

### 36.8 Multi-Compute Ausführungsmodell

Mehrere Monolithe arbeiten streng phasenparallel:

    Phase 0:
        M1, M2, M3, M4: lokale Daten laden
    Phase 1:
        lokale Berechnung
    Phase 2:
        Reduktion nach Baumstruktur
    Phase 3:
        Austausch von Ghost-Daten
    Phase 4:
        Fortsetzung der Berechnung

Jeder Monolith weiß:

- wann er sendet,
- wann er empfängt,
- welche Pfade aktiv sind.

### 36.9 Ghost-Layer Austausch (CFD)

Bei CFD-basierten Modellen werden Ghost Layers deterministisch übertragen:

    Ghost(X) @ Slot t = f(Partition Layout)

Da keine Latenzschwankungen existieren:

- keine Instabilität,
- keine halbleeren Ghost-Daten,
- kein Jitter,
- kein MPI-Waiting.

### 36.10 Multi-Compute für KI-Modelle

Mehrere Monolithe können:

#### (A) Datenparallel arbeiten

    N Samples → N Partitionen

#### (B) Modellparallel arbeiten

    Layer 0–3 → M1
    Layer 4–7 → M2
    Layer 8–11 → M3

#### (C) Pipelineparallel arbeiten

    Forward @ M1 → M2 → M3 → M4

Alles deterministisch.

### 36.11 Multi-Compute für Big Data

Big-Data Workloads profitieren besonders:

- deterministische Partitionierung
- deterministische Map/Reduce-Blöcke
- deterministische Aggregationen
- keine Stragglers
- keine Shuffle-Jitter

KORA ersetzt Shuffle durch statische Reduktionspfade.

### 36.12 Multi-Compute Performance & Skalierung

Da Kommunikation deterministisch ist:

- perfekte Linearskalierung bis zu Bandbreitengrenzen
- keine Kommunikationsoverheads durch Variabilität
- vorhersehbare Latenzprofile
- keine Zyklenverschwendung durch Warten

Skalierungsmodell (vereinfachte Form):

    T_N = (T_local + T_com) / N

wobei T_com eine *feste Größe* ist.

### 36.13 Fehlerverhalten im Cluster

Bei Fehlern:

- defekte Monolithe werden isoliert
- Cluster fährt deterministisch in Safe State
- TSF definiert fallback-Routinen oder stoppt

Keine dynamische Neuverteilung.

### 36.14 Wissenschaftlicher Nutzen

- deterministische Reduktionen → ideal für numerische Modelle
- deterministische Kommunikation → ideal für CFD
- keine MPI-Jitter → ideal für HPC
- perfekte Skalierung → ideal für große KI-Modelle
- reproduzierbare Cluster-Ergebnisse → ideal für Publikationen

### 36.15 Fazit

KORA-Cluster sind nicht klassische HPC-Cluster, sondern deterministische Multi-Compute-Systeme. 
Durch feste Kommunikation, feste Reduktionspfade, deterministische Partitionierung und phasenparallele Ausführung wird eine Skalierungsqualität erreicht, die mit klassischen Architekturen nicht möglich ist.

Der Monolith bleibt die elementare Einheit —  
die Cluster-Fabric multipliziert seine Fähigkeiten deterministisch.

---

## 37. Security, Integrity & Fault Domains 
(strukturelle Sicherheit, deterministische Fehlerzonen)

KORA verfolgt ein anderes Sicherheitsmodell als klassische Systeme. 
Da der Monolith keine Prozesse, keine Syscalls, keinen Scheduler und keinen dynamischen Code besitzt, entfallen viele Angriffswege moderner IT-Systeme. 
Sicherheit wird durch Struktur gewährleistet – nicht durch Softwarekomplexität.

Dieses Kapitel beschreibt:

- strukturelle Sicherheit,
- deterministische Fehlerdomänen,
- Integritätsgarantien,
- vertrauenswürdige Ausführung,
- Host–Monolith-Verantwortlichkeiten,
- Fehlererkennung und Fehlerreaktion.

### 37.1 Grundprinzip: keine Angriffsfläche durch fehlende Dynamik

Der Monolith besitzt **keinen Codepfad**, der manipuliert werden kann.

Er besitzt:

- keine Programme (nur TSF, aber kein ausführbarer Code),
- keine Threads,
- keine Prozesse,
- keine Syscalls,
- keine Register, die externe Programme beschreiben könnten,
- keine dynamischen Speicherzugriffe,
- keine spekulativen Ausführungen,
- keine Interrupts,
- keine Cache-Hierarchien.

Die deterministische Struktur bildet das Sicherheitsmodell.

### 37.2 Sicherheitsgrundlagen

KORA-Sicherheit basiert auf vier Grundprinzipien:

1. **Strukturelle Isolation**  
   Jede Tile-Gruppe, Memorybank und DMA-Einheit ist statisch isoliert.

2. **Unveränderlichkeit**  
   TSF definiert vollständig, was passiert – es gibt nichts, das dynamisch „ausgeführt“ werden kann.

3. **Vollständige Verifikation**  
   Ein TSF wird vollständig geprüft, bevor es ausgeführt wird.

4. **Deterministisches Fehlerverhalten**  
   Fehler können nur strukturell passieren, nicht durch Manipulation.

### 37.3 Angriffsflächen reduzierter Systeme

Typische Angriffsvektoren:

- Buffer Overflows  
- ROP/JOP  
- Spekulative Seiteneffekte  
- Jitter-Induzierte Leakage  
- Timing-Attacken  
- Prozessübernahme  
- Privilege Escalation

sind auf dem Monolithen **nicht möglich**, da:

    es keinen angreifbaren Kontrollfluss gibt.

Die einzige Möglichkeit, dem Monolithen etwas „unterzuschieben“, wäre ein manipuliertes TSF – doch dies wird vollständig verifiziert.

### 37.4 TSF-Integrität

Jeder TSF-Datensatz wird geprüft:

- Strukturvorgaben,
- Scheduling Trees,
- DMA-Kollisionen,
- Memory-Mapping,
- Pfadlängen,
- Knotenvalidität,
- Blockdefinitionen,
- numerische Profile,
- Reduktionspfade.

Ein manipuliertes TSF führt zu:

    TSF-Reject → Fehlercode → Abbruch

Kein Teil des Systems wird ausgeführt, wenn TSF nicht perfekt valide ist.

### 37.5 Host–Monolith Sicherheitsmodell

Die Verantwortlichkeiten sind strikt getrennt:

#### Der Host:

- ist Angriffspunkt
- läuft unter OS
- kann kompromittiert werden
- kann manipulierte Dateien sehen

#### Der Monolith:

- akzeptiert nur validierte TSF-Programme
- sieht keine Dateisysteme
- sieht keine externen Befehle
- folgt ausschließlich einer strukturellen Ausführung

Selbst ein kompromittierter Host kann nur:

- ungültiges TSF senden → Monolith lehnt ab
- ungültige Datenblöcke senden → Datenprüfung erkennt dies

Er kann **nicht**:

- Code injizieren,
- Kontrolle übernehmen,
- Prozesse manipulieren.

### 37.6 Fault Domains im Monolithen

Fehler können nur strukturell auftreten:

#### (A) Tile-Fehler  

z. B. beschädigte Recheneinheit

#### (B) Memorybank-Fehler  

z. B. fehlerhafte Bank oder Latenzabweichung

#### (C) Fabric-Link-Fehler  

z. B. defektes physikalisches Segment

#### (D) Clock-Domain-Fehler  

z. B. unerwartete Frequenzabweichung

#### (E) Temperaturgrenzfehler  

z. B. Überhitzung

Für jeden Fehler existiert ein deterministisches Fehlerverhalten.

### 37.7 Fehlermodell

Monolith-Fehler sind **immer deterministisch**, nicht zufällig:

    Defekt → Fehlerflag → Ausführung stoppt → Host bekommt Fehler

Nie:

- teilweise korrupte Berechnung,
- undefiniertes Verhalten,
- semikorrigierte Werte,
- „silent corruption“.

### 37.8 Safe-State-Modell

Der Monolith besitzt einen Safe State:

- Tiles deaktiviert,
- DMA deaktiviert,
- Memorybanks eingefroren,
- Fabric-Pfade stillgelegt,
- Temperaturen im Low-Power-Modus stabilisiert,

Der Safe State wird ausgelöst:

- bei TSF-Fehlern,
- bei Bankfehlern,
- bei Tilefehlern,
- bei Fabricfehlern,
- bei thermischen Grenzverletzungen.

Safe State = deterministische Schutzposition.

### 37.9 Deterministische Fehlerreaktionen

Beispiele:

    Tile-Fehler → Immediate Abort  
    Memorybank-Fehler → Bank isolieren  
    Fabric-Latenzfehler → Cluster-Stop  
    Temperaturfehler → Safe Mode

Keine dynamische Neuverteilung.  
Keine heuristische Reaktion.  
Keine Stochastik.  

Alle Fehlerreaktionen sind *vorhersagbar*.

### 37.10 Externe Vertrauensmodelle

KORA unterstützt wissenschaftliche Vertrauensmodelle:

- Golden Runs  
- TSF-Signaturen  
- Host-Signaturen  
- Block-Checksumms  
- deterministisches Logging  
- nummerierte Reduktionspfade  

Ein Monolith kann Teil eines Audit-Prozesses sein.

### 37.11 Datenintegrität

Der Host validiert:

- Blockgrößen
- Checksummen
- Strukturinformationen
- Reihenfolgen

Der Monolith validiert:

- TSF-Struktur
- DMA-Fenster
- Scheduling Trees

Integritätsschichten sind doppelt vorhanden.

### 37.12 Cross-Monolith Sicherheitsmodell

Im Cluster gelten zusätzliche Garantien:

- ein defekter Monolith wird isoliert
- deterministische Reduktionsbäume werden unterbrochen
- Cluster kann nicht „teilweise“ weiterlaufen
- keine Datenkontamination zwischen Partitionen

Cluster-Sicherheit ist strukturell, nicht dynamisch.

### 37.13 Kein Seiteneffekt-Leakage

Da es keine Caches gibt:

- keine Cache-Timing-Angriffe
- keine Cache-Line-Leakage
- keine Spekulation
- keine Branch-Prediction-Attacken

Da es keine Jitter gibt:

- keine Timing-Angriffe über Latenzvariation

KORA ist intrinsisch resistent gegen viele moderne Angriffsklassen.

### 37.14 Wissenschaftlicher Security-Nutzen

Deterministische Ausführung ist nicht nur eine Performance-Eigenschaft, sondern eine Sicherheitseigenschaft:

- keine Hidden States  
- keine Nebenkanäle  
- keine unkontrollierbaren Variablen  
- vollständige Transparenz  

Für wissenschaftliche Publikationen ideal.

### 37.15 Fazit

KORA bricht mit klassischer IT-Sicherheit, indem es dynamische Komplexität durch strukturelle Einfachheit ersetzt. 
Durch deterministische Fehlerdomänen, statische Isolation, vollständige Verifikation und Safe-State-Modelle entsteht ein System, das:

- sicher,
- überprüfbar,
- integer,
- robust,
- transparent

ist — ohne kryptische Sicherheitsmechanismen, sondern durch die Architektur selbst.

---

## 38. Orchestration, Scheduling & Workflow Control 
(HPC-Batch, Parameter-Sweeps, deterministische Pipelines)

KORA besitzt keinen internen Scheduler, kein OS und keine dynamische Prozessverwaltung. 
Dennoch müssen Modelle, Jobs, Experimente und umfangreiche wissenschaftliche Arbeitsabläufe orchestriert werden. 
Dieser Abschnitt beschreibt, wie KORA in existierende Orchestrierungs- und Scheduling-Systeme integriert wird – ohne seine deterministische Natur zu verlieren.

Die Kontrolle erfolgt vollständig außerhalb des Monolithen:

    Host → Workflow Engine → TSF → Monolith

### 38.1 Grundprinzip: externe Orchestrierung, interne Deterministik

Orchestrierung bedeutet:

- Reihenfolge festlegen,
- Abhängigkeiten definieren,
- Parameter variieren,
- Ergebnisse sammeln,
- Cluster-Wechsel steuern.

Dies geschieht alles im Host-Ökosystem.

Im Monolithen passiert ausschließlich:

    deterministische Ausführung eines TSF-Programms.

Der Host orchestriert, der Monolith rechnet.

### 38.2 Integration in HPC-Batch-Systeme

KORA kann in alle gängigen HPC-Scheduler integriert werden:

- SLURM
- PBS / Torque
- LSF
- HTCondor

Die typische Pipeline:

    sbatch job.sh → Host → TSF-Deployment → Monolith-Run → Host → Output

Ein Job-Script enthält:

- TSF-Erzeugung,
- Input-Mapping,
- Monolith-Startsignal,
- Ausgabe-Collect,
- Checksummen,
- Logging.

Beispiel (Einrückung):

    srun kora-run --tsf model.tsf --input data.h5 --output result.h5

### 38.3 Workflow-Systeme für komplexe Experimente

KORA integriert sich in:

- Snakemake
- Nextflow
- Airflow
- Luigi
- CWL
- Argo Workflows

Beispielablauf:

1. Schritt: Eingabedaten generieren  
2. Schritt: TSF erstellen  
3. Schritt: Monolith-Lauf  
4. Schritt: Ergebnis zurückschreiben  
5. Schritt: Analyse/Visualisierung  
6. Schritt: Validierung  

Alles orchestriert vom Host.

### 38.4 Job Scheduling: nicht dynamisch, sondern strukturell

KORA selbst führt kein Scheduling aus.

Scheduling passiert:

- ausschließlich auf dem Host,
- mit klassischen Methoden,
- in Queue-Systemen.

Der Host definiert:

- Startreihenfolge,
- Prioritäten,
- Parallelisierung,
- Ablaufregeln.

Der Monolith garantiert:

    konstante Zeit pro Run.

Dadurch wird Scheduling *einfacher*, nicht komplexer.

### 38.5 Parameter Sweeps

Parameter Sweeps sind ein zentrales Element wissenschaftlicher Forschung:

- Hyperparameter-Optimierung in KI,
- Parametervariationen in CFD,
- Sensitivitätsanalysen in Mathematik,
- Datenmodellexperimente in Big Data.

KORA unterstützt Parameter Sweeps perfekt:

    Sweep = N Runs mit identischen TSF-Strukturen und variierenden Parametern

Der Vorteil:

- deterministische Laufzeit,
- identische numerische Eigenschaften,
- kein Rauschen durch Jitter,
- perfekte Vergleichbarkeit.

Beispiel:

    for viscosity in [0.01, 0.005, 0.001]:
        run(model, viscosity)

### 38.6 Multi-Run Pipelines

Viele wissenschaftliche Workflows benötigen sequentielle Runs:

- iteratives Lösen nichtlinearer PDEs,
- Mehrphasen-Materialmodelle,
- Optimierungsalgorithmen,
- iterative KI-Trainingsschritte.

KORA erlaubt:

    Run 1 → Ausgabedatei → TSF2 → Run 2 → Ausgabedatei → ...

Da alle Runs deterministisch sind, sind Pipelines:

- vollständig reproduzierbar,
- exakt vergleichbar,
- wissenschaftlich auditierbar.

### 38.7 Ensemble Runs

Für große Forschungsmodelle:

    Ensemble = viele unabhängige Instanzen desselben Modells

KORA eignet sich ideal:

- keine gegenseitige Beeinflussung,
- konstante Energie pro Run,
- deterministische Zeitdauer,
- perfekte Vergleichbarkeit der Ergebnisse.

Beispiel: Klimamodelle

    1000 Runs mit leicht veränderten Initialwerten
    → deterministische, statistisch saubere Ensembles

### 38.8 Disaster-Safe Orchestrierung

Durch deterministisches Verhalten ist das Recovery trivial:

Wenn ein Run abbricht:

- Ursache ist deterministisch,
- kein Zustand ist verloren,
- keine dynamische Migration nötig.

Workflow-Systeme können:

- ab Schritt N erneut starten,
- TSF und Input wiederverwenden,
- Ergebnis deterministisch reproduzieren.

### 38.9 Checkpointing (strukturell, nicht dynamisch)

KORA kennt keine dynamischen Checkpoints.

Stattdessen:

    strukturelle Checkpoints = Input/Output des Monolithen

Jede Phase, jeder Run ergibt:

- Eingabedaten (Checkpoint)
- TSF (Ausführungsmodell)
- Ausgabedaten (Checkpoint)
- Telemetrie (Validierung)

Damit entsteht ein vollständiger Reproduzierbarkeitsbaum.

### 38.10 Visualization & Meta-Orchestrierung

Visualisierungstools können:

- Scheduling Trees anzeigen,
- TSF-Strukturen darstellen,
- DMA-Fenster visualisieren,
- Multi-Monolith-Kommunikation darstellen.

Orchestrierungsebene kann:

- Heatmaps erzeugen,
- Performanceprofile bauen,
- Energiegraphen rendern,
- Multi-Run-Analysen durchführen.

### 38.11 Cloud-Orchestrierung

KORA lässt sich (Host-seitig) in Cloud-Workflows integrieren:

- Kubernetes (Controller steuert nur Hosts)
- Argo Workflows
- Terraform (für Host-Ressourcen)
- Serverless-Pipelines (für Pre/Post-Prozesse)

Jeder Monolith bleibt:

    containerfrei, kernelunabhängig, deterministisch.

### 38.12 Warum deterministische Orchestrierung überlegen ist

Bei klassischen HPC/GPU-Systemen:

- Runs dauern unterschiedlich lang,
- manche Jobs hängen,
- manche Straggler bremsen Pipelines,
- Performance variiert von Lauf zu Lauf,
- Batch-Slots müssen gepuffert werden.

Bei KORA:

- jeder Run hat exakt bekannte Länge,
- keine Straggler,
- kein Jitter,
- perfekte Planbarkeit,
- ideale Auslastung.

Für Rechenzentren bedeutet das:

- weit bessere Ressourcenplanung,
- vorhersagbare Energieprofile,
- deterministische Queue-Laufzeiten.

### 38.13 Fazit

KORA besitzt kein eigenes Scheduling – und genau das ist sein Vorteil.  
Durch deterministische Innenstruktur und vollständige äußere Orchestrierung entsteht ein System mit:

- planbaren Ausführungszeiten,
- starker HPC-Integration,
- idealen Workflow-Bedingungen,
- sauberer Multi-Run-Reproduzierbarkeit,
- exzellenter Skalierbarkeit,
- perfekter wissenschaftlicher Vergleichbarkeit.

KORA lässt sich dadurch in jede existierende Infrastruktur einbinden –  
ohne Kompromisse bei seiner deterministischen Kernphilosophie.

---

## 39. Monitoring, Telemetry & Deterministic Observability 
(Metriken, Zeitprofile, Audit-Logs)

Der Monolith ist deterministisch. Dadurch ist auch seine Beobachtung deterministisch. 
Monitoring, Telemetrie und Auditierung sind keine heuristischen Analyseprozesse – sondern exakt beschreibbare Zustandsabfragen.

Dieses Kapitel definiert die vollständige Mess-, Beobachtungs- und Auditierarchitektur von KORA.

### 39.1 Grundprinzip: Beobachtung ohne Einfluss

Klassische HPC- und GPU-Systeme leiden unter:

- Mess-Jitter,
- OS-bedingten Verzögerungen,
- Sampling-Schwankungen,
- variablen Energieprofilen,
- zeitlichen Interferenzen.

Beim Monolithen gilt:

    Beobachtung beeinflusst Ausführung nicht.

Telemetry ist:

- non-intrusive,
- deterministic,
- phasenbasiert,
- vollständig wiederholbar.

### 39.2 Messpunkte (Observability Anchors)

Der Monolith definiert interne Messpunkte, die nie variieren:

- Beginn jeder Phase
- Ende jeder Phase
- DMA-Fensteröffnungen
- Reduktionsfenster
- Tile-Aktivitäten
- Memorybank-Zugriffe
- Fabric-Link-Transferpunkte

Beispiel:

    Phase 12 Start @ Cycle 884,736
    Phase 12 End   @ Cycle 886,164

Dies ist für jeden Run identisch.

### 39.3 Zeitprofile

Zeitprofile bestehen aus:

- T_phase_i  
- T_dma_j  
- T_reduction_k  
- T_total  

Alle sind deterministisch.

Ein Zeitprofil ist ein vollständiges Abbild des Scheduling Trees.

Beispiel (Einrückung):

    {
        "Phase 0":  42 cycles,
        "Phase 1": 1284 cycles,
        "Phase 2":  76 cycles,
        "Total":   1402 cycles
    }

### 39.4 Energieprofile

Da die Leistung konstant ist:

    E_total = P_constant × T_total

Monitoring liefert:

- konstante Leistungsaufnahme,
- minimale Schwankung (<0.5%),
- prozessorinterne Telemetrie,
- Rack-Level-Energieprofil.

Keine:

- Boost-Spikes,
- Frequenzsprünge,
- Spannungsschwankungen.

### 39.5 Tile-Aktivitätsprofile

Tiles melden Aktivität in deterministischen Taktschritten:

    tile_activity[tile_id][phase] = active / idle

Beispiel:

    Tile 184:
        Phase 0: active
        Phase 1: active
        Phase 2: idle

Dies zeigt:

- Lastverteilung,
- Effizienz,
- Numerikpfade.

### 39.6 Memorybank-Profile

Jede Memorybank meldet:

- Zugriffszahl,
- Latenz,
- Bankkonflikte (nur im Fehlerfall),
- thermische Daten.

Beispiel:

    Bank 17:
        accesses: 43812
        latency: 3 cycles (constant)
        temp: 52.1°C

### 39.7 DMA-Profile

DMA-Fenster werden überwacht:

- Startzyklus,
- Endzyklus,
- Übertragungsgröße,
- Latenz,
- Bandbreitenauslastung.

Beispiel:

    DMA Window 14:
        size: 2 MB
        bandwidth: 256 GB/s
        time: 8.1 microseconds

### 39.8 Fabric-Profile (Cross-Monolith)

Bei Cluster-Betrieb:

    CMF-Slot 23:
        source: M1
        dest: M3
        block: 14
        latency: 3 cycles
        jitter: 0 cycles

Keine dynamischen Routingeffekte.

### 39.9 Audit Logs

Audit Logs enthalten:

- TSF-ID
- TSF-Hash
- Eingabedaten-Checksumme
- Ausgabedaten-Checksumme
- Zyklusprofile
- Energieprofil
- Fehlerflags
- Fabric-Ereignisse

Audit Logs sind:

- unveränderbar,
- deterministisch,
- signierbar,
- ideal für wissenschaftliche Publikationen.

### 39.10 Reproduzierbarkeit der Telemetrie

Ein einzigartiges Merkmal:

    Telemetrie ist bit-genau reproduzierbar zwischen Läufen.

Beispiel:

    T_phase_7:
        Run 1: 328 microseconds
        Run 2: 328 microseconds
        Run 3: 328 microseconds

In GPU/HPC-Systemen ist das unmöglich.

### 39.11 Monitoring im Workflow-Kontext

Workflow-Systeme können:

- Telemetrie speichern,
- Profile vergleichen,
- Regressionen erkennen,
- numerische Stabilität überwachen.

Beispiel:

    compare(run_A.profile, run_B.profile) → identical

Wenn Profile abweichen:

    → Hardwarefehler oder TSF-Fehler

Keine stochastische Ursache.

### 39.12 Sicherheit durch Observability

Die Telemetrie kann genutzt werden für:

- Security Auditierung,
- Integritätsprüfungen,
- Erkennung unerwarteter Abweichungen,
- Fehleranalyse.

Da keine dynamischen Pfade existieren, ist jede Abweichung praxisrelevant.

### 39.13 Visualisierungen

Auf Basis deterministischer Daten können Visualisierungen erzeugt werden:

- Heatmaps von Tile-Aktivität,
- Fabric-Topologien,
- Zeitlinien der Phasen,
- Energiegraphen,
- Memory-Flow-Diagramme,
- Scheduling-Tree-Zeitprofile.

Diese Visualisierungen sind _immer_ identisch für denselben TSF und dieselben Daten.

### 39.14 Wissenschaftlicher Nutzen

Deterministische Telemetrie ermöglicht:

- perfekte Reproduzierbarkeit,
- fehlerfreie Validierung,
- transparente Veröffentlichung,
- präzise Energieangaben,
- exakte Performancevergleiche.

KORA wird dadurch zu einem Messinstrument –  
nicht nur zu einem Recheninstrument.

### 39.15 Fazit

Monitoring, Telemetrie und Observability in KORA sind strukturelle Eigenschaften, keine add-on Tools.  
Durch deterministische Zeit-, Energie- und Kommunikationsprofile entsteht ein System, das:

- perfekt nachvollziehbar,
- wissenschaftlich abgesichert,
- auditierbar,
- robust,
- transparent

ist — eine neue Qualität der Beobachtbarkeit in der HPC- und KI-Welt.

---

## 40. Evolution & Next-Generation Architecture 
(Generationenmodell, TSF-Kompatibilität, Entwicklungswege)

KORA ist nicht als einmalige Architektur gedacht, sondern als langfristiges, deterministisches Rechenmodell. 
Das bedeutet: neue Monolith-Versionen, neue Technologien und neue wissenschaftliche Anforderungen müssen integriert werden können, 
ohne die Kerneigenschaften zu zerstören:

- Deterministik
- Reproduzierbarkeit
- TSF-Kompatibilität
- numerische Konsistenz
- strukturelle Sicherheit

Dieses Kapitel beschreibt, wie die KORA-Architektur evolutionär weiterentwickelt werden kann.

### 40.1 Grundprinzip: Evolution ohne Bruch

Die wichtigste Designregel lautet:

    Jede neue Generation ist strukturell kompatibel zur vorherigen.

Ziele:

- TSF-Kompatibilität bewahren,
- numerische Konsistenz sicherstellen,
- deterministische Scheduling Trees erhalten,
- keine dynamische Komplexität einführen.

Neue Generationen erweitern — sie verändern nicht.

### 40.2 Generationsmodell

KORA verwendet ein Generationensystem:

- **M1**: Grundarchitektur, Referenzdesign
- **M2**: optimierte Memorybanks, höhere Bandbreite
- **M3**: erhöhte Tile-Anzahl, bessere Effizienz
- **M4**: vollständige Fabric-Erweiterung, Clusteroptimierung

Jede Generation hat:

- identische funktionale Struktur,
- identische TSF-Definition,
- identisches deterministisches Ausführungsmodell.

Nur:

- Latenzen,
- Bandbreiten,
- Tile-Anzahlen,
- Energiewerte

dürfen sich ändern.

### 40.3 TSF-Kompatibilität über Generationen

TSF ist die zentrale Konstante.  
Es definiert:

- Scheduling Trees,
- DMA-Fenster,
- Memory-Mappings,
- Reduktionspfade,
- Clusterpfade.

Neue Generationen dürfen TSF erweitern, aber niemals brechen.

Kompatibilitätsregeln:

1. TSF v1 läuft unverändert auf M1–M4  
2. Neue TSF-Funktionen sind optional  
3. Alte TSF-Strukturen bleiben gültig  
4. Keine dynamischen Extensions  
5. Keine variablen Ausführungspfade

Damit bleibt KORA wissenschaftlich stabil.

### 40.4 Numerikprofile

Für Forschungsintegrität gibt es feste Profile:

- **Numerikprofil A** (IEEE 754)
- **Numerikprofil B** (stabile Mixed Precision)
- **Numerikprofil C** (Soft-FP, speziell für Reproduzierbarkeit)

Eine neue Generation darf:

- mehr Präzision hinzufügen,
- neue FP-Einheiten integrieren,

darf aber nicht:

- Reihenfolgen variieren,
- FP-Ausführungswege verändern,
- Reduktionspfade ändern.

### 40.5 Erweiterung der Tile-Anzahl

Neue Monolithen können:

- mehr Tiles,
- mehr Tile-Gruppen,
- breitere Vektoreinheiten

enthalten.

Voraussetzung:

    Scheduling Trees müssen skalieren, aber deterministisch bleiben.

Beispiele:

    M1: 256 Tiles
    M2: 384 Tiles
    M3: 512 Tiles
    M4: 768 Tiles

TSF beschreibt nur Strukturen — nicht Hardwaregrenzen — deshalb bleibt es kompatibel.

### 40.6 Erweiterung der Memorybanks

Memorybanks können erweitert werden:

- mehr Banks,
- größere Banks,
- geringere Latenzen.

Neue Generationen können andere physische Eigenschaften besitzen, solange:

- Bank-Zugriffsmodell gleich bleibt,
- deterministische Zugriffsreihenfolge unverändert bleibt.

### 40.7 Erweiterung der Fabric

Die Cross-Monolith Fabric kann über Generationen verbessert werden:

- höhere Bandbreiten,
- niedrigere Latenzen,
- mehr Links,
- komplexere deterministische Routingbäume.

Aber:

    TDM-Slots und Pfaddefinitionen müssen deterministisch bleiben.

### 40.8 Energieeffizienz-Optimierung

Neue Generationen können:

- effizientere Tiles,
- effizientere DMA-Einheiten,
- optimierte Clock-Domains

haben.

Solange gilt:

- Leistung bleibt konstant während der Ausführung,
- keine Boost-Mechanismen,
- keine Frequenzsprünge.

Determinismus ist wichtiger als Effizienzsteigerung.

### 40.9 Compiler-Generationskompatibilität

Der SCI-Compiler garantiert:

- TSF v1 → kompatibel mit allen Generationen
- TSF v2 → optional, aber abwärtskompatibel
- keine generationalen Brüche

Das bedeutet:

    Ein 20 Jahre altes TSF muss auf einem M8-System laufen können.

Wissenschaftliche Archivdaten bleiben nutzbar.

### 40.10 Software-Stack über Generationen hinweg

Python/HAPI-Modelle:

- laufen unverändert,
- generieren identische TSF-Ausführungsmodelle.

C/C++/Fortran-Wrappers:

- bleiben stabil,
- ändern keine Semantik.

KI-Framework-Backends:

- bleiben kompatibel zur TSF-Struktur.

### 40.11 Zukünftige Erweiterungsrichtungen

#### 40.11.1 Höhere Dimensionen

- 4D-/5D-Scheduling Trees  
- komplexe PDE-Systeme  

#### 40.11.2 Super-Monolithen

- mehrere Monolithe auf einem Die  
- integrierte CMF  
- Ultra-Low-Latency-Banks

#### 40.11.3 Soft-FP Einheiten

- vollständig reproduzierbare arithmetische Modelle  
- unabhängig von Hardwarepräzision  

#### 40.11.4 Deterministische On-Die Networking-Knoten

- Fabric direkt integriert  
- multi-die deterministische Ausführung  

### 40.12 Langfristige Integritätsgarantien

KORA verpflichtet sich strukturell zu:

1. deterministischen Ausführungspfaden  
2. stabilen FP-Reihenfolgen  
3. TSF-Abwärtskompatibilität  
4. auditierbaren Ergebnissen  
5. reproduzierbaren Simulationen  

Dies macht KORA einzigartig in der HPC-Welt.

### 40.13 Fazit

KORA ist so konzipiert, dass es nicht nur heute, sondern über Jahrzehnte hinweg stabil und wissenschaftlich verlässlich bleibt.  
Durch strikte Trennung von:

- deterministischer Innenschicht,
- erweiterbarer Außenschicht,

entsteht ein System, das sich technologisch weiterentwickeln kann, ohne seine wissenschaftliche Identität zu verlieren.

KORA wächst — aber es zerbricht niemals seine deterministische Grundlage.

---

## 41. Compliance, Validation & Scientific Trust 
(Zertifizierung, Governance, Auditierbarkeit)

KORA ist eine deterministische Rechenarchitektur, deren wichtigste Eigenschaft nicht Geschwindigkeit ist, sondern Vertrauenswürdigkeit. 
Dieses Kapitel beschreibt, wie KORA überprüft, zertifiziert, veröffentlicht und wissenschaftlich verantwortbar gemacht wird. 
Es bildet den Rahmen für alle späteren Publikationen, die sich auf KORA stützen.

### 41.1 Grundprinzip: Vertrauen durch Transparenz und Deterministik

Wissenschaftliches Vertrauen entsteht nicht durch Marketing, sondern durch:

- nachvollziehbare Struktur,
- überprüfbare Modelle,
- reproduzierbare Ergebnisse,
- deterministische Zeitverläufe,
- Prüfpfade,
- auditierbare Ausführung.

KORA erfüllt diese Anforderungen intrinsisch.

### 41.2 Compliance-Dimensionen

KORA betrachtet Compliance in fünf Dimensionen:

1. **Wissenschaftliche Compliance**  
   – Reproduzierbarkeit, Peer Review, numerische Konsistenz

2. **Technische Compliance**  
   – deterministische TSF-Ausführung, Hardwareintegrität

3. **Operative Compliance**  
   – Korrekte Integration in Rechenzentren und Host-Umgebungen

4. **Methodische Compliance**  
   – klare Regeln für Modellierung, Logging und Analyse

5. **Regulatorische Compliance**  
   – Energieeffizienzrichtlinien, Datenschutz, Auditierbarkeit

### 41.3 Formal Verification

Da KORA deterministisch ist, kann ein großer Teil der Architektur formal verifiziert werden:

- Scheduling Trees  
- DMA-Fenster  
- Reduktionspfade  
- Memorypfade  
- Tile-Abhängigkeiten  

Die formale Verifikation prüft:

    Sind alle Pfade widerspruchsfrei und kollisionsfrei?

Das Ergebnis:

- mathematische Beweise anstelle von Benchmark-Hypothesen
- logisch korrekte Ausführungsmodelle

### 41.4 TSF Validation

Jedes TSF wird vor der Ausführung geprüft:

- Strukturvalidierung
- numerische Profile
- Konfliktanalyse
- Deadlock-Prüfung
- deterministische Pfadprüfung

Dies garantiert:

    Nur vollständig korrekte Modelle erreichen die Hardware.

### 41.5 Scientific Trust Model

KORA führt ein wissenschaftliches Vertrauensmodell ein:

- deterministische Wiederholbarkeit  
- universelle Reproduzierbarkeit  
- vollständiges Logging  
- Golden Runs  
- Checksum-basierte Validierung  

Ein wissenschaftlicher Lauf ist damit:

    transparent, dokumentiert, wiederholbar, auditierbar.

### 41.6 Golden-Run-Zertifizierung

Ein Golden Run enthält:

- TSF-Datei  
- Modellparameter  
- Inputdaten  
- Outputdaten  
- Zyklusprofile  
- Energieprofile  
- Telemetrie  

Golden Runs dienen als:

- Peer-Review-Basis
- Referenzmodell
- Benchmark-Ersatz
- Regressionsvalidierung

Jede Forschungsgruppe kann eigene Golden Runs definieren.

### 41.7 Peer-Review-Kompatibilität

KORA erleichtert Peer Review durch:

- identische Ergebnisse bei jeder Ausführung  
- deterministische numerische Abläufe  
- vollständige Logs  
- reproduzierbare TSF-Modelle  

Reviewer können:

- Modelle verifizieren,
- TSF-Struktur prüfen,
- Ergebnisse reproduzieren,
- Numerikprofile vergleichen.

### 41.8 Hardware-Compliance

Ein KORA-Monolith besitzt:

- deterministische Clock-Domain,
- konstante Leistungsaufnahme,
- transparente thermische Profile,
- geprüfte Memorybanks,
- deterministische Fabric-Latenz.

Das System kann zertifiziert werden:

    M3 Hardware Revision B – Verified Stable Deterministic Compute

### 41.9 Software-Compliance

Der Software-Stack (HAPI, SCI, Simulator):

- ist deterministisch,
- besitzt feste Ausführungsreihenfolgen,
- vermeidet dynamische Komplexität,
- wird versioniert nach wissenschaftlichen Regeln.

Versionen:

    SCI v1.0 → kompatibel zu allen Monolith-Generationen  
    SCI v2.0 → erweitert, aber abwärtskompatibel  

### 41.10 Rechenzentrums-Compliance

Rechenzentren können KORA zertifizieren als:

- deterministic hardware zone  
- reproducible compute environment  
- scientifically audited infrastructure  

Da keine Boost-Mechanismen existieren:

- Energie ist berechenbar,
- thermische Last ist stabil,
- Monitoring ist konstant.

### 41.11 Audit Trails

Audit Trails enthalten:

- jede TSF-Ausführung,
- alle Zeitstempel,
- alle DMA-Fenster,
- alle Reduktionen,
- alle Memoryzugriffe,
- Energieprofile,
- Temperaturprofile,
- Hardwarefehler,
- Host-Parameter.

Sie sind:

- chronologisch,
- unveränderbar,
- signierbar.

### 41.12 Regulatory Readiness

Für regulatorische Umfelder (z. B. Energieeffizienz, wissenschaftliche Publikationen, Industrieprozesse) bietet KORA:

- deterministische Nachweise,
- dokumentierbare Energieprofile,
- zertifizierbare Ausführungsmodelle,
- transparente Fehlerberichte.

### 41.13 Long-Term Scientific Archiving

Eine Forschungsgruppe kann archivieren:

- TSF-Dateien (modellkompakt)
- Metadaten (Parameter)
- Eingabedaten
- Ausgabedaten
- Zeitprofile
- Energieprofile

Somit entsteht ein archivierbares Wissenschaftsmodell.

Auch in 30 Jahren kann ein Monolith der Generation M8:

    ein TSF von 2025 ausführen.

### 41.14 Trust by Design

KORA ist nicht „trusted“ durch externe Mechanismen, sondern:

    trust is built into the structure.

Schlüssel:

- keine Blackbox-Mechanismen
- keine dynamischen Scheduling-Effekte
- keine OS-Komplexität
- deterministische Memorypfade
- vollständige Transparenz

### 41.15 Fazit

KORA definiert eine neue Form wissenschaftlicher und technischer Vertrauenswürdigkeit.  
Durch:

- deterministische Ausführung,
- formale Validierung,
- Golden-Run-Zertifizierung,
- vollständige Auditierbarkeit,
- strukturierte Compliance,
- langfristige TSF-Kompatibilität,

entsteht ein System, das technisch, wissenschaftlich und regulatorisch zuverlässig ist.  
KORA ist damit nicht nur ein Rechenmodell —  
es ist ein Vertrauensmodell.

---

## 42. End-to-End Pipeline: From Model to Deterministic Execution 
(Modell → TSF → Validierung → Monolith)

Die KORA-Architektur definiert nicht nur Hardware, Compiler und Monitoring, sondern eine vollständige deterministische Rechenpipeline. 
Jedes wissenschaftliche Modell durchläuft denselben Weg – vom High-Level-Entwurf bis zur bitgenauen Ausführung.

Dieses Kapitel beschreibt die gesamte End-to-End-Pipeline.

### 42.1 Übersicht der Pipeline

Die Pipeline besteht aus 7 Stufen:

1. Modellbeschreibung (Python/HAPI, C/C++, Fortran)
2. Compiler-Phase 1: Strukturierung
3. Compiler-Phase 2: Scheduling Trees
4. TSF-Erzeugung
5. TSF-Validierung
6. Monolith-Ausführung
7. Ergebnisrückgabe & Logging

Diese Pipeline ist identisch für:

- CFD,
- KI,
- Big Data,
- PDE-Systeme,
- Lineare Algebra,
- Materialwissenschaften,
- numerische Simulationen.

### 42.2 Stufe 1 – High-Level Modellbeschreibung

Ein Modell wird in einer bestehenden Sprache formuliert:

- Python (HAPI / NumPy / PyTorch / JAX)
- C/C++ (Hochleistungsmodule)
- Fortran (CFD, numerische Mathematik)
- Domain-spezifische Modelle (DL, ML, PDE)

Beispiele:

    u = field((1024, 1024))
    u_next = stencil(u, Laplace)

oder KI:

    model = Transformer(...)
    y = model(x)

Der Monolith selbst sieht diesen Code nie.

### 42.3 Stufe 2 – Compiler Phase 1: Strukturierung

Der SCI-Compiler übersetzt die Modellbeschreibung in:

- elementare Blöcke,
- mathematische Operationen,
- Speicherlayouts,
- deterministische Operatorgraphen,
- eindeutige Datenflüsse.

Diese Phase baut den „mathematischen Kern“ des Modells.

### 42.4 Stufe 3 – Compiler Phase 2: Scheduling Trees

Die Scheduling Tree Engine erzeugt einen vollständigen, deterministischen Ausführungsplan:

- Tile-Zuordnung,
- Datenzugriffsreihenfolgen,
- Reduktionspfade,
- DMA-Fenster,
- Bankzugriffe,
- Phasenstrukturen,
- Ghost-Layer Übertragungen (CFD),
- Layer-Abfolgen (KI),
- Map/Reduce-Abfolgen (Big Data).

Ergebnis:

    Ein vollständiger, deterministischer Scheduling Tree.

### 42.5 Stufe 4 – TSF-Erzeugung

TSF (Tiled Scheduling Format) beschreibt vollständig:

- alle Operationen,
- alle Zeitfenster,
- alle Datenpfade,
- alle DMA-Transfers,
- alle Phasen,
- alle Partitionen (Cluster),
- alle Reduktionswege.

TSF ist kompakt, strukturell, deterministisch.

Beispiel:

    TSF:
        phases: 214
        tiles: 512
        dma_windows: 38
        reductions: 12

### 42.6 Stufe 5 – TSF-Validierung (Host-seitig & Monolith-intern)

Jedes TSF durchläuft zwei Validierungsphasen:

#### Host-validierung:

- Syntaxcheck
- Strukturprüfung
- Parameterprüfung
- Konflikterkennung

#### Monolith-validierung:

- Bankkollisionen
- DMA-Kollisionen
- Slot-Konflikte
- Scheduling Tree Konsistenz
- Reduktionspfade

Nur wenn beide Ebenen erfolgreich sind:

    TSF Accepted → Ausführung möglich

### 42.7 Stufe 6 – Deterministische Ausführung

Die Ausführung erfolgt:

- phasenbasiert,
- kollisionsfrei,
- ohne OS,
- ohne Scheduler,
- ohne Threads,
- ohne Interrupts.

Der Ablauf:

    Phase 0: Input Read
    Phase 1: Compute
    Phase 2: Reduction
    Phase 3: Ghost Exchange
    Phase 4: Compute
    ...
    Phase N: Output Writeback

Jede Phase hat feste Zyklusdauer.

Beispiel:

    Phase 37 = 312 cycles
    Phase 38 = 408 cycles

### 42.8 Stufe 7 – Ausgabe, Logging, Validierung

Nach Ausführung:

- Ergebnisse stehen in definierten Memorybereichen,
- DMA-Fenster geben die Ergebnisse an den Host,
- Audit-Logs werden erstellt,
- Telemetrie wird gespeichert,
- Energieprofil wird erfasst.

Der Host schreibt:

- Dateien (HDF5, Parquet, PyTorch .pt, NumPy .npy, CSV)
- Validierungschecks (Checksummen)
- Telemetrie
- Multirun-Vergleiche

### 42.9 Multi-Run Pipeline (CFD, KI, Big Data)

Bei iterativen Systemen:

    Run1 → Result → TSF2 → Run2 → Result → TSF3 → ...

Wichtig:

- Jeder Run ist deterministisch.
- Zeitprofile bleiben identisch.
- Numerik bleibt stabil.

### 42.10 Parameter Sweeps & Automatisierung

Parameter Sweeps:

- Hyperparameter-Optimierung,
- Sensitivitätsanalysen,
- Materialmodelle,
- Big-Data Modellvarianten.

Die Pipeline verändert nur:

- Parameterdatei,
- Eingabeblöcke,

aber nicht den TSF-Kern.

### 42.11 Integration in Rechenzentren

Rechenzentren orchestrieren:

- SLURM / PBS / LSF Batchläufe,
- Argo / Snakemake / Nextflow Pipelines,
- Kubernetes-basierte Host-Instanzen.

Der Monolith bleibt containerfrei.

Orchestrierungslogik:

    Workflow → TSF → Monolith → Output → Logging

### 42.12 Fehlerszenarien in der Pipeline

Fehlertypen:

- geschädigte Tiles
- defekte Banks
- Fabric-Link-Ausfall
- unvollständige Eingabedatei
- TSF-Konsistenzfehler

Reaktion:

- deterministisches Stoppen,
- Logging,
- Safe State,
- Retry auf anderem Monolithen.

### 42.13 Reproduzierbarkeit & Dokumentation

Jeder vollständige Run erzeugt:

- TSF-Datei
- Inputdaten
- Outputdaten
- Zeitprofile
- Energieprofile
- Fabric-Daten
- Memoryprofile
- Tileaktivität
- Fehlerflags

Damit ist jeder Run ein vollständiges wissenschaftliches Artefakt.

### 42.14 Fazit

Die End-to-End Pipeline von KORA ist vollständig deterministisch, transparent und wissenschaftlich reproduzierbar.  
Sie verbindet:

- High-Level Modellierung,
- strukturelle Kompilierung,
- Validierung,
- deterministische Hardwareausführung,
- Telemetrie,
- Logging,
- Workflowintegration,
- Reproduzierbarkeit.

KORA definiert damit eine neue, vollständige, vertrauenswürdige Rechenpipeline –  
von der Idee bis zum wissenschaftlichen Ergebnis.

---

## 43. Governance, Operational Model & Scientific Stewardship 
(Betrieb, Verantwortung, Veröffentlichung)

KORA ist nicht nur eine Architektur, sondern ein langfristiges wissenschaftliches Projekt. 
Damit es über Jahre und Jahrzehnte stabil bleibt, benötigt es ein Governance-Modell, das technische, wissenschaftliche und operative Verantwortung klar regelt.

Dieses Kapitel beschreibt das institutionelle, organisatorische und wissenschaftliche Modell hinter KORA.

### 43.1 Grundprinzip: Wissenschaftliche Verantwortung

KORA ist so konzipiert, dass:

- wissenschaftliche Integrität,
- Langzeitpflege,
- methodische Transparenz,
- auditierbare Prozesse,
- deterministische Ergebnisse

in jedem Nutzungsszenario erhalten bleiben.

Dies erfordert keine zentrale Instanz, sondern klar definierte Rollen und Prozesse.

### 43.2 Rollenmodell

#### 43.2.1 Architektur-Stewards

Verantwortlich für:

- Weiterentwicklung der Monolith-Architektur,
- TSF-Kompatibilität,
- deterministische Ausführung,
- Hardwaredesign-Vorgaben.

#### 43.2.2 Compiler-Stewards (SCI/HAPI)

Verantwortlich für:

- TSF-Spezifikation,
- Compiler-Versionierung,
- numerische Konsistenz,
- Modellierungsregeln.

#### 43.2.3 Scientific Users

Nutzer aus:

- CFD,
- KI,
- Materialwissenschaften,
- Mathematik,
- Data Science,
- Physik,
- Geowissenschaften.

Sie erzeugen:

- Modelle,
- Golden Runs,
- wissenschaftliche Publikationen.

#### 43.2.4 Infrastructure Operators

Rechenzentren:

- SLURM-Integration,
- Monitoring,
- Energieprofilmanagement,
- Audit-Logs.

### 43.3 Veröffentlichungsmodell

KORA wird unter einer offenen wissenschaftlichen Lizenz veröffentlicht:

- vollständige Spezifikationen,
- Referenzimplementierungen,
- Simulator,
- SCI-Compiler,
- HAPI-Frontend,
- Beispiele,
- Golden Runs.

Publikationen sind:

- transparent,
- reproduzierbar,
- vollständig dokumentiert.

### 43.4 Langzeitarchivierung & Versionierung

Alle Architekturversionen, Compiler-Versionen und TSF-Versionen werden:

- versioniert,
- archiviert,
- abwärtskompatibel gehalten,
- wissenschaftlich geprüft.

Regel:

    Ein Modell, das heute läuft, muss in 20 Jahren identisch laufen.

Dieses Archivierungsmodell stellt die Grundlage für OSF-/Zenodo-Publikationen.

### 43.5 Community-Modell

KORA ist keine proprietäre Plattform.  
Es funktioniert nach einem wissenschaftlichen Stewardship-Modell:

- offene Spezifikationen,
- offene Simulation,
- offene Compiler,
- transparente Diskussionen,
- Peer-Review-Kompatibilität.

Die Community besteht aus:

- Wissenschaftlerinnen,
- Ingenieuren,
- Rechenzentrumsbetreibern,
- Entwicklern.

### 43.6 Änderungsprozess (Governance Cycle)

Jede Änderung an:

- TSF,
- SCI,
- HAPI,
- Scheduling Trees,
- Fabric Definition,
- Memorybank-Profilen,

durchläuft einen klaren Prozess:

1. Proposal  
2. Community Review  
3. Simulation & Validation  
4. Determinismusprüfung  
5. Abwärtskompatibilitätsprüfung  
6. Versionierung  
7. Veröffentlichung

Keine Änderung darf:

- Deterministik brechen,
- Reproduzierbarkeit beeinträchtigen,
- TSF brechen,
- numerische Profile ändern.

### 43.7 Kontrollmechanismen

#### 43.7.1 Determinismus-Garantie

Jede Evolution muss garantieren:

    deterministische Wiederausführung aller existierenden TSF-Dateien.

#### 43.7.2 Numerische Konsistenz

Neue Numerikprofile dürfen ältere nicht ersetzen.

#### 43.7.3 Scientific Audit

Wissenschaftliche Ergebnisse müssen:

- überprüfbar,
- reproduzierbar,
- dokumentiert,

sein.

#### 43.7.4 Simulator-Konformität

Der Simulator ist Referenz und Gesetzbuch:

    Simulation == Hardware

### 43.8 Rechenzentrumsbetrieb

Rechenzentren nutzen:

- deterministische Konfigurationen,
- konstanten Energiebedarf,
- auditierbare Logs,
- strukturierte Hardwareknoten.

Governance zwischen Operatoren und KORA-Stewards:

- definierte Schnittstellen,
- klare Zuständigkeiten,
- deterministische Fehleranalyse,
- dokumentierte Prozesse.

### 43.9 Institutionelle Nutzung

Institutionen können KORA einsetzen für:

- Forschungsnetzwerke,
- wissenschaftliche Großprojekte,
- Langzeitstudien,
- meteorologische Modelle,
- Klimasimulationen,
- KI-Modelle mit hohem Reproduzierbarkeitsbedarf.

Das Governance-Modell unterstützt:

- Citizen Science,
- Open Science,
- kollaborative Forschung,
- Cross-Institutional Verification.

### 43.10 Industrielle Nutzung

Industrien profitieren von:

- deterministischen Berechnungen,
- reproduzierbaren Prozessmodellen,
- auditierbaren Abläufen.

KORA eignet sich für:

- Materialentwicklung,
- Energiesysteme,
- Fertigungsprozesse,
- Sicherheitstechnologien,
- Big Data Analytik.

Governance-Regel:

    industrielle Integrationen dürfen die deterministische Grundstruktur niemals verändern.

### 43.11 Ethik & Verantwortung

KORA ist ein wissenschaftliches Werkzeug. 
Stewardship bedeutet:

- ethische Nutzung,
- keine Manipulation durch dynamische Systeme,
- keine Blackbox-Mechanismen,
- keine versteckten Variablen,
- vollständige Transparenz.

Ein deterministisches System hat keine versteckten Handlungspfade, daher:

    Ethik = Transparenz + Reproduzierbarkeit.

### 43.12 Zukunftssicherheit

Das Governance-Modell ist so ausgelegt, dass KORA:

- Versionen über Jahrzehnte hinweg stabil hält,
- Monolith-Generationen sauber weiterentwickelt,
- wissenschaftliches Vertrauen strukturell bewahrt,
- Community-Evolution fördert.

### 43.13 Fazit

KORA-Governance basiert auf:

- deterministischer Technik,
- wissenschaftlicher Integrität,
- langfristiger Stabilität,
- offener Wissenschaft,
- reproduzierbaren Ergebnissen,
- klarer Verantwortung.

Es ist kein proprietäres Projekt —  
sondern ein wissenschaftliches Fundament, das über Generationen tragfähig bleibt.

---

## 44. Documentation, Publishing & Long-Term Knowledge Architecture
(KORA-Dokumentation, OSF/Zenodo-Veröffentlichung, Wissensarchitektur)

KORA ist ein deterministisches Rechensystem, dessen Nutzen nur dann realisiert werden kann, wenn die Dokumentation selbst strukturiert, dauerhaft, präzise und wissenschaftlich anschlussfähig ist. 
Dieses Kapitel beschreibt die Architektur der Dokumentation, der Veröffentlichung und des Wissensmanagements.

### 44.1 Grundprinzip: Dokumentation als strukturelles Element

Dokumentation ist nicht „ergänzend“, sondern Teil der Architektur.  
Sie definiert:

- wie Modelle verwendet werden,
- wie TSF aufgebaut ist,
- wie Scheduling Trees gelesen werden,
- wie Fehler analysiert werden,
- wie Monolith-Cluster funktionieren,
- wie Ergebnisse reproduziert werden.

KORA folgt dem Prinzip:

    Code is not the system.  
    Structure + Documentation = System.

### 44.2 Dokumentationsschichten

KORA besitzt vier Ebenen der Dokumentation:

1. **High-Level Overview**
   - Einführung
   - Motivation
   - deterministische Philosophie
   - Anwendungsbereiche  

2. **Architecture Specification**  
   (Kapitel 1–43)  
   - Hardware  
   - Compiler  
   - TSF  
   - Scheduling Trees  
   - DMA  
   - Fabric  
   - Cluster  
   - Monitoring  
   - Governance  

3. **Simulation & Reference Framework**  
   - Simulator  
   - TSF-Validator  
   - numerische Profile  
   - Golden Runs  
   - Testsysteme  

4. **Praktische Nutzer-Dokumente**
   - Tutorials  
   - API-Docs (HAPI, SCI)  
   - Python-Integration  
   - Workflow-Beispiele  
   - HPC/Cloud Integration  

Diese vier Ebenen bilden die vollständige Wissensarchitektur.

### 44.3 Versionierung

KORA nutzt eine deterministische Versionierungsstrategie:

- Architectural Version  
- Compiler Version  
- TSF Version  
- Documentation Version  

Beispiel:

    Architecture: M3
    Compiler: SCI v1.2
    TSF: v1.0
    Documentation: 2.0

Versionen ändern sich nur bei substanziellen Änderungen.  
Die deterministische Basis bleibt unverändert.

### 44.4 Zitier- und Referenzmodell

Für wissenschaftliche Arbeiten existiert ein klarer Zitierstandard:

- KORA als Architektur
- TSF-Spezifikation
- SCI-Compiler
- Golden Runs
- Referenz-Simulationen

Empfohlener Zitierstil:

    KORA Architecture Specification, Version 2.0 (2025).  
    OSF Repository: <osf.io/...>.

### 44.5 Langzeitarchitektur des Wissens

KORA stellt sicher, dass:

- Dokumente langfristig verständlich bleiben,
- alle TSF-Modelle archiviert werden,
- alle Simulationen reproduzierbar sind,
- wissenschaftliche Ergebnisse dauerhaft abrufbar bleiben.

Dazu gehören:

- OSF als Wissensspeicher,
- Zenodo DOI für jede Version,
- GitHub für Compiler und Simulator,
- interne Referenz-Datenbanken für Golden Runs.

### 44.6 Dokumentationsprinzipien

Dokumentation folgt fünf Kernregeln:

1. **Klarheit über Natürlichkeit**  
   – keine unnötige Komplexität  

2. **Technische Präzision über Prosa**  
   – deterministische Aussagen  

3. **Struktur über Stil**  
   – Dokumentation spiegelt Architektur  

4. **Reproduzierbarkeit über Rhetorik**  
   – jede Aussage muss überprüfbar sein  

5. **Langzeitlesbarkeit über kurzzeitige Trends**  
   – Markdown, kein proprietäres Format  

### 44.7 Deep Documentation: technisch + narrativ

KORA benötigt zwei Dokumentationsmodi:

#### (A) Technische Dokumentation  

- TSF  
- Scheduling Trees  
- DMA  
- Fabric  
- Hardwareprofile

#### (B) Wissenschaftliche Dokumentation  

- Motivation  
- Methodik  
- Anwendungsfälle  
- Vergleich mit HPC/GPU  
- Energieprofile  
- Validierungsmodelle

Beide zusammen erlauben eine vollständige Einordnung.

### 44.8 Veröffentlichungskanal: OSF & Zenodo

KORA wird vollständig veröffentlicht über:

- **OSF** (strukturierte Projektseite)  
- **Zenodo** (versionierte Releases mit DOI)  
- **GitHub** (Compiler & Simulator Quellcode)

Ein wissenschaftlicher Release umfasst:

- Architektur-Spezifikation  
- Simulation Framework  
- Golden Runs  
- Testdaten  
- Modelle  
- Lizenzierung  

### 44.9 Dokumentationspflege und Governance

Die Dokumentation wird gepflegt durch:

- Architecture Stewards
- Compiler Stewards
- Scientific Review Board

Pflegeprozess:

1. Proposal der Änderung  
2. Diskussion  
3. deterministische Prüfung  
4. Versionierung  
5. Release  

Damit bleibt KORA konsistent.

### 44.10 Warum Dokumentation Teil der Architektur ist

Weil KORA deterministisch ist, muss auch die Dokumentation deterministisch sein:

- keine Widersprüche  
- keine dynamischen Verhaltensbeschreibungen  
- klare Verantwortung  
- reproduzierbares Wissen  

Dokumentation IST ein Systemteil — nicht Zubehör.

### 44.11 Fazit

Kapitel 44 fasst die gesamte Wissensarchitektur von KORA zusammen.  
Durch strukturierte Dokumentation, offene Veröffentlichung und klare Versionierung wird KORA:

- verständlich,
- überprüfbar,
- wissenschaftlich nutzbar,
- langfristig stabil,
- institutionell vertrauenswürdig.

Dokumentation wird zu einem tragenden Element der deterministischen Architektur.

---

## 45. Applied KORA: Scientific & Industrial Use Cases
(CFD, KI, Big Data, Materialwissenschaften, HPC)

Die deterministische KORA-Architektur ist universell einsetzbar – überall dort, wo strukturierte, intensive Rechnungen durchgeführt werden. 
Dieses Kapitel beschreibt die zentralen wissenschaftlichen und industriellen Einsatzbereiche von KORA. 
Die Beispiele zeigen, wie TSF, Scheduling Trees und deterministische Ausführung in der Praxis genutzt werden.

### 45.1 Grundprinzip: deterministisches Rechnen für reale Probleme

Viele wissenschaftliche und industrielle Probleme leiden unter:

- nichtdeterministischer Hardware,
- scheduling-bedingten Variationen,
- Cache- und Jittereffekten,
- numerischer Inkonsistenz,
- unzuverlässigen Benchmarks.

KORA eliminiert diese Probleme strukturell.  
Dadurch entstehen:

- präzise Zeitverläufe,
- reproduzierbare Ergebnisse,
- wiederholbare wissenschaftliche Runs,
- kontrollierte Multi-Run Pipelines,
- stabile Energieprofile.

Diese Eigenschaften sind in vielen Disziplinen direkt nutzbar.

### 45.2 Anwendungsbereich 1 – CFD & PDE (Strömungsmechanik, Physik, Ingenieurwissenschaften)

CFD ist prädestiniert für KORA:

- Stencils sind deterministisch,
- Ghost-Layer-Austausch ist exakt definierbar,
- iterative Lösungsschemata wiederholen sich perfekt,
- numerische Fehler lassen sich isolieren.

Beispiele:

1. **Navier-Stokes 3D**
    - deterministische Iterationsschritte  
    - exakte Reduktionspfade für Druckkorrekturen  

2. **Finite-Element-Methoden**
    - deterministische Assembly  
    - deterministische Matrix-Vektor-Multiplikationen  

3. **Wärmetransport / Turbulenzmodelle**
    - identische Ergebnisse bei Multi-Run Pipelines  

Vorteile:

- perfekte Reproduzierbarkeit,
- bessere Debugbarkeit,
- stabile Energieprofile,
- verlässliche Vergleichbarkeit.

### 45.3 Anwendungsbereich 2 – KI / Deep Learning

KI-Modelle sind empfindlich gegenüber Nichtdeterministik:

- Floating-Point-Varianz,
- Race Conditions in Reduktionen,
- atomare Operationen,
- nichtdeterministische Summationsreihenfolgen.

KORA erzeugt:

- identische Gradientenläufe,
- identische Gewichte,
- identische Loss-Kurven,
- perfekte Trainingsreproduzierbarkeit.

Beispiele:

1. **BERT / Transformer-Modelle**
    - deterministische MatMul-Blöcke  
    - deterministische Attention-Reduktionen  

2. **Diffusion Modelle**
    - deterministische Pipeline-Schritte  
    - Analyse stochastischer Fehler ohne Hardware-Rauschen  

3. **Vision-Modelle**
    - deterministische Convolutions  
    - stabile Feature-Maps  

Dies erleichtert:

- Forschung,
- Debugging,
- Peer Review,
- Optimierungsprozesse.

### 45.4 Anwendungsbereich 3 – Big Data & Analytics

Viele Big-Data-Systeme leiden unter:

- Stragglern,
- Shuffle-Jitter,
- nichtdeterministischen Aggregationen.

KORA strukturiert Daten deterministisch:

- feste Partitionen,
- statische Map/Reduce-Pfade,
- konstante Bandbreite,
- deterministische Aggregationen.

Beispiele:

1. **Sort/Merge / Agg Pipelines**  
2. **Streaming Analytics / Batch Analytics**  
3. **Graphverarbeitung (PageRank etc.)**  

Vorteile:

- keine Straggler,
- perfekte Wiederholbarkeit,
- präzise Skalierung.

### 45.5 Anwendungsbereich 4 – Materialwissenschaften

In der Materialforschung sind Simulationen oft:

- hochdynamisch,
- sensitiv,
- schwer reproduzierbar.

KORA bietet:

- deterministische Nachbarschaftslisten,
- deterministische Stencil-Operationen,
- exakte Kräfteberechnungen,
- ideale Bedingungen für molekulare Simulationen.

Dies verbessert die:

- wissenschaftliche Validität,
- Abgleichbarkeit,
- numerische Stabilität.

### 45.6 Anwendungsbereich 5 – Geophysik & Klimawissenschaften

Große Modelle benötigen:

- deterministische Ausführung über viele Knoten,
- stabile Reduktionspfade,
- perfekte Ghost-Layer-Konsistenz.

Beispiele:

1. **Klimamodelle**  
2. **Seismische Wellenausbreitung**  
3. **Geodynamik**  

KORA bietet:

- ideale deterministische Multi-Compute-Strukturen,
- hundertprozentige Reproduzierbarkeit für Jahrzehnte.

### 45.7 Anwendungsbereich 6 – Industrie & Engineering

Industrieprozesse profitieren direkt:

- Prozesssimulation,
- Qualitätskontrolle,
- Energieoptimierung,
- deterministische Modelle für Audit-Prozesse.

Beispiele:

- Strömungsoptimierung von Produkten  
- Materialfehleranalyse  
- Energieverteilungssysteme  
- Echtzeit-Diagnosesysteme  
- deterministische Digital Twins  

### 45.8 Energieeffizienz-Vorteile in realen Anwendungen

Durch konstante Leistungsaufnahme:

- keine Boost-Spikes,
- kein Throttling,
- stabile Kühlung,
- berechenbare Energieprofile.

KORA-Cluster haben:

- planbare Energiekosten,  
- deterministen Energiebedarf pro Run,  
- präzise Leistungsprofile.

Dies ist für:

- Rechenzentren,
- Forschungseinrichtungen,
- Unternehmen

ein entscheidender Vorteil.

### 45.9 Multi-Run & Langzeitstudien

Viele Studien benötigen:

- tausende identische Runs,
- lange Zeiträume,
- historische Vergleichbarkeit,
- präzise Fehlerquantifizierung.

KORA liefert:

    identische Ergebnisse in jedem Run.

Dies erlaubt:

- neue Forschungsarten,
- bisher unmögliche Vergleichsstudien,
- langfristige wissenschaftliche Projekte.

### 45.10 Warum deterministische Architektur in der Praxis überlegen ist

Weil:

- jede Wissenschaftlichkeit auf Wiederholbarkeit basiert,
- jede Optimierung Vergleichbarkeit benötigt,
- jede Simulation Stabilität verlangt.

KORA löst systemisch:

- Varianzprobleme  
- Messunsicherheiten  
- HPC-Jitter  
- KI-Instabilitäten  
- Big-Data-Straggling  
- Cluster-Jitter  
- numerische Drift  

und bietet stattdessen:

- mathematische Klarheit,
- physikalische Stabilität,
- methodische Transparenz.

### 45.11 Fazit

KORA ist ein universelles deterministisches Rechensystem, das in Wissenschaft, Industrie, KI, Big Data und Simulationen gleichermaßen einsetzbar ist.  
Die deterministische Natur des Monolithen erzeugt:

- Stabilität,  
- Wiederholbarkeit,  
- wissenschaftliche Zuverlässigkeit,  
- energieeffiziente Performance,  
- jahrzehntelange Vergleichbarkeit.

KORA ist nicht nur eine Architektur —  
es ist ein Werkzeug für echte wissenschaftliche und industrielle Präzision.

---

## 46. Sustainability, Efficiency & Long-Term Operational Impact
(Energieeffizienz, Betriebsökonomie, ökologische Wirkung)

KORA ist nicht nur eine technische Architektur, sondern ein Modell für nachhaltiges wissenschaftliches Rechnen. 
Durch deterministische Hardware, statische Leistungsaufnahme und reproduzierbare Abläufe entsteht ein System, das grundlegende ökologische, ökonomische und operationelle Vorteile bietet.

Dieses Kapitel beschreibt die langfristigen Auswirkungen und Nachhaltigkeitsmerkmale.

### 46.1 Grundprinzip: Nachhaltigkeit durch deterministische Struktur

Klassische HPC- und KI-Systeme verschwenden Energie durch:

- Boost-Mechanismen,
- variablen Takt,
- Cache-Jitter,
- ineffiziente Scheduling-Effekte,
- verteilte Straggler,
- mehrfach ausgeführte Runs wegen Nichtdeterministik.

KORA eliminiert diese systemischen Ineffizienzen.

Prinzip:

    Wenn die Architektur deterministisch ist, ist auch Energie deterministisch.

### 46.2 Energieeffizienz der Ausführung

Die Leistungsaufnahme des Monolithen ist:

- konstant,
- stabil,
- thermisch vorhersehbar,
- ohne Boost-Spitzen,
- ohne Throttling.

Daraus folgen:

- präzise Energiekalkulation,
- 30–100× geringere Overhead-Verluste (im Vergleich zu GPU/CPU),
- extrem hohe energetische Effizienz pro ausgeführtem Modell.

Beispiel:

    Energieverbrauch = konstante Leistung × deterministische Zeit

Keine Varianz, keine Unsicherheit.

### 46.3 Reduktion von Rechenabfällen

In klassischen KI-/HPC-Systemen wird Energie verschwendet durch:

- instabile Runs,
- erneute Läufe wegen Floating-Point-Varianz,
- abweichende Optimierpfade,
- Mischpräzisionsfehler,
- Straggler-Neustarts,
- unvorhersehbare Scheduling-Effekte.

Bei KORA entfällt dies komplett:

    Jeder Run liefert exakt dasselbe Ergebnis.

Damit reduziert KORA wissenschaftlichen Rechenabfall strukturell.

### 46.4 Hardware-Lebensdauer & thermische Stabilität

KORA-Monolithen arbeiten ohne:

- Boost-Spannungen,
- variable Taktdomains,
- sprunghafte thermische Peaks.

Dadurch:

- geringere Materialbelastung,
- längere Lebensdauer,
- reduzierte Fehleranfälligkeit,
- weniger Kühlbedarf.

Nachhaltigkeitsvorteil:

    Hardware bleibt wissenschaftlich nutzbar, selbst nach vielen Jahren.

### 46.5 Reduktion der Rechenzentrumskomplexität

Da der Monolith:

- deterministisch,
- statisch,
- OS-frei

arbeitet, entfällt:

- vielschichtiger Software-Stack,
- komplexes Scheduling,
- dynamisches Lastmanagement,
- Hypervisor-/Container-Overhead.

Dies senkt:

- Stromkosten,
- Wartung,
- Upgrade-Pfade,
- Ausfallrisiken.

### 46.6 Vergleich mit klassischen Rechenarchitekturen

#### GPU/TPU:

- hohe Varianz,
- dynamische Frequenzsprünge,
- Overhead 40–60 %,
- schwer kalkulierbare Energie.

#### CPU:

- enormer OS- und Context-Overhead,
- nichtdeterministische Latenzen,
- starker Cache-Druck.

#### KORA:

- Overhead < 10 %,
- deterministischer Energiepfad,
- konstante Leistungsaufnahme,
- ideal für Langzeitprojekte,
- stabile Hardwareprofile.

### 46.7 Wissenschaftliche Nachhaltigkeit

Wiederholbarkeit ist wissenschaftlich essenziell:

- Klimamodelle,
- medizinische Simulationen,
- Materialforschung,
- numerische Solvers,
- KI-Modelle.

KORA bietet:

- perfekte Wiederholbarkeit über Jahrzehnte,
- nachvollziehbare Ergebnisse,
- stabil archivierbare TSF-Dateien.

Dies schafft:

    nachhaltige wissenschaftliche Infrastruktur.

### 46.8 Ökonomische Nachhaltigkeit

KORA reduziert Kosten durch:

- planbare Energieverbrauchsmuster,
- längere Hardwarelebensdauer,
- weniger Fehlerszenarien,
- geringeren Kühlbedarf,
- deterministische Laufzeiten (bessere Planung).

Zudem sinken operative Kosten:

- weniger Software-Stack,
- weniger Administratorstunden,
- weniger Debugging.

### 46.9 Skalierung ohne Energie-Explosion

KORA skaliert durch:

- deterministische Partitionierung,
- statische Fabric-Pfade,
- Multiplikation deterministischer Einheiten.

Dadurch bleibt Energie:

- linear,
- vorhersehbar,
- clusterfreundlich.

Keine exponentiellen Skalierungskurven wie bei KI-Clustern üblich.

### 46.10 Nachhaltige Rechenzentren

Für Rechenzentren ergibt sich:

- eindimensionale Kühlplanung (ohne Peaks),
- deterministische Stromlinien,
- stabile Redundanz,
- einfacher Lastenausgleich,
- verlässliche Kapazitätsplanung.

Ein KORA-Cluster kann geplant werden wie:

    ein präzises Energieinstrument, nicht wie ein chaotisches HPC-System.

### 46.11 Lebensdauer von Modellen und Simulationen

Weil TSF:

- stabil,
- abwärtskompatibel,
- archivierungsfähig

ist, überleben Modelle:

- Hardwaregenerationen,
- Softwaregenerationen,
- Rechenzentrumswechsel.

Nachhaltigkeit bedeutet hier:

    Ein Modell verliert seinen Wert nicht durch Infrastrukturwechsel.

### 46.12 Umweltwirkung

Die deterministische Eliminierung von Overhead reduziert:

- CO₂-Ausstoß,
- Materialverschleiß,
- Abwärme,
- Cluster-Strombedarf,
- Wiederholungsrechnungen,
- Rechenzeit.

Typische Schätzung:

    Reduktion 80–95 % Energieverbrauch pro problemgröße.

Dies ist ein einzigartiger Vorteil der deterministischen Architektur.

### 46.13 Fazit

KORA definiert Nachhaltigkeit nicht als Nebeneffekt, sondern als unmittelbares Ergebnis seiner Architektur.  
Durch:

- deterministische Ausführung,
- konstante Leistungsaufnahme,
- reproduzierbare Ergebnisse,
- lange Hardwarelebensdauer,
- niedrigen Overhead,
- stabile Rechenzentren,

entsteht ein System, das ökologisch, ökonomisch und wissenschaftlich nachhaltig ist.

Nicht nur schnell — sondern verantwortungsvoll.

---

## 47. Glossary of Terms 
(Technisches Glossar)

Das Glossar definiert alle zentralen Begriffe der KORA-Architektur, des Compiler-Stacks, der Scheduling-Modelle und des deterministischen Hardwaredesigns. 
Es dient als schnelle Referenz für Wissenschaftler, Entwickler und Reviewer.

#### **A**

**Active Tile**  
Teil eines Tiles, der aktuell eine Operation ausführt, im Gegensatz zu idle oder wait.

**Audit Log**  
Unveränderbares Log über jede TSF-Ausführung: Zeitprofile, DMA-Fenster, Memoryzugriffe, Energieprofil, Fehlerflags.

#### **B**

**Bank (Memory Bank)**  
Autarke Speicherbank mit fester Zugriffszeit; zentrale Einheit für deterministischen Speicherzugang.

**Bandwidth Determinism**  
Konstante Bandbreitenpfade ohne Jitter oder dynamisches Routing.

**Blockformat (KORA Block)**  
Feste Input- und Output-Datenblöcke (1–4 MB), die der Monolith direkt liest.

#### **C**

**CFD (Computational Fluid Dynamics)**  
Ein wichtiger wissenschaftlicher Anwendungsbereich von KORA.

**Cluster Fabric (CMF)**  
Deterministische Cross-Monolith-Fabric; steuert TDM-basierte Kommunikation zwischen Monolithen.

**Compute Phase**  
Ein Abschnitt im Scheduling Tree, in dem nur Rechenoperationen stattfinden.

**Compiler (SCI)**  
Übersetzt High-Level Modelle in deterministische TSF-Dateien.

#### **D**

**Deterministic Execution**  
Ausführung ohne Varianz: identische Ergebnisse, identische Zeit, identische Energie.

**DMA Window**  
Definierter Speichertransfer mit fester Größe, fester Reihenfolge, fester Zyklusdauer.

**Documentation Version**  
Versionsnummer der offiziellen KORA-Dokumentation.

#### **E**

**Energy Profile**  
Konstantes Leistungsprofil eines gesamten Runs: abgeleitet aus fester Leistung × deterministische Zeit.

**Execution Phase**  
Ein geordneter Schritt im Scheduling Tree (Compute, DMA, Reduction).

#### **F**

**Fabric Link**  
Verbindung zwischen Monolithen mit deterministischer Latenz.

**Formal Verification**  
Mathematische Prüfung, dass Scheduling Trees kollisionsfrei und widerspruchsfrei sind.

#### **G**

**Ghost Layer**  
Randbereiche eines Subdomains in CFD/PDE, die in festen Abfolgen ausgetauscht werden.

**Golden Run**  
Vollständig archivierter Referenzlauf: TSF, Inputs, Outputs, Telemetrie, Energieprofil.

#### **H**

**HAPI (High-Level API)**  
Frontend für Modellierung in Python/C++, welches TSF-kompatible Modelle generiert.

**Hybrid Model**  
Modell, das CPU/Host und Monolith kombiniert.

#### **I**

**Idle Tile**  
Ein Tile, das im aktuellen Scheduling Tree-Abschnitt nicht aktiv ist.

**Input Mapping**  
Zuordnung externer Datenformate zu KORA-Blockformaten.

#### **J**

**Jitter**  
Variation in Zeit oder Energie. In KORA: existiert nicht.

#### **K**

**KORA Monolith**  
Deterministische Recheneinheit mit festen Tiles, festen Memorybanks und fester DMA-Struktur.

**KORA Block**  
1–4 MB Blockformat für deterministische Datenübertragung.

#### **L**

**Latency (Deterministic)**  
Feste, unveränderliche Übertragungsverzögerung im Monolith oder in der Fabric.

**Load Phase**  
Scheduling-Abschnitt, in dem Eingabedaten in Memorybanks geladen werden.

#### **M**

**Memorybank**  
Getrennte Speicherbank mit festen Zugriffszeiten und deterministischen Zugriffspfaden.

**Model Partitioning**  
Aufteilung eines Modells in deterministische Subdomains/Tile-Gruppen.

**Monolith Cluster**  
Mehrere Monolithe, die über CMF verbunden sind.

#### **N**

**Numerical Profile**  
Fest definierter Satz an FP-Operationen und -Reihenfolgen.

**Non-Determinism (verboten)**  
Dynamische Variabilität in Ausführungsreihenfolgen; in KORA systemisch ausgeschlossen.

#### **O**

**Observability Anchors**  
Fixe Messpunkte im Scheduling Tree für Telemetrie.

**Output Writeback**  
Letzte Stufe eines Runs: deterministische Ausgabe über DMA-Fenster.

#### **P**

**Phase**  
Ein Teil des Scheduling Trees: Compute, DMA, Ghost Exchange, Reduction.

**Power Determinism**  
KORA-Eigenschaft: fix konstante Leistungsaufnahme während der gesamten Ausführung.

#### **Q**

**Queue (HPC)**  
Externes Scheduling-System (SLURM/PBS/LSF) für Host-Orchestrierung.

#### **R**

**Reduction Path**  
Deterministische numerische Reduktion (Summation, Aggregation, Scatter/Gather).

**Reproducibility**  
In KORA: bit-genaue, zeit-gleiche, energie-gleiche Wiederholung eines Runs.

#### **S**

**Scheduling Tree**  
Exakte deterministische Abfolge aller Rechen-, DMA- und Kommunikationsschritte.

**Soft-FP**  
Software-Floating-Point-Profil für kontrollierte numerische Reproduzierbarkeit.

**Simulator (Reference)**  
Referenzmodell, das identisches Verhalten wie die Hardware hat.

**Sustainability**  
Energieeffiziente, langlebige Architektur durch deterministische Mechanismen.

#### **T**

**Tile**  
Kleinste Recheneinheit im Monolith; führt deterministische Operationen aus.

**TSF (Tiled Scheduling Format)**  
Format zur vollständigen Beschreibung der deterministischen Ausführung.

**Telemetry**  
Deterministische Messdaten: Zeitprofile, Energie, DMA, Memory, Tileaktivität.

#### **U**

**Uniform Latency**  
Konstante, unveränderliche Latenzen über die gesamte Ausführung.

#### **V**

**Verification Layer**  
Mehrstufiges Validierungssystem für TSF, Scheduling Trees und Hardwarepfade.

#### **W**

**Workflow Integration**  
Anbindung an Snakemake, Nextflow, Airflow, SLURM etc. via Host-Orchestrierung.

#### **Z**

**Zero Jitter Architecture**  
KORA-Grundprinzip: kein Timing-Jitter, keine Varianz, keine dynamischen Effekte.

---

## 48. Acronyms & Abbreviations 
(Abkürzungsverzeichnis)

Dieses Kapitel listet alle in der KORA-Architektur verwendeten Abkürzungen auf. 
Es dient als schnelle Referenz für wissenschaftliche Leser, Entwickler, Reviewer und Rechenzentrumsoperatoren.

#### **A**
**API** – Application Programming Interface  
**AIMD** – Additive Increase / Multiplicative Decrease (nur im Vergleich zu TCP, nicht in KORA)  
**AVA** – Automated Validation Architecture  

#### **B**
**BD** – Big Data  
**BOM** – Bill of Materials  

#### **C**
**CFD** – Computational Fluid Dynamics  
**CMF** – Cluster Meta-Fabric (deterministische Cross-Monolith Fabric)  
**CPU** – Central Processing Unit  
**CWL** – Common Workflow Language  

#### **D**
**DMA** – Direct Memory Access  
**DL** – Deep Learning  

#### **E**
**E2E** – End-to-End  
**ETL** – Extract-Transform-Load  

#### **F**
**FEA** – Finite Element Analysis  
**FEM** – Finite Element Method  
**FP** – Floating Point  

#### **G**
**GPU** – Graphics Processing Unit  
**GPGPU** – General Purpose GPU  
**GFlop/s** – Milliarden Floating-Point-Operationen pro Sekunde  

#### **H**
**HAPI** – High-Level API (KORA Modellierungsinterface)  
**HPC** – High-Performance Computing  
**HDF5** – Hierarchical Data Format Version 5  

#### **I**
**IO** – Input/Output  
**IDE** – Integrated Development Environment  

#### **J**
**JSON** – JavaScript Object Notation  

#### **K**
**KORA** – *Kinetic-Oriented Reproducible Architecture*  
**KI** – Künstliche Intelligenz (AI)  

#### **L**
**LSF** – Load Sharing Facility (HPC Scheduler)  
**LLC** – Last Level Cache (nur im Vergleich mit CPU/GPU; nicht in KORA)  

#### **M**
**ML** – Machine Learning  
**MPI** – Message Passing Interface (nur Referenz; KORA ersetzt MPI durch determ. Fabric)  

#### **N**
**NIC** – Network Interface Controller  
**NLP** – Natural Language Processing  

#### **O**
**OS** – Operating System  
**OSF** – Open Science Framework  

#### **P**
**PDE** – Partial Differential Equation  
**PFlop/s** – Billiarden Floating-Point-Operationen pro Sekunde  
**PBS** – Portable Batch System (HPC Scheduler)  

#### **Q**
**QoS** – Quality of Service (nur extern relevant, nicht im Monolith)  

#### **R**
**RDMA** – Remote Direct Memory Access  
**ROC** – Rate of Convergence  

#### **S**
**SCI** – Scheduling & Compilation Interface (KORA Compiler)  
**SLURM** – Simple Linux Utility for Resource Management  
**S3** – Simple Storage Service (Object Store)  

#### **T**
**TSF** – Tiled Scheduling Format  
**TDP** – Thermal Design Power  

#### **U**
**UTC** – Coordinated Universal Time  

#### **V**
**VTK** – Visualization Toolkit  
**VHDL** – Hardware Description Language  
**Verilog** – Hardware Description Language  

#### **W**
**WLF** – Workload Factor (Simulation)  
**WIP** – Work In Progress  

#### **Z**
**ZJ** – Zero Jitter (KORA Architekturprinzip)  

### 48.1 Fazit

Dieses Abkürzungsverzeichnis bildet den Abschluss des Hauptteils der technischen Dokumentation. 
Es ermöglicht eine schnelle Orientierung über alle in KORA verwendeten technischen Begriffe und stellt sicher, 
dass die Dokumentation sowohl strukturell als auch sprachlich vollständig ist.

---

## 49. Appendix A: Mathematical Foundations of Deterministic Scheduling
(Formale Grundlagen, Scheduling-Modelle, Invarianten)

Dieses Kapitel definiert die mathematischen Grundlagen, die die deterministische Ausführung von KORA ermöglichen. 
Es dient als wissenschaftlicher Unterbau der gesamten Architecture Specification und richtet sich an Leser mit mathematischem, HPC- oder Compiler-Hintergrund.

### 49.1 Motivation

KORA basiert auf der Idee, dass jede Berechnung strukturell vorhersagbar wird, wenn:

1. alle Operationen geordnet sind,  
2. alle Speicherzugriffe eindeutig definiert sind,  
3. alle Kommunikationspfade kollisionsfrei sind,  
4. keine dynamischen Ereignisse auftreten.  

Damit entsteht eine **mathematisch beschreibbare Ausführung**.

### 49.2 Formale Definition: Scheduling Tree

Ein Scheduling Tree ist ein gerichteter, azyklischer Baum:

    T = (V, E)

mit:

- V  = Phasen (Compute, DMA, Reduction, Ghost Exchange)  
- E  = gerichtete Kanten (Ausführungsabhängigkeiten)

Eigenschaften:

1. **Azyklizität**  
       ∄ Pfad v → … → v  
   Keine zyklischen Abhängigkeiten.

2. **Ordnungsrelation**  
       ∀ (u → v) ∈ E : u < v  
   Jede Phase hat eine eindeutige Position.

3. **Vollständigkeit**  
       Jede Operation gehört genau zu einer Phase.

### 49.3 Zeitinvarianz

Für jede Phase p ∈ V gilt:

    T(p) = konstante Anzahl Zyklen

Der gesamte Run ist die Summe aller Phasen:

    T_total = Σ T(p)

Keine Phase hat Varianz.  
Damit ergibt sich:

    Var(T_total) = 0

### 49.4 Speicherinvarianz

Für jede Memorybank B_i gilt:

1. **Feste Zugriffsreihenfolge**  
       A(B_i) = [a₁, a₂, …, aₙ]  
   Reihenfolge ist invariant.

2. **Feste Latenz**  
       L(B_i) = konst.

3. **Konfliktfreiheit**  
       ∀ Paare (a_k, a_m) : keine Überschneidung im selben Zyklus.

Damit ist jede Speichertransaktion deterministisch.

### 49.5 DMA-Invarianz

Ein DMA-Fenster W ist definiert als:

    W = (src, dst, size, start_cycle, end_cycle)

Invarianten:

- size ist konstant  
- start_cycle ist konstant  
- end_cycle ist konstant  

Daraus folgt:

    Dauer(W) = end_cycle – start_cycle = konst.

DMA ist vollständig kollisionsfrei, da:

    ∀ W_i, W_j : Zeitintervalle disjunkt

### 49.6 Reduktionsinvarianz

Numerische Reduktion ist ein deterministischer Baum:

    R = (N, K)

mit:

- N = numerische Knoten (FP-Operationen)
- K = deterministische Reihenfolge

Eigenschaften:

- Reihenfolge ist fest
- keine atomaren Race Conditions
- kein paralleler Summations-Jitter

Numerischer Wert:

    result = f(f(f(a1, a2), a3), …, an)

statt:

    nichtdeterministische parallele Reduktion

### 49.7 Kommunikationsinvarianz (Cluster Fabric)

Für Fabric-Pfade zwischen Monolithen gilt:

    latency = konst.
    jitter = 0
    route = fix definiert
    slot = fix zugeordnet

Formale Eigenschaft:

    ∀ Pakete p_i, p_j : arrival(p_i) - arrival(p_j) = konst.

Damit existiert keine Reihenfolgenunsicherheit.

### 49.8 Korrektheitsinvarianten der gesamten Architektur

Für die gesamte Ausführung gelten fünf zentrale Invarianten:

#### (1) Deterministische Reihenfolge

    ∀ u, v ∈ V : Ordnung(u, v) unveränderlich

#### (2) Deterministische Zeit

    T_total ist invariant über alle Läufe

#### (3) Deterministischer Speicher

    Zugriffsmuster sind eindeutig definiert

#### (4) Deterministische Kommunikation

    Fabric-Latenz und Slotzuweisung sind fix

#### (5) Numerische Deterministik

    FP-Reihenfolge ist unveränderlich

Dies bildet den mathematischen Kern von KORA.

### 49.9 Formale Aussage über Reproduzierbarkeit

Sei R ein vollständiger KORA-Run:

    R = (TSF, Input, Output, Telemetry)

Dann gilt:

    ∀ R₁, R₂ mit identischem TSF und Input:
        Output(R₁) = Output(R₂)
        Time(R₁)   = Time(R₂)
        Energy(R₁) = Energy(R₂)
        Telemetry(R₁) = Telemetry(R₂)

Dies ist der mathematische Beweis für:

    bitgenaue, zeitgleiche, energiegleiche Reproduzierbarkeit.

### 49.10 Relevanz für wissenschaftliche Anwendungen

Wissenschaft profitiert unmittelbar von diesen Invarianten:

- KI-Training ohne numerische Varianz  
- CFD ohne Iterationsdrift  
- Big-Data ohne Straggler-Effekte  
- Materialsimulationen mit stabilen Kraftmodellen  
- geophysikalische Modelle mit konstanter Stabilität  

Die deterministische Architektur wird damit zu einem mathematischen Werkzeug.

### 49.11 Fazit

Die deterministische Natur von KORA ist nicht zufällig, sondern mathematisch konstruiert:  
durch Scheduling Trees, Speicherinvarianten, DMA-Invarianten, numerische Pfade und deterministische Kommunikation.

Kapitel 49 bildet die formale Grundlage, auf der alle vorherigen Kapitel stehen —  
und zeigt:  
    Determinismus ist mathematisch erzwingbar.

---

## 50. Appendix B: TSF Format Specification
(Definition, Struktur, Semantik, Validierung)

Dieses Kapitel definiert das TSF-Format formell und vollständig. TSF ist das zentrale Austauschformat
zwischen Modell, Compiler, Simulator und KORA-Monolith.  
Es beschreibt deterministisch jede Operation, jede Phase, jede Speicherbewegung und jeden Kommunikationsschritt.

TSF ist stabil, versioniert, abwärtskompatibel und wissenschaftlich archivierbar.

### 50.1 Zweck und Eigenschaften von TSF

TSF ist ein strukturiertes, deterministisches Ausführungsmodell mit folgenden Eigenschaften:

- abstrakt, nicht hardwarekonkret  
- vollständig deterministisch  
- kompakt (typisch wenige MB)  
- versioniert  
- validierbar (formale Regeln)  
- geeignet für Langzeitarchivierung  
- unabhängig von Compiler- oder Hardwaregenerationen  

### 50.2 TSF – Gesamtstruktur

Ein TSF besteht aus fünf Hauptsektionen:

1. **Header**  
2. **Topology**  
3. **Phases**  
4. **Memory Layout**  
5. **DMA / Fabric / Reduction Blocks**

Formale Struktur:

    TSF = {
        header: {...},
        topology: {...},
        phases: [...],
        memory: {...},
        ops: {
            dma: [...],
            compute: [...],
            reduction: [...],
            communication: [...]
        }
    }

### 50.3 Section 1 – Header

Der Header beschreibt:

- TSF-Version  
- Compiler-Version  
- Architekturziel (z. B. M1/M2/M3)  
- numerisches Profil  
- Metadaten  

Beispiel:

    header:
        tsf_version: 1.0
        compiler_version: 1.2
        target_architecture: M3
        numeric_profile: C
        model_name: "navier_stokes_3d"
        timestamp: "2025-11-20T17:42:00Z"

### 50.4 Section 2 – Topology

Die Topology definiert:

- Tileanzahl  
- Gruppierungen  
- Memorybanks  
- Fabric-Links  
- Clusterkonfiguration  

Beispiel:

    topology:
        tiles: 512
        tile_groups: 32
        memory_banks: 128
        banks_per_tile_group: 4
        fabric_links: 16
        cluster_id: 0

### 50.5 Section 3 – Phases

Die Phasen bilden den Scheduling Tree.  
Jede Phase ist ein deterministischer Schritt:

- compute  
- dma  
- reduction  
- ghost exchange  
- barrier (falls nötig, aber deterministisch)

Formale Struktur:

    phases:
        - id: 0
          type: "dma_in"
          start_cycle: 0
          end_cycle: 412
        - id: 1
          type: "compute"
          start_cycle: 413
          end_cycle: 1024
        - id: 2
          type: "reduction"
          start_cycle: 1025
          end_cycle: 1378

Phasen sind strikt geordnet:

    phases[i].end_cycle <= phases[i+1].start_cycle

### 50.6 Section 4 – Memory Layout

Der Memory-Layer definiert:

- Zuordnung von Datenblöcken zu Memorybanks  
- Offsets  
- Alignment  
- deterministische Partitionierung  

Struktur:

    memory:
        blocks:
            - id: 0
              bank: 17
              offset: 4096
              size: 131072
            - id: 1
              bank: 17
              offset: 135168
              size: 131072

### 50.7 Section 5 – Operation Blocks (ops)

#### 50.7.1 DMA-Operationen

Struktur:

    dma:
        - id: 0
          phase: 0
          src: "host"
          dst: "bank_17"
          size: 2MB
          start_cycle: 0
          end_cycle: 412

Deterministische Regeln:

- keine Überlappung mit anderen DMA-Fenstern  
- feste Start-/Endzyklen  
- konstante Größe  

#### 50.7.2 Compute-Operationen

Struktur:

    compute:
        - id: 5
          phase: 1
          tile_group: 7
          op: "matmul"
          input_blocks: [0, 1]
          output_block: 2

Compute-Operationen sind rein lokal (keine Race Conditions).

#### 50.7.3 Reduction-Operationen

Struktur:

    reduction:
        - id: 11
          phase: 2
          path: "deterministic_tree"
          inputs: [2,3,4]
          output: 5

Regeln:

- keine atomaren parallelen Summationen  
- deterministischer Baum  
- feste Reihenfolge  

#### 50.7.4 Communication (Fabric)

Struktur:

    communication:
        - id: 20
          phase: 14
          src_monolith: 0
          dst_monolith: 3
          block: 7
          slot: 2
          latency: 3

Regeln:

- feste Slotzuweisung  
- deterministische Latenz  
- kein dynamisches Routing  

### 50.8 Validierungsregeln (formal)

TSF ist nur gültig, wenn alle folgenden Bedingungen erfüllt sind:

1. **Kein Zyklus im Phase-Graphen**  
2. **Keine DMA-Überlappung**  
3. **Keine Memorybank-Kollisionen**  
4. **Deterministische Reduktion**  
5. **Fabric-Pfade eindeutig**  
6. **keine nichtdefinierten Felder**  
7. **Versionskompatibilität gesichert**  

Der Validator prüft diese Regeln mathematisch.

### 50.9 TSF-Versionierung

TSF ist unabhängig von:

- Compiler-Version  
- Monolith-Generation  
- High-Level Modell

Versionierung:

    TSF v1.0 – Basisspezifikation  
    TSF v1.1 – Erweiterungen, vollständig abwärtskompatibel  
    TSF v2.0 – optional, erweitert, niemals brechend  

Wissenschaftlich bedeutet dies:

    Ein TSF aus dem Jahr 2025 muss auf einem Monolith aus 2045 laufen.

### 50.10 Minimal TSF Example

Ein vollständiges, minimales Beispiel:

    header:
        tsf_version: 1.0
        model_name: "minimal"
    topology:
        tiles: 4
        memory_banks: 8
    phases:
        - id: 0
          type: "compute"
          start_cycle: 0
          end_cycle: 12
    memory:
        blocks:
            - id: 0
              bank: 1
              offset: 0
              size: 256
    ops:
        compute:
            - id: 0
              phase: 0
              tile_group: 0
              op: "add"
              input_blocks: [0]
              output_block: 0

### 50.11 Fazit

Das TSF-Format ist die formal definierte, deterministische Beschreibung jeder Ausführung eines Modells auf einem KORA-Monolithen.
Es bildet die Grundlage für:

- Hardwareausführung  
- Simulation  
- Validierung  
- wissenschaftliche Archivierung  
- langfristige Kompatibilität  

TSF ist das Herzstück der deterministischen KORA-Architektur.

---

## 51. Appendix C: Reference Simulator Architecture
(Software-Referenzmodell der deterministischen KORA-Hardware)

Der KORA-Referenzsimulator bildet das Verhalten eines Monolithen vollständig deterministisch nach.
Er ist nicht nur ein Entwicklungswerkzeug, sondern ein wissenschaftlicher Prüfstand, um:

- TSF-Dateien zu validieren,
- Scheduling Trees zu testen,
- numerische Profile zu prüfen,
- Hardwareverhalten zu replizieren,
- Regressionen zu erkennen.

Dieses Kapitel beschreibt Struktur, Module und Funktionsweise des Referenzsimulators.

### 51.1 Grundprinzipien des Simulators

Der Simulator erfüllt drei Kernaufgaben:

1. **Exakte funktionale Abbildung**  
   – alle Operationen, DMA-Fenster, Reduktionen, Speicherpfade

2. **Exakte zeitliche Abbildung**  
   – identische Zyklen wie die Hardware  
   – kein Jitter, keine Varianz

3. **Exakte numerische Abbildung**  
   – Floating-Point-Reihenfolgen  
   – deterministische Reduktionsbäume

Damit entsteht:

    Simulation == Hardware

Dies ist die oberste Validierungsregel.

### 51.2 Modularer Aufbau des Simulators

Der Simulator besteht aus fünf Hauptmodulen:

1. **TSF Parser**  
2. **Topology Engine**  
3. **Phase Executor**  
4. **Memory Model**  
5. **Telemetry Engine**

Struktur:

    simulator/
        parser/
        topology/
        executor/
        memory/
        telemetry/

### 51.3 Modul 1 – TSF Parser

Der Parser:

- liest das TSF (YAML/JSON),
- prüft Syntax,
- extrahiert Phasen,
- extrahiert Topologie,
- extrahiert DMA/Compute/Reduction-Blöcke.

Beispielalgorithmus:

    parse_header()
    parse_topology()
    parse_phases()
    parse_memory()
    parse_ops()

Der Parser erzeugt eine interne Struktur:

    TSFInternal = {
        header,
        phases,
        memory_blocks,
        ops_dma,
        ops_compute,
        ops_reduction,
        ops_communication
    }

### 51.4 Modul 2 – Topology Engine

Dieses Modul bildet die Hardwarestruktur ab:

- Tiles  
- Tile-Gruppen  
- Memorybanks  
- Fabric-Links  
- deterministische Pfade  

Die Topology Engine erzeugt:

    HardwareModel:
        tiles[]
        banks[]
        links[]
        groups[]

Alle Objekte sind deterministisch initialisiert.

### 51.5 Modul 3 – Phase Executor

Der Phase Executor ist das Herzstück des Simulators.

Er führt jede Phase exakt wie die Hardware aus:

1. **DMA In**  
2. **Compute Block**  
3. **Reduction Block**  
4. **Ghost Exchange**  
5. **DMA Out**

Für jede Phase gilt:

- feste Startzyklen,
- feste Endzyklen,
- keine Abweichung,
- deterministische Reihenfolge.

Die Simulationszeit wächst exakt:

    cycle ← cycle + (end_cycle - start_cycle)

### 51.6 Modul 4 – Memory Model

Das Memory-Modell enthält:

- deterministische Latenzen,
- feste Bankzuordnung,
- Konfliktfreiheit,
- konstante Zugriffszeiten.

Jeder Zugriff ist:

    (bank, offset, size, cycle)

Das Memorymodell garantiert:

    kein Cache,
    kein Prefetch,
    keine dynamischen Effekte.

### 51.7 Modul 5 – Telemetry Engine

Die Telemetrie verfolgt:

- Zeitprofile jeder Phase  
- DMA-Übertragungszeiten  
- Tile-Aktivität  
- Memoryzugriffe  
- numerische Reduktionsabläufe  
- Fabric-Nachrichten  

TelemetryOutput:

    telemetry = {
        T_phase[],
        T_dma[],
        T_reduction[],
        memory_accesses[],
        fabric_transfers[]
    }

Alle Werte müssen identisch zur Hardware sein.

### 51.8 Zyklusgenaue Simulation

Ein wesentliches Merkmal:

    Der Simulator zählt Zyklen.

Beispiel:

    Phase 0: cycles 0–412
    Phase 1: cycles 413–1024
    Phase 2: cycles 1025–1378

Damit können:

- Energieprofile berechnet werden,
- Zeitprofile verglichen werden,
- deterministische Regressionstests durchgeführt werden.

### 51.9 Numerisches Modell (Soft-FP / IEEE)

Der Simulator unterstützt:

- IEEE 754 (Hardwarepräzision)
- Soft-FP Profil C (vollständig deterministische Softwarearithmetik)

Soft-FP wird verwendet für:

- wissenschaftliche Archivläufe,
- Validierung,
- Vergleich unterschiedlicher Hardwaregenerationen.

Numerische Operationen werden als deterministische Bäume ausgeführt.

### 51.10 Validierungsmodus

Der Simulator besitzt einen Validation Mode:

- prüft alle TSF-Invarianten,
- prüft Scheduling Trees,
- prüft Bankkollisionen,
- prüft deterministische Reduktionen,
- prüft Fabric-Pfade.

Validation Output:

    errors[]
    warnings[]
    invariants_passed[]

Wenn Fehler auftreten:

    TSF is invalid.

### 51.11 Regressionstests

Der Simulator unterstützt Regressionstests:

- Vergleich zweier Telemetriedateien,
- Vergleich zweier Output-Datensätze,
- Vergleich zweier Energieprofile,
- Vergleich zweier numerischen Resultate.

Regel:

    Wenn irgendetwas abweicht → deterministischer Fehler.

Regressionen sind sofort identifizierbar.

### 51.12 Integration mit Host-Systemen

Der Simulator wird genutzt:

- als Pre-Deployment-Test,
- in CI/CD Pipelines,
- in Forschungseinrichtungen,
- für TSF-Verifikation,
- für Debugging.

CI/CD-Beispiel:

    tsf → simulator → telemetry → compare → pass/fail

### 51.13 Beispiel eines vollständigen Simulationslaufs

Ablauf:

    load TSF  
    validate TSF  
    initialize topology  
    cycle = 0  
    for phase in phases:
        execute(phase)
        log telemetry  
    output results  
    write telemetry  
    verify invariants  
    exit  

Der gesamte Ablauf ist deterministisch.

### 51.14 Referenzimplementierung

Die offizielle Referenzimplementierung:

- Python (klar lesbar)
- deterministisches Soft-FP
- identisches Scheduling-Verhalten
- identisches Memorymodell
- identische DMA-Logik

Sie dient als:

- Goldstandard  
- Testbasis  
- Kompatibilitätsmodel  
- wissenschaftliche Dokumentation  

Hardware darf nie vom Simulator abweichen.

### 51.15 Fazit

Der KORA-Referenzsimulator ist eine vollständig deterministische Softwareabbildung des Monolithen.  
Er bildet:

- Zeit,
- Numerik,
- Speicher,
- Fabric,
- Reduktionen,
- DMA,
- Telemetrie

exakt ab.

Der Simulator ist damit:

- Validierungswerkzeug,  
- wissenschaftliches Messinstrument,  
- Archivierungsbasis,  
- Integrationsschicht,  
- Garant für Hardwaretreue.

Er ist der mathematische und technische „Beweis“, dass KORA deterministisch ist.

---

## 52. Appendix D: Project Structure & Repository Layout
(Ordnerstruktur, Dateien, Versionierung, Golden Run Archivierung)

Dieses Kapitel definiert die empfohlene Struktur eines vollständigen KORA-Projekts.  
Die Struktur ist für wissenschaftliche Veröffentlichungen (OSF, Zenodo),  
für Implementierungen (GitHub)  
und für interne Forschungsgruppen identisch.

Ziel:  
    Jedes KORA-Projekt soll klar, reproduzierbar und langfristig verständlich sein.

### 52.1 Grundprinzipien eines KORA-Repositories

Ein KORA-Projekt muss:

1. **deterministische Ausführung dokumentieren**,  
2. **TSF-Dateien klar ablegen**,  
3. **Simulationsergebnisse archivieren**,  
4. **Golden Runs unveränderlich speichern**,  
5. **Dokumentation auf Markdown-Basis führen**,  
6. **Versionen klar trennen**,  
7. **komplett nachvollziehbar** bleiben – selbst nach Jahrzehnten.

Daraus folgt die empfohlene Struktur.

### 52.2 Top-Level-Struktur

Die Wurzel eines Projekts hat folgende Verzeichnisse:

    /
    ├── docs/
    ├── tsf/
    ├── models/
    ├── simulator/
    ├── runs/
    │    ├── golden/
    │    ├── validation/
    │    └── experiments/
    ├── metadata/
    ├── examples/
    ├── scripts/
    └── LICENSE

Diese Struktur ist minimal, aber ausreichend für vollständige wissenschaftliche Veröffentlichungen.

### 52.3 /docs – Dokumentation

    /docs
        01_Executive_Summary.md
        02_Architecture_Specification.md
        03_Simulation_Framework.md
        04_Use_Cases.md
        05_Methodology.md
        appendix/
            A_mathematics.md
            B_tsf_spec.md
            C_simulator.md
            D_project_structure.md

Eigenschaften:

- alle Dokumente in Markdown  
- nummeriert  
- eindeutig  
- versioniert  
- maschinenlesbar  
- langfristig stabil

### 52.4 /tsf – TSF-Dateien

    /tsf
        model1/
            model1_base.tsf
            model1_variantA.tsf
        model2/
            model2_small.tsf
            model2_large.tsf

Regeln:

- TSF-Dateien niemals verändern  
- Neue Versionen werden als neue Dateien gespeichert  
- TSF ist ein wissenschaftliches Archivformat  

TSF-Dateien können klein (10–50 KB) oder komplex (mehrere MB) sein.

### 52.5 /models – Modellquellcode

    /models
        python/
            navier_stokes.py
            bert_training.py
            bigdata_pipeline.py
        cxx/
            matmul.cpp
            stencil_solver.cpp
        domain_specific/
            pde/
            ml/
            analytics/

Hier liegen die Modelle, die später in TSF übersetzt werden.

### 52.6 /simulator – Referenzsimulator

    /simulator
        reference_simulator.py
        validation_tools.py
        telemetry_tools.py
        tests/
            tsf_validation_tests/
            regression_tests/
        examples/
            minimal_example/
            cfd_example/
            ml_example/

Wichtig:

- Simulator ist referenziell, nicht optimiert  
- Simulator ist Standard für Regressionstests  
- Alle TSF-Dateien müssen im Simulator ausführbar sein  

### 52.7 /runs – Ergebnisse, Golden Runs & Experimente

    /runs
        golden/
            navier_stokes/
                tsf/
                input/
                output/
                telemetry/
                metadata.json
            bert/
                tsf/
                input/
                output/
                telemetry/
                metadata.json
        validation/
            run_2025_11_20/
                tsf/
                result/
                compare.json
        experiments/
            cfd_param_sweep/
                params/
                results/
                telemetry/
            ml_lr_tests/

#### 52.7.1 Golden Runs

Golden Runs sind unveränderliche Referenzläufe:

- einheitliche Ordnerstruktur  
- TSF + Input + Output + Telemetry  
- Metadaten  
- Hashwerte  
- validiert  

Golden Runs sind das Fundament wissenschaftlicher Reproduzierbarkeit.

### 52.8 /metadata – Metadaten, DOI, Lizenz

    /metadata
        license.txt
        version.txt
        citations.json
        release_notes.md
        doi.txt

Besonders wichtig für OSF oder Zenodo:

- `doi.txt` enthält den DOI für Archivierung  
- `version.txt` enthält die Architekturversion  

### 52.9 /examples – Minimale & didaktische Beispiele

    /examples
        minimal/
            minimal.py
            minimal.tsf
            run.sh
        cfd/
        ml/
        bigdata/

Diese Beispiele erleichtern neuen Nutzern den Einstieg.

### 52.10 /scripts – Automatisierungs- & Hilfswerkzeuge

    /scripts
        generate_tsf.py
        run_simulator.sh
        compare_runs.py
        validate_all.sh

Scripts dienen als:

- CI/CD-Basis  
- Regressionstest-Pipeline  
- Automatisierungswerkzeuge  

### 52.11 Versionierungsstrategien für Repositories

KORA empfiehlt:

- Semantic Versioning für Dokumentation  
- TSF-Version nach Spezifikation  
- Simulator-Version separat  
- Modelle versionieren durch neue Ordner  

Beispiel:

    docs v1.1
    tsf format v1.0
    simulator v1.2

Alles bleibt voneinander entkoppelt.

### 52.12 Archivierung auf OSF / Zenodo

Standard-Archiv:

    osfproject/
        docs/
        tsf/
        golden_runs/
        simulator/
        metadata/

Zenodo erhält:

- tar.gz der gesamten Struktur  
- DOI  
- version.txt  
- Lizenz  
- Prüfsummen  

Dadurch:

- vollständige Reproduzierbarkeit  
- langfristige Stabilität  
- wissenschaftliche Nachvollziehbarkeit  

### 52.13 Warum diese Struktur?

Weil KORA:

- deterministisch ist,
- langfristig archivierbar,
- wissenschaftlich orientiert,
- transparent,
- versionsstabil,
- reproduzierbar.

Ein KORA-Projekt ist kein Codehaufen,  
sondern ein **wissenschaftlicher Forschungsartefakt-Bestand**.

### 52.14 Fazit

Kapitel 52 definiert den strukturellen Aufbau jedes KORA-Projekts.  
Mit dieser Struktur können:

- Forschungsgruppen sauber arbeiten,  
- Rechenzentren integrieren,  
- Golden Runs archivieren,  
- TSF-Versionen stabil gepflegt werden,  
- wissenschaftliche Ergebnisse eindeutig referenziert werden.

KORA-Projekte bleiben damit über Jahrzehnte nutzbar und nachvollziehbar.

---

## 53. Appendix E: Reference Tables for Energy & Time Calculations
(Grundlagen, Tabellen, Parameterbereiche)

Dieses Kapitel enthält alle Referenztabellen für Zeit- und Energieabschätzungen, 
die in KORA-Dokumentation, Simulationen und Use Cases verwendet werden.  
Die Werte basieren auf öffentlich dokumentierten HPC-Systemen, KI-Clustern und
deterministischen Architekturparametern des Monolithen.

Sie dienen als stabile Grundlage für wissenschaftliche Vergleiche.

### 53.1 Grundgleichungen

Zeit:

    T_total = Σ T_phase_i

Energie:

    E_total = P_constant × T_total

Overheadklassifikation:

    overhead_classical = 40–60 %
    overhead_kora       = 5–10 %

Reduktionsfaktor:

    reduction_factor = (1 - overhead_kora) / (1 - overhead_classical)

Kommunikationszeit (klassisch):

    T_comm = latency × hops + message_size / bandwidth

Kommunikationszeit (KORA):

    T_comm_kora = message_size / deterministic_bandwidth

### 53.2 Reale Energie- und Leistungswerte (Referenzsysteme)

#### Tabelle 53.2-A – GPU-basierte Systeme (2023–2025)

| System                        | Power pro GPU | Training Power (8 GPUs) | Bemerkung                    |
|-------------------------------|---------------|---------------------------|----------------------------|
| Nvidia A100 40GB PCIe         | 250 W         | 2.0 kW                    | Standard HPC Node          |
| Nvidia A100 80GB SXM4         | 400 W         | 3.2 kW                    | Cloud-Trainingsknoten      |
| Nvidia H100 SXM5              | 700 W         | 5.6 kW                    | High-End KI-Training       |
| TPU v4 Pod (pro TPU)          | 350 W         | 2.8 kW (8er Gruppe)       | Google TPU cluster         |

#### Tabelle 53.2-B – CPU-basierte HPC-Systeme

| System                        | Power pro Node | Bemerkung                              |
|-------------------------------|----------------|----------------------------------------|
| AMD EPYC 7xx2                 | 450–600 W      | inkl. DRAM, NIC, Motherboard           |
| Intel Sapphire Rapids         | 500–700 W      | HPC/AI Hybrid                          |
| HPC Node (CPU + 2 GPUs)       | 1.2–1.8 kW     | typischer Clusterknoten                |

#### Tabelle 53.2-C – Rechenzentrumskonstanten (PUE)

| Einrichtungstyp               | PUE            | Bemerkung                              |
|-------------------------------|----------------|----------------------------------------|
| Hyperscaler                   | 1.10–1.25      | sehr effizient                         |
| Forschungseinrichtungen       | 1.20–1.40      | typische Werte                         |
| Industrierechenzentren        | 1.40–1.80      | ältere Infrastruktur                   |

### 53.3 KORA-Referenzwerte (Architektur M3)

#### Tabelle 53.3-A – Monolith-Leistungsparameter

| Parameter                       | Wert           | Bemerkung                       |
|---------------------------------|----------------|---------------------------------|
| Dauerleistung (P_constant)      | 1.2 kW         | keine Peaks, kein Boost         |
| Leistungsvariabilität           | ±0.5 %         | thermische Stabilität           |
| Takt                            | 1.5 GHz (eff.) | Takt ist konst. / jittersicher  |
| Tiles                           | 512            | M3-Referenzwert                 |
| Memorybanks                     | 128            | deterministische Latenz         |

#### Tabelle 53.3-B – Kommunikations- & DMA-Parameter

| Parameter                   | Wert                  | Bemerkung                         |
|-----------------------------|-----------------------|-----------------------------------|
| Deterministische Latenz     | 3 cycles              | CMF                               |
| DMA-Bandbreite              | 256 GB/s              | konstant                          |
| Fabric-Bandbreite           | 1.2 TB/s              | fixiert (TDM)                     |
| Jitter                      | 0                     | systemisches Architekturziel      |

### 53.4 Zeitabschätzungen für typische Workloads

#### BERT Training (Large)

| Phase                  | Zeit (klassisch) | Zeit (KORA) | Bemerkung                    |
|------------------------|------------------|-------------|------------------------------|
| Compute                | 80 %             | 80 %        | FLOP-dominiert               |
| Kommunikation          | 15 %             | 4–6 %       | deterministisch / TDM        |
| Overhead               | 40–60 %          | 5–10 %      | Scheduling, Jitter, Cache    |
| **Gesamt**             | 100 %            | ~65–75 %    | realistische Reduktion       |

#### Big Data Pipeline

| Phase                  | Zeit (klassisch) | Zeit (KORA) | Bemerkung                    |
|------------------------|------------------|-------------|------------------------------|
| Shuffle / Merge        | 50–70 %          | 10–20 %     | deterministische Partitionen |
| Compute                | 30–40 %          | 30–40 %     | unverändert                  |
| Overhead               | 20–50 %          | 5–10 %      | kein dynamischer Scheduler   |

#### CFD (3D Navier-Stokes)

| Phase                  | Zeit (klassisch) | Zeit (KORA) | Bemerkung                    |
|------------------------|------------------|-------------|------------------------------|
| Stencil Compute        | 60–70 %          | 60–70 %     | FLOP-limitiert               |
| Ghost Exchange         | 20–30 %          | 5–10 %      | deterministische Pfade       |
| Overhead               | 10–25 %          | 5–10 %      | deterministische Reihenfolge |

### 53.5 Energiekalkulationen (typisch)

#### Beispiel 1 – BERT Training Large

| System                               | Dauer    | Leistung | Energie      |
|--------------------------------------|----------|----------|--------------|
| GPU-Cluster (8× H100)                | 5–7 Tage | 5.6 kW   | ~700–940 kWh |
| GPU-Cluster + Overhead (Jitter, PUE) | –        | –        | 900–1300 kWh |
| **KORA M3**                          | 3–4 Tage | 1.2 kW   | 85–115 kWh   |

→ **Einsparung: 85–92 %**

#### Beispiel 2 – CFD Simulation Large

| System                              | Energie     |
|-------------------------------------|-------------|
| CPU/GPU HPC Node                    | 150–250 kWh |
| Klassischer Cluster (mehrere Nodes) | 300–600 kWh |
| **KORA M3**                         | 40–70 kWh   |

→ **Einsparung: 70–85 %**

### 53.6 Referenztabelle: Overhead-Faktoren

| Komponente                    | Klassisch          | KORA             |
|-------------------------------|--------------------|------------------|
| Scheduling Overhead           | 10–25 %            | 0 %              |
| OS/Kernel Overhead            | 5–15 %             | 0 %              |
| Cache/NUMA Variabilität       | 10–30 %            | 0 %              |
| Fabric-Jitter                 | 5–20 %             | 0 %              |
| Straggler                     | 5–20 %             | 0 %              |
| Overhead gesamt               | 40–60 %            | 5–10 %           |

### 53.7 Referenztabelle: Kommunikationsmodelle

#### Klassisches HPC-Modell (MPI)

    T = α + β·n + jitter

#### KORA-Modell (TDM Fabric)

    T = n / bandwidth  
    jitter = 0  
    α = konstante deterministische Latenz  

### 53.8 Referenztabelle: Faktoren für realistische Simulation

Für jede Simulation im Projekt gilt:

| Parameter                | Typische Werte        |
|--------------------------|-----------------------|
| Overhead_classical       | 0.40–0.60             |
| Overhead_kora            | 0.05–0.10             |
| P_monolith               | 1.2 kW                |
| FLOPs GPU Node           | 250–500 TFLOPs/s      |
| FLOPs KORA M3            | 50–80 TFLOPs/s (eff.) |
| sync_per_step klassisch  | 4–16                  |
| sync_per_step KORA       | 1–2                   |

### 53.9 Fazit

Kapitel 53 liefert die Referenztabellen, auf denen alle Energie- und Zeitmodelle im KORA-Projekt basieren.  
Diese Tabellen sind notwendig für:

- Simulationen,  
- Vergleichsstudien,  
- wissenschaftliche Publikationen,  
- Reproduzierbarkeit,  
- Modelle für Reviewer.

Sie bilden das quantitative Fundament der gesamten Spezifikation.

---

## 54. Appendix F: Deterministic Error Handling & Fault Models
(Fehlermodelle, Wiederherstellung, deterministische Reaktion)

KORA ist eine deterministische Architektur.  
Dies gilt nicht nur für korrekte Ausführung, sondern auch für Fehlersituationen.  
Selbst Fehler werden deterministisch behandelt, um:

- Reproduzierbarkeit,
- wissenschaftliche Integrität,
- Restart-Fähigkeit,
- Debugbarkeit,
- Auditierbarkeit

zu garantieren.

Dieses Kapitel beschreibt die Fehlermodelle und das deterministische Fehlerverhalten des Monolithen.

### 54.1 Grundprinzipien des Fehlerverhaltens

Fehler dürfen **niemals Nichtdeterminismus erzeugen**.  
Daher gelten folgende Regeln:

1. Fehler lösen keine dynamischen Alternativpfade aus.  
2. Fehler unterbrechen deterministisch die aktuelle Phase.  
3. Fehler werden vollständig geloggt, bevor der Zustand verändert wird.  
4. Fehler erzeugen keinen partiellen Output.  
5. Keine automatische Wiederholung innerhalb der Hardware.  
6. Recovery erfolgt ausschließlich auf Host-Ebene — strukturiert und deterministisch.  

Damit entsteht:

    deterministic error → deterministic response → deterministic recovery

### 54.2 Fehlertypen (klassifiziert)

KORA unterscheidet fünf Fehlerklassen:

#### (A) **Tile Errors**

- beschädigte Tile-Recheneinheit  
- fehlerhafte FP-Einheit  
- ungewöhnliche Tile-Aktivität (z. B. „always idle“)  

#### (B) **Memorybank Errors**

- Bitfehler  
- Bankzugriffsverletzungen (falsche Offsetgröße)  
- thermische Grenzverletzungen  

#### (C) **DMA Errors**

- unvollständige Übertragungen  
- fehlerhafte Blockgröße  
- Start/End-Zyklus passt nicht zu TSF  

#### (D) **Fabric Errors (Clusterbetrieb)**

- defekter Link  
- Slot-Kollision  
- Verbindungsabbruch zwischen Monolithen  

#### (E) **TSF Structural Errors**

- Scheduling-Tree-Inkonsistenz  
- Reduktionspfad verletzt  
- Memoryblock nicht definiert  
- Phase überschneidet sich mit einer anderen  

Alle werden deterministisch behandelt.

### 54.3 Fehlererkennung (Hardwareseitig)

Der Monolith besitzt keine adaptive Fehlerkorrektur wie klassische CPUs oder GPUs.  
Stattdessen:

- statische Grenzen,
- deterministische Sensorik,
- feste Prüfpfade.

Beispiele:

    TileError: FP Unit #37 reports mismatch @ cycle 142882
    MemoryError: bank 12 ECC mismatch
    DMAError: size mismatch (expected 2MB, got 2097024 bytes)
    FabricError: slot 5 collision detected

Diese Meldungen sind bitgenau reproduzierbar bei identischem Fehler.

### 54.4 Fehlerreaktion (Deterministisch)

Jeder Fehler führt zu einem standardisierten Ablauf:

1. **Freeze Phase**  
       Die Phase wird sofort angehalten.  
       Kein Fortschritt, kein Weiterlaufen.

2. **Safe State Export**  
       Telemetrie wird eingefroren und vollständig gesichert.

3. **Abort Signal**  
       Das TSF wird beendet — deterministisch, ohne Alternativpfade.

4. **Output Blocked**  
       Ausgabe erfolgt nicht, es entstehen keine halbvaliden Ergebnisse.

5. **Return to Host**  
       Der Host erhält vollständige Fehlerdaten.

Dies erzeugt **keine Varianz** im Verhalten.

### 54.5 Fehlerlogging

Fehler erzeugen ein vollständiges Audit:

    error:
        type: "MemoryBankError"
        phase: 17
        cycle: 884812
        bank: 12
        details: "ECC mismatch"
        tsf_hash: <...>
        input_checksum: <...>
        timestamp: <UTC>

Logging ist:

- vollständig,
- deterministisch,
- chronologisch korrekt.

### 54.6 Fehler auf Simulationsebene

Der Simulator bildet Fehler *identisch* ab:

- identische Phase stoppt,
- identische Meldungen,
- identische Telemetrie,
- identische Zyklusposition.

Beispiel:

    sim_error:
        tile: 7
        op: "matmul"
        cycle: 5221
        description: "operand invalid"

Simulationsfehler sind damit hardwareäquivalent.

### 54.7 Recovery-Modell (Host-seitig)

Der Monolith führt *keine* automatische Recovery durch.  
Der Host übernimmt deterministisch:

1. Prüfen des Fehlertyps  
2. Erneutes Zuweisen eines TSF zu einem anderen Monolithen  
3. OPTIONAL: Re-Anstoßen desselben TSF mit identischen Inputs  

Das Ergebnis ist deterministisch:

    identical input → identical result
    unless hardware fault → identical fault

Somit können Fehler reproduziert werden.

### 54.8 Multi-Run-Fehler in großen Experimenten

In großen wissenschaftlichen Experimenten mit vielen Läufen:

- Fehler betreffen nur den spezifischen Run,  
- Telemetrie erlaubt exakte Diagnose,  
- Pipeline kann nach Phase N neu starten.

Wichtig:

        Kein Fehler beeinflusst die Ergebnisse anderer Runs.

### 54.9 Clusterfehler (Fabric Errors)

Fehler im Fabric-TDM-System werden wie folgt behandelt:

1. Slot wird isoliert  
2. Nachricht wird verworfen  
3. Run wird deterministisch abgebrochen  
4. Telemetrie zeigt fehlerhaften Slot  

Host kann:

- Slot neu konfigurieren (deterministisch),  
- Monolith-Knoten austauschen,  
- Run verifizieren.

### 54.10 Vergleich: klassischer HPC-Fehler vs. KORA-Fehler

| Aspekt                  | Klassisches HPC         | KORA                         |
|-------------------------|--------------------------|------------------------------|
| Fehlerpfade             | nondeterministisch       | deterministisch             |
| Recovery                | komplex, dynamisch       | Host-gesteuert, fix         |
| Teilresultate           | möglich, aber inkonsistent | nie gespeichert           |
| Kommunikation           | jitteranfällig           | deterministisch             |
| Diagnose                | schwierig                | telemetriegestützt          |
| Reproduzierbarkeit      | oft unmöglich            | immer möglich               |

KORA vereinfacht Fehlermanagement systemisch.

### 54.11 Wissenschaftliche Vorteile deterministischer Fehler

Fehler sind:

- reproduzierbar,  
- messbar,  
- analysierbar,  
- vergleichbar.

Designfehler, numerische Instabilitäten und Hardwaredefekte können exakt isoliert werden.

Dies ist ein wesentlicher Vorteil in:

- Compilerentwicklung,  
- wissenschaftlicher Forschung,  
- numerischer Mathematik,  
- KI-Training,  
- CFD/PDE-Simulationen.

### 54.12 Formale Garantien für Fehlermodelle

KORA garantiert:

1. **Keine dynamischen Ausweichpfade**  
2. **Keine zeitlichen Schwankungen in Fehlerreaktionen**  
3. **Fehler sind deterministisch reproduzierbar**  
4. **Alle Fehler sind vollständig protokolliert**  
5. **Kein Zustand geht verloren**  
6. **Recovery erfolgt klar definiert über den Host**

Diese Regeln verhindern jede Form von nichtdeterministischem Verhalten.

### 54.13 Fazit

KORA behandelt Fehler nicht als Ausnahmefälle,  
sondern als deterministische Ereignisse mit fest definierten Abläufen.

Dadurch werden:

- Debugging,
- wissenschaftliche Analyse,
- Regressionstests,
- Zertifizierung,
- Reproduzierbarkeit

dramatisch vereinfacht.

KORA bleibt auch im Fehlerfall ein vollkommen transparentes,  
vorhersagbares und wissenschaftlich zuverlässiges System.

---

## 55. Appendix G: Deterministic Numerical Models (Soft-FP & Exact Arithmetic)
(Soft-FP Profil C, deterministische FP-Reihenfolgen, numerische Reproduzierbarkeit)

Dieses Kapitel beschreibt die numerischen Modelle, die KORA nutzt, um vollständige deterministische Reproduzierbarkeit sicherzustellen – 
unabhängig von:

- Hardwaregeneration,
- FP-Einheiten,
- Compiler-Version,
- Scheduling-Variationen,
- parallelen Operationen,
- Rundungsfolgen.

Ziel:  
    KORA liefert *identische* numerische Ergebnisse, auch über Jahrzehnte.

### 55.1 Motivation: Warum deterministische Numerik?

In klassischen HPC/KI-Systemen entsteht Nichtdeterministik durch:

- variierende FP-Reihenfolgen  
- nondeterministische Reduktionen  
- atomare Operationen  
- compilerinduzierte Optimierungen  
- unterschiedliche Hardware-Pipelines  
- Boost-/Throttling-Effekte  

Diese Faktoren führen zu:

- unterschiedlichen Ergebnissen,  
- inkonsistenten Loss-Kurven,  
- instabilen CFD-Modellen,  
- schwer interpretierbarer Messwertermüdung,  
- erschwerter Peer-Review-Reproduzierbarkeit.

KORA eliminiert diese Probleme vollständig.

### 55.2 Numerical Profiles (A, B, C)

KORA definiert drei numerische Profile:

#### Profil A – IEEE 754 Hardware-FP  

- exakte Reihenfolge der FP-Operationen  
- keine dynamischen Varianten  
- geeignet für KI- und CFD-Workloads  

#### Profil B – Mixed Precision (deterministisch)  

- Kombination aus FP32/FP16  
- fester Reduktionsbaum  
- deterministischer Casting-Pfad  

#### Profil C – Soft-FP (vollständig deterministische Softwarearithmetik)  

- CPU-ähnliche Softwarearithmetik  
- ideal für Archivläufe  
- unabhängig von Hardware-FP  
- identische Ergebnisse über Hardwaregenerationen hinweg  

Profil C ist Grundlage für Golden Runs.

### 55.3 Deterministischer FP-Pfad

Ein numerischer Ausdruck:

    y = (a + b) * c + d

wird in KORA als deterministischer Baum ausgeführt:

    t1 = a + b
    t2 = t1 * c
    y  = t2 + d

Niemals:

- parallele Summation,  
- variable Reduktionsreihenfolge,  
- hardwareabhängige Optimierungen.

Reihenfolge ist Teil des TSF.

### 55.4 Reduktionsbäume

Reduktionen sind der häufigste Ort für FP-Nichtdeterministik.

Beispiel klassisch:

    sum = MPI_Allreduce(data)

→ Reihenfolge unspezifisch  
→ Ergebnis variiert

In KORA:

    deterministic_reduce(tree, data)

Der Reduktionsbaum ist:

- statisch,
- im TSF definiert,
- invariant,
- völlig unabhängig vom Clusterlayout.

Beispielstruktur:

        r7
      /    \
    r3      r6
   / \     / \
  r1 r2  r4 r5

### 55.5 Soft-FP: exakte Softwarearithmetik

Soft-FP (Profil C) stellt sicher:

- identische FP-Ergebnisse auf allen Maschinen  
- unabhängig von FP-Hardware  
- unabhängig von Generationen  
- ideal für Golden Runs  
- auditierbare numerische Abläufe  

Soft-FP nutzt:

- deterministische Additions-/Multiplikationsroutinen,
- exakte Rundungsmodelle,
- fest definierte Normalisierungsregeln,
- kontrollierte Overflow-/Underflow-Pfade.

Beispieloperation (konzeptuell):

    soft_add(a, b):
        align exponents
        add mantissas
        normalize
        round (rule = "nearest_even")
        return result

Alles ist strukturell fixiert.

### 55.6 Deterministische Casting-Modelle

Casting zwischen:

- FP64 → FP32,  
- FP32 → FP16,  
- FP16 → BF16,

erfolgt über feste Regeln:

- definierte Rundung,  
- definierte Sättigung,  
- definierter Exponentenbereich,  
- keine hardwareabhängige Variation.

Beispiel:

    cast_fp32_to_fp16(x):
        truncate mantissa
        round half-even
        saturate to FP16 range

### 55.7 FP-Komponenten ohne Varianz

KORA garantiert deterministisches Verhalten bei:

- Fused-Multiply-Add (FMA)  
- Dot Products  
- Convolutions  
- MatMul  
- Attention Scores  
- PDE-Stencil-Berechnungen  
- Ghost-Layer-Kopplung  

Beispiel:

    dot = SUM_i (a_i * b_i)

klassisch: variiert aufgrund paralleler Summation  
KORA: deterministische Reihenfolge

### 55.8 Einfluss auf KI-Training

Mit deterministischer Numerik erhält man:

- identische Gradientenläufe  
- identische Weight-Updates  
- identische Loss-Kurven  
- bitgenaue Lernverläufe  

Dies ermöglicht:

- perfekte Reproduzierbarkeit,  
- exakte Debugbarkeit,  
- Multi-Run-Vergleiche ohne statistisches Rauschen.

### 55.9 Einfluss auf CFD/PDE

Deterministische Numerik erzeugt:

- stabile Iterationsfolgen  
- identische Residuen  
- identische Konvergenzpfade  
- perfekte Multi-Run-Kopierbarkeit  
- ideal für Sensitivitätsanalysen  

CFD-Iterationen driftfrei.

### 55.10 Identische Ergebnisse über Hardwaregenerationen hinweg

Ein TSF + Soft-FP-Profil erzeugt:

    identisches Ergebnis auf M1, M2, M3, M8 …

→ kein numerischer Drift  
→ keine abweichenden FP-Pipelines  
→ keine mikroarchitekturbedingten Unterschiede

Dies ist ein Einzigartigkeitsmerkmal von KORA.

### 55.11 Numerische Telemetrie

Numerikprofile werden protokolliert:

    numeric_profile: C
    fp_operations: 4,234,992
    reductions: 182
    rounding_model: "nearest_even"
    soft_fp: true

Dies erlaubt wissenschaftliche Prüfung der numerischen Stabilität.

### 55.12 Formale Garantie

Für jede numerische Operation läuft:

    operation(result₁) == operation(result₂)

unter gleichen TSF- und Input-Bedingungen.

Damit ist KORA:

- wissenschaftlich überprüfbar  
- archivierungsfähig  
- generationsübergreifend stabil  

### 55.13 Fazit

Kapitel 55 beschreibt das deterministische Numerikmodell von KORA.  
Mit Soft-FP, festen FP-Reihenfolgen, deterministischen Reduktionen und festen Casting-Modellen entsteht:

- absolut reproduzierbare Numerik,
- hardwareunabhängige Stabilität,
- idealer wissenschaftlicher Standard,
- eindeutige Interpretation von Ergebnissen.

KORA garantiert damit nicht nur deterministische Ausführung —  
sondern deterministische Mathematik.

---

## 56. Appendix H: Validation Test Suite Specification
(Validierungslogik, Tests, Regression, Reproduzierbarkeit)

Dieses Kapitel definiert die vollständige Validierungs- und Testarchitektur für KORA.  
Sie stellt sicher, dass:

- jede TSF-Datei korrekt ist,
- jede Simulation reproduzierbar ist,
- jede numerische Operation deterministisch bleibt,
- jeder Hardwarelauf exakt überprüfbar ist.

Der Validation Stack ist essenziell für wissenschaftliche Qualitätssicherung.

### 56.1 Ziele der Validierungssuite

Die Validierungssuite garantiert:

1. **Korrektheit**
       TSF-Dateien entsprechen der Spezifikation und sind logisch konsistent.

2. **Determinismus**
       Ergebnisse, Zeiten, Energieprofile sind über Runs identisch.

3. **Integrität**
       Modelle sind vollständig, unverändert und durch Prüfsummen abgesichert.

4. **Reproduzierbarkeit**
       Ergebnisse können über Jahre und Hardwaregenerationen reproduziert werden.

5. **Fehlerdiagnose**
       Fehler werden korrekt erkannt, klassifiziert und gemeldet.

### 56.2 Komponenten der Validation Suite

Die Suite besteht aus fünf Hauptkomponenten:

1. **TSF Validator**  
2. **Topology Validator**  
3. **Phase Graph Analyzer**  
4. **Numerical Validator**  
5. **Regression Engine**

Struktur:

    validation/
        tsf_validator.py
        topology_validator.py
        phase_graph_analyzer.py
        numerical_validator.py
        regression_engine.py
        test_cases/
            tsf/
            numerical/
            topology/
            regression/

### 56.3 TSF Validator

Überprüft:

- Format (YAML/JSON)
- Version
- Vollständigkeit
- Pflichtfelder
- keine unbekannten Felder
- numerische Typen
- deterministische Feldwerte

Beispiele:

    missing_field: phases
    invalid_type: memory.blocks[0].size

Der Validator erzeugt:

    tsf_validation_report.json

### 56.4 Topology Validator

Überprüft:

- Tileanzahl korrekt
- Memorybank-Zuordnung vollständig
- Fabric-Links valide
- deterministische Topologieparameter

Fehlerbeispiel:

    topology_error:
        tile_groups: 32
        banks_per_tile_group: 4
        declared_banks: 127
        expected_banks: 128

### 56.5 Phase Graph Analyzer

Analyse des Scheduling Trees:

Der Graph muss:

1. azyklisch sein  
2. strikt geordnet  
3. keine Überlappungen besitzen  
4. konstante Start-/Endzyklen haben  
5. deterministische Ablaufstruktur besitzen  

Beispiel Fehlerausgabe:

    phase_conflict:
        phase_id: 5
        overlaps_with: 6
        type: "time_overlap"

### 56.6 Numerical Validator

Testet numerische Korrektheit:

- deterministische FP-Sequenzen  
- Soft-FP Profil C  
- Reduktionsbäume  
- Roundings (nearest even)  
- keine atomaren Variationen  
- Casting-Regeln

Ergebnis:

    numerical_validation:
        soft_fp: ok
        reductions: ok
        casting: ok
        invariants: all_passed

### 56.7 Regression Engine

Vergleicht zwei vollständige Runs:

- Zeiten  
- Energieprofile  
- Tile-Aktivität  
- Reduktionsergebnisse  
- Telemetriedaten  
- komplette FP-Ausgabe  

Vergleich definiert:

    identical → pass
    variant   → fail

Output:

    regression_report.json

### 56.8 Standard-Testfälle

#### 56.8.1 TSF-Testfälle

    test_cases/tsf/
        valid_minimal/
        valid_complex/
        invalid_missing_fields/
        invalid_topology/
        invalid_dma_overlap/

#### 56.8.2 Topologietestfälle

    test_cases/topology/
        correct_structure/
        missing_links/
        invalid_bank_layout/

#### 56.8.3 Numerische Testfälle

    test_cases/numerical/
        fp_basic/
        reduction_tree/
        rounding/
        casting/

#### 56.8.4 Regressionstestfälle

    test_cases/regression/
        identical_runs/
        modified_tsf/
        different_inputs/

### 56.9 Golden Run Verifikation

Jeder Golden Run muss bestehen:

- TSF Validierung  
- Numerik Validierung  
- Telemetrie-Kohärenz  
- Run-Zeitprüfung  
- Energieprüfung  
- Hash-Verifikation  

Beispiel:

    golden_run:
        status: "verified"
        tsf_hash: 9f71a2...
        output_hash: 2ab5c9...
        telemetry_hash: c81c14...

### 56.10 Telemetrieprüfung

Die Telemetrie enthält:

- Zykluszahl
- DMA-Zeiten
- Reduktionspfade
- Speicherzugriffe
- Fabric-Kommunikation

Validator prüft:

- keine fehlenden Events
- keine zeitlichen Anomalien
- deterministische Reihenfolgen

### 56.11 Vergleichsmetriken

#### Zeitvergleich:

    abs(T1 - T2) = 0

#### Energievergleich:

    abs(E1 - E2) < epsilon_energy
    epsilon_energy = 0.1 %

#### Numerischer Vergleich:

    bitgenaue Identität bei Profil C  
    numerische Identität bei Profil A/B

#### Telemetrie:

    identify mismatches in timeline, tile activity, dma events, reduction events

### 56.12 Integration in CI/CD

Typischer Workflow:

    tsf → validate
              ↓
         simulator → telemetry
              ↓
         regression → report
              ↓
         pass/fail → commit allowed?

Dabei:

- kein Merge ohne vollständige Validierung  
- Golden Runs dienen als Referenz  

### 56.13 Formale Validierungsinvarianten

1. **TSF vollständig**  
2. **Keine Überlappung**  
3. **Numerik deterministisch**  
4. **Reduktionen deterministisch**  
5. **Topologie gültig**  
6. **Fabric korrekt**  
7. **Memoryzugriffe konfliktfrei**

Wenn alle erfüllt sind:

    run_valid = true

### 56.14 Fazit

Kapitel 56 beschreibt die vollständige, deterministische Validierungsumgebung von KORA.  
Sie stellt sicher, dass jede simulierte oder ausgeführte TSF-Datei:

- korrekt,
- vollständig,
- deterministisch,
- konsistent,
- reproduzierbar

ist.

Damit bildet die Validation Suite den wissenschaftlichen Eckpfeiler der gesamten Architektur.

---

## 57. Appendix I: TSF Transformation & Optimization Rules
(Transformation, Optimierung, Korrektheitsregeln)

Dieses Kapitel spezifiziert die vollständigen Regeln für die Transformation eines
High-Level-Modells in eine deterministische TSF-Datei sowie für erlaubte Optimierungen.

Das Ziel der Regeln ist:
- deterministische Transformierbarkeit,
- formale Korrektheit aller Optimierungen,
- wissenschaftlich überprüfbare Pipeline,
- garantiert stabile Ausführungsreihenfolge.

### 57.1 Transformationspipeline (High-Level → TSF)

Die Transformation verläuft in sechs Schritten:

1. **High-Level Model Parsing**  
2. **Graph Construction (Compute Graph)**  
3. **Static Memory Allocation**  
4. **Phase Scheduling**  
5. **DMA/Communication Insertion**  
6. **TSF Serialization**

Formale Darstellung:

    model → compute_graph → memory_layout → scheduling_tree →
    dma_insertion → tsf

Jeder Schritt ist deterministisch und vollständig definiert.

### 57.2 Schritt 1 – High-Level Model Parsing

Unterstützte Eingabeformate:

- Python Modelle (NumPy, PyTorch, TensorFlow)
- PDE-Modelle
- Big-Data-Pipelines
- Domain-Specific Languages (DSL)

Parsingregeln:

- keine dynamischen Kontrollstrukturen  
- keine Datenabhängigkeiten, die erst zur Laufzeit entstehen  
- keine nicht-deterministischen Operatoren  

Ergebnis:

    compute_graph = DAG aller Operationen

### 57.3 Schritt 2 – Compute Graph Construction

Ein Compute Graph G = (V, E) ist:

- azyklisch
- topologisch sortierbar
- vollständig deterministisch

Regeln:

- jeder Knoten = elementare Operation  
- jede Kante = feste Datenabhängigkeit  
- keine indirekten, dynamischen Abhängigkeiten  

Beispiel:

    matmul → add → relu

### 57.4 Schritt 3 – Static Memory Allocation

Ziel:

- alle Datenblöcke deterministisch in Memorybanks platzieren  
- keine dynamischen Allokationen  
- keine variablen Offsets  

Algorithmus:

    assign banks
    assign offsets (aligned)
    check for conflicts

Ergebnis:

    memory_blocks = deterministische Liste fester Datenbezüge

### 57.5 Schritt 4 – Phase Scheduling

Der Scheduling Tree T wird aus dem Compute Graph generiert.

Eigenschaften:

- strikte lineare Reihenfolge  
- deterministische Ausführung  
- keine parallelen FP-Zweige zur Laufzeit  
- alle Denkzyklen vollständig statisch definierbar  

Jede Phase:

- compute  
- dma_in  
- dma_out  
- reduction  
- ghost_exchange  

Start/Ende-Zyklen:

    start_cycle = fixed integer
    end_cycle   = fixed integer

### 57.6 Schritt 5 – DMA & Communication Insertion

Regeln für DMA-Insertion:

1. DMA wird *vor* Compute eingefügt  
2. Größe ist konstant  
3. Start- und Endzyklen eindeutig  
4. keine Überschneidungen  
5. jeder Block wird deterministisch geladen/geschrieben

Regeln für Communication (Cluster):

- Fabric-Slots sind fest zugewiesen  
- kein dynamisches Routing  
- deterministische Path-Zuordnung  
- keine Wiederholversuche (keine Retries)

### 57.7 Schritt 6 – TSF Serialization

Regeln:

- YAML/JSON Format  
- keine optionalen, dynamischen Felder  
- deterministische Reihenfolge der Felder  
- Hashbarkeit garantiert (SHA256)  

Beispiel:

    tsf_hash = sha256(tsf_content)

Damit ist das TSF unveränderlich und archivierbar.

### 57.8 Optimierungsregeln (TSF → optimiertes TSF)

KORA erlaubt Optimierungen nur, wenn sie:

- deterministisch,
- vollständig definiert,
- mathematisch korrekt,
- formell sicher,
- rekonstruierbar

sind.

Optimierungen sind in vier Kategorien:

1. **Phase Fusion**  
2. **Memory Block Reuse**  
3. **DMA Coalescing**  
4. **Reduction Tree Optimization**

### 57.9 Optimierung 1 – Phase Fusion

Zwei Compute-Phasen dürfen kombiniert werden, wenn:

- gleiche Tile-Gruppe  
- gleiche Memorybanks  
- keine Abhängigkeit zwischen ihnen  
- kein DMA oder Communication dazwischen  
- resultierende Phase weiterhin zeitlich konsistent ist  

Beispiel:

    compute(phase 2) + compute(phase 3) → compute(phase 2')

Verboten:

- Fusion über Reduktionsgrenzen  
- Fusion über DMA-Grenzen

### 57.10 Optimierung 2 – Memory Block Reuse

Blöcke dürfen recycelt werden, wenn:

- kein weiterer Knoten in graph den alten Block referenziert  
- Bankkonflikte ausgeschlossen sind  
- Alignment erhalten bleibt  

Beispiel:

    block A ist nicht mehr benötigt → wiederverwendbar für B

Diese Optimierung ist vielfach nützlich in ML-Modellen.

### 57.11 Optimierung 3 – DMA Coalescing

Zwei DMA-Transfers können zusammengelegt werden, wenn:

- gleiche Quelle  
- gleiches Ziel  
- angrenzende Offsets  
- zusammenhängender Datenblock  
- keine zeitlichen Konflikte  

Beispiel:

    DMA(0–2MB) + DMA(2–4MB) → DMA(0–4MB)

### 57.12 Optimierung 4 – Reduction Tree Optimization

Der Reduktionsbaum darf umgeordnet werden, wenn:

- Ordnung bleibt vollständig deterministisch  
- FP-Sequenz unverändert  
- Rundungsreihenfolge identisch  

Erlaubt:

- Balancieren des Baums zur Laufzeitreduzierung  
- Gruppierung identischer Operationen  

Nicht erlaubt:

- parallele Summation  
- unspezifische Reordering  
- hardwareabhängige Reduktionspfade

### 57.13 Verbotene Optimierungen

Nicht erlaubt sind:

- Lazy Evaluation  
- On-the-fly DMA  
- dynamische Reduktionen  
- Cache-basierte Optimierungen  
- spekulative Ausführung  
- Out-of-Order Execution  
- Scheduler-basierte Variabilität  

Diese würden deterministische Eigenschaften verletzen.

### 57.14 Validierung von Optimierungen

Jede TSF-Optimierung wird mit drei Tests abgesichert:

1. **Structural Validation**  
2. **Numerical Validation**  
3. **Regression Against Golden Run**  

Wenn alle Testmodule bestehen:

    optimized_tsf is valid

### 57.15 Transformation Safety Theorem (informal)

Sei:

- T₀ ein ursprüngliches TSF  
- T₁ ein transformiertes TSF  
- V die Menge aller Validierungsinvarianten

Wenn:

    T₀ ∈ V  ∧  T₁ ∈ V  ∧  numerical_equivalence(T₀, T₁)

dann gilt:

    execution(T₀) = execution(T₁)

Dies ist die formale Grundlage für Optimierungen.

### 57.16 Fazit

Kapitel 57 definiert alle Regeln, die gewährleisten:

- korrekte Transformation von Modellen in TSF,  
- sichere deterministische Optimierung von TSF,  
- strukturelle und numerische Korrektheit,  
- vollständige wissenschaftliche Reproduzierbarkeit.

Damit bildet Appendix I den Kern der TSF-Compilerlogik und ist wesentlich für Entwickler und Reviewer.

---

## 58. Appendix J: Reference Workload Definitions
(Definitionen, Parameter, Gleichungen, Datensätze)

Dieses Kapitel definiert die offiziellen KORA-Referenz-Workloads.  
Sie dienen als Grundlage für:

- Simulationen  
- Vergleich zwischen Hardwaregenerationen  
- Energie- und Zeitmodelle  
- Reviewergutachten  
- öffentliche Reproduzierbarkeit  

Die Workloads sind bewusst so gewählt, dass sie drei Hauptklassen abdecken:

1. **FLOP-dominant** (BERT)  
2. **Memory-/Communication-dominant** (Big Data)  
3. **PDE/Stencil-dominant** (CFD)  

### 58.1 CFD Reference Workload – Navier-Stokes 3D (Incompressible)

#### 58.1.1 Physikalisches Modell

Die 3D Navier-Stokes Gleichungen:

    ∂u/∂t + (u·∇)u = -∇p + ν ∇²u  
    ∇·u = 0

mit:

- u: Geschwindigkeit  
- p: Druck  
- ν: Viskosität  

#### 58.1.2 Diskretisierung (Finite Differences, 7-Point Stencil)

Für jeden Zeitschritt:

    u_new = stencil(u_old)  
    p_new = poisson_solve(u_new)  

Stencil:

    center * c0  
    + neighbors_x * c1  
    + neighbors_y * c2  
    + neighbors_z * c3

Poisson-Löser:

    ∇²p = f(u)

#### 58.1.3 Griddefinitionen

##### **CFD Small**

| Dimension | Wert |
|----------|------|
| Grid     | 128 × 128 × 64 |
| Steps    | 200 |
| ν        | 0.001 |

##### **CFD Large**

| Dimension | Wert |
|----------|------|
| Grid     | 512 × 512 × 256 |
| Steps    | 300 |
| ν        | 0.001 |

#### 58.1.4 Kommunikationsmuster (Cluster)

Ghost Exchange:

- pro Dimension jeweils 2 Schichten  
- feste Größe pro Schritt  
- deterministisches Kommunikationsvolumen  

#### 58.1.5 Output

- Residuen pro Schritt  
- Geschwindigkeit und Druckfelder als HDF5  
- Telemetrie: Stencilzeiten, Austauschzeiten  

### 58.2 BERT Reference Workload – Pretraining (MLM + NSP)

#### 58.2.1 Modellkonfiguration

| Parameter       | Wert |
|-----------------|------|
| Modellgröße     | BERT Base |
| Layers          | 12 |
| Hidden Size     | 768 |
| Attention Heads | 12 |
| Sequence Length | 512 |

#### 58.2.2 Datenset

Wikipedia 2024 (bereinigt):

- 3.3B Tokens  
- 32k WordPiece Vokabular  

#### 58.2.3 Trainingskonfiguration

Optimierer: Adam  
Loss: MLM + NSP  
Batch Size pro Step: 128  
Steps: 100k  

#### 58.2.4 FLOP-Basis

Flops pro Step (BERT Base):

    ~3.7 × 10^11 FLOPs

Gesamt:

    100k × 3.7e11 = 3.7 × 10^16 FLOPs

#### 58.2.5 Kommunikation (klassisch)

- AllReduce für Gradienten  
- 4–16 Sync-Punkte pro Schritt  
- hohes Kommunikationsvolumen  

KORA:

- deterministische Reduktion  
- 1–2 Sync-Punkte  
- konstante Latenz  

#### 58.2.6 Output

- Loss-Kurven  
- Checkpoints (optional)  
- Telemetrie: Compute/DMA/Reduction Pfade  

### 58.3 Big Data Reference Workload – Large Shuffle/Join Pipeline

#### 58.3.1 Beschreibung

Eine klassische Analysepipeline:

1. **Read 500 GB** Parquet  
2. **Shuffle + repartition** (key=customer_id)  
3. **Join** zweier großer Tabellen (10^9 Zeilen)  
4. **GroupBy/Aggregation**  
5. **Write Output** (100–200 GB)

#### 58.3.2 Datenset

Synthetic / Generator:

- 1B Rows  
- 20 Columns  
- 5 Key Columns  
- 15 Value Columns  

Verteilung: Zipfian (realistische Lastverteilung)

#### 58.3.3 Klassische Pipeline (Spark/Flink)

Phasen:

- Shuffle (50–70 % der Laufzeit)  
- Sortieren  
- Merge  
- Join  
- GroupBy  

Kommunikationsvolumen:

    200–400 GB pro Shuffle

#### 58.3.4 KORA-Pipeline

- deterministische Partitionierung  
- deterministische Shuffle-Slots  
- deterministische DMA  
- kein dynamischer Scheduler  
- kein Straggler  

Zeitersparnis:

    40–70 %

Energieersparnis:

    60–85 %

#### 58.3.5 Output

- aggregierte Tabellen (100–200 GB)  
- Zeitprofile für Shuffle, Join, GroupBy  
- Telemetrie: Fabric, DMA, Memory  

### 58.4 Zusammenfassung der Referenzparameter

| Workload | FLOP-lastig | Memory-lastig | Communication-lastig | Ziel |
|----------|-------------|---------------|------------------------|------|
| CFD      | mittel      | hoch          | mittel                 | PDE/Stencils |
| BERT     | extrem hoch | gering        | mittel–hoch            | KI/ML |
| Big Data | gering      | extrem hoch   | extrem hoch            | Analyse/Merge |

Diese Kombination ermöglicht:

- vollständige Beschreibung der Performance  
- Vergleichbarkeit über Hardwaregenerationen  
- Benchmarking  
- Evaluation der Vorteile von KORA  

### 58.5 Fazit

Kapitel 58 definiert vollständig die drei offiziellen Referenz-Workloads,  
auf denen alle Simulationen, Energievergleiche und wissenschaftlichen Aussagen von KORA basieren.

Damit ist gewährleistet:

- Reproduzierbarkeit  
- Vergleichbarkeit  
- Reviewertauglichkeit  
- wissenschaftliche Transparenz

---

## 59. Appendix K: Security & Integrity Model
(Integrität, Sicherheit, Manipulationsschutz, deterministische Ausführung)

Dieses Kapitel definiert das Sicherheits- und Integritätsmodell von KORA.  
Es beschreibt, wie TSF-Dateien, Ausführungsumgebungen und Monolith-Cluster gegen:

- Manipulation,
- fehlerhafte TSFs,
- inkonsistente Inputs,
- unerlaubte Eingriffe,
- Laufzeitmanipulationen

geschützt werden — ohne jemals Nichtdeterminismus einzuführen.

### 59.1 Grundprinzipien der KORA-Sicherheit

KORA basiert auf vier Sicherheitsprinzipien:

1. **Deterministische Ausführung**  
       kein Out-of-Order, kein Cache, kein Spekulativpfad

2. **Host-Verifikation**  
       Host prüft vor Ausführung, nicht die Hardware selbst

3. **Unveränderliche TSF-Dateien**  
       ausführbare TSFs sind signiert, versioniert, checksum-gesichert

4. **Transparenz durch vollständige Telemetrie**  
       jede Operation ist nachvollziehbar und prüfbar

### 59.2 Schutzumfang

Das Security-Modell schützt folgende Ebenen:

- TSF-Dateien  
- Eingabedaten  
- Scheduling Trees  
- DMA- und Fabric-Operationen  
- numerische Pfade (Reduktionen, FP)  
- Memorybank-Zugriffe  
- Cluster-Kommunikation  
- Telemetrie  

Nicht geschützt (bewusst ausgelagert):

- Host-Betriebssystem  
- Hosting-Umgebung  
- externer Storage  

Die Sicherheit ist damit hardwareseitig deterministisch, jedoch hostabhängig bei I/O.

### 59.3 TSF Integrity Model

Jede TSF-Datei wird signiert in drei Schichten:

#### (A) **Hash Layer**  

SHA256 über den gesamten TSF-Inhalt.

    tsf_hash = sha256(tsf_content)

#### (B) **Signature Layer**  

Optionale digitale Signatur:

    signature = sign(tsf_hash, private_key)

#### (C) **Metadata Layer**  

Dokumentiert:

    tsf_version
    compiler_version
    timestamp
    author
    signature

Zusammen bilden sie:

    TSFIntegrityEnvelope

Das TSF darf nie verändert werden — Versionen werden immer neu gespeichert.

### 59.4 Input Data Integrity

Inputs enthalten:

- checksum_sha256
- dataset_version
- format_descriptor

Beispiel:

    input_integrity:
        sha256: "7a981..."
        schema: "bert_wiki2024"
        version: 1.0

Regeln:

1. Input darf nicht dynamisch erzeugt werden  
2. Änderungen → neue Version  
3. Host validiert vor Ausführung den Hash  
4. Keine Laufzeitmodifikationen erlaubt  

### 59.5 Memory Access Integrity

Memoryzugriffe sind deterministisch:

- feste Bankzuweisung  
- feste Offsets  
- keine dynamischen Pointer  
- keine vermischten Memoryspaces  
- keine Out-of-Bounds-Zugriffe

Hardwarevalidierung:

    if (access > limit) → deterministic_fault

Kein Wiederholversuch, keine Korrektur — nur deterministischer Abbruch.

### 59.6 DMA Integrity

DMA-Transfers sind strikt definiert:

- Größe  
- Quelle  
- Ziel  
- Start-/Endzyklen  

Hardware prüft:

    dma.size == declared_size
    dma.src  == declared_src
    dma.dst  == declared_dst

Fehler lösen aus:

- sofortiger Freeze  
- Telemetrie  
- deterministisches Abbruchsignal  

### 59.7 Fabric Integrity (Cluster-Sicherheit)

Fabric ist vollständig deterministisch:

- kein dynamisches Routing  
- keine adaptive Linkauswahl  
- keine dynamischen Slotzuweisungen  
- keine Wiederholpakete  

Integritätsschutz:

1. Slotprüfung  
2. Pfadprüfung  
3. Zyklusprüfung  
4. Kollisionsdetektion  

Beispiel einer Fehlermeldung:

    fabric_integrity_error:
        slot: 3
        expected_path: 0→2
        observed_path: 0→4
        cycle: 99123

### 59.8 Deterministic Execution Integrity

Der Kern der Sicherheit besteht aus:

1. **kein Out-of-Order Execution**  
2. **keine Cache-Abhängigkeit**  
3. **konstante Taktfrequenz**  
4. **konstante Latenzen**  
5. **keine Variabilität durch Boost/Throttling**  
6. **keine spekulative Pfade**

Dadurch wird:

    Execution Integrity = 100 % deterministisch

### 59.9 Host-Side Security Layer

Der Host übernimmt:

- Zertifikatsprüfung  
- Hash-Prüfung  
- Freigabe der Ausführung  
- Export der Telemetrie  
- Archivierung  

Host-Regeln:

1. TSF muss gültig validiert sein  
2. Input muss in Hash-Datenbank existieren  
3. Modellversion muss verifizierbar sein  
4. Telemetrie muss vollständig exportiert werden  

### 59.10 Cluster-Sicherheitsprotokolle

In Clusterläufen:

- jeder Monolith prüft eigene Fabric-Slots  
- Host synchronisiert TSFs aller Knoten  
- deterministische Round-Robin-Freigabe  

Kein Monolith darf:

- ungeprüfte TSFs ausführen  
- Fabric-Slots dynamisch ändern  
- Nachrichten interpretieren  

### 59.11 Angriffsszenarien und Schutzmechanismen

#### Szenario 1 – Manipulierter TSF  

→ wird durch Hash/Signature abgefangen  
→ Ausführung verweigert

#### Szenario 2 – Eingabedaten manipuliert  

→ Input-Hash stimmt nicht  
→ Ausführung verweigert

#### Szenario 3 – Fabric-Manipulation (Cluster)  

→ Slotabweichung erzeugt deterministischen Fehler  
→ Run wird abgebrochen

#### Szenario 4 – numerische Manipulation  

→ numerischer Pfad im TSF definiert  
→ Abweichung erzeugt deterministischen Fehler

#### Szenario 5 – Host mit Malware  

→ außerhalb des KORA-Modells  
→ mitigierbar durch signierte TSFs/Inputs  
→ Hardware selbst bleibt deterministisch

### 59.12 Integritäts-Telemetrie

Jeder Run speichert:

    integrity_report:
        tsf_hash
        input_hash
        telemetry_hash
        fault_count
        warnings
        timestamp
        cluster_node_map

Damit sind Runs prüfbar und archivalisch nutzbar.

### 59.13 Formale Integritätsgarantien

1. **TSF ist unveränderlich**  
2. **Numerik ist unveränderlich**  
3. **Scheduling Trees sind unveränderlich**  
4. **Memoryzugriffe sind überprüfbar**  
5. **Kommunikation ist deterministisch und überprüfbar**  
6. **Telemetrie ist vollständig**  
7. **Runs sind auditierbar**

Dies ermöglicht wissenschaftliche Vergleiche über Jahrzehnte hinweg.

### 59.14 Fazit

Kapitel 59 definiert das vollständige Sicherheits- und Integritätsmodell von KORA.  
Es kombiniert:

- deterministische Hardware  
- verifizierbare TSFs  
- Hash-basierte Integrität  
- hostseitige Validierung  
- vollständige Telemetrie  

→ zu einem System, das gegen Manipulation robust ist  
→ und dennoch 100 % deterministisch bleibt.

---

## 60. Appendix L: Hardware Physical Layout & Signaling
(physisches Layout, Tile-Topologie, Memorybanks, Fabric, Signaldomänen)

Dieses Kapitel beschreibt das abstrakte physische Layout des KORA-Monolithen.  
Es dient nicht zur Fertigung, sondern zur wissenschaftlichen und architekturellen Einordnung:

- Wie sind Tiles physisch angeordnet?
- Wie sind Memorybanks angebunden?
- Wie funktioniert die deterministische Fabric (TDM)?
- Wie sind Taktdomänen strukturiert?
- Wie wird Signalintegrität gewährleistet?

Damit wird die konzeptionelle Hardwarebasis von KORA vollständig transparent.

### 60.1 Monolith – Übersicht der physischen Struktur

Der KORA-Monolith ist ein flächiger, einheitlicher Chip mit:

- **512 Tiles** (M3-Referenz)
- **128 Memorybanks**
- **16 Fabric-Links (TDM)**
- **fester und deterministischer Verdrahtung**

Das Layout folgt einer **4-Ebenen-Struktur**:

1. **Tile Layer**  
2. **Memory Layer**  
3. **Interconnect / Fabric Layer**  
4. **Clock & Power Layer**

Diese Ebenen sind fest verschachtelt und werden gemeinsam synthetisiert.

### 60.2 Tile Layer (Compute Plane)

#### 60.2.1 Anordnung

Tiles sind in einem 32×16 Raster angeordnet:

    rows:    32
    columns: 16
    total:   512 tiles

Vorteile dieser Anordnung:

- geringe Latenz zwischen Nachbarn  
- deterministische Kommunikationsentfernung  
- homogener thermischer Lastfluss  
- perfekte Zuordnung zu Tile Groups

#### 60.2.2 Tile Gruppen

Je 16 Tiles bilden eine **Tile Group**:

    16 tiles/group → 32 groups total

Jede Gruppe besitzt:

- feste lokale Bankzuordnung
- festen lokalen Fabric-Abschnitt
- stabile Taktdomäne

### 60.3 Memory Layer (128 deterministische Memorybanks)

#### 60.3.1 Memorybank-Verteilung

Memorybanks sind nicht zentralisiert, sondern **flächig verteilt** — nach folgendem Muster:

- jede Tile Group besitzt **4 lokale Memorybanks**  
- gesamte Verteilung: 32 Gruppen × 4 = 128 Banks

Beispiel:

    Group 0 → Banks 0–3  
    Group 1 → Banks 4–7  
    ...

Dadurch entstehen:

- konstante Latenzen  
- keine NUMA-Unterschiede  
- vollständig deterministische Zugriffszeiten  
- keine dynamischen Memorypfade

#### 60.3.2 Bankanbindung

Jede Bank ist:

- mit deterministischer Punkt-zu-Punkt-Verbindung angebunden  
- mit fester Latenz (3 cycles)  
- ohne Caches  
- ohne Prefetching  
- ohne Reordering  
- ohne Koherenzprotokoll

Dies stellt sicher:

    Memory Integrity = 100 % deterministisch

### 60.4 Interconnect Layer (Deterministic Fabric)

Die Fabric besteht aus **16 bidirektionalen TDM-Links**.

#### 60.4.1 TDM (Time-Division Multiplexing)

TDM-Slotdefinition:

- jeder Slot hat feste Länge (z. B. 64 cycles)
- jeder Slot hat festen Adressaten
- Routing ist konstant
- keine dynamische Slotvergabe

Ein Nachrichtenpfad ist:

    src_group → fabric_link → dst_group

und bleibt immer identisch.

#### 60.4.2 Fabric-Topologie (2D Mesh)

Physische Struktur:

- 32 Tile Groups in 4×8 Anordnung
- Fabric Links bilden ein 2D-Mesh
- Routing folgt deterministisch festen Pfaden

Vorteile:

- keine Paketkollisionen  
- keine variable Hop-Anzahl  
- keine dynamische Routingentscheidung  

### 60.5 Clock & Power Layer

#### 60.5.1 Taktdomänen

KORA besitzt:

- **eine globale Haupttaktdomäne**,  
- **Plus lokale Subdomänen** pro Tile Group für kurze Leitungswege.

Der Takt ist:

- konstant  
- jitterfrei  
- synchron mit Fabric-Slots  
- synchron mit DMA-Fenstern  

Keine Boost-Modi, kein Throttling:

    frequency(t) = constant

#### 60.5.2 Power Layer

Das Powermodell ist flächig und gleichmäßig:

- symmetrische Stromverteilung  
- deterministische Versorgung  
- konstante Leistungsaufnahme  
- keine lastabhängigen Spannungsschwankungen  

Dies verhindert:

- variable Latenzen  
- dynamische Frequenzschwankungen  
- thermisch bedingte Variabilität

### 60.6 Signalintegrität & deterministische Leitungswege

Wesentlich:

- alle Leitungen haben feste, synthetisch validierte Längen  
- deterministische Delay-Budgets  
- identisches Verhalten über alle Chips  
- keine post-Layout Variabilität

Signaling garantiert:

- konstante Latenz  
- keine Crosstalk-Abhängigkeiten  
- deterministisches Timing über die komplette Chipfläche  

### 60.7 Kommunikationspfade innerhalb des Monolithen

#### 60.7.1 Tile → Memory

Pfadlänge:
- konstant  
- 3 cycles Latenz

#### 60.7.2 Tile → Tile (Gruppe)

Pfadlänge:
- ≤ 2 cycles (lokal)
- keine Kollisionen möglich

#### 60.7.3 Tile → Tile (zwischen Gruppen)

Pfad:
    Tile (A) → Local Hub → Fabric Link → Local Hub → Tile (B)

Hop-Anzahl:
- fixiert  
- unabhängig von Auslastung  

### 60.8 Deterministische Thermik

Zur Gewährleistung deterministischer Zeit- und Energieprofile:

- Power verteilt symmetrisch  
- kein lokales Thermal Boosting  
- deterministische Kühlkurven  
- konstante Chiptemperatur unter Last  

Dadurch:

    Latenz = konstant  
    Energieverbrauch = konstant

### 60.9 Beispielhafte schematische Darstellung (abstrakt)

    +--------------------------------------------------+
    |        Tile Layer (32 × 16 Tiles)                |
    |  +--------------------------------------------+  |
    |  | Tiles + Tile Groups + Local Hubs           |  |
    |  +--------------------------------------------+  |
    |                                                  |
    |        Memory Layer (128 Banks)                  |
    |  +--------------------------------------------+  |
    |  | Fixed-latency banks (4 per group)           | |
    |  +--------------------------------------------+  |
    |                                                  |
    |        Interconnect (TDM Fabric)                 |
    |  +--------------------------------------------+  |
    |  | Time-slotted deterministic Links (16)       | |
    |  +--------------------------------------------+  |
    |                                                  |
    |        Clock & Power Layer                       |
    |  +--------------------------------------------+  |
    |  | Global Clock + Uniform Power Delivery       | |
    |  +--------------------------------------------+  |
    +--------------------------------------------------+

Dieses Diagramm ist rein konzeptionell — keine Fertigungsdetails.

### 60.10 Fazit

Kapitel 60 beschreibt das abstrakte physische und signaltechnische Layout des KORA-Monolithen:

- deterministische Verdrahtung  
- konstante Latenzen  
- synchronisierte Taktdomänen  
- TDM-Fabric  
- flächig verteilte Memorybanks  
- garantie deterministischer Ausführung

Damit ist die Hardwarebasis vollständig beschrieben und konsistent mit dem deterministischen KORA-Modell.

---

## 61. Appendix M: Deterministic Cluster Topologies
(Clusterarchitektur, deterministische Kommunikation, TDM-Scaling)

Dieses Kapitel definiert, wie mehrere KORA-Monolithe zu einem deterministischen Cluster
zusammengeschaltet werden können.  
Das Ziel:  
    deterministische Multi-Monolith-Ausführung ohne Jitter, ohne Dynamik, ohne Straggler.

Alle Topologien sind statisch, vollständig deterministisch und TSF-kompatibel.

### 61.1 Grundprinzipien deterministischer KORA-Cluster

Ein KORA-Cluster folgt fünf Kernprinzipien:

1. **Keine dynamische Routenentscheidung**  
       – alle Pfade sind vorab definiert (TSF + Cluster-Map)

2. **Time-Division Fabric (TDM)**  
       – jedes Paket hat festen Slot + festen Zyklus

3. **Identische Hop-Anzahl für gleiche Pfade**  
       – keine variable Verzögerung

4. **Keine Retry-Mechanismen**  
       – Fehler → deterministischer Abbruch

5. **Homogene Nodes**  
       – gleiche Monolith-Generation, gleiche Fabric-Spezifikation

Damit entsteht ein völlig jitterfreies Cluster.

### 61.2 Architekturübersicht

Ein KORA-Cluster besteht aus:

- N × Monolith-Knoten  
- TDM-Fabric zwischen den Knoten  
- deterministischer Cluster-Map  
- Host-System mit Scheduling-Kontrolle  
- TSF-Dateien, die über alle Knoten verteilt sind  

Layout:

    host → node group → monolith tiles → fabric → node group → host

### 61.3 Cluster-Topologien (zertifiziert deterministisch)

KORA unterstützt sechs deterministische Topologien:

1. **1D Line Topology**  
2. **2D Mesh Topology**  
3. **2D Torus Topology**  
4. **Star Deterministic Topology**  
5. **Hierarchical Mesh**  
6. **Hybrid Torus-Mesh**

Alle Topologien sind *statisch*, *vorab definiert* und *TSF-kompatibel*.

### 61.4 Topologie 1 – 1D Line

Beispiel:

    Node0 — Node1 — Node2 — Node3

Eigenschaften:

- linear deterministisch  
- fixed hop count  
- geeignet für sequentielle PDE-Modelle  
- einfach zu validieren

Hop-Latenz:

    latency_total = hops × 3 cycles

### 61.5 Topologie 2 – 2D Mesh (Standard)

Beispiel:

    Node00  Node01  Node02
    Node10  Node11  Node12
    Node20  Node21  Node22

Vorteile:

- homogene Hop-Anzahl  
- gute Skalierbarkeit  
- deterministisches Routing im Raster  
- geeignet für CFD, ML, Analytics

Jeder Node hat bis zu 4 deterministische Verbindungen:

- North, South, East, West

### 61.6 Topologie 3 – 2D Torus

Beispiel:

    Node00 -- Node01 -- Node02 --+
      |                          |
    Node10 -- Node11 -- Node12 --+
      |                          |
    Node20 -- Node21 -- Node22 --+

Eigenschaften:

- toroidale Wrap-Around-Verbindungen  
- konstante Entfernung zwischen Knoten  
- ideal für PDE-locality  

Formale Garantie:

    maximaler Abstand = konstanter Wert

### 61.7 Topologie 4 – Star Deterministic Topology

Zentrum: Node0  
Alle anderen Knoten verbinden sich deterministisch mit Node0.

Vorteile:

- ideal für zentralisierte Aggregationsworkloads  
- deterministisch, solange Slots fix sind

Nachteil:

- weniger skalierbar für große N

### 61.8 Topologie 5 – Hierarchical Mesh (Cluster of Clusters)

Beispiel:

    MeshGroup0 — MeshGroup1 — MeshGroup2

Jede Gruppe ist:

- eigenständiges Mesh (3×3, 4×4 etc.)  
- durch TDM-Links deterministisch verbunden  

Einsatz:

- sehr große Cluster  
- regionale Partitionierung  

### 61.9 Topologie 6 – Hybrid Torus-Mesh

Eine Kombination aus:

- innerem Mesh  
- äußerem Torus  

Ziel:

- Minimierung der längsten Pfade  
- ideale Balance zwischen Skalierbarkeit und deterministischem Verhalten

### 61.10 Deterministische Fabric-Routingregeln

Routing erfolgt strikt nach folgenden Regeln:

1. Jeder Pfad ist statisch definiert  
2. Jede Nachricht besitzt einen festen Slot  
3. Kein Node entscheidet zur Laufzeit über Routen  
4. Jeder Hop hat feste Latenz (3 cycles)  
5. Keine Wiederholpakete  

Routingfunktion:

    route(src, dst) = f_topology(src, dst)

wobei f_topology deterministisch ist.

### 61.11 Synchronisationsmodell

Cluster-Synchronisation basiert nicht auf:

- MPI  
- dynamischen Barriers  
- OS-Scheduler

Sondern auf:

- TSF-definierten Sync-Phasen  
- fixen Austauschpunkten  
- deterministischen Fabric-Slots  

Synchronisation ist erforderlich für:

- Ghost Exchange (CFD)  
- Gradient Reductions (ML)  
- Shuffle Barriers (Big Data)

### 61.12 Deterministische Ghost Exchange (CFD)

Ghost Exchange:

- feste Datenmenge  
- deterministischer Slot  
- synchronisiert mit Phase Scheduler  
- keine dynamischen Messages  
- nicht abhängig vom Clusterauslastung

Formel:

    T_ghost = (ghost_size / fabric_bandwidth) + fixed_latency

### 61.13 Deterministische Reduktion (ML)

KORA ersetzt AllReduce (MPI) durch:

- deterministischen Baum  
- feste Pfade  
- konstante Zeit  
- feste Slotzuweisung

Ergebnis:

    latency_reduce = constant

auch bei tausenden Knoten.

### 61.14 Deterministische Shuffle (Big Data)

Shuffle-Aufgaben:

- Partitionierung ist deterministisch  
- jeder Slot repräsentiert feste Partition  
- Merge wird deterministisch ausgeführt  
- kein Straggler-Effekt  
- kein Rebalancing  

Vorteil:

    shuffle_latency = 60–80 % geringer als klassisch

### 61.15 TSF Cluster Mapping

TSF-Dateien können mehrere Nodes enthalten:

    tsf:
        nodes: 16
        mapping:
            tile_group → node
            fabric_slot → link
            reduction_path → nodes[...]

Jedes Mapping ist vollständig statisch.

### 61.16 Fehlerverhalten im Cluster

Clusterfehlerverhalten ist deterministisch:

- Slot-Kollision → deterministischer Abbruch  
- Fabric-Abweichung → deterministischer Abbruch  
- fehlender Node → deterministischer Abbruch  

Kein Retry, kein Fallback-Routing.

### 61.17 Skalierungsgrenzen der deterministischen Cluster

Theoretisch:

- bis zu einige Tausend Nodes  
- abhängig von:
    - Fabric-Breite
    - Topologie
    - Sync-Punkten
    - Slotanzahl

Praktisch:

- Mesh: 1024 Nodes  
- Torus: 4096 Nodes  

Alle deterministisch skalierbar.

### 61.18 Vorteile deterministischer Cluster

1. **Null Jitter**  
2. **Null Straggler**  
3. **Null dynamisches Routing**  
4. **Null Overhead durch Scheduler**  
5. **Maximale Vorhersagbarkeit**  
6. **Ideale wissenschaftliche Reproduzierbarkeit**  

### 61.19 Fazit

Kapitel 61 beschreibt ausführlich, wie mehrere Monolithe zu deterministischen Clustern organisiert werden können.  
Durch statische Topologien, TDM-basierte Kommunikation und deterministische Pfade entsteht:

- perfekte Skalierbarkeit,  
- perfekte Reproduzierbarkeit,  
- eliminierter Overhead,  
- vorhersagbares Verhalten über tausende Nodes.

Damit erweitert Appendix M die KORA-Philosophie von deterministischer Einzelhardware auf deterministische Hochleistungscluster.

---

## 62. Appendix P: Reproducibility Protocol for Long-Term Studies
(Reproduzierbarkeit, Archivierung, Validierung, DOI-Standards)

Dieses Kapitel definiert das vollständige Protokoll zur wissenschaftlichen Reproduzierbarkeit von KORA-Runs.
Es stellt sicher, dass:

- Ergebnisse über Jahrzehnte reproduzierbar bleiben,  
- Daten und Modelle eindeutig identifizierbar sind,  
- Telemetrie vollständig bleibt,  
- TSFs unverändert archiviert werden,  
- Reviewer vollständig prüfen können,  
- DOIs saubere Versionen referenzieren.

Dieses Protokoll ist Grundlage für OSF- und Zenodo-Publikationen.

### 62.1 Ziele des Reproduzierbarkeitsprotokolls

Das Protokoll garantiert:

1. **wissenschaftliche Nachvollziehbarkeit**  
2. **Langzeitarchivierbarkeit** (20–50 Jahre)  
3. **Auditierbarkeit aller Schritte**  
4. **bitgleiche Reproduzierbarkeit von Golden Runs**  
5. **integritätsgesicherte Versionierung**

Es ist kompatibel mit:

- Open Science Framework (OSF)  
- Zenodo  
- institutional repositories  
- CI/CD-Systemen  

### 62.2 Reproduzierbarkeit: Kerndefinition

Ein Run R ist reproduzierbar, wenn gilt:

    R_input == R'_input
    R_tsf   == R'_tsf
    R_output == R'_output
    R_telemetry == R'_telemetry
    R_time == R'_time
    R_energy == R'_energy

und keinerlei Varianz besteht.

KORA garantiert diese Gleichheit durch deterministische Ausführung.

### 62.3 Struktur eines vollständig archivierbaren Runs

Jeder Run wird archiviert als Ordner:

    run_<id>/
        tsf/
            model.tsf
        input/
            data/
            schema.json
        output/
            tensors/
            results/
        telemetry/
            timeline.json
            energy.json
        metadata/
            run_info.json
            hashes.json
            integrity.json

Alle Dateien müssen unveränderlich sein.

### 62.4 Golden Run Definition

Ein **Golden Run** ist:

- vollständig validiert  
- signiert  
- unveränderlich  
- referenzierbar per DOI  
- bitgleich reproduzierbar  
- telemetriekomplett  

Golden Runs dienen als:

- Referenzwert  
- Regressionstestbasis  
- wissenschaftliches Archivierungsobjekt  

Golden Runs werden separat gelagert:

    runs/golden/<model>/

### 62.5 Versionierungsmodell

Versionierung erfolgt **mehrschichtig**:

#### (A) TSF-Version
    tsf_version: 1.0 / 1.1 / 2.0

#### (B) Modell-Version
    model_version: 1.0.1

#### (C) Input-Version
    input_version: 2024_v3

#### (D) Run-Version
    run_version: "1.0"

#### (E) Repository/Paper-Version
    release_version: "v1.1"

Alle Versionen werden im Ordner:

    metadata/version.txt

aufgeführt.

### 62.6 Hashing und Integrität

Jede Datei wird per SHA256 gehasht:

    sha256(file) → 64-stelliger Hash

`hashes.json` enthält:

- tsf_hash  
- input_hash  
- output_hash  
- telemetry_hash  
- metadata_hash  

Beispiel:

    {
        "tsf": "9f71bc...",
        "input": "7a188d...",
        "output": "71df33...",
        "telemetry": "1170a3..."
    }

Hash-Verletzungen → Run ungültig.

### 62.7 Metadaten: vollständige Beschreibung eines Runs

`run_info.json` enthält:

- Modellname  
- Startzeitpunkt  
- Endzeitpunkt  
- Anzahl Schritte  
- Energieverbrauch  
- Hardwareprofil  
- tsf_version  
- numeric_profile  
- simulator_version  
- cluster_mapping  
- input_description  

Damit ist jeder Run vollständig dokumentiert.

### 62.8 Telemetrieanforderungen

Pflichtdaten in `telemetry/`:

1. Phase-Timeline  
2. DMA-Operationen  
3. Reduktionspfade  
4. Memorybank-Zugriffe  
5. Fabric-Ereignisse  
6. numerische Stabilitätsdaten  
7. Energieverlauf (kW → kWh)  

Telemetrie ist entscheidend für:

- Debugging  
- Reproduzierbarkeit  
- Audit Trails  

### 62.9 Reproduzierbarkeits-Checkliste (wissenschaftlich)

Vor Archivierung eines Runs:

1. **TSF validiert?**  
2. **Numerik validiert?**  
3. **Topologie validiert?**  
4. **Regressionsprüfung bestanden?**  
5. **Telemetrie vollständig?**  
6. **Hashprüfung erfolgreich?**  
7. **Metadaten vollständig?**  
8. **Versionierung konsistent?**  
9. **Cluster-Mapping deterministisch?**  
10. **Golden Run geeignet?** (optional)

Wenn alle Bedingungen erfüllt sind:

    run_status = "VALID"

### 62.10 DOI-Integration (OSF & Zenodo)

Archivierungsstrategie:

- Golden Runs → eigene DOI  
- Dokumentation → eigene DOI  
- TSF-Spezifikation → eigene DOI  
- Paper/Report → eigene DOI  
- Versionen eindeutig trennbar

Beispiel-Ordnerstruktur bei Zenodo:

    archive_v1.1/
        docs/
        tsf/
        golden_runs/
        simulator/
        metadata/
        checksums.txt

DOI pointet immer auf das vollständige Archiv.

### 62.11 Reproduktionsprotokoll für Reviewer

Reviewer müssen folgendes tun:

1. Archiv herunterladen  
2. Checksums prüfen  
3. TSF validieren  
4. Simulator ausführen  
5. Telemetrie vergleichen  
6. Hashgleichheit bestätigen  
7. Ergebnisberichte erzeugen  

Wenn Output = Golden Run Output:

    reproduction = success

### 62.12 Langzeitarchivierung (10–50 Jahre)

Empfehlungen:

- Aufbewahrung in offenen Formaten (Markdown, JSON, YAML, HDF5)  
- Keine Binärformate ohne Spezifikation  
- Alle TSFs unverändert aufbewahren  
- Hostumgebungen per Container konservieren  
- Simulator-Version archivierbar halten  

Dateien sind so entworfen, dass zukünftige Systeme sie problemlos interpretieren können.

### 62.13 Minimal Example (Mini-Repro-Set)

Ein minimaler reproduzierbarer Run hat:

    /tsf/model.tsf
    /input/data/
    /output/results/
    /telemetry/timeline.json
    /metadata/run_info.json
    /metadata/hashes.json

Damit lässt sich der Run beliebig oft reproduzieren.

### 62.14 Reproduzierbarkeitsgarantien

KORA garantiert:

1. **bitgenaue Numerik (Profil C)**  
2. **bitgenaue TSF-Struktur**  
3. **zyklusgenaue Ausführung**  
4. **konstante Energieprofile**  
5. **konstante Telemetrie**  
6. **statische Cluster-Pfade**  
7. **keine Algorithmenvariabilität**  

Daher gilt:

    reproduction_possible = true
    across_years = true
    across_hardware_generations = true

### 62.15 Fazit

Kapitel 62 beschreibt das vollständige Protokoll für wissenschaftliche Reproduzierbarkeit.  
Mit deterministischen TSFs, vollständiger Telemetrie, signierten Runs, Hash-basierten Prüfungen und klarer Versionierung entsteht:

- eine dauerhaft überprüfbare Forschungsgrundlage,  
- ein robustes Archiv für Open Science,  
- ein international reproduzierbares Ökosystem.

KORA ist damit nicht nur ein deterministisches System —  
sondern ein wissenschaftlich reproduzierbares Framework für Jahrzehnte.

---

## 63. Appendix Q: Deterministic API & Host Interface Specification (HAPI & SCI)
(Host Interface, API-Design, deterministische Kontrollpfade)

Dieses Kapitel beschreibt die beiden zentralen Host-Schnittstellen von KORA:

1. **HAPI – High-Level API**  
   Für Modellierer und High-Level-Frameworks.

2. **SCI – Scheduling & Compilation Interface**  
   Für Compiler, TSF-Generatoren und Host-Systeme.

Beide Schnittstellen sind vollständig deterministisch und eindeutig spezifiziert.  
Sie ermöglichen es, Modelle in TSF umzuwandeln, Monolithe auszuführen und Telemetrie sicher abzurufen.

### 63.1 Grundprinzipien der API-Designs

HAPI und SCI folgen fünf fundamentalen Regeln:

1. **Deterministische Semantik**  
       keine nondeterministischen API-Pfade.

2. **Keine dynamischen Zustände**  
       jeder API-Aufruf verändert den Zustand vorhersehbar.

3. **Idempotente Kontrollkommandos**  
       doppeltes Senden eines Befehls erzeugt identisches Ergebnis.

4. **Explizite Versionierung**  
       API-Versionen sind immer angegeben.

5. **Unabhängigkeit von Host-Frameworks**  
       API ist host-agnostisch (Python, C++, Rust, Go etc.).

### 63.2 HAPI – High-Level API

#### 63.2.1 Ziel der HAPI

HAPI dient dazu:

- Modelle zu laden,  
- Parameter zu setzen,  
- TSFs zu erzeugen,  
- Simulationen zu starten,  
- Ergebnisse abzurufen.

Sie ist **nicht** für Hardware-spezifische Details gedacht.

### 63.2.2 HAPI – Kernfunktionen

#### (A) Modell laden

    model = hapi.load_model("navier_stokes.py")

#### (B) Parameter setzen

    model.set_params({
        "grid": [512, 512, 256],
        "viscosity": 0.001
    })

#### (C) TSF erzeugen

    tsf = hapi.generate_tsf(model)

#### (D) Simulation starten

    result = hapi.simulate(tsf)

#### (E) Telemetrie abrufen

    telemetry = result.telemetry()

Alle Funktionen sind deterministisch – *gleiche Inputs → gleiche Outputs*.

### 63.3 SCI – Scheduling & Compilation Interface

SCI ist die Low-Level-Schnittstelle, die für:

- Compiler  
- TSF-Generatoren  
- Host-Systeme  
- Cluster-Management  

konzipiert ist.

### 63.3.1 Kernaufgaben von SCI

SCI steuert:

1. TSF-Validierung  
2. TSF-Übertragung an Monolithe  
3. deterministische Ausführung  
4. Telemetrie-Streaming  
5. Fehlererkennung  
6. Integration von Clustern

SCI arbeitet stets **zyklusgenau** und **zustandstransparent**.

### 63.3.2 SCI – Kommandos

#### (A) TSF laden

    sci.load_tsf(tsf_path)

→ Fehler bei ungültigen oder nicht validierten TSFs.

#### (B) Ausführung starten

    sci.run()

Startet den deterministischen Run.  
Keine Parameter erlaubt – *alle Werte sind im TSF definiert.*

#### (C) Status abrufen

    sci.status()

→ Werte: "idle", "running", "fault", "complete"

#### (D) Telemetrie streamen

    sci.telemetry(subsystem="dma")

Unterstützte Subsysteme:

- cycles  
- dma  
- fabric  
- reduction  
- memory  
- energy  

#### (E) Fehlerbericht abrufen

    sci.fault_report()

#### (F) Cluster-Topologie setzen (falls relevant)

    sci.set_cluster_map("cluster_map.json")

### 63.4 Deterministische API-Invarianten

#### 63.4.1 Keine versteckten Zustände

Es gibt:

- keinen globalen Scheduler,  
- keine dynamischen Optionen,  
- keine Umgebungsabhängigkeit.

#### 63.4.2 Keine zeitliche Varianz

Auch API-Reaktionen haben:

- konstante Antwortzeiten,  
- klare Zustandsübergänge,  
- keine Race Conditions.

#### 63.4.3 Keine dynamischen Ressourcen

Weder HAPI noch SCI allokieren:

- Memory on-the-fly  
- Compute auf Anfrage  
- asynchrone Buffer  

Alles wird statisch vorbereitet.

### 63.5 Fehlerverhalten der API

API löst niemals dynamische Recovery aus.

Stattdessen:

1. deterministischer Fehler  
2. vollständiger Report  
3. Abbruch  
4. Zustand: "fault"

Beispiel:

    error:
        tsf: invalid
        detail: "phase 7 overlaps with phase 8"

### 63.6 Clusterfunktionalität in SCI

SCI kann Multinode-Cluster deterministisch steuern:

#### (A) Topologie laden

    sci.set_cluster_map("mesh_4x4.json")

#### (B) TSF auf Knoten verteilen

    sci.distribute_tsf(mode="striped")

#### (C) Clusterlauf starten

    sci.run_cluster()

#### (D) Telemetrie pro Node

    sci.telemetry(node="3")

#### (E) Regression pro Node

    sci.compare_telemetry(node="3", golden="node3_gold.json")

### 63.7 Integration in Rechenzentrumssysteme

SCI kann in folgende Systeme integriert werden:

- Slurm  
- PBS  
- LSF  
- Kubernetes (deterministische Pods)  
- Bare-metal Nodes  

Mapping:

    cluster_scheduler → sci.run_cluster()

Keine dynamische Zuteilung von Ressourcen.  
Cluster müssen vor Start deterministisch fixiert sein.

### 63.8 Beispiel eines vollständigen Host-Workflows

    model = hapi.load_model("bert_base.py")
    model.set_params({"hidden_size": 768})
    tsf = hapi.generate_tsf(model)
    sci.load_tsf(tsf)
    sci.set_cluster_map("mesh_4x4.json")
    sci.run_cluster()
    telemetry = sci.telemetry("all")
    sci.export_results("run_2025_11_21/")

### 63.9 Formale Garantien

HAPI und SCI garantieren:

1. **Deterministische Ausführung aller Kommandos**  
2. **Idempotenz aller Kontrollaufrufe**  
3. **vollständige Zustandswiederholbarkeit**  
4. **numerische Reproduzierbarkeit**  
5. **Telemetrie-Transparenz**  

Diese Eigenschaften sind zentral für:

- Open Science  
- Reproduzierbarkeit  
- Cluster-Stabilität  
- Debugging  
- Peer Review

### 63.10 Fazit

Kapitel 63 definiert die deterministischen APIs von KORA.  
HAPI bietet High-Level-Steuerung,  
SCI bietet Low-Level-Kontrolle,  
beide garantieren maximale Reproduzierbarkeit und Transparenz.

Dieses Kapitel bildet den formalen Abschluss des Host-Schnittstellendefinitionsraums.

---

## 64. Appendix R: Formal Proofs of Determinism (Extended)
(Formale Beweise, Invarianten, Scheduling, Kommunikation, Numerik)

Dieses Kapitel erweitert die formalen Grundlagen aus Kapitel 49 und liefert
vollständige, strenge Beweise für die deterministische Ausführung, Kommunikation,
Numerik und Cluster-Synchronisation von KORA.

Es richtet sich an:
- theoretische Informatiker
- Reviewer bei wissenschaftlichen Veröffentlichungen
- Verifikationsingenieure
- Auditoren
- HPC-/Compiler-Forscher

### 64.1 Grundbegriffe

Wir definieren:

- T: Scheduling Tree  
- V: Menge der Phasen (Nodes)  
- E: Menge gerichteter Kanten (Abhängigkeiten)  
- M: Menge der Memorybanks  
- F: Menge der Fabric-Pfade  
- D: Menge der DMA-Operationen  
- R: Menge der Reduktionen  

Eine KORA-Ausführung besteht aus einem Tupel:

    K = (T, M, F, D, R)

Die deterministische Ausführung ist definiert als:

    run(K, input) → (output, telemetry)

### 64.2 Theorem 1 – Azyklische Scheduling-Deterministik

#### 64.2.1 Aussage

Wenn der Phase-Graph T azyklisch ist, ist die Ausführungsreihenfolge eindeutig bestimmt.

Formaler:

    T = (V, E)
    E enthält keine gerichteten Zyklen
    ⇒ topologische Ordnung V* ist eindeutig

#### 64.2.2 Beweis

Da T ein DAG ist, existiert mindestens eine topologische Ordnung.

KORA erzwingt zusätzlich:

- eindeutige Startzyklen  
- eindeutige Endzyklen  

Damit ist jede Phase p_i eindeutig definiert:

    start(p_i) < start(p_j) ⇔ p_i kommt vor p_j

Da es keine Variation der Zyklen gibt:

    Var(start(p_i)) = 0  
    Var(end(p_i))   = 0

Damit existiert nur **eine** gültige Reihenfolge.

QED.

### 64.3 Theorem 2 – Zeitinvarianz der Ausführung

#### 64.3.1 Aussage

Für jede Phase p ∈ V ist die Ausführungszeit konstant:

    T(p) = end(p) - start(p) = konst.

Damit ist:

    T_total = Σ T(p)

invariant.

#### 64.3.2 Beweis

Da:
- Taktfrequenz konstant,
- keine Boost-Mechanismen,
- alle Operationen statisch geschedult,
- keine dynamischen Speicherzugriffe,

gilt:

    Zeit(p) = #Zyklen(p) × (1/frequenz) = konstant

Somit:

    T_total(input) = T_total(für jedes identische input)

Damit ist die Gesamtlaufzeit deterministisch.

QED.

### 64.4 Theorem 3 – Deterministische Memoryzugriffe

#### 64.4.1 Aussage

Jeder Speicherzugriff besitzt:

- feste Bank,
- festen Offset,
- feste Größe,
- feste Zykluszuordnung.

Damit ist der gesamte Speicherpfad deterministisch.

#### 64.4.2 Beweis

Memorymapping:

    mem(p) = (bank, offset, size, cycle)

ist vollständig statisch.  
Da es:

- keine Caches,
- keinen Prefetch,
- keinen dynamischen Reuse,
- keine Coherency-Protokolle

gibt, gilt:

    mem_access(p, run1) = mem_access(p, run2)

für alle p ∈ V.

Somit bleibt der Speicherpfad invariant.

QED.

### 64.5 Theorem 4 – DMA-Determinismus

#### 64.5.1 Aussage

Jede DMA-Operation d ∈ D besitzt:

- festen Startzyklus  
- festen Endzyklus  
- feste Blockgröße  
- feste Quelle und Ziel

und ist disjunkt zu allen anderen DMA-Fenstern.

#### 64.5.2 Beweis

KORA erzwingt formal:

1. Disjunktheit:
       ∀ d_i, d_j ∈ D, i ≠ j:
           [start_i, end_i] ∩ [start_j, end_j] = ∅

2. Feste Parameter:
       size(d) = konstant
       src(d)  = konstant
       dst(d)  = konstant

Da es keine dynamischen DMA-Repeats gibt (0 Retries):

    dma(run1) = dma(run2)

für alle gültigen Runs.

QED.

### 64.6 Theorem 5 – Fabric-Determinismus im Cluster

#### 64.6.1 Aussage

Für jede Nachricht n ∈ F gilt:

- slot(n) ist konstant
- route(n) ist konstant
- latency(n) ist konstant

Damit ist die Reihenfolge aller Cluster-Nachrichten deterministisch.

#### 64.6.2 Beweis

Fabric TDM erzwingt:

    slot(n) = f(src, dst, topology)

Die Funktion f ist statisch und abhängig nur von der Clustergeometrie.

Da Routing nicht dynamisch ist:

    route(n) = f_route(src, dst)

Eine Nachricht wird exakt in einem festen Zeitpunkt übertragen:

    transmit_cycle(n) = slot(n) × slot_length + offset

Damit:

    arrival_cycle(n) = transmit_cycle(n) + hops × latency

Da alle Parameter konstant sind:

    arrival_cycle(n) invariant

Somit ist jede Kommunikation deterministisch.

QED.

### 64.7 Theorem 6 – Reduktions-Determinismus

#### 64.7.1 Aussage

Jede Reduktion r ∈ R ist deterministisch, wenn:

- Baumstruktur fix  
- Reihenfolge fix  
- Numerikprofil fix  

#### 64.7.2 Beweis

Reduktionsbaum:

        r7
       /  \
     r3    r6
    / \   / \
   r1 r2 r4 r5

Da:

- keine parallele Summation  
- keine dynamischen Reorderings  
- f(a,b) → deterministische FP oder Soft-FP

gilt:

    reduce(run1) = reduce(run2)

QED.

### 64.8 Theorem 7 – Numerische Reproduzierbarkeit (Soft-FP)

#### 64.8.1 Aussage

Soft-FP (Profil C) erzeugt bitgenaue Resultate für jede numerische Operation.

#### 64.8.2 Beweis

Soft-FP definiert:

- exakte Align-Regeln  
- exakte Mantissenoperationen  
- exakte Rundungsregeln  
- exakte Normalisierung  

Damit ist die Funktion:

    soft_fp_op(a, b)

ein **deterministischer endlicher Automatenübergang**.

Da der gesamte FP-Baum deterministisch ist:

    result(run1) = result(run2)

bitgenau.

QED.

### 64.9 Theorem 8 – Gesamt-Determinismus der Ausführung

#### 64.9.1 Aussage

Wenn Scheduling, DMA, Memory, Kommunikation und Numerik deterministisch sind,
ist der gesamte Run deterministisch.

#### 64.9.2 Beweis

Der Run ist:

    run(K, input) = (output, telemetry)

mit:

    K = (T, M, F, D, R)

Da alle fünf Komponenten deterministisch sind:

- T → eindeutige Reihenfolge  
- M → eindeutige Speicherzugriffe  
- F → eindeutige Kommunikation  
- D → eindeutige DMA  
- R → eindeutige Numerik  

ist die Ausführung vollständig determiniert.

Somit gilt:

    run(K, input1) = run(K, input2)

für identische Inputs.

QED.

### 64.10 Korollar – Energie- und Zeitdeterminiertheit

Da:

- T_total deterministisch (Theorem 2)
- Leistung konstant (Kapitel 53)
- Kommunikation deterministisch (Theorem 5)

gilt:

    E_total = P × T_total = konstant

Energie ist damit genauso deterministisch wie Zeit und Output.

QED.

### 64.11 Fazit

Kapitel 64 liefert erweiterte formale Beweise dafür, dass:

- Scheduling  
- DMA  
- Kommunikation  
- Numerik  
- Speicher  
- Cluster  

und damit der gesamte KORA-Monolith deterministisch sind.

Diese Beweise bilden den theoretischen Kern der Reproduzierbarkeit und
wissenschaftlichen Zuverlässigkeit von KORA.

---

## 65. Appendix S: Energy Modeling Framework (Extended)
(Energiemodell, thermische Modelle, Fabric-/DMA-Kosten, PUE, Vergleich)

Dieses Kapitel beschreibt das vollständige Energiemodell von KORA.  
Es erweitert die Grundlagen aus Kapitel 5 und 53 um:

- detaillierte Energiebilanzierung  
- thermische Modelle  
- Fabric-/DMA-Kosten  
- Lastprofile  
- PUE-Propagation  
- Vergleichsformeln für GPU/HPC/Monolith  

Es richtet sich an Energie-/Thermikexperten, HPC-Architekten und Reviewer.

### 65.1 Ziele des Energiemodells

Das Modell ermöglicht:

1. **Vergleich klassischer GPU-Systeme mit KORA**
2. **Vorhersage des Energieverbrauchs**
3. **Reproduzierbare wissenschaftliche Benchmarks**
4. **ökologische Bewertung**
5. **energieeffiziente Optimierung von Workloads**

Es ist so gestaltet, dass es über Jahrzehnte stabil und vergleichbar bleibt.

### 65.2 Struktur der Energiekomponenten

Ein vollständiger Energieverbrauch setzt sich aus folgenden Komponenten zusammen:

1. **Compute Energy (E_compute)**  
2. **Memory Energy (E_memory)**  
3. **DMA Energy (E_dma)**  
4. **Fabric Energy (E_fabric)**  
5. **Control/Idle Energy (E_ctl)**  
6. **Cooling/PUE Overhead (E_pue)**  

Der Gesamtverbrauch ist:

    E_total = E_compute + E_memory + E_dma + E_fabric + E_ctl + E_pue

### 65.3 Compute Energy (E_compute)

Für deterministische Systeme gilt:

    E_compute = P_compute × T_compute

mit:

- P_compute = konstante Compute-Leistung  
- T_compute = deterministische Zyklenzeit  

Da keine Varianz existiert:

    Var(E_compute) = 0

(Dies unterscheidet KORA fundamental von GPUs.)

### 65.4 Memory Energy (E_memory)

Memorykosten bestehen aus:

- Bank-Aktivierung  
- Datenzugriff  
- Refresh-Kosten (nicht variabel)  

Formel:

    E_memory = N_accesses × E_access(bank)

Da Memorybanks deterministisch verteilt sind:

    E_access(bank) = konstant

Im Gegensatz zu GPU/HPC:  
→ keine Cache-Abhängigkeit  
→ keine variablen Latenzen  
→ keine Unstetigkeiten

### 65.5 DMA Energy (E_dma)

DMA-Kosten bestehen aus:

- Quellzugriff  
- Übertragung  
- Zielzugriff  

Formel:

    E_dma = Σ (size_i × e_dma_byte)

wobei:

- size_i deterministisch  
- e_dma_byte konstant

Auch hier:

    Var(E_dma) = 0

### 65.6 Fabric Energy (E_fabric)

Fabric basiert auf TDM-Links:

- konstante Datenrate  
- konstantes Multiplexing  
- konstante Hop-Kosten  

Formel:

    E_fabric = Σ (bytes × e_link) + hops × e_hop

Da hops deterministisch:

    E_fabric invariant

### 65.7 Control/Idle Energy (E_ctl)

KORA besitzt:

- kein OS  
- keinen Scheduler  
- keine dynamischen Threads  
- keine Interrupts  

Control-Energie folgt:

    E_ctl = P_ctl × T_total

wobei P_ctl extrem niedrig und konstant ist.

### 65.8 Cooling/PUE Propagation (E_pue)

PUE (Power Usage Effectiveness):

    PUE = (IT_Power + Cooling_Power) / IT_Power

Für Rechenzentren typischer Werte:

- schlecht: 1.7–2.0  
- gut: 1.3–1.5  
- hyperscale: 1.15

KORA erzeugt sehr wenig Abwärme → niedrige Heizlast → niedriger PUE.

Energie nach PUE:

    E_total_pue = E_total × PUE

Da KORA weniger Verlustwärme erzeugt:

    PUE_kora < PUE_gpu

Typische Werte (konservativ):

- GPU-Cluster: 1.50  
- KORA-Monolith: 1.20

### 65.9 Dynamische Lastprofile

#### 65.9.1 Klassische GPU-Systeme:

- Boost-Mechanismen  
- variable Frequenzen  
- thermische Throttles  
- dynamischer Load Balancer  

Daraus folgen:

- variable Zuordnung von Tasks  
- variable Latenzen  
- variabler Energieverbrauch

#### 65.9.2 KORA:

- konstante Frequenz  
- konstante Spannung  
- kein Throttling  
- kein dyn. Scheduler  
- kein Power Management  

Daraus folgen:

- konstante Energie pro Operation  
- konstante Performance  
- perfekte wissenschaftliche Vergleichbarkeit

### 65.10 Energievergleich: GPU vs KORA

GPU-Energie:

    E_gpu = (E_compute + E_memory + E_dma + E_fabric + E_ctl) × PUE_gpu
           + E_var

E_var variiert mit:

- Temperatur  
- Boost  
- Load Balance  
- Cache-Zuständen

KORA-Energie:

    E_kora = (E_compute + E_memory + E_dma + E_fabric + E_ctl) × PUE_kora

Ohne Varianzterm.

#### Verhältnis:

    E_kora / E_gpu ≈ 0.05–0.25

(5–25 %, abhängig vom Workload)

### 65.11 Thermisches Modell

KORA erzeugt:

- lineare Temperaturkurven  
- keine Hotspots  
- keine schnellen Temperaturwechsel  

GPU erzeugt:

- steile Temperaturwechsel  
- unvorhersagbare Boosts  
- variable Kühlleistung  

Thermische Bilanz:

    E_cooling ∝ ΔT × k_cooling

Da ΔT bei KORA sehr gering:

    E_cooling_kora < E_cooling_gpu

### 65.12 Zeit/Energie-Korrelation

Da die Zeit deterministisch ist:

    E_total = P × T_total

Dies gilt sowohl bei:

- Einzelmonolith  
- Cluster  
- Multinode-Shuffles  

Enormer Vorteil für:

- Wissenschaft  
- Reproduzierbarkeit  
- Energieaudit

### 65.13 Energie-Sensitivitätsanalyse

Ein kleiner Parameterwechsel, z. B.:

- andere Gridgröße  
- anderes Batchsize  
- andere Datenmenge  

ändert nur:

    T_total

Aber nicht:

- Leistungsaufnahmen  
- Kosten pro Operation  

Keine Interaktionseffekte.

### 65.14 Beispielrechnung (CFD Large)

Angenommen:

- P = 3.2 kW  
- T = 11.5 h  

Dann:

    E = 3.2 × 11.5 = 36.8 kWh

Unter realistischem PUE = 1.20:

    E_total ≈ 44.2 kWh

GPU-Cluster:

- z. B. 30 GPUs  
- P_total ≈ 35 kW  
- T ≈ 17 h  
- PUE ≈ 1.50

    E_total_gpu ≈ 892 kWh

Ersparnis:

    ≈ 95 %

### 65.15 Langzeit-Energiebewertung (wissenschaftlich)

KORA ermöglicht:

- jahrzehntelange Energievergleiche  
- unveränderliche Modellbasis  
- bitgenaue Basisdaten  

Im Gegensatz zu GPU-Systemen, die:

- Boost-Stufen ändern  
- Treibervarianten ändern  
- Firmware ändern  
- Varianz in Rechenzeit und Energie haben

### 65.16 Fazit

Kapitel 65 beschreibt ein vollständiges, erweiterbares Energiemodell, mit dem:

- Energieverbräuche  
- Vergleichswerte  
- thermische Modelle  
- PUE-Abschätzungen  
- und Workload-Profile  

für KORA, GPU-Cluster und klassische HPC-Systeme transparent gegenübergestellt werden.

Dieses Modell bildet die Grundlage für ökologische Bewertung, Kostenberechnung und Energieauditfähigkeit.

---

## 66. Appendix T: Deterministic I/O & Storage Model
(Ein-/Ausgabe, Checkpoints, Logging, deterministisches Dateiverhalten)

Dieses Kapitel beschreibt das I/O- und Storage-Modell von KORA.  
Es garantiert, dass alle Ein- und Ausgaben deterministisch sind, unabhängig von:

- Hostbetriebssystem  
- Filesystem  
- Cluster  
- Zeit  
- Umgebung  
- Konfiguration  
- Laufzeitvariabilität klassischer Systeme

Damit bildet Appendix T die Grundlage für wissenschaftliche Reproduzierbarkeit und Archivierung.

### 66.1 Ziele des deterministischen I/O-Modells

Das Modell garantiert:

1. **bitgenaue Outputs**  
2. **deterministische Checkpoints**  
3. **deterministische Sequenzen von I/O-Operationen**  
4. **transparente Versionierung**  
5. **universellen Import/Export**  
6. **stabile Archivierung**  

Ziel ist die totale Abwesenheit jeglicher I/O-Variabilität.

### 66.2 Grundprinzipien

Das I/O-Modell folgt sechs invarianten Regeln:

1. **Keine Zeitabhängigkeit**  
       → keine timestamps in Ergebnissen  
       → keine clock-getriebene Variabilität  

2. **Keine Nebenläufigkeit**  
       → kein asynchrones Schreiben  
       → keine Threads im I/O-Pfad  

3. **Keine Puffer-Variabilität**  
       → I/O erfolgt in festen Blockgrößen  

4. **Statische Dateistruktur**  
       → alle Dateiformate sind streng definiert  

5. **Statische Ausgabeparameter**  
       → keine dynamischen Dateinamen, keine Zufallswerte  

6. **Inhaltsbasierte Hashes**  
       → alle Dateien prüfen sich selbst mittels SHA256

### 66.3 Deterministische Dateistruktur

Ein kompletter Lauf hat die Struktur:

    run_<id>/
        input/
        output/
        checkpoints/
        logs/
        telemetry/
        metadata/

Jede Datei:

- besitzt festen Namen  
- besitzt feste Felder  
- ist vollständig beschrieben  
- ist versioniert  

### 66.4 Deterministische Dateinamen

Dateinamen bestehen aus:

    <purpose>_<version>.<extension>

Beispiele:

    velocity_1.0.h5
    pressure_1.0.h5
    loss_curve_1.0.json
    energy_1.0.json

Keine Zeitstempel, keine Zufallswerte, keine dynamischen Suffixe.

### 66.5 Deterministische HDF5-Ausgabe

HDF5 wird genutzt für:

- Tensorfelder (CFD)  
- Modellgewichte (ML)  
- große Datenausgaben  

Regeln:

1. Gruppenstruktur fix  
2. Datensätze fix  
3. Datentypen fix  
4. Endianness fix  
5. Chunk-Größen fix  
6. Kompressionsparameter fix  

Beispielstruktur:

    /field/
        u (float32)
        v (float32)
        w (float32)
    /pressure/
        p (float32)

Damit ist jeder HDF5-Output bitgenau reproduzierbar.

### 66.6 Deterministische JSON-Ausgabe

JSON wird genutzt für:

- Telemetrie  
- Logs  
- Metadaten  

Regeln:

1. Key-Sortierung lexikografisch  
2. feste Formatierung (spaces=4)  
3. kein Newline am Ende  
4. numerisch deterministische Darstellung (kein scientific drift)

Beispiel:

    {
        "cycles": 1234567,
        "phase": 14,
        "energy_kwh": 3.812
    }

### 66.7 Checkpointing

Checkpoints folgen:

    checkpoint_<step>.ckpt

Mechanik:

- deterministische Reihenfolge  
- statische Binärformate  
- keine Kompression variiert zur Laufzeit  
- feste Blockgrößen  

Beispielinhalte:

    state:
        tile_group_0: [...]
        tile_group_1: [...]
    memory:
        bank_0: [...]
        bank_1: [...]

Checkpoints sind vollständig bitgenau.

### 66.8 Logging

Logging erfolgt in:

    logs/run.log

Log-Eigenschaften:

- keine Timestamps  
- deterministische Reihenfolge  
- deterministische Inhalte  

Beispiel:

    RUN_START
    LOAD_TSF
    VALIDATE_TSF
    EXECUTE_PHASE_1
    EXECUTE_PHASE_2
    RUN_END

### 66.9 Telemetrie

Telemetrie besteht aus:

    telemetry/timeline.json
    telemetry/fabric.json
    telemetry/dma.json
    telemetry/memory.json
    telemetry/energy.json

Alle Dateien folgen deterministischem JSON-Modell.

### 66.10 Import/Export-Modell

Import:

- Eingabedateien werden per SHA256 validiert  
- Schema-Dateien beschreiben exakte Datenfelder  
- fehlerhafte Inputs → deterministischer Abbruch  

Export:

- Dateien unveränderlich  
- Hashes in `metadata/hashes.json` gespeichert  
- ideal für Archivierung  

### 66.11 Host-Filesystem-Interaktion

Interaktion mit Host-FS ist minimal:

- keine parallelen Schreibprozesse  
- feste Flush-Punkte  
- konstante Blockgrößen  
- keine Abhängigkeit von Kernel-Cache

Dadurch bleibt I/O unabhängig von:

- Betriebssystem  
- Kernel-Version  
- Filesystem-Typ  
- Hintergrundprozessen  

### 66.12 Multi-Node I/O (Cluster)

Bei mehreren Monolithen:

    node_0/output/
    node_1/output/
    node_2/output/

Jeder Node schreibt deterministisch zu festen Zeiten.

Keine kollektiven Schreiboperationen wie:

- MPI-IO  
- Collective FileWrites  
- POSIX Shared I/O  

Dadurch entstehen keine Race Conditions.

### 66.13 I/O-Failure Model

Fehler sind deterministisch:

    I/O_ERROR:
        file: "field_1.0.h5"
        reason: "checksum mismatch"
        cycle: 993124

Keine automatische Recovery.

### 66.14 Archivierung (Langzeit)

Empfohlene Struktur:

    archive/
        run_0001/
        run_0002/
        runs_index.json
        checksums.txt

Archive sind stabil über Jahrzehnte:

- offene Formate  
- eindeutige Schemas  
- keine hostabhängigen Elemente  

### 66.15 Fazit

Kapitel 66 definiert ein deterministisches I/O-Modell mit:

- bitgenauer Reproduzierbarkeit  
- stabilen Outputformaten  
- deterministischen Checkpoints  
- deterministischem Logging  
- clusterkompatibler I/O-Struktur  
- wissenschaftlicher Auditierbarkeit  

Damit ist garantiert, dass jeder KORA-Run – unabhängig von Zeit, Ort oder Hardwaregeneration – identische Ergebnisse hervorbringt.

---

## 67. Appendix U: Reference Cluster Deployment Guide
(Deterministische Cluster-Aufstellung, Verkabelung, Initialisierung, Betrieb)

Dieses Kapitel beschreibt die Referenzempfehlungen für den Aufbau eines
deterministischen KORA-Clusters.  
Die Richtlinien sind *nicht* betriebssystemspezifisch, sondern legen
fest:

- Topologien  
- Verkabelung  
- Konfigurationsdateien  
- deterministische Initialisierung  
- Bootreihenfolge  
- Cluster-Mapping  
- Node-Integrität  
- Telemetrie-Setup  

Ziel:  
**Jeder KORA-Cluster soll unabhängig vom Betreiber deterministisch laufen.**

### 67.1 Clustergrundlagen

Ein KORA-Cluster besteht aus:

- N KORA-Monolithknoten  
- deterministischen TDM-Fabric-Verbindungen  
- Host-System (Master Node)  
- Cluster-Map  
- TSF-Distribution  
- Telemetrie-Collector  

Clustergröße (Beispiele):

- Small: 4–16 Nodes  
- Medium: 32–128 Nodes  
- Large: 256–4096 Nodes

Topologie muss **vor Laufzeit festgelegt** werden (kein dynamischer Aufbau).

### 67.2 Unterstützte deterministische Topologien

Siehe Appendix M für Details.

Typisch:

1. 2D Mesh (Standard)  
2. 2D Torus (CFD-optimiert)  
3. Star (ML-Aggregation)  
4. Hierarchical Mesh (sehr große Cluster)

Für Deployments wird Mesh empfohlen:

    rows = R  
    cols = C  
    nodes = R × C

### 67.3 Physische Verkabelung

#### 67.3.1 Fabric-Kabel

Die Fabric besteht aus:

- 16 deterministischen Links pro Node  
- festen Ein-/Ausgängen  
- TDM-Zeitfenstern  

Hardware-Ports:

    port_0: north
    port_1: east
    port_2: south
    port_3: west
    port_4–15: optional mesh/torus extensions

#### 67.3.2 Verkabelungsregeln

1. Jeder Port verbindet exakt *einen* Nachbarn.  
2. Keine Kreuzungen, keine Switche, keine Hubs.  
3. Nur Punkt-zu-Punkt-Verbindungen.  
4. Kabellängen innerhalb ±5% Toleranz.  
5. Kein Hot-Plugging (Cluster wird kalt verdrahtet).  

### 67.4 Cluster-Mapping-Dateien

Das Cluster-Mapping ist ein zentrales Element:

    cluster_map.json

Beispiel:

    {
        "topology": "mesh",
        "rows": 4,
        "cols": 4,
        "nodes": [
            {"id":0, "pos":[0,0], "ports":{"east":1}},
            {"id":1, "pos":[0,1], "ports":{"west":0,"south":5}},
            ...
        ]
    }

Regeln:

- Position eindeutig  
- Ports eindeutig  
- Topologie vollständig beschrieben  

### 67.5 Host-Konfiguration

Der Host ist:

- Master Node  
- TSF-Verteiler  
- Telemetrie-Kollector  
- Validierungsmaschine  
- Cluster-Orchestrator  

Host-Aufgaben:

1. Cluster-Map laden  
2. TSF validieren  
3. TSF auf Nodes verteilen  
4. Cluster synchron starten  
5. Telemetrie sammeln  
6. Hashes prüfen  
7. Ergebnisse archivieren  

Der Host führt **keine Berechnungen** aus.

### 67.6 Bootreihenfolge

#### 67.6.1 Kaltstart (empfohlen)

1. Host starten  
2. Fabric aktivieren  
3. alle Nodes booten  
4. Fabric-Handshake validieren  
5. Cluster-Map prüfen  
6. TSF verteilen  
7. Cluster initialisieren  
8. Run starten

#### 67.6.2 Warmstart (selten)

- nur für Debugging  
- nicht empfohlen bei produktionellen Runs  

### 67.7 Deterministische Initialisierung

Initialisierung besteht aus:

1. **Fabric-Zeit-Fixierung**  
2. **DMA-Slot-Synchronisation**  
3. **Clock Domain Lock**  
4. **Tile Group Reset**  
5. **Memorybank Zeroing (optional)**  
6. **Cluster Heartbeat aktivieren**

Sobald alle Nodes:

- identische Clock-Lock-Signale  
- identische Fabric-Ping-Runden  

erreicht haben, gilt:

    cluster_state = "READY"

### 67.8 TSF-Distribution

TSF wird per SCI verteilt:

    sci.distribute_tsf("model.tsf", mode="striped")

Modi:

- **striped** – TSF auf alle Nodes streifenweise verteilen  
- **replicated** – TSF auf allen Nodes vollständig  
- **partitioned** – TSF gemäß Cluster-Map segmentiert  

Fehler in der Verteilung führen zum deterministischen Abbruch.

### 67.9 Starten deterministischer Clusterläufe

Clusterlauf starten:

    sci.run_cluster()

Algorithmus:

1. Host sendet Startsignal.  
2. Nodes fixieren ihren Startzyklus.  
3. Fabric beginnt im exakt gleichen Fabric-Slot.  
4. DMA wird deterministisch aktiviert.  
5. Telemetrie beginnt mit Zyklus 0.  

### 67.10 Telemetriesammlung

Telemetrie wird nodeweise gesammelt:

    telemetry/node_0/*
    telemetry/node_1/*

Host-Collector:

- sammelt zyklusgenaue Daten  
- prüft Hashes  
- synchronisiert Telemetriezeilen  

Telemetrie umfasst:

- DMA  
- Memory  
- Fabric  
- Energie  
- Phase Timeline  
- Reduktionen  

Damit sind Clusterläufe **vollständig auditierbar**.

### 67.11 Fehlerbehandlung

Deterministisches Fehlerverhalten:

- Slot-Kollision → Fault  
- Fabric-Pfadabweichung → Fault  
- Node-Abweichung → Fault  
- TSF-Fehler → Fault

Cluster hält sofort an.

Host erhält:

    fault_type
    node_id
    cycle
    detail

Keine automatische Recovery.

### 67.12 Beispiel einer vollständigen Deployment-Checkliste

#### 1. Hardware  

- Kabelkonsistenz prüfen  
- Ports prüfen  
- Mesh/Torus bestätigen  
- Spannungsversorgung stabil  

#### 2. Host  

- cluster_map.json geladen  
- TSF validiert  
- Golden Runs vorhanden?  

#### 3. Initialisierung  

- Clock Domain Lock passt  
- Fabric-Zeit fixiert  
- Tile Groups bereit  

#### 4. Lauf  

- sci.run_cluster()  
- Telemetrie sammeln  
- Hashes prüfen  
- Ergebnisse archivieren  

### 67.13 Beispiel-Topologien

#### 4x4 Mesh

    (0,0) -- (0,1) -- (0,2) -- (0,3)
      |        |        |        |
    (1,0) -- (1,1) -- (1,2) -- (1,3)
      |        |        |        |
    (2,0) -- (2,1) -- (2,2) -- (2,3)
      |        |        |        |
    (3,0) -- (3,1) -- (3,2) -- (3,3)

#### 3x3 Torus

    [0,0] -- [0,1] -- [0,2] --+
      |        |        |     |
    [1,0] -- [1,1] -- [1,2] --+
      |        |        |     |
    [2,0] -- [2,1] -- [2,2] --+

### 67.14 Empfehlungen für Rechenzentren

- keine Switches verwenden  
- deterministische Verkabelung  
- redundante Stromversorgung  
- identische Kabellängen  
- Host in separater Node-Gruppe  
- Golden Runs archivieren  

### 67.15 Fazit

Kapitel 67 beschreibt die vollständige, deterministische Vorgehensweise,
einen KORA-Cluster zu deployen.  
Das Deployment bleibt:

- transparent  
- nachvollziehbar  
- auditierbar  
- wiederholbar  
- vollständig deterministisch  

Damit ist KORA sowohl für Forschungseinrichtungen als auch für
Rechenzentren einsetzbar, ohne Komplexität oder Variabilität einzuführen.

---

## 68. Appendix V: Educational Examples
(Einfach nachvollziehbare Beispiele zur Illustration der KORA-Prinzipien)

Dieses Kapitel enthält eine Sammlung kleiner, leicht verständlicher Beispiele, die
die deterministischen Prinzipien von KORA demonstrieren.

Die Beispiele richten sich an:

- Studierende
- neue Wissenschaftlerinnen und Wissenschaftler
- Reviewer
- Personen aus anderen Fachbereichen
- Interessierte, die den deterministischen Ansatz nachvollziehen wollen

Alle Beispiele sind *vollständig ausführbar* (über Simulator) und *bitgenau reproduzierbar*.

### 68.1 Beispiel 1 – Minimaler TSF (Addition zweier Zahlen)

Dies ist der kleinste mögliche TSF, der zwei Zahlen addiert.

#### Zweck

Das Beispiel zeigt:

- wie ein TSF strukturiert ist  
- wie deterministische Phasen funktionieren  
- wie die Ausgabe reproduzierbar bleibt  

#### Mini-TSF

    tsf:
        version: 1.0
        phases:
            - id: 0
              op: "load"
              src: "input/a"
              dst: "r0"
            - id: 1
              op: "load"
              src: "input/b"
              dst: "r1"
            - id: 2
              op: "add"
              a: "r0"
              b: "r1"
              dst: "r2"
            - id: 3
              op: "store"
              src: "r2"
              dst: "output/c"

#### Resultat

Bei Eingaben:

    a = 7
    b = 5

ist:

    output/c = 12

Jeder Lauf liefert denselben Output.

### 68.2 Beispiel 2 – Deterministischer Mini-CFD-Stencil (2×2×2)

Dieses Beispiel simuliert *einen* Stencil-Schritt auf einem *sehr kleinen* 2×2×2-Gitter.

#### Zweck

Es demonstriert:

- Memory-Mapping  
- Stencil-Kernel  
- deterministische Berechnung  

#### Mini-TSF (Ausschnitt)

    phases:
        - id: 0
          op: "stencil7"
          grid: [2,2,2]
          input: "u_old"
          output: "u_new"
          coeffs: [c0, c1]

Das Ergebnis ist klein genug, um es manuell nachrechnen zu können.

### 68.3 Beispiel 3 – Deterministischer Mini-Reduction-Baum

#### Zweck

Demonstriert:

- deterministische Reduktionen
- feste Reihenfolge
- numerische Reproduzierbarkeit
- Unterschied zu GPU-Reduktionen

#### Beispielzahlen

    [3.0, 1.0, 2.0, 4.0]

#### Feste Reihenfolge

    (((3.0 + 1.0) + 2.0) + 4.0)

Ergebnis:

    10.0

Soft-FP-Version ergibt bitidentisch denselben Wert.

### 68.4 Beispiel 4 – Mini-BERT-Forward-Pass (1 Layer)

#### Zweck

Zeigt:

- deterministische Matrixmultiplikation  
- deterministische Attention-Berechnung  
- feste Rechenpfade  

#### Setup

    seq_len = 4
    hidden = 8
    heads = 2

Mini-TSF führt:

1. QKV-Linear  
2. Attention Scores  
3. Softmax  
4. Weighted Sum  

durch — mit deterministischen FP-Schritten.

### 68.5 Beispiel 5 – Kleinstes Big-Data-Beispiel

#### Zweck

Demonstriert deterministische:

- Partitionierung  
- Shuffle  
- Join  
- Aggregation  

#### Beispiel-Datensatz

Tabelle A:

| id | value |
|----|--------|
| 1  |   5    |
| 2  |   3    |

Tabelle B:

| id | weight |
|----|--------|
| 1  |   10   |
| 2  |    2   |

#### Shuffle

Partitionen:

    id % 2

#### Join (deterministisch)

Ergebnis:

| id | value | weight |
|----|--------|---------|
| 1  |   5    |   10    |
| 2  |   3    |    2    |

### 68.6 Beispiel 6 – Mini-Clusterlauf (2 Nodes)

#### Zweck
Demonstriert:

- deterministische Kommunikation  
- feste Fabric-Slots  
- feste Nachrichtenpfade  

#### Setup

    Node0 ↔ Node1

Mini-Nachricht:

    "u_boundary" von Node0 nach Node1 im Slot 3

Fabric-Parameter:

    slot_length = 64 cycles  
    hops = 1  
    link_latency = 3 cycles  

Ankunftszyklus:

    3 × 64 + 3 = 195 cycles

Kein Jitter.

### 68.7 Beispiel 7 – Telemetrie-Minibeispiel

Beispiel `timeline.json`:

    {
        "cycles": [0, 512, 1024, 1536],
        "phase":  [0,   1,    2,    3 ]
    }

Beispiel `energy.json`:

    {
        "kwh": 3.812,
        "profile": [0.32, 0.32, 0.32, 0.32]
    }

### 68.8 Beispiel 8 – Mini-Golden-Run

Ein gültiger Golden Run für Beispiel 1 sieht so aus:

    run_0001/
    tsf/
    add_two_ints.tsf
    input/
    a.txt
    b.txt
    output/
    c.txt
    metadata/
    hash.json
    run_info.json

Hashes identisch → Run gültig.

### 68.9 Fazit

Dieses Kapitel stellt kleine, leicht nachvollziehbare Beispiele bereit, die zeigen:

- wie TSFs aufgebaut sind  
- wie deterministische Rechenmodelle funktionieren  
- wie Numerik, Memory, DMA und Fabric zusammenarbeiten  
- wie Mini-Cluster laufen  
- wie Telemetrie aussieht  

Diese Beispiele dienen als erste Lernbasis und als didaktische Ergänzung für das Verständnis der vollständigen KORA-Spezifikation.

---

## 69. Appendix W: Glossary of Deterministic Computing Concepts
(Begriffe rund um deterministische Systeme, KORA-Architektur, TSF, HPC)

Dieses Glossar enthält die wichtigsten Begriffe der KORA-Spezifikation.
Sie dienen als Referenz und erleichtern das Lesen der Dokumentation.

#### A

##### **Acyclic Execution**  
Ausführung ohne gerichtete Zyklen. Grundlage des deterministischen Scheduling Trees.

##### **API (HAPI/SCI)**  
Host-Schnittstellen von KORA zur TSF-Erzeugung, Validierung und Ausführung.

##### **Attention Determinism**  
Die Eigenschaft, dass Attention-Berechnungen (ML) bitgenau reproduzierbar sind.

#### B

##### **Bank (Memory Bank)**  
Feste Speichersegmente im Monolithen mit unabhängigen, deterministischen Latenzen.

##### **Boundary Exchange (Ghost Exchange)**  
Datenaustausch für PDE-Gitter (CFD). Bei KORA deterministisch im TDM-Slot.

##### **Block Size (I/O)**  
Feste I/O-Blöcke ohne dynamische Pufferung; wichtig für deterministische Speicherung.

#### C

##### **Cache-Free Architecture**  
KORA besitzt kein Cache-Hierarchie-Modell, um Variabilität zu vermeiden.

##### **CFD (Computational Fluid Dynamics)**  
Klasse numerischer Simulationen für Strömungsmodelle; wichtig als Benchmark-Workload.

##### **Cluster Map**  
JSON-Datei, die die deterministische Fabric-Topologie eines Clusters definiert.

##### **Compute Integrity**  
Die Eigenschaft, dass Rechenergebnisse bitgenau sind und unabhängig von Laufzeitbedingungen.

#### D

##### **DMA (Direct Memory Access)**  
Feste, deterministische Kopierfenster ohne dynamische Wiederholversuche.

##### **Deterministic Execution**  
Ausführung, bei der Ergebnisse, Zeit und Energieverbrauch invariant bleiben.

##### **Deterministic Fabric**  
Netzwerkmodell von KORA, basierend auf TDM und festen Routen.

##### **Deterministic FP (Soft-FP)**  
Bitgenaue, softwaremodellierte FP-Arithmetik für vollständige Reproduzierbarkeit.

#### E

##### **Energy Profile**  
Zeitlicher Verlauf der Leistungsaufnahme; bei KORA deterministisch konstant.

##### **Execution Timeline**  
Zyklusgenaue Liste aller Phasen eines TSFs.

#### F

##### **Fabric (TDM Fabric)**  
Kommunikationsnetzwerk, das deterministisch nach festen Zeit-Slots arbeitet.

##### **Fault Determinism**  
Fehler erzeugen deterministische Abbrüche ohne Wiederholungen.

##### **FLOPs (Floating Point Operations)**  
Operationen pro Sekunde; im GPU-Kontext oft peak-abhängig → variabel, in KORA stabil.

#### G

##### **Golden Run**  
Referenzausführung, vollständig validiert, signiert und reproduzierbar.

##### **Ghost Cell**  
Gitterrandzelle, die für PDE-Methoden zwischen Nodes ausgetauscht wird.

#### H

##### **HAPI**  
High-Level API für Modell-Interaktion, Parametrisierung, TSF-Erzeugung.

##### **Hash Integrity**  
Jede Datei im KORA-System wird durch SHA256 gesichert.

#### I

##### **Idempotent Execution**  
Mehrfache API-Befehle erzeugen denselben Systemzustand.

##### **Input Schema**  
Definition des Formats und der Version von Eingabedaten.

#### J

##### **Jitter (Nonexistent)**  
Zeitliche Variabilität, die in klassischen Systemen auftritt – in KORA eliminiert.

#### K

##### **KORA Monolith**  
Deterministische Hardwareeinheit ohne Caches, Boosting oder dynamische Zeitverhalten.

##### **Kernel Fusion (Deterministic)**  
Vorab kombinierte Rechenschritte, die statisch optimiert und deterministisch ausgeführt werden.

#### L

##### **Latency Determinism**  
Alle Latenzen für Speicher- und Fabric-Operationen sind konstant.

##### **Load Balance (Nonexistent)**  
Klassische Lastverteilung wird nicht benötigt; Scheduling ist statisch fixiert.

#### M

##### **Memory Mapping**  
Feste Zuordnung von Datenbereichen zu Memorybanks und Offsets.

##### **Mesh Topology**  
2D-Cluster-Anordnung, ideal für deterministische Kommunikation.

##### **Monolith Generation (M1/M3)**  
Abstrakte Entwicklungslinien der KORA-Hardware.

#### N

##### **Numerical Determinism**  
Bitgenaue oder reproduzierbare numerische Ergebnisse (Profil B/C).

##### **Node ID**  
Eindeutige Identifikationsnummer eines Monolithen im Cluster.

#### O

##### **Output Integrity**  
Alle Output-Dateien sind vollständig deterministisch.

##### **Overhead (Classical)**  
Variabilität durch Scheduler, Cache Misses, Boosts etc.; von KORA eliminiert.

#### P

##### **Phase Scheduler**  
Deterministischer Ablaufplan der TSF-Phasen.

##### **PUE (Power Usage Effectiveness)**  
Energieeffizienzkennzahl; bei KORA niedriger durch geringe Wärmeentwicklung.

#### Q

##### **Queue-Free Execution**  
Es gibt keine dynamischen Queues; jede Operation ist vorab definiert.

#### R

##### **Reduction Tree**  
Deterministischer Summations-/Reduktionsgraph für ML-Modelle und PDEs.

##### **Reproducibility Protocol**  
Formale Regeln zur Archivierung und Wiederholbarkeit eines Runs.

#### S

##### **SCI (Scheduling & Compilation Interface)**  
Low-Level-Schnittstelle zur TSF-Verteilung & Clustersteuerung.

##### **Soft-FP**  
Softwaremodellierte deterministische FP-Arithmetik.

##### **Static Scheduling**  
Keine Laufzeitplanung; alles erfolgt vorher festgelegt.

#### T

##### **TSF (Task Scheduling Format)**  
Die zentrale, deterministische Ausführungsbeschreibung von KORA.

##### **Timeline**  
Zyklusbasierte Beschreibung der Ausführung aller Phasen und DMA-/Fabric-Operationen.

##### **Torus Topology**  
Cluster-Topologie mit Wrap-Around-Verbindungen.

#### U

##### **Unroll Factor (Deterministic)**  
Statisch definierter Faktor zur Schleifenentfaltung, ohne variablen Einfluss.

#### V

##### **Versioned Input/Output**  
Jede Datei besitzt eine klare Versionsnummer, damit Reproduktionen möglich bleiben.

#### W

##### **Workload**  
Definierte Aufgabe in CFD, ML, Big Data, Simulation oder numerischen Modellen.

#### Z

##### **Zero Jitter Guarantee**  
Absolute zeitliche Variationsfreiheit aller Abläufe.

### 69.1 Fazit

Dieses Glossar definiert alle wesentlichen Begriffe der KORA-Spezifikation
und bildet die sprachliche Grundlage für:

- Forschung  
- Entwicklung  
- Peer Review  
- Lehre  
- Dokumentation  

Es dient als verbindliche Referenz für alle KORA-bezogenen Publikationen.

---

## 70. Appendix X: Comparison with Classical Systems (non-normative)
(Vergleich mit GPU-Computing, HPC-Clustern, Big-Data-Frameworks)

Dieses Kapitel dient der wissenschaftlichen Einordnung von KORA.  
Es vergleicht KORA mit klassischen Systemen, ohne normative Aussagen zu treffen.
Alle Vergleiche dienen der Orientierung — nicht der Bewertung oder Produktentscheidung.

### 70.1 Motivation des Vergleichs

KORA führt ein *deterministisches* Rechenmodell ein.  
Konventionelle Systeme sind:

- spekulativ  
- cache-basiert  
- scheduling-abhängig  
- jitterbehaftet  
- boost-/thermik-variabel  
- I/O-variabel  
- nicht reproduzierbar

Dieses Kapitel zeigt strukturelle Unterschiede in:

1. Ausführungsmodell  
2. Energieprofil  
3. Zeitprofil  
4. Kommunikationsverhalten  
5. Numerischer Reproduzierbarkeit  
6. Scheduling  
7. Fehlerinvarianz  

### 70.2 Vergleichskategorien

Der Vergleich erfolgt in sechs Kategorien:

1. **Ausführungsmodell**  
2. **Determinismus**  
3. **Kommunikation & Synchronisation**  
4. **Numerik & FP-Stabilität**  
5. **Energieeffizienz**  
6. **Reproduzierbarkeit**

### 70.3 GPU-Systeme (z. B. NVIDIA, AMD)

#### 70.3.1 Ausführungsmodell

GPUs basieren auf:

- Caches  
- Speculative Load/Store  
- dynamischem Warp Scheduling  
- variablen Kernfrequenzen  
- Boost/Throttling  
- Straggler-Effekten  

Das führt zu:

- variierender Zeit  
- variierender Energie  
- variierenden numerischen Ergebnissen  

#### KORA im Vergleich

KORA:

- keine Caches  
- keine spekulativen Pfade  
- keine Boost-Mechanismen  
- konstante Taktfrequenz  
- statische Scheduling Trees  

Ergebnis:

    GPU: variable Execution
    KORA: exakt deterministische Execution

### 70.4 HPC-Cluster (CPU + MPI)

#### 70.4.1 Scheduling

MPI basiert auf:

- OS-Scheduler  
- Thread-Level Parallelismus  
- dynamischen Barriers  
- variablen Netzwerk-Latenzen  

Das erzeugt:

- Jitter  
- Straggler  
- variable Reduktionszeiten  
- Lastungleichverteilung  

#### KORA im Vergleich

KORA:

- keine OS-Interferenz  
- keine dynamischen Barriers  
- deterministische Fabric  
- konstante Pfade  
- Null-Straggler-Garantie  

### 70.5 Big-Data-Frameworks (Spark, Flink, Hadoop)

#### 70.5.1 Variabilität

Big-Data-Frameworks besitzen:

- dynamische Partitionierung  
- Spekulation  
- Retry-Mechanismen  
- Garbage Collection  
- JVM-Jitter  
- Netzwerkvariabilität  

#### KORA im Vergleich

KORA:

- deterministische Partitionierung  
- keinerlei Retry  
- keine GC  
- statische DMA  
- deterministische Shuffle-Slots  

Ergebnis:

    Big Data: variable Shuffle & Join Latency
    KORA: konstante Shuffle & Join Latency

### 70.6 Numerischer Vergleich

#### 70.6.1 GPU & CPU Numerik

- Floating Point variiert durch Reihenfolge, Scheduling und Instruktionspfade  
- Reduktionen nicht stabil  
- Reihenfolge nicht definiert  
- Ergebnisse können Hardware-/Treiber-bedingt differieren  

#### KORA im Vergleich

KORA:

- feste Reduktionsbäume  
- deterministische FP-Profile  
- optionale bitgenaue Soft-FP (Profil C)  
- keine Varianz auf Hardwareebene  

### 70.7 Energievergleich

#### 70.7.1 GPU-Cluster

- hohe Peak-Leistung  
- hoher Stromverbrauch  
- thermisches Throttling  
- Kühlbedarf stark lastabhängig  

#### 70.7.2 HPC-Cluster

- ineffiziente Kommunikation  
- hoher Netzwerk-Overhead  
- Energie variiert mit Auslastung  

#### KORA

- konstante Leistungsaufnahme  
- niedrige Wärmeentwicklung  
- deterministische Energieprofile  
- niedrige PUE  

Typischer Vergleich:

    KORA:   5–25 % Energie eines GPU-Clusters
    HPC:    150–300 % Energie relativ zu KORA
    Big Data: stark variabel, häufig >200 %

### 70.8 Zeitprofil

GPU:

- variabel  
- abhängig von Treiber, Boost, Temperatur

HPC:

- abhängig von Stragglern, OS und Netzwerk

Big Data:

- abhängig von GC, Shuffle, Partitionen

KORA:

- zyklusgenau  
- vollständig invariant  
- messtechnisch überprüfbar

### 70.9 Kommunikationsverhalten

GPU:

- NCCL, dynamische Pfade  
- variable Latenzen  
- Paketverlust möglich

HPC:

- MPI, dynamische Routen  
- Blocking & Non-blocking Variabilität  

KORA:

- deterministische TDM-Fabric  
- feste Pfade  
- feste Latenzen  
- keine Wiederholpakete  

### 70.10 Fehlerverhalten

GPU/HPC/Big Data:

- Retry  
- Backoff  
- dynamische Rekonfiguration  
- variable Ergebnisse nach Fehlern  

KORA:

    Fehler → deterministischer Abbruch

Keine Wiederholung, keine dynamische Routenwahl.

### 70.11 Reproduzierbarkeit

GPU:

- durch Nichtdeterminismus nicht vollständig möglich  
- Softmax, Reduktionen variieren  

HPC:

- OS-Scheduler beeinflusst Ergebnisse  
- Netzwerk-Jitter → Laufzeit variiert  

Big Data:

- GC, Shuffle, Partitionierung → nicht reproduzierbar  

KORA:

- vollständige bitgenaue Reproduzierbarkeit  
- identische Zeit, Energie, FP, I/O  
- Telemetrie vollständig archiviert  

### 70.12 Zusammenfassung der Unterschiede

| Kategorie | GPU | HPC | Big Data | KORA |
|----------|-----|-----|----------|-------|
| Determinismus | ✗ | ✗ | ✗ | ✓ |
| Zeitstabilität | ✗ | ✗ | ✗ | ✓ |
| Energievariabilität | hoch | mittel | hoch | sehr gering |
| Spekulatives Verhalten | ✓ | ✓ | ✓ | ✗ |
| Netzwerk | variabel | variabel | variabel | deterministisch |
| Numerik | variabel | variabel | variabel | fix/stabil/bitgenau |
| Reproduzierbarkeit | eingeschränkt | eingeschränkt | gering | vollständig |

### 70.13 Fazit

Dieses Kapitel ordnet KORA im technischen Umfeld ein.  
Es zeigt:

- warum deterministische Systeme völlig andere Eigenschaften haben  
- wie KORA klassische HPC/GPU/Big-Data-Ansätze ergänzt, nicht ersetzt  
- wie deterministische Modelle neue Forschungswege ermöglichen  

Damit bildet Appendix X das kontextuelle Abschlusskapitel der Spezifikation.

---

## Versionierung

- **Dokument:** `03_Architecture_Specification_Technical.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  

