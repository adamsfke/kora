# KORA – Abstract

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Abstract / Projektübersicht
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Überblick
    2.  Motivation
    3.  Kernidee
    4.  Architekturmodelle A, B, C
    5.  Simulationsergebnisse (v3.0)
    6.  Wissenschaftliche Relevanz
    7.  Reproduzierbarkeitsrahmen
    8.  Energieeffizienz
    9.  Dokumentation v2.0
    10. Schlussfolgerung

---

## 1. Überblick

KORA ist eine neuartige, deterministische Rechenarchitektur für wissenschaftliche Modellierung, 
künstliche Intelligenz und Big-Data-Anwendungen. Das Projekt verfolgt einen radikalen Paradigmenwechsel 
weg von klassischen HPC-/GPU-Modellen hin zu einem kohärenzorientierten Rechenprinzip, 
das Reproduzierbarkeit, Energieeffizienz und numerische Stabilität in den Mittelpunkt stellt.

Während heutige Systeme von nichtdeterministischen Effekten geprägt sind – Scheduling-Jitter, 
variablen Reduktionsreihenfolgen, OS-Noise, PCIe-Variabilität und dynamischen Kommunikationsmustern 
– eliminiert KORA diese Probleme strukturell. Das Ergebnis ist eine Architektur, in der 
wissenschaftliche Modelle nicht nur schneller, sondern vor allem **bitgenau reproduzierbar**, 
energieeffizient und auditierbar ausgeführt werden.

KORA Version 2.0 besteht aus einem vollständigen Architekturpaket, einer deterministischen 
Software-Implementierung (KORA-2), einem durchgängigen Reproduzierbarkeitsmodell, einer umfassenden 
Simulation Methodology sowie einer konsistenten Benchmark- und Energieanalyse (v3.0). 
Die Dokumentation umfasst neun Kernmodule sowie zwei Hintergrunddokumente (wissenschaftliche Basis und Referenzen).

---

## 2. Motivation

Moderne wissenschaftliche Recheninfrastrukturen stoßen an strukturelle Grenzen.  
Trotz steigender FLOPs stagnieren viele Bereiche der Wissenschaft, weil klassische Systeme:

- Ergebnisse nicht reproduzierbar liefern  
- numerische Drift aufweisen  
- von Jitter und Scheduling-Variabilität beeinflusst werden  
- unverhältnismäßig viel Energie für Overheads verbrauchen  
- schwer auditierbar sind  
- unter Last unvorhersehbare Latenzspitzen zeigen  

KI-Modelle, CFD-Simulationen, Klimamodelle und Big-Data-Pipelines werden durch diese Probleme fundamental eingeschränkt.  
Trotz Milliardeninvestitionen in Hardware wird ein Kernproblem nicht gelöst: **Der Verlust globaler Kohärenz.**

KORA adressiert genau dieses Problem.

---

## 3. Kernidee

KORA basiert auf vier Prinzipien:

### 3.1 Deterministische Ausführung  
Alle Operationen laufen in exakt definierter Reihenfolge ab.  
Keine Interrupts, keine dynamischen Reduktionen, kein OS-Noise.

### 3.2 Kohärente globale Datenstruktur  
KORA nutzt den SRDB (Structural Runtime Data Bus) –  
eine deterministische, globale Speicherarchitektur ohne Caches und ohne nichtdeterministische Kommunikation.

### 3.3 Zeitlich deterministische Datenbewegung  
Daten bewegen sich ausschließlich in fest definierten DMA-Fenstern, vollständig reproduzierbar.

### 3.4 TSF als deterministisches Modellformat  
Das Tensor Sequence Format beschreibt *jede einzelne Operation*,  
jeden Speicherzugriff und jede Synchronisation deterministisch.

Diese vier Elemente erzeugen eine Rechenarchitektur, die selbst auf Standard-Hardware (KORA-SW) deutlich stabiler, effizienter und reproduzierbarer ist als klassische HPC-/GPU-Systeme.

---

## 4. Architekturmodelle A, B, C

KORA definiert drei Architekturebenen:

### Architektur A — HPC/GPU (Baseline)  
Nichtdeterministisch, energieineffizient, jitteranfällig.  
Dient als Referenzbasis.

### Architektur B — KORA-SW (Software-Determinismus)  
Läuft auf Standard-Hardware.  
Reduziert Varianz um zwei Größenordnungen  
und verbessert Speed/Energie signifikant.

### Architektur C — KORA-HW (Hardware-Determinismus)  
Volldeterministische Hardwarearchitektur.  
Keine Caches, keine Interrupts, keine Dynamik.  
Bitidentische Wissenschaft für KI, CFD, Klima und Big Data.

---

## 5. Simulationsergebnisse (v3.0)

Die v3.0-Simulation zeigt klare Muster:

### KORA-SW (B):
- **1.3–2.6× schneller**
- **40–70 % weniger Energie**
- **reproduzierbar bis auf ±0.005–0.02 %**

### KORA-HW (C):
- **5–6× schneller bei KI / Big Data**
- **15–20× schneller bei CFD**
- **97–99 % weniger Energieverbrauch**
- **0.000 % Drift (bitgenau)**

Diese Werte sind keine Optimierung, sondern eine strukturelle Konsequenz der Architektur.

---

## 6. Wissenschaftliche Relevanz

### 6.1 KI  
Stabilität ist entscheidend.  
KORA macht KI-Läufe deterministisch und auditierbar.

### 6.2 CFD  
CFD reagiert extrem empfindlich auf Jitter.  
KORA eliminiert Jitter vollständig.

### 6.3 Klima & Wissenschaft  
Wiederholbarkeit ist fundamental.  
KORA liefert bitgenaue Ergebnisse – unabhängig von Zeit, Hardware oder Systemlast.

### 6.4 Big Data  
Datenbewegung bestimmt den Energieverbrauch.  
KORA minimiert Datenbewegung strukturell.

---

## 7. Reproduzierbarkeitsrahmen

KORA definiert Reproduzierbarkeit als architekturabhängige Eigenschaft.  
Ein Modell ist reproduzierbar, wenn:

- Sequenzen deterministisch  
- Speicher deterministisch  
- FP-Pfade deterministisch  
- Datenbewegungen deterministisch  
- Kommunikation deterministisch  
- Scheduling deterministisch  

TSF, Scheduling Trees und SRDB sorgen dafür, dass alle drei Ebenen (Software, Architektur, Datenpfade) bitgenau wiederholbar bleiben.

---

## 8. Energieeffizienz

KORA eliminiert klassische Overheads:

- DVFS  
- OS-Noise  
- Interconnect Jitter  
- Cache-Kohärenzkosten  
- variable DMA-Fenster  
- dynamische Reduktionen  

Dadurch werden bis zu **99 % Energie** eingespart.  
In Kombination mit deterministischer Ausführung entsteht eine robuste, planbare Energieprofilierung.

---

## 9. Dokumentation v2.0

Die KORA-Dokumentfamilie umfasst:

01 Executive Summary  
02 Architecture Overview  
03 Technical Architecture Specification  
04 Software Specification  
05 Simulation Methodology  
06 Future Outlook  
07 Reproducibility Specification  
08 Evaluation and Benchmarks  
09 Release Notes  
10 Background and Scientific Basis  
11 References  

Gemeinsam bilden sie ein wissenschaftlich fundiertes, konsistentes Architekturpaket.

---

## 10. Schlussfolgerung

KORA ist die erste kohärenzorientierte Rechenarchitektur, die:

- deterministisch  
- bitgenau reproduzierbar  
- extrem energieeffizient  
- HPC-tauglich  
- KI-fähig  
- auditierbar  
- wissenschaftlich valide  
- und hardwareübergreifend stabil  

arbeitet.

KORA schafft eine neue Klasse wissenschaftlicher Systeme,  
in denen Geschwindigkeit eine Folge ist — nicht das Ziel.  
Die eigentliche Errungenschaft ist globale Kohärenz.

Damit stellt KORA einen Paradigmenwechsel dar:

Wissenschaftliche Modelle werden nicht länger tolerierbaren Zufällen überlassen,  
sondern erhalten eine stabile, deterministische Grundlage.

KORA — **The architecture for reproducible science.**

---

## Versionierung

- **Dokument:** `00_Abstract.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
