# KORA – Zukunftsprojektion und Relevanzzeitpunkt

## Wann wird kohärenzorientierte Architektur systemrelevant?

**Autoren:** Frank Meyer  
**Version:** 1.0 (November 2025)  
**Dokumenttyp:** Trend-Analyse und Prognose

---

## Inhaltsverzeichnis

1. Executive Summary
2. Treibende Faktoren
3. Technologische Entwicklung
4. Ökonomische Schwellenwerte
5. Regulatorische Rahmenbedingungen
6. Zeitstrahl und Szenarien
7. Strategische Empfehlungen
8. Risiken und Unsicherheiten
9. Zusammenfassung und Schlussfolgerungen

---

## 1. Executive Summary

### 1.1 Kernaussage

KORA wird zwischen **2028-2033** für spezialisierte Big-Data-Workloads systemrelevant, getrieben durch:

1. **Energiekosten** steigen auf 0,50-0,70 €/kWh (Dekarbonisierung)
2. **Moore's Law** endet praktisch (<10% Verbesserung pro Generation)
3. **KI-Trainingsvolumen** erreicht >1 Mio große Modelle/Jahr global
4. **Datacenter-Kapazitätsgrenzen** erzwingen Effizienz-Innovation
5. **Regulierung** schreibt Energieeffizienz-Standards vor

**Wahrscheinlichste Zeitfenster:**

- **Forschungsrelevanz** (erste Deployments in Labs): **2027-2029**
- **Industrielle Relevanz** (Hyperscaler-Adoption): **2030-2033**
- **Massenmarkt** (Standard für Big-Data): **2035+**

### 1.2 Trigger-Ereignisse

Wenn eines dieser Ereignisse eintritt, wird KORA **sofort** relevant:

| Ereignis | Wahrscheinlichkeit bis 2030 | Auswirkung |
|----------|----------------------------|------------|
| Strompreis >0,60 €/kWh | 30% | Macht KORA ökonomisch zwingend |
| Datacenter-Genehmigungsstopp (EU-Metropolen) | 60% | Effizienz wird Genehmigungskriterium |
| Moore's Law <10% pro Generation | 80% | Architektur wird einziger Hebel |
| Carbon-Tax >100 €/Tonne CO₂ | 40% | 96% Energie-Einsparung = Wettbewerbsvorteil |
| GPT-5+ Training >50 Mio € (Energie-dominiert) | 70% | Frontier-Labs suchen verzweifelt Effizienz |

---

## 2. Treibende Faktoren

### 2.1 Energiekosten-Entwicklung

**Aktueller Stand (2025):**
```
Industriestrom (EU-Durchschnitt): 0,25-0,35 €/kWh
Datacenter-Kontrakte: 0,15-0,25 €/kWh
Trend: +3-5% pro Jahr (strukturell)

Treiber:
- Dekarbonisierung (CO₂-Zertifikate steigen)
- Netzausbau-Kosten (Smart Grid, Speicher)
- Ausstieg fossile Brennstoffe (teurere Alternativen kurzfristig)
```

**Projektion:**

| Jahr | Strompreis (€/kWh) | Veränderung | KORA-Relevanz |
|------|-------------------|-------------|---------------|
| 2025 | 0,30 | Baseline | Nische |
| 2028 | 0,35 | +17% | Interessant für Early Adopters |
| 2030 | 0,45 | +50% | Ökonomisch attraktiv |
| 2033 | 0,60 | +100% | Kritische Masse erreicht |
| 2035 | 0,70 | +133% | Standard für Big-Data |

**Kritischer Punkt:**

Bei **0,45-0,50 €/kWh** (erwartet 2030-2031) wird KORA für Institutionen mit >500 Trainings/Jahr ökonomisch zwingend.

### 2.2 KI-Trainingsvolumen

**Aktueller Trend:**
```
2020: ~10.000 große Modell-Trainings weltweit (>1B Parameter)
2023: ~50.000
2024: ~100.000 (Verdopplung pro Jahr)
2025: ~200.000 (geschätzt)

Wachstumsrate: 100% pro Jahr (2020-2025)
Verlangsamung erwartet: 50-70% pro Jahr (2025-2030)
```

**Projektion:**
```
2026: ~350.000 Trainings
2028: ~1.000.000 Trainings ← KORA-Schwelle erreicht
2030: ~2.500.000 Trainings
2033: ~6.000.000 Trainings
2035: ~10.000.000 Trainings
```

**Kritischer Punkt:**

Bei **>1 Mio Trainings/Jahr global** (2028-2029) wird der Markt für spezialisierte Hardware groß genug für Amortisation von KORA-Entwicklungskosten.

### 2.3 Moore's Law – Das Ende der Skalierung

**Historische Entwicklung:**

| Zeitraum | Transistor-Dichte-Wachstum | Charakteristik |
|----------|---------------------------|----------------|
| 1970-2005 | 2× pro 2 Jahre | Klassisches Moore's Law |
| 2005-2015 | 1,8× pro 2 Jahre | Verlangsamung beginnt |
| 2015-2025 | 1,5× pro 2 Jahre | Deutliche Verlangsamung |
| 2025-2030 | 1,2× pro 2 Jahre | Praktisches Ende |
| 2030+ | <1,1× pro 2 Jahre | Atomare Grenzen |

**Prozess-Roadmap:**

```
Aktuell (2025): 3nm (TSMC N3)
2026: 2nm (erste Produktion)
2027: A14 (1,4nm-äquivalent)
2028-2029: ~1nm
2030+: Sub-1nm (Gate-All-Around, Nanosheet)
```

**Problem:** Physikalische Grenzen

```
Herausforderungen ab <3nm:
- Quantentunneling (Elektronen durchdringen Gates)
- Leakage-Ströme (Standby-Leistung steigt)
- Variabilität (Atomare Schwankungen relevant)
- Herstellungskosten (Exponentiell steigend)

Kosten pro Transistor:
2015 (14nm): 0,01 Cent
2020 (7nm):  0,015 Cent (+50%)
2025 (3nm):  0,025 Cent (+150%)
2030 (1nm):  0,045 Cent (+350%)

→ Moore's Law gilt nicht mehr ökonomisch
```

**Kritischer Punkt:**

Wenn Prozess-Skalierung **<10% Verbesserung pro Generation** liefert (2029-2031), wird Architektur-Effizienz (wie KORA) zum **einzigen** verbliebenen Hebel für Performance-Steigerung.

### 2.4 Datacenter-Kapazitätsgrenzen

**Aktuelle Situation:**

```
Globale Datacenter-Kapazität: ~10 GW elektrische Leistung (2025)
KI-Workloads: ~30% = 3 GW
Wachstum: 20% pro Jahr

Projektion:
2028: 17 GW (KI: 6,8 GW)
2030: 25 GW (KI: 10 GW)
2033: 44 GW (KI: 17,6 GW)
```

**Infrastruktur-Limitierungen:**

| Stadt | Status | Problem |
|-------|--------|---------|
| Frankfurt | Moratorium seit 2024 | Stromnetz-Kapazität erschöpft |
| Amsterdam | Genehmigungsstopp 2023 | Umweltauflagen |
| Dublin | Obergrenze erreicht 2022 | Nationale Stromversorgung limitiert |
| Singapur | Keine neuen DCs 2019 | Land- und Energie-Knappheit |

**Kritischer Punkt:**

Wenn Kapazitätslücke **>20%** erreicht (2029-2030), werden neue Datacenter nur noch genehmigt, wenn sie **signifikant effizienter** sind als Bestand. KORA mit 80-95% Energieeinsparung wird dann **Compliance-Werkzeug**.

---

## 3. Technologische Entwicklung

### 3.1 Konkurrierende Technologien

**Chiplet-Architekturen (AMD, Intel):**

```
Status 2025:
- AMD MI300: 8 Chiplets + 8 HBM
- Intel Ponte Vecchio: 47 Tiles
- Apple M-Serie: Heterogene Chiplets

Vorteile:
+ Höherer Yield als Monolithe
+ Flexibilität (Mix verschiedener Tiles)
+ Bewährte Fertigungstechnologie

Nachteile:
- Inter-Chiplet-Latenz (50-100ns)
- Kohärenz-Overhead bleibt
- Energieeffizienz suboptimal

Zeitlinie:
2025-2028: Chiplets dominieren High-End-Computing
2028-2030: Kohärenz-Overhead wird spürbar bei Big-Data
2030+: KORA wird attraktiv für Kohärenz-kritische Workloads
```

**GPU-Evolution:**

```
NVIDIA-Roadmap:
2024: Blackwell (B100) – 20 Petaflops/GPU
2026: Next-Gen (vermutlich "C"-Serie) – 40 Petaflops/GPU
2028: Übernächste Generation – 60-80 Petaflops/GPU

Grenzen:
- Power-Wall: 1000W+ TDP (Kühlung wird Problem)
- PCIe-Bottleneck: Host-Device-Transfers bleiben langsam
- Non-Determinismus: Warp-Scheduling bleibt probabilistisch

KORA-Positionierung:
Konkurriert NICHT mit GPUs für Matrix-Ops
Konkurriert für strukturierte Big-Data, wo GPU-Overhead dominiert
```

**Wafer-Scale-Integration (Cerebras):**

```
Cerebras WSE-3 (2023):
- 46.225 mm² (ganzer Wafer)
- 900.000 Cores
- 44 GB On-Chip-Memory
- Preis: $2-5 Millionen

Zeitlinie:
2025-2027: Cerebras etabliert sich in Top-0,1% (National Labs)
2027-2029: Zeigt: Wafer-Scale funktioniert (Validierung)
2029-2031: KORA positioniert sich als "Cerebras-Light" (10% der Kosten)

Synergien:
Cerebras-Erfolg ebnet Weg für KORA (akzeptiert große Dies)
```

### 3.2 KORA-Entwicklungs-Timeline

**Phase 1: Software-Framework (2025-2027)**

```
Meilensteine:
Q4 2025: Open-Source-Release (OSF/GitHub)
Q2 2026: Erste Pilotprojekte (Helmholtz, DLR, Fraunhofer)
Q4 2026: Empirische Validierung (15-30% Verbesserung nachgewiesen)
Q2 2027: Workshop auf SC/ISC (Internationale Aufmerksamkeit)
Q4 2027: Phase-2-Funding gesichert (öffentlich oder privat)

Erfolgsmetriken:
- 5+ Forschungsinstitute nutzen KORA aktiv
- 20+ wissenschaftliche Zitationen
- Messbare Performance-Verbesserung bestätigt
```

**Phase 2: Multi-Chip-Module (2027-2029)**

```
Meilensteine:
Q2 2028: FPGA-Prototyp (KORA-Core-Logik)
Q4 2028: MCM-Design fertig (4-8 Tiles)
Q2 2029: Tape-Out (erste Chips)
Q4 2029: Validierung und Benchmarking

Investition:
- FPGA-Prototyping: 500k-1M €
- MCM-Design: 2-5M €
- Tape-Out: 5-10M €
- Total: 8-16M €

Partner:
- Foundry: TSMC/Samsung/GlobalFoundries
- Design-Tools: Synopsys/Cadence
- Forschungsförderung: EU Horizon, BMBF
```

**Phase 3: Monolithischer ASIC (2029-2033)**

```
Meilensteine:
Q2 2030: Monolith-Design-Start
Q4 2030: Tape-Out (2.500 mm² Die @ 3nm)
Q2 2031: Erste Samples
Q4 2031: Validierung (BERT-Benchmark: 96% Einsparung bestätigt?)
Q2 2032: Kleine Serien-Produktion (100-500 Chips)
Q4 2032: Erste Deployments bei Hyperscalern
2033: Ramp-Up (1000+ Chips/Jahr)

Investition:
- Design: 10-20M €
- Tape-Out: 30-50M €
- Validierung: 5-10M €
- Total: 45-80M €

Break-Even:
Bei 1000 Chips/Jahr à 150k € = 150M € Umsatz
Profitabel ab Jahr 3-4 nach Markteinführung
```

---

## 4. Ökonomische Schwellenwerte

### 4.1 Total Cost of Ownership (TCO)

**Vergleich über 5 Jahre (Forschungsinstitut, 100 Trainings/Jahr):**

```
Standard (heute):
  Hardware: 80.000 €
  Energie/Jahr: ~174.000 kWh = ~52.000 € (steigend 4%/Jahr)
  5-Jahres-TCO: ~360.000 €

KORA-Software (2026):
  Hardware: 80.000 € + 10.000 € SW-Entwicklung
  Energie/Jahr: ~143.000 kWh = ~43.000 € (-18%)
  5-Jahres-TCO: ~305.000 € (-15%)

KORA-Hardware (2031):
  Hardware: 150.000 €
  Energie/Jahr: ~4.500 kWh = ~2.000 € (-99%)
  5-Jahres-TCO: ~163.000 € (-55%)
```

**Break-Even-Matrix:**

| Strompreis (€/kWh) | Trainings/Jahr | Break-Even KORA-HW (Jahre) |
|--------------------|----------------|---------------------------|
| 0,30 | 50 | 0,8 |
| 0,30 | 100 | 0,4 |
| 0,30 | 500 | <0,1 |
| 0,45 | 50 | 0,5 |
| 0,45 | 100 | 0,3 |
| 0,45 | 500 | <0,1 |
| 0,60 | 50 | 0,4 |
| 0,60 | 100 | 0,2 |
| 0,60 | 500 | <0,1 |

**Berechnung (Beispiel: 0,30 €/kWh, 100 Trainings/Jahr):**
```
Zusätzliche HW-Kosten: 150.000 - 80.000 = 70.000 €
Energie-Einsparung pro Training: 5.797 - 45 = 5.752 kWh
Kosten-Einsparung: 5.752 × 0,30 = 1.726 € pro Training
Break-Even: 70.000 / 1.726 = 40,6 Trainings = 0,4 Jahre
```

**Kritischer Punkt:**

Bei **0,30 €/kWh** (aktuell) und **100+ Trainings/Jahr** (typisch für mittlere Forschungsinstitute) ist Break-Even bereits nach **unter 1 Jahr** erreicht – das macht KORA-Hardware extrem attraktiv ab **~2031** (wenn verfügbar).

Bei höheren Strompreisen (0,45-0,60 €/kWh ab 2030) amortisiert sich KORA-Hardware in **Monaten statt Jahren**.

### 4.2 Marktgröße und Adoption-Kurve

**Globaler adressierbarer Markt (TAM):**

```
Segment 1: Forschungsinstitute (Helmholtz, Fraunhofer, Max-Planck, Universities)
- Anzahl: ~500 weltweit
- KORA-Systeme pro Institut: 2-10
- Marktgröße: 1.000-5.000 Systeme
- Umsatzpotenzial: 150-750M €

Segment 2: Mittlere Hyperscaler / Cloud-Provider
- Anzahl: ~50 (z.B. OVH, Hetzner, Scaleway)
- KORA-Systeme pro Provider: 100-1.000
- Marktgröße: 5.000-50.000 Systeme
- Umsatzpotenzial: 0,75-7,5 Mrd €

Segment 3: Top-Hyperscaler (Google, Amazon, Microsoft, Meta)
- Anzahl: ~10
- KORA-Systeme pro Hyperscaler: 10.000-100.000
- Marktgröße: 100.000-1.000.000 Systeme
- Umsatzpotenzial: 15-150 Mrd €

Total Addressable Market (TAM) 2030-2035: 16-158 Mrd €
```

**Adoption-Phasen:**

| Phase | Jahre | Anteil | Charakteristik |
|-------|-------|--------|----------------|
| Innovatoren | 2027-2028 | 2,5% | Pionier-Institute (Helmholtz, MIT) |
| Early Adopters | 2028-2030 | 13,5% | Forschungsorientierte Organisationen |
| Early Majority | 2030-2032 | 34% | Pragmatische Institutionen, erste Hyperscaler |
| Late Majority | 2032-2035 | 34% | Konservative Adopter, Mainstream |
| Laggards | 2035+ | 16% | Späte Nachzügler |

---

## 5. Regulatorische Rahmenbedingungen

### 5.1 EU Green Deal und AI Act

**Projektion – Regulierungsentwicklung:**

| Jahr | Regulierung | Auswirkung auf KORA |
|------|-------------|---------------------|
| 2026 | EU AI Act Revision 1.0 | Erste Nachhaltigkeits-Diskussionen |
| 2028 | Energy Efficiency Directive (EED) erweitert auf Datacenter | Effizienzkennzeichnung (A-G) für KI-Training |
| 2030 | Carbon Border Adjustment Mechanism (CBAM) auf Cloud-Services | Indirekte Carbon-Preise auf ineffiziente Systeme |
| 2032 | EU AI Sustainability Regulation | Mindeststandardsstandards (z.B. <50 kWh/Mrd Parameter) |
| 2034 | Carbon Tax auf Datacenter-Betrieb | Direkte Besteuerung ineffizienter Infrastruktur |

**KORA-Vorteil durch Regulierung:**

Wenn Regulierung Effizienz-Standards vorschreibt, wird KORA von **Nice-to-have** zu **Compliance-Requirement**.

### 5.2 Carbon-Pricing

**Projektion – Direkte Datacenter-Besteuerung:**

| Jahr | CO₂-Preis (€/t) | Gilt für DC? | Einsparung KORA (100 Trainings/Jahr) |
|------|----------------|-------------|--------------------------------------|
| 2025 | 0 | Nein | 0 € |
| 2028 | 100 | Nein | 0 € |
| 2030 | 120 | Ja | 27.600 € |
| 2033 | 150 | Ja | 34.500 € |
| 2035 | 200 | Ja | 46.000 € |

**Berechnung (Beispiel 2030):**
```
CO₂-Intensität EU-Strom: 0,4 kg CO₂/kWh

Standard pro Training: 5.797 kWh × 0,4 = 2.319 kg CO₂
KORA pro Training: 45 kWh × 0,4 = 18 kg CO₂
Einsparung: 2.301 kg CO₂ = 2,3 Tonnen

Carbon-Tax: 2,3 × 120 €/t = 276 € pro Training
100 Trainings: 27.600 € pro Jahr
```

**Kritischer Punkt:**

Bei Carbon-Tax >100 €/Tonne (2030+) entstehen **zusätzliche 27.000-46.000 € Einsparung** pro 100 Trainings – das beschleunigt KORA-Amortisation dramatisch (von Monaten auf Wochen).

---

## 6. Zeitstrahl und Szenarien

### 6.1 Integrierter Zeitstrahl

**2025-2027: Foundation-Phase**

```
2025 Q4: OSF-Publikation, Open-Source-Release
2026 Q2: Erste Pilotprojekte (3-5 Institute)
2026 Q4: Empirische Validierung (Paper bei SC/IPDPS)
2027 Q2: Erste Zitationen, Community-Interest wächst
2027 Q4: Phase-2-Funding (8-16M €) gesichert

Treiber:
- Wissenschaftliche Neugier
- Reproduzierbarkeits-Probleme in ML werden bewusster
- Steigende Energiekosten (+15% kumulativ)

KORA-Relevanz: Nische (Forschung)
```

**2028-2030: Acceleration-Phase**

```
2028 Q2: FPGA-Prototyp demonstriert Vorteile
2028 Q4: Moore's Law zeigt <15% Verbesserung/Generation
2029 Q2: Erste MCM-Prototypen (4-8 Tiles)
2029 Q4: KI-Trainings-Volumen >1 Mio/Jahr global
2030 Q2: Monolith-Design-Start
2030 Q4: Strompreis erreicht 0,45 €/kWh (EU-Durchschnitt)

Treiber:
- Moore's Law-Ende wird offensichtlich
- Datacenter-Kapazitätsgrenzen in Metropolen
- Regulierungsdiskussion (EU) beginnt

KORA-Relevanz: Early Adopters (10-50 Systeme deployed)
```

**2031-2033: Mainstream-Phase**

```
2031 Q2: Erste monolithische KORA-Chips (Samples)
2031 Q4: Benchmarks bestätigen 80-95% Energieeinsparung
2032 Q2: Serien-Produktion (100-500 Chips)
2032 Q4: Erste Hyperscaler-Deployments (Google/Meta/Amazon)
2033 Q2: Carbon-Tax auf Datacenter (EU)
2033 Q4: 50% Marktdurchdringung bei Zielgruppe

Treiber:
- Empirische Beweise (nicht nur Simulationen)
- Regulatorischer Druck (Effizienz-Standards)
- Ökonomische Zwangsläufigkeit (0,60 €/kWh)

KORA-Relevanz: Mainstream (1.000-5.000 Systeme deployed)
```

**2034-2036: Maturity-Phase**

```
2034: Wafer-Scale-KORA für Exascale (Cerebras-Konkurrenz)
2035: KORA-Prinzipien beeinflussen nächste GPU/CPU-Generation
2036: Standard für wissenschaftliches Big-Data-Computing

KORA-Relevanz: Etabliert (10.000+ Systeme)
```

### 6.2 Szenario-Analyse

**Pessimistisches Szenario (30% Wahrscheinlichkeit):**

```
Annahmen:
- Strompreise steigen nur auf 0,35 €/kWh (statt 0,60 €/kWh)
- Moore's Law verlangsamt sich weniger stark (noch 15% pro Generation)
- KI-Hype endet, Trainingsvolumen stagniert bei 500k/Jahr
- Keine Regulierung von Datacenter-Effizienz

Konsequenz:
- KORA bleibt Nische für Reproduzierbarkeits-kritische Anwendungen
- Phase 3 (Monolith) wird nicht finanziert
- Relevanz: <1.000 Systeme bis 2035
```

**Realistisches Szenario (50% Wahrscheinlichkeit):**

```
Annahmen:
- Strompreise erreichen 0,50 €/kWh bis 2030
- Moore's Law <10% Verbesserung pro Generation ab 2030
- KI-Trainings 1-2 Mio/Jahr bis 2030
- Soft-Regulierung (freiwillige Effizienz-Standards)

Konsequenz:
- KORA etabliert sich in Forschung und mittleren Hyperscalern
- Monolith wird produziert (kleine Serie, 1.000-5.000 Chips)
- Relevanz: 2.000-8.000 Systeme bis 2035
```

**Optimistisches Szenario (20% Wahrscheinlichkeit):**

```
Annahmen:
- Energiekrise verschärft sich (0,70 €/kWh bis 2030)
- Moore's Law endet abrupt (<5% pro Generation)
- KI-Boom hält an (5+ Mio Trainings/Jahr bis 2033)
- Harte Regulierung (EU mandatorische Effizienz-Standards)

Konsequenz:
- KORA wird Standard für Big-Data
- Monolith in Massen-Produktion (10.000+ Chips/Jahr)
- Top-Hyperscaler deployen massiv
- Relevanz: 20.000+ Systeme bis 2035
```

---

## 7. Strategische Empfehlungen

### 7.1 Für KORA-Projekt

**Kurzfristig (2025-2027):**

1. **Maximiere Sichtbarkeit:** Top-Konferenzen, Open-Source-Community
2. **Validiere Kernthesen:** Prototyp mit 15-30% Verbesserung
3. **Baue Partnernetzwerk:** 5-10 Forschungsinstitute

**Mittelfristig (2027-2030):**

1. **Sichere Finanzierung:** 15-20M € für MCM-Entwicklung
2. **Demonstriere Hardware:** FPGA/MCM mit 40-60% Verbesserung
3. **Etabliere Standards:** KORA-API, Benchmark-Suite

**Langfristig (2030-2035):**

1. **Skaliere Produktion:** 1.000-10.000 Chips/Jahr
2. **Erweitere Domänen:** Enterprise-Big-Data, Cloud-Integration
3. **Beeinflusse Standards:** Kohärenz in nächster Generation

### 7.2 Für Potenzielle Adopter

**Forschungsinstitute:**
- **Jetzt (2025):** Teste Software-KORA (kein Risiko)
- **2027-2028:** Evaluiere bei validierter Software-Version
- **2030+:** Hardware-Version bei Break-Even

**Mittlere Hyperscaler:**
- **2028-2029:** Evaluiere MCM-Prototypen
- **2031-2032:** Pilot-Deployment (10-50 Nodes)

**Top-Hyperscaler:**
- **2030+:** Evaluiere bei empirischen Daten
- Vergleiche mit interner Custom-ASIC-Entwicklung

---

## 8. Risiken und Unsicherheiten

### 8.1 Technologische Risiken

**Yield-Problem (40% Wahrscheinlichkeit):**
- Monolith erreicht <50% Yield
- **Mitigation:** Conservative Design, mehr Redundanz, Plan B: MCM

**Determinismus nicht erreichbar (20%):**
- Keine bit-identische Reproduzierbarkeit
- **Mitigation:** Extensive Validierung Phase 1, Fallback: probabilistisch

### 8.2 Markt-Risiken

**Energiekosten steigen nicht (30%):**
- Strompreis bleibt <0,35 €/kWh
- **Mitigation:** Fokus auf Reproduzierbarkeit, nicht nur Energie

**KI-Hype endet (25%):**
- Trainingsvolumen stagniert
- **Mitigation:** Positionierung für HPC (unabhängig von KI)

### 8.3 Konkurrenz-Risiken

**Chiplets werden "gut genug" (50%):**
- AMD/Intel optimieren Kohärenz stark
- **Mitigation:** KORA fokussiert extreme Kohärenz-Anforderungen

---

## 9. Zusammenfassung und Schlussfolgerungen

### 9.1 Wahrscheinlichste Timeline

```
2025-2027: Foundation (Software-Validierung, Community)
2028-2030: Inflection Point (Moore's Law, Energie, Adoption)
2031-2033: Mainstream (Hardware-Produktion, Hyperscaler)
2034+: Maturity (Standard für kohärenz-kritische Workloads)

Kritisches Jahr: 2029-2030
→ Confluence mehrerer Treiber
→ Fenster für KORA-Relevanz öffnet sich
```

### 9.2 Kern-Aussagen

1. **KORA wird relevant, aber nicht universal:** Nische 10-20% des Marktes, TAM 5-15 Mrd €
2. **Timing ist kritisch:** Optimal 2028-2032, zu früh/spät problematisch
3. **Mehrfache Treiber nötig:** Kombination von 3+ Faktoren macht KORA zwingend
4. **Adoption folgt Chasm-Modell:** Innovatoren → Early Adopters → Chasm → Mainstream
5. **Risiken sind managebar:** Validierbar in Phase 1+2, flexibles Reagieren

### 9.3 Finale Einschätzung

**KORA wird zwischen 2028-2033 für spezialisierte Big-Data-Workloads systemrelevant.**

Wahrscheinlichkeitsverteilung:

| Szenario | Wahrscheinlichkeit | Systeme bis 2035 |
|----------|-------------------|-------------------|
| **Scheitern** (Technisch oder Markt) | 20% | <500 |
| **Nische** (Forschung dominant) | 30% | 1.000-5.000 |
| **Mainstream** (Etablierter Standard) | 40% | 10.000-50.000 |
| **Dominanz** (Trigger-Events) | 10% | >100.000 |

**Erwartungswert:** KORA wird ein **erfolgreicher Nischen-Player** mit bedeutendem Impact auf wissenschaftliches Computing und spezialisierten Einfluss auf kommerzielle Big-Data-Verarbeitung.

Die Innovation liegt nicht in revolutionärer Neuheit, sondern in der **konsequenten Anwendung fundamentaler Prinzipien** (Kohärenz, Determinismus, Spezialisierung) auf moderne Problemstellungen – ein "Zurück zu den Wurzeln" zur richtigen Zeit.

---

## Anhang A: Methodik der Projektion

### A.1 Datenquellen

**Energiekosten-Projektion:**
- Eurostat Energy Price Statistics (2015-2025)
- IEA World Energy Outlook 2024
- EU Carbon Market Data (EEX)

**KI-Trainingsvolumen:**
- Papers with Code (Trends in Model Sizes)
- Stanford AI Index Report 2024
- Epoch AI Compute Trends

**Moore's Law:**
- ITRS/IRDS Roadmaps (2020, 2023)
- TSMC/Samsung Technology Roadmaps
- IEEE ISSCC Papers (Process Node Advancement)

**Datacenter-Kapazität:**
- Synergy Research Group Datacenter Census
- IEA Datacenter Energy Consumption Report
- Uptime Institute Global Data Center Survey

### A.2 Projektions-Methoden

**Trend-Extrapolation:** Lineare Regression für Energiekosten (R² = 0,82)

**Exponentielles Wachstum:** Logistische Wachstumsfunktion für KI-Trainings mit Sättigungsgrenze

**Delphi-Methode:** Experteneinschätzungen für Regulierungs-Wahrscheinlichkeiten

### A.3 Unsicherheits-Quantifizierung

Alle Projektionen haben **Konfidenzintervalle (80%)**:

| Variable | 2028 | 2033 |
|----------|------|------|
| Strompreis | 0,30-0,40 €/kWh | 0,45-0,75 €/kWh |
| KI-Trainings | 0,7-1,5 Mio/Jahr | 4-8 Mio/Jahr |
| Moore's Law | 10-20% Verbesserung | 5-10% Verbesserung |
| KORA-Relevanz | Nische-Early Adopters | Early Majority-Mainstream |

---

## Anhang B: Vergleich mit historischen Technologie-Adoptionen

### B.1 Analoge Technologie-Übergänge

**RISC vs. CISC (1980er-1990er):**
```
Ähnlichkeiten zu KORA:
- Vereinfachung statt Komplexität
- Spezialisierung statt General-Purpose
- 15-25 Jahre für volle Adoption

Lektion: KORA folgt vermutlich RISC-Muster (langsam, Nische-First)
```

**SSD vs. HDD:**
```
Unterschiede:
- SSD war universell besser (keine Trade-offs außer Preis)
- KORA opfert Flexibilität

Lektion: 10-20 Jahre für Mainstream
```

**Virtualisierung (VMware, Cloud):**
```
Lektion für KORA:
- 10-15 Jahre Innovators → Mainstream
- Ökonomischer Druck beschleunigt
- Ökosystem ist kritisch
```

### B.2 Adoption-Geschwindigkeit-Faktoren

| Faktor | RISC | SSD | Virtualisierung | KORA (geschätzt) |
|--------|------|-----|-----------------|------------------|
| Performance-Vorteil | 2-3× | 100× | 2-3× | 1,2-6× |
| Kompatibilität | Neu-Compile | Plug-and-Play | Software-only | Neu-Compile |
| Zeit zu Mainstream | 15 Jahre | 10 Jahre | 10 Jahre | 10-15 Jahre |

**Prognose:** KORA folgt eher **RISC-Muster** (langsam, Nische-First, 15-20 Jahre) als **SSD-Muster** (schnell, Universal).

---

## Anhang C: Glossar und Abkürzungen

**ASIC** – Application-Specific Integrated Circuit  
**BSP** – Bulk-Synchronous Parallel  
**CBAM** – Carbon Border Adjustment Mechanism  
**CFD** – Computational Fluid Dynamics  
**DI** – Determinismus-Index  
**ECC** – Error-Correcting Code  
**EED** – Energy Efficiency Directive  
**FG** – Fragmentierungsgrad  
**FLOP** – Floating-Point Operation  
**FPGA** – Field-Programmable Gate Array  
**HBM** – High-Bandwidth Memory  
**HPC** – High-Performance Computing  
**IRQ** – Interrupt Request  
**KVI** – Kohärenz-Verlust-Index  
**MCM** – Multi-Chip Module  
**MTBF** – Mean Time Between Failures  
**NUMA** – Non-Uniform Memory Access  
**RDMA** – Remote Direct Memory Access  
**SIMD** – Single Instruction Multiple Data  
**SRDB** – Single Resonance Data Bus  
**TAM** – Total Addressable Market  
**TCO** – Total Cost of Ownership  
**TDP** – Thermal Design Power  

---

**Ende der Zukunftsprojektion**

**Lizenz:** CC-BY-SA 4.0  
**Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
**Kontakt:** adamsfke@proton.me  
**Letzte Aktualisierung:** November 2025

**Disclaimer:** Diese Projektion basiert auf aktuell verfügbaren Daten und Trends. Tatsächliche Entwicklungen können signifikant abweichen. Alle Wahrscheinlichkeitsangaben sind subjektive Einschätzungen basierend auf strukturierter Analyse, keine Garantien.
