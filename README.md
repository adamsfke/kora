# KORA – A Deterministic, Energy-Efficient Architecture Model
Version 2.0 — Realmodell v3.0

**Status:** Machbarkeitsstudie

KORA ist ein Architektur- und Ausführungsmodell für effiziente,
deterministische und reproduzierbare Hochleistungsberechnung.
Es wurde speziell für Workloads entwickelt, die heute stark durch
nichtlineare Overheads limitiert sind:

- KI-Training (z. B. BERT, GPT-Modelle)
- Big-Data-Analysen und ETL-Strecken
- numerische Simulationen (CFD, FEM, Klima/Wetter)
- datenintensive wissenschaftliche Anwendungen

KORA zeigt, dass massive Leistungs- und Effizienzgewinne
nicht durch mehr FLOPs, sondern durch die Reduktion von
Memory-, Communication- und Synchronisations-Overheads erreicht werden.

---

## Inhalte der Version 2.0

Version 2.0 stellt eine vollständige Überarbeitung des ursprünglichen Modells dar.
Neu eingeführt wurden:

- ein realitätsnahes **Compute–Memory–Communication–Sync-Modell (v3.0)**  
- realistische Architekturparameter (A/B/C)  
- ein universelles Simulationsmodell, das alle Workloads abdeckt  
- vollständige Unterstützung für deterministische Ausführung (r_bit, r_run)  
- realistische Workload-Klassen (BERT, BD-S, BD-L, CFD-M, CFD-L)  
- energie- und zeitbasierte Performancevergleiche  
- neue Markdown-Dokumente mit klarer wissenschaftlicher Struktur  

---

## Architekturvarianten (A/B/C)

### Architektur A – Standard HPC/KI  

Realistische Basis bestehender Rechenzentren  
(hohe Overheads, hohe Energie, niedrige Reproduzierbarkeit).

### Architektur B – KORA-SW  

Softwareoptimierte Variante auf bestehender Hardware  
(40–70 % Energieeinsparung, 1.3–2.6× Speedup).

### Architektur C – KORA-HW Monolith  

Monolithische Hardware mit deterministischen Datenpfaden  
(97–99 % Energieeinsparung, 5–20× Speedup).

Volle Parameterdetails sind in  
`02_Architecture_Specification.md` beschrieben.

---

## Workloads

KORA v2.0 unterstützt fünf typisierte Workload-Familien:

| Key | Workload | Limitierung |
|------|----------|-------------|
| BERT | BERT-Large Training | Compute |
| BD_S | Big-Data Small (52 GB ETL) | Memory |
| BD_L | Big-Data Large (1 TB, Shuffle) | Memory/Comm/Sync |
| CFD_M | CFD Medium (100M Zellen) | Communication/Sync |
| CFD_L | CFD Large (Climate) | Sync/Comm |

---

## Simulationen

Die Simulationen basieren auf dem **v3.0-Realmodell**
(siehe `03_Simulation_Methodology.md`), das vier unabhängige Terme abbildet:

- Compute  
- Memory  
- Communication  
- Synchronisation  

Ein Korrekturfaktor \(S_W\) pro Workload kalibriert Architektur A exakt
auf reale Referenzwerte.

Für alle Workloads und Architekturen führt dies zu realistischen Zeiten
und Energieverbräuchen.

---

## Kernergebnisse

### Geschwindigkeit

- **KORA-SW (B):** 1.3–2.6× schneller  
- **KORA-HW (C):** 5–20× schneller  

### Energieeffizienz

- **KORA-SW (B):** 40–70 % weniger Energie  
- **KORA-HW (C):** 97–99 % weniger Energie  

### Reproduzierbarkeit

| Arch | r_bit | r_run |
|------|-------|--------|
| A | 0.4 | 1.10 |
| B | 0.8 | 1.02 |
| C | 1.0 | 1.00 |

---

## Projektstruktur

    /
        README.md
		LICENSE.md

    /docs
        00_Abstract.md
        01_Executive_Summary.md
        02_Architecture_Overview.md
        03_Architecture_Specification_Technical.md
        04_Software_Specification.md
        05_API_Reference_TSF_HAPI_ISR.md
        06_Reproducibility_Specification.md
        07_Evaluation_and_Benchmarks.md
        08_Simulation_Methodology.md
        09_Future_Outlook.md
        10_Release_Notes_v2.0.md
        11_Background_and_Scientific_Basis.md
        12_References.md
    
    /simulation
        kora_sim_engine_v3.py

---

## Simulation Package

Die Simulation ist vollständig implementiert in:

[kora_sim_engine_v3.py]

**Kommandos:**

    python3 kora_sim_engine_v3.py

Ausgabe:

- Zeit in Stunden  
- Energie in kWh  
- Speedup  
- Energieeinsparungen  
- Zeitanteile (Compute, Memory, Comm, Sync)

---

## Lizenz

Alle Inhalte dieses Projekts stehen unter **CC-BY-SA 4.0** und **MIT** (für Code):

- **Frei nutzbar** für Forschung, Lehre und kommerzielle Anwendungen
- **Namensnennung erforderlich**: "KORA Project, Frank Meyer in Kooperation mit Claude"
- **Share-Alike**: Abgeleitete Werke müssen unter gleicher Lizenz stehen

Vollständige Lizenz: siehe `LICENSE.md`

---

## Ziel der Veröffentlichung

KORA soll Forschern, Ingenieuren und Unternehmen als Blaupause dienen:

- für effizientere Hardware  
- für optimierte Softwarepipelines  
- für deterministische Rechenabläufe  
- für energieeffiziente Rechenzentren  
- für verlässliche wissenschaftliche Simulationen  

Version 2.0 bildet das Fundament für zukünftige Weiterentwicklungen,
insbesondere für KORA-HW-Prototyping und Multi-Monolith-Systeme.

---

## Danksagung

Dieses Projekt entstand aus der Erkenntnis, dass moderne IT-Architekturen für Big-Data-Langläufer suboptimal sind. 
KORA ist ein Versuch, durch Rückkehr zu fundamentalen Prinzipien (Kohärenz, Determinismus, Batch-Processing) strukturelle Effizienz zurückzugewinnen.

KORA entstand unter struktureller Hilfe von **ChatGPT** *(OpenAI)* und **Claude** *(Anthropic)*.

---

## Versionierung

- **Dokument:** `README.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  