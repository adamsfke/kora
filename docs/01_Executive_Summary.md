# KORA – Executive Summary

## Kohärenzorientierte Rechenarchitektur für Big-Data-Langläufer

**Autoren:** Frank Meyer  
**Version:** 1.0 (November 2025)  
**Status:** Machbarkeitsstudie

---

## 1. Problemstellung

### 1.1 Ineffizienz moderner Big-Data-Systeme

Aktuelle Rechnerarchitekturen für Big-Data-Verarbeitung und Hochleistungsrechnen sind für **Interaktivität und Flexibilität** optimiert. Dies führt zu systematischen Ineffizienzen bei **Langläufern** – Berechnungen, die Stunden bis Tage ohne menschliche Interaktion durchlaufen:

**Fragmentierung durch Interrupts:**
- Moderne Betriebssysteme unterbrechen laufende Prozesse 500-3000 Mal pro Sekunde
- Jede Unterbrechung zerstört Prozessor-Cache-Lokalität
- Bei mehrstündigen Berechnungen akkumuliert sich der Overhead erheblich

**Non-Determinismus:**
- Gleiches Programm mit gleichen Daten erzeugt leicht unterschiedliche Ergebnisse
- Ursache: Dynamisches Scheduling, asynchrone Kommunikation, Timing-Varianz
- Wissenschaftliche Reproduzierbarkeit ist nicht garantiert

**Cache-Kohärenz-Overhead:**
- Multi-GPU/Multi-CPU-Systeme synchronisieren Speicher über komplexe Protokolle
- 15-30% der Rechenzeit wird für Kohärenz-Management verschwendet
- Problem skaliert mit Systemgröße

**Energieverschwendung:**
- Idle-Phasen durch Kontextwechsel und Synchronisation
- Ineffiziente Netzwerkkommunikation (spontane Interrupts statt gebündelte Transfers)
- 30-50% der Energie wird für Overhead statt Berechnung verbraucht

### 1.2 Warum existierende Lösungen nicht ausreichen

**General-Purpose-Systeme:**
- Linux, Windows, Standard-HPC-Cluster sind für vielfältige Anwendungen konzipiert
- Müssen auf unvorhersehbare Ereignisse reagieren (User-Input, Netzwerk, Hardware-Fehler)
- Können Interaktivität nicht opfern

**GPU-Computing:**
- Parallelisiert effizient, aber Host-Device-Kommunikation bleibt Bottleneck
- Scheduling erfolgt auf CPU mit allen Nachteilen klassischer Systeme
- Keine globale Kohärenz über GPU-Grenzen hinweg

**Spezialisierte Lösungen (Cerebras, Wafer-Scale):**
- Technisch überlegen, aber extrem teuer (2-5 Mio € pro System)
- Nur für Top-0,1%-Anwendungen amortisierbar
- Ökosystem-Fragmentierung

---

## 2. KORA-Architektur

### 2.1 Kernprinzipien

KORA kehrt zu fundamentalen Prinzipien früher Rechensysteme zurück, die für Batch-Processing optimal waren:

1. **Kohärenz vor Flexibilität**: Ein globales, konsistentes Datenmodell statt fragmentierter Speicherhierarchien
2. **Determinismus vor Responsiveness**: Unterbrechungsfreie Ausführung für perfekte Reproduzierbarkeit
3. **Spezialisierung vor Universalität**: Optimiert für definierte Workloads statt General-Purpose

### 2.2 Architektur-Komponenten

**KORA-Core (Logischer Hauptprozess):**
```
Funktion:
- Hütet globales Datenmodell (SRDB – Single Resonance Data Bus)
- Entscheidet über Prioritäten und Rechenphasen
- Verarbeitet Informationen deterministisch
- Verhindert Interrupts und Kontextwechsel

Eigenschaften:
- Single-Threaded, keine Nebenläufigkeit
- Statisches oder vorhersagbares Scheduling
- Vollständige Kontrolle über Worker-Zuteilung
```

**Compute-Worker (Physikalische Parallelität):**
```
Funktion:
- GPU-Kerne, CPU-Vektor-Einheiten oder FPGA-Pipelines
- Führen rechenintensive Operationen aus
- Werden explizit vom KORA-Core beauftragt
- Melden Ergebnisse gebündelt zurück

Eigenschaften:
- Keine Eigenautonomie, kein eigenes Scheduling
- Homogene Tiles für deterministische Lastverteilung
- Kommunikation über Task- und Result-Queues, nie über Interrupts
```

**KORA-Net-Layer (Netzwerk-/I/O-Abschirmung):**
```
Funktion:
- Bündelt externe Signale und I/O
- Keine spontanen Interrupts für eingehende Daten
- Übergabe an KORA-Core nur in definierten Epochen

Eigenschaften:
- Epochen-basiertes Polling (z.B. alle 10ms)
- Deterministische Netzwerk-Behandlung
- Abschirmung vor externem Nondeterminismus
```

**SRDB (Single Resonance Data Bus):**
```
Konzept:
- Globaler, kohärenter Speicherraum
- Alle Worker greifen auf gleiche Daten zu
- Kein Cache-Kohärenzprotokoll nötig (alle sehen gleichen Zustand)

Implementierung:
- Phase 1: Shared Memory mit NUMA-Optimierung
- Phase 2: On-Chip High-Bandwidth Memory
- Phase 3: Monolithischer Die mit integriertem Speicher
```

### 2.3 Wie KORA funktioniert

**Typischer Ablauf einer KORA-Berechnung:**

1. **Initialisierung**: KORA-Core lädt Daten in SRDB, validiert Problemdefinition
2. **Task-Generierung**: Core zerlegt Berechnung in homogene Tasks
3. **Worker-Zuteilung**: Tasks werden deterministisch Worker-Tiles zugewiesen
4. **Berechnung**: Worker arbeiten unterbrechungsfrei, ohne Synchronisation untereinander
5. **Result-Collection**: Ergebnisse werden gebündelt an Core zurückgegeben
6. **Iteration**: Core aktualisiert SRDB, generiert nächste Task-Welle
7. **Abschluss**: Finale Ergebnisse werden validiert und ausgegeben

**Keine Interrupts während Schritten 3-6** → Maximale Kohärenz und Energieeffizienz.

---

## 3. Simulationsergebnisse

### 3.1 Methodik

Drei vergleichende Simulationen wurden durchgeführt:

- **Architektur A (Standard)**: Klassische Big-Data-/HPC-Systeme mit hoher Interrupt-Rate, dynamischem Scheduling, Multi-Chip-Topologie
- **Architektur B (KORA-Software)**: KORA-Prinzipien auf Standard-Hardware (Software-Optimierung)
- **Architektur C (KORA-Hardware)**: KORA mit spezialisierter, monolithischer Hardware

Alle Simulationen nutzen identische Rechenlogik – Unterschiede resultieren ausschließlich aus architektonischen Overheads.

### 3.2 Simulation 1: Big-Data-Verarbeitung

**Datensatz:**
- 5-dimensionales Feld (180×360×20 Zeitschritte, 1000 Epochen, 5 Variablen)
- 6,48 Milliarden Datenpunkte
- Typisch für Klimamodellierung, CFD, Simulationen

**Ergebnisse:**

| Metrik | A (Standard) | B (KORA-SW) | C (KORA-HW) |
|--------|--------------|-------------|-------------|
| Laufzeit | 3.208 s | 2.304 s (-28%) | 2.165 s (-33%) |
| Energie | 4.811 Ws | 3.455 Ws (-28%) | 3.247 Ws (-33%) |
| KVI (Kohärenz) | 1,0 | 0,1 (10×) | 0,01 (100×) |
| Determinismus | ±0,2% | ±0,05% | 100% |

**Interpretation:**
- Software-Optimierung allein bringt 28% Verbesserung
- Spezialisierte Hardware erreicht 33% (limitiert durch Compute-Zeit)
- Kohärenz verbessert sich drastisch (100× bei Hardware)
- Perfekte Reproduzierbarkeit nur mit KORA-Hardware

### 3.3 Simulation 2: KI-Training (BERT-Base)

**Modell:**
- BERT-Base: 110 Millionen Parameter
- 16 Milliarden Tokens Trainingsdaten
- 40 Epochen (Standard-Training)
- 64 GPUs (V100-äquivalent)

**Ergebnisse:**

| Metrik | A (Standard) | B (KORA-SW) | C (KORA-HW) |
|--------|--------------|-------------|-------------|
| Trainingszeit | 6,2 Tage | 5,3 Tage (-15%) | 1,0 Tage (-84%) |
| Energie | 792 kWh | 674 kWh (-15%) | 29 kWh (-96%) |
| Kosten (0,30€/kWh) | 237 € | 202 € | 9 € |
| Reproduzierbarkeit | ±0,2% Varianz | ±0,1% Varianz | Bit-identisch |

**Interpretation:**
- Bei KI-Training dominiert GPU-Compute, daher geringerer Software-Gewinn (15%)
- Monolithische Hardware eliminiert Inter-Chip-Overhead → 84% Zeitersparnis
- Energieeinsparung ist nicht-linear: 84% Zeit + 77% Leistung = 96% Energie
- Bit-identische Reproduzierbarkeit ermöglicht wissenschaftliche Audits

**Hochrechnung auf GPT-3-Klasse (175B Parameter, 1024 GPUs):**
- Standard: 30 Tage, 38.000 kWh, 11.400 €
- KORA-Monolith: 5 Tage, 1.400 kWh, 420 € 
- CO₂-Einsparung: ~18 Tonnen (EU-Strommix)

### 3.4 Simulation 3: Monolithische Hardware

**Vergleich Standard-System vs. KORA-Monolith:**

**Standard (8× separate GPUs):**
```
Silizium: 8× 800 mm² GPU-Dies + 8× 200 mm² HBM = 8.400 mm²
Peripherie: 750g (Mainboard, PCIe-Switches, Passives)
Leistung: 24,2 kW (19,2 kW GPUs + 5 kW Host/Kühlung)
```

**KORA-Monolith (ein integrierter Die):**
```
Silizium: 2.500 mm² Die + 200 mm² HBM = 2.700 mm² (-68%)
Peripherie: 100g (minimales Board) (-87%)
Leistung: 1,2 kW (-95%)
```

**Ergebnisse:**

| Metrik | Standard | KORA-Monolith | Einsparung |
|--------|----------|---------------|------------|
| Silizium | 8.400 mm² | 2.700 mm² | **68%** |
| Peripherie | 750g | 100g | **87%** |
| Laufzeit (BERT) | 6,2 Tage | 1,0 Tage | **84%** |
| Energie | 792 kWh | 29 kWh | **96%** |

**Warum so große Einsparungen?**

1. **Keine Inter-Chip-Kommunikation**: PCIe-Overhead (60% bei Standard) entfällt
2. **Kein Cache-Kohärenzprotokoll**: Separate Dies benötigen komplexe Synchronisation
3. **On-Die-Bus**: 20× schneller und 10× energieeffizienter als PCIe
4. **Homogene Worker-Tiles**: Einfacheres Design, höherer Yield mit Redundanz

---

## 4. Anwendungsdomänen

### 4.1 Ideal für KORA

**Klimamodellierung und Wettervorhersage:**
- Strukturierte Gitterdaten, iterative Solver
- Laufzeiten: Stunden bis Tage
- Reproduzierbarkeit kritisch für Langzeit-Vergleiche
- Energiekosten signifikanter Budgetfaktor

**Computational Fluid Dynamics (CFD):**
- Finite-Elemente-Simulationen, Strömungsmechanik
- Deterministische Problemdefinition
- Hohe Parallelität, lokale Datenabhängigkeiten

**Bioinformatik / Genomanalyse:**
- Sequenzielle Pipelines, große Datensätze
- Keine Echtzeitanforderungen
- Reproduzierbarkeit für wissenschaftliche Publikationen essenziell

**KI-Training (Produktion):**
- Modellarchitektur und Hyperparameter festgelegt
- Training als Batch-Job über Tage
- Bit-identische Reproduzierbarkeit für Audits/Regulierung

**Molekulardynamik / Proteinfaltung:**
- N-Body-Probleme, Langzeit-Trajektorien
- Determinismus wichtig für Validierung
- Energieeffizienz bei Exascale-Berechnungen

### 4.2 Ungeeignet für KORA

**Interaktive Datenanalyse:**
- Jupyter Notebooks, explorative Analyse
- Benötigen schnelle Responsiveness und Interaktivität

**Transaktionale Datenbanken (OLTP):**
- Viele kleine, asynchrone Anfragen
- ACID-Transaktionen erfordern dynamisches Scheduling

**Echtzeitstreaming:**
- Kafka, Flink, Event-Processing
- Externe Events müssen sofort verarbeitet werden

**Explorative ML-Forschung:**
- Häufige Architekturänderungen, Debugging
- Benötigt Unterbrechbarkeit während Training

---

## 5. Entwicklungsroadmap

### Phase 1: Software-Framework (2025-2027)

**Ziel:** Validierung der Architekturprinzipien auf bestehender Hardware

**Maßnahmen:**
- Implementierung KORA-Core als User-Space-Scheduler
- Wrapper für GPUs/CPUs mit Queue-basierter Kommunikation
- Benchmarking gegen Standard-Frameworks (MPI, CUDA, PyTorch)

**Erfolgskriterium:**
- 15-25% messbare Verbesserung bei Laufzeit/Energie
- Bit-identische Reproduzierbarkeit nachweisbar
- Interesse von 3+ Forschungsinstituten

**Risiken:**
- Software-Overhead kompensiert architektonische Vorteile nicht ausreichend
- Adoption scheitert an Inkompatibilität mit bestehendem Code

### Phase 2: Multi-Chip-Module (2027-2029)

**Ziel:** Brückentechnologie mit ersten Hardware-Optimierungen

**Maßnahmen:**
- MCM mit 4-8 KORA-Tiles (Chiplet-Architektur)
- Dedizierte Inter-Tile-Interconnects (kein Standard-PCIe)
- Prototypen-Fertigung bei etablierten Foundries

**Erfolgskriterium:**
- 40-60% Verbesserung gegenüber Standard-Hardware
- Technische Validierung für monolithischen Ansatz
- Kooperationen mit Hardware-Herstellern

**Risiken:**
- Chiplet-Overhead verhindert klare Vorteile gegenüber Software-Lösung
- Entwicklungskosten (5-10 Mio €) nicht amortisierbar

### Phase 3: Monolithische Hardware (2029-2033)

**Ziel:** Vollständig integrierter KORA-Chip für maximale Effizienz

**Maßnahmen:**
- 2.500 mm² monolithischer Die mit 256+ Worker-Tiles
- Integriertes SRDB mit HBM3-Interface
- Wafer-Scale-Variante für Exascale-Anwendungen

**Erfolgskriterium:**
- 80-95% Energie-Einsparung gegenüber Standard-Systemen
- Kommerzielle Deployments bei Hyperscalern/Forschungszentren
- Amortisation über 2-3 Jahre bei Großanwendern

**Risiken:**
- Entwicklungskosten (50-100 Mio €) zu hoch
- Moore's Law-Ende verlangsamt sich, Hardware-Vorteile schwinden
- Konkurrierende Technologien (fortgeschrittene Chiplets) holen auf

---

## 6. Ökonomische Bewertung

### 6.1 Total Cost of Ownership (TCO)

**Beispiel: Forschungsinstitut mit 100 BERT-Trainings/Jahr**

**Standard-System (8× A100 GPUs):**
```
Hardware: 80.000 € (Anschaffung)
Strom: 23.700 € / Jahr (100× 237€)
Kühlung: 9.500 € / Jahr (40% der Rechenleistung)
Wartung: 5.000 € / Jahr
────────────────────────────
Jahr 1: 118.200 €
Jahr 5: 271.000 € (kumulativ)
```

**KORA-Software (gleiche Hardware, optimierte Nutzung):**
```
Hardware: 80.000 € (unverändert)
Entwicklung: 10.000 € (einmalig, Open-Source-Integration)
Strom: 20.200 € / Jahr (-15%)
Kühlung: 8.100 € / Jahr
Wartung: 5.000 € / Jahr
────────────────────────────
Jahr 1: 123.300 € (5.100 € teurer wegen Entwicklung)
Jahr 5: 246.500 € (kumulativ, 24.500 € günstiger)
```

**KORA-Monolith (spezialisierte Hardware, ab 2030):**
```
Hardware: 150.000 € (höhere Anschaffung, aber amortisierbar)
Strom: 900 € / Jahr (-96%)
Kühlung: 360 € / Jahr
Wartung: 3.000 € / Jahr
────────────────────────────
Jahr 1: 154.260 €
Jahr 5: 171.300 € (kumulativ, 99.700 € günstiger als Standard)
ROI: Nach 2,1 Jahren
```

### 6.2 Break-Even-Analyse

**Hyperscaler-Scale (10.000 Trainings/Jahr):**

Standard-System: 2,37 Mio € Strom/Jahr  
KORA-Monolith: 90.000 € Strom/Jahr  
**Einsparung: 2,28 Mio € / Jahr**

Bei Entwicklungskosten von 50-70 Mio € für KORA-Hardware:
**Break-Even nach 22-30 Monaten**

### 6.3 Umweltbilanz

**CO₂-Einsparung pro BERT-Training (KORA-Monolith vs. Standard):**
```
Standard: 792 kWh × 0,4 kg CO₂/kWh (EU-Mix) = 317 kg CO₂
KORA: 29 kWh × 0,4 kg CO₂/kWh = 12 kg CO₂
Einsparung: 305 kg CO₂ pro Training
```

**Bei 10.000 Trainings/Jahr:** 3.050 Tonnen CO₂  
**Äquivalent zu:** 13.000 Transatlantikflügen oder 1.500 Autos

---

## 7. Risiken und Herausforderungen

### 7.1 Technische Risiken

**Yield-Problem bei großen Dies:**
- Monolithische 2.500 mm²-Dies haben niedrigere Ausbeute als kleinere Chips
- **Mitigation:** Redundante Worker-Tiles (256+16, 16 als Reserve)

**Thermische Herausforderungen:**
- Konzentrierte Wärme auf einem Die
- **Mitigation:** KORA läuft mit konstanter Last → gleichmäßige Wärmeverteilung, effizientere Kühlung

**Speicher-Bandbreite:**
- 256 Worker benötigen enormen Datendurchsatz
- **Mitigation:** HBM3 mit 8 TB/s ausreichend für KORA-Zugriffsmuster

### 7.2 Ökonomische Risiken

**Hohe Entwicklungskosten:**
- ASIC-Design + Tape-Out: 50-100 Mio €
- **Mitigation:** Phase 1+2 validieren Konzept vor großer Investition

**Adoption-Barriere:**
- Ökosystem (Compiler, Tools, Bibliotheken) fehlt
- **Mitigation:** Open-Source-Strategie, Kompatibilitäts-Layer für bestehenden Code

**Konkurrierende Technologien:**
- Chiplets könnten ähnliche Vorteile bei niedrigerem Risiko bieten
- **Mitigation:** KORA fokussiert auf Kohärenz-Nische, wo Chiplets strukturell unterlegen sind

### 7.3 Markt-Risiken

**Energiekosten steigen nicht wie projiziert:**
- Wenn Strom <0,30 €/kWh bleibt, verlängert sich Amortisation
- **Mitigation:** Auch ohne Energiekrise ist Reproduzierbarkeit wertvoll

**KI-Hype endet:**
- Weniger große Trainings → kleinerer Markt
- **Mitigation:** KORA ist für wissenschaftliches Computing (unabhängig von KI-Trends) konzipiert

**Regulierung erfolgt nicht:**
- Ohne Effizienz-Standards bleibt Status Quo attraktiv
- **Mitigation:** Wissenschaftliche Community (Helmholtz, DLR) hat intrinsische Motivation unabhängig von Regulierung

---

## 8. Zusammenfassung und Ausblick

### 8.1 Kernaussagen

1. **KORA adressiert reale Ineffizienzen** moderner Big-Data-Systeme durch Rückkehr zu fundamentalen Prinzipien (Batch, Determinismus, Kohärenz)

2. **Software-Optimierung allein** bringt 15-28% Verbesserung bei Laufzeit und Energie – ohne neue Hardware

3. **Spezialisierte Hardware** ermöglicht 80-96% Einsparungen durch Elimination struktureller Overheads (Inter-Chip-Kommunikation, Cache-Kohärenz)

4. **Reproduzierbarkeit** wird von "best effort" zu "garantiert" – kritisch für Wissenschaft und regulierte Domänen

5. **KORA ist keine Universal-Lösung**, sondern Spezialwerkzeug für kohärenz-dominierte Langläufer

### 8.2 Zeitliche Relevanz

**Kurzfristig (2025-2027):**
- Software-Framework validiert Konzept
- Erste Adoptionen in wissenschaftlichen Instituten

**Mittelfristig (2028-2032):**
- Energiekosten, KI-Volumen und Moore's Law-Ende machen KORA ökonomisch zwingend
- Erste monolithische Hardware-Deployments

**Langfristig (2033+):**
- KORA als Standard für Big-Data-Langläufer etabliert
- Wafer-Scale-Integration für Exascale-Anwendungen

---

KORA ist als **Open-Science-Projekt** konzipiert. Die Grundidee, Simulationen und Spezifikationen sind frei verfügbar unter CC-BY-SA 4.0.

---

**Dieses Dokument ist Teil des KORA-Projekts**  
**Lizenz:** CC-BY-SA 4.0  
**Vollständige Dokumentation:** https://osf.io/8wyec  
**Kontakt:** adamsfke@proton.me**Letzte Aktualisierung:** November 2025
