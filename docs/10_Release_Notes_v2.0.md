# KORA - Release Notes – Version 2.0  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0  
**Dokumenttyp:** Offizielle Versionsbeschreibung für OSF  
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Überblick
    2.  Ziele der Version 2.0
    3.  Wichtige neue Dokumente in v2.0
    4.  Überarbeitete Dokumente
    5.  Einheitliches Architekturmodell (neu)
    6.  Vereinheitlichte Simulation (neu)
    7.  Reproduzierbarkeitsrahmen (neu)
    8.  Energie- und Performanceanalyse (neu)
    9.  Konsistente Terminologie (neu)
    10. Entfernte oder zusammengeführte Inhalte
    11. Kompatibilitätshinweise
    12. Ausblick auf Version 2.1 und Phase-2-Dokumente
    13. Zusammenfassung

---

## 1. Überblick

Diese Release Notes beschreiben alle Änderungen, Ergänzungen und strukturellen Erweiterungen, die im Rahmen der KORA Version 2.0 vorgenommen wurden. Version 2.0 stellt die erste vollständige, wissenschaftlich konsolidierte und architekturkohärente Dokumentation des KORA-Systems dar.

Die Änderungen umfassen nicht nur inhaltliche Erweiterungen, sondern eine grundsätzliche Neuordnung des gesamten KORA-Dokumentationskörpers, die Vereinheitlichung der Terminologie, die Einführung deterministischer Modelle und die Integration der v3.0-Simulationsergebnisse.

Version 2.0 bildet die Grundlage aller zukünftigen Veröffentlichungen, der OSF-Publikation sowie der geplanten Phase-2-Hardwareprojekte.

---

## 2. Ziele der Version 2.0

Version 2.0 verfolgt drei übergeordnete Ziele:

    1. Konsolidierung aller KORA-Dokumente in einer einheitlichen Architektur- und Methodiklogik
    2. Einführung eines vollständigen Reproduzierbarkeits- und Evaluationsrahmens
    3. Vorbereitung des Übergangs zur deterministischen Hardwarearchitektur (Phase 2 und 3)

---

## 3. Wichtige neue Dokumente in v2.0

Version 2.0 führt mehrere vollständig neue Kern-Dokumente ein:

    05 Simulation_Methodology.md  
        Vereinheitlicht alle Simulationen in ein gemeinsames Overhead-Modell.
    
    07 Reproducibility_Specification.md  
        Formalisiert Reproduzierbarkeit als architektureigene Eigenschaft.
    
    08 Evaluation_and_Benchmarks.md  
        Stellt alle Benchmarkdaten dar und interpretiert die Ergebnisse v3.0.

    04 Software_Specification.md  
        Definiert KORA-2, die deterministische Software-Ebene.

Diese Dokumente sind zentrale Bausteine für OSF und wissenschaftliche Validierung.

---

## 4. Überarbeitete Dokumente

Mehrere bestehende Dokumente wurden vollständig überarbeitet:

    01 Executive Summary  
        Inhaltlich erweitert, strukturell neu angeordnet, NT-kompatibel.

    02 Architecture Overview  
        Neu geschrieben für nicht-technische Wissenschaftler.

    03 Technical Architecture Specification  
        umfassend restrukturiert, vollständige Hardwaredarstellung.

    06 Future Outlook  
        komplett neu konzipiert mit architekturgetriebener Zukunftslogik.

Alle überarbeiteten Dokumente folgen jetzt einer konsistenten Terminologie und Struktur.

---

## 5. Einheitliches Architekturmodell (neu)

Version 2.0 integriert erstmals ein vollständiges, einheitliches Architekturmodell für:

    Architektur A: HPC/GPU (Baseline)
    Architektur B: KORA-SW (Deterministische Software)
    Architektur C: KORA-HW (Deterministische Hardware)

Dieses Modell wird verwendet für:

    Simulationen
    Benchmarks
    Energieanalyse
    Reproduzierbarkeit
    Zukunftsprojektionen

Es ersetzt alle vorherigen getrennten Modelle.

---

## 6. Vereinheitlichte Simulation (neu)

Die v3.0-Simulationsergebnisse wurden vollständig integriert und basieren nun auf:

    Overhead-Modell:
        T_compute + T_sync + T_sched + T_bus + T_irq + T_cs

    Workload-Modell:
        O_base, M_base, S_base

Die Ergebnisse sind reproduzierbar, konsistent und wissenschaftlich zitierfähig.

---

## 7. Reproduzierbarkeitsrahmen (neu)

Version 2.0 definiert erstmals:

    Reproduzierbarkeitsmetriken (δ_op, δ_fp, δ_mem, δ_seq)
    Golden Runs
    TSF als Reproduzierbarkeitsvertrag
    deterministische Debugging- und Auditmodi
    Architekturebenen der Reproduzierbarkeit (TSF, Software, Hardware)

Dies stellt KORA als einzigartiges Reproduzierbarkeitssystem dar.

---

## 8. Energie- und Performanceanalyse (neu)

Version 2.0 enthält:

    vollständige Benchmarktabellen
    Speedup-Analysen
    Energieverbrauchsvergleiche
    strukturell begründete Interpretationen

Ergebnisse:

    KORA-SW (B):
        1.3–2.6× schneller, 40–70 % weniger Energie

    KORA-HW (C):
        5–20× schneller, 97–99 % weniger Energie

Diese Werte gelten als offizielle Referenz.

---

## 9. Konsistente Terminologie (neu)

Einheitliche Begriffe:

    SRDB
    Scheduling Tree
    TSF
    Deterministic DMA Windows
    Overhead Model
    Architecture A/B/C
    KORA-2 Runtime

Alle Dokumente teilen jetzt dieselbe semantische Grundlage.

---

## 10. Entfernte oder zusammengeführte Inhalte

Folgende veraltete oder redundante Konzepte aus Version 1.x wurden entfernt:

    alte Monolith-Simulation  
    getrennte Big-Data-/KI-/CFD-Simulationen  
    mehrere frühere Architekturversionen  
    inkonsistente Energie-Modelle  
    alte Zukunftsszenarien  
    nicht deterministische Debugging-Modelle  

Sie wurden konsolidiert, vereinheitlicht oder durch die neue Methodik ersetzt.

---

## 11. Kompatibilitätshinweise

Version 2.0 ist:

    abwärtskompatibel hinsichtlich TSF  
    nicht abwärtskompatibel hinsichtlich Dokumentstruktur  
    vollständig kompatibel mit zukünftiger KORA-Hardware  
    vollständig OSF-kompatibel  

Alle TSF-Dateien, die unter Version 2.0 erzeugt werden,  
werden auf KORA-HW (Phase 2 und 3) identisch ausführbar sein.

---

## 12. Ausblick auf Version 2.1 und Phase-2-Dokumente

Version 2.1 (optional) wird voraussichtlich enthalten:

    KORA Hardware Prototype Specification  
    KORA Tile Fabric Whitepaper  
    HAPI/ISR/TSF API Reference  
    Multi-Tile Synchronization Specification  

Diese Inhalte sind nicht Teil der v2.0 Basis, sondern der Phase-2 Entwicklung.

---

## 13. Zusammenfassung

Version 2.0 ist die erste vollständig kohärente, deterministische und wissenschaftlich belastbare Beschreibung des KORA-Projekts.  
Sie besteht aus:

    01–09 Kerndokumenten (Software, Hardware, Methodik, Benchmarks, Zukunft)
    einheitlichen Modellen, Begriffen und Simulationsergebnissen
    vollständigen Reproduzierbarkeits- und Energieanalysen
    klarer Abgrenzung zu traditionellen HPC-Systemen

Version 2.0 bildet die Grundlage:

    für alle OSF-Veröffentlichungen
    für zukünftige Hardwarearbeiten (Phase 2/3)
    für wissenschaftliche Zusammenarbeit
    für regulatorische Nutzung

KORA Version 2.0 ist damit vollständig definiert, nachvollziehbar dokumentiert und stabil reproduzierbar.

---

## Versionierung

- **Dokument:** `10_Release_Notes.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  

