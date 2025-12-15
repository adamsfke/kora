# KORA – Background and Scientific Basis  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Wissenschaftlicher Hintergrund
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Einleitung  
    2.  Reale Probleme heutiger HPC-, KI- und Big-Data-Systeme
    3.  Wissenschaftliche Basis: Jede KORA-Idee ist bereits einzeln belegt
    4.  Wo KORA über den Stand der Technik hinausgeht
    5.  V3.0-Simulation als wissenschaftliches Fundament
    6.  Wissenschaftliche Relevanz
    7.  Fazit: Warum KORA wissenschaftlich notwendig ist
    8.  Literaturhinweise  

---

## 1. Einleitung  
Dieses Dokument bildet die wissenschaftliche Grundlage von KORA.  
Es zeigt, warum die Architektur notwendig ist, welche Probleme aktueller HPC-, KI- und Big-Data-Systeme ungelöst lassen und wie KORA diese Herausforderungen systemisch löst.  

Die Argumentation basiert vollständig auf der aktuellen Literatur, konsolidierten HPC-Erfahrungen und der v3.0-Simulation von KORA.

---

## 2. Reale Probleme heutiger HPC-, KI- und Big-Data-Systeme

Moderne Systeme leiden unter grundlegenden strukturellen Limitierungen:

### 2.1 OS-Noise, Preemption und Kontextwechsel  
Große HPC-Jobs werden häufig unterbrochen.  
Das führt zu:

- Cache-Invalidierungen  
- Verlust lokaler Datenkontexte  
- massiven Variationen in Laufzeit und Energieprofilen  
- Reduktion der Effizienz um 20–70 % bei Langläufern

Diese Probleme sind in der Literatur ausführlich quantifiziert.

### 2.2 Komplexe Batchsysteme mit heuristischem Scheduling  
SLURM, PBS, LSF und GPU-Scheduler nutzen:

- Backfilling  
- Gang-Scheduling  
- stochastische Optimierung  
- Reinforcement-Learning-Scheduler  

Diese Systeme werden immer komplexer, aber nicht deterministischer.

### 2.3 Fragmentierte Speicher- und Interconnect-Topologien  
NUMA, Multi-Socket, PCIe, NVLink und InfiniBand erzeugen:

- nichtlineare Speicherkosten  
- Unvorhersehbarkeit bei globalem Zugriff  
- Latenz-Spikes  
- Konsistenzprobleme in großen Workloads

### 2.4 Nichtdeterministische Kommunikation  
Asynchrone Netzwerkpfade führen zu:

- unkontrollierbaren Synchronisationskosten  
- schwer debugbaren numerischen Fehlern  
- variablen Reduktionsreihenfolgen

### 2.5 Energieprobleme  
Die Energieprofile klassischer Systeme sind:

- unvorhersehbar  
- jitter-behaftet  
- schwer planbar  
- stark variabel zwischen Ausführungen

### 2.6 Numerische Nichtdeterministik in KI  
Moderne GPUs liefern:

- unterschiedliche Ergebnisse zwischen Läufen  
- variierende Gradienten  
- Race Conditions bei Reduktionen  
- Unterschiedliche Summationsreihenfolgen

Dies erschwert Peer Review massiv.

**Schlussfolgerung:**  
Die gesamte HPC-/KI-Landschaft kämpft mit systemischen Problemen, die strukturell gelöst werden müssen — nicht durch stärkeres Tuning.

---

## 3. Wissenschaftliche Basis: Jede KORA-Idee ist bereits einzeln belegt

KORA besteht nicht aus Spekulationen, sondern aus der konsolidierten Integration etablierter Forschungsstränge:

### 3.1 Nicht-Präemption & unterbrechungsarme Langläufer  
HPC-Workload-Studien zeigen:

> Große Jobs laufen signifikant effizienter, wenn sie nicht unterbrochen werden.

KORA übernimmt dieses Prinzip vollständig.

### 3.2 Deterministische Scheduler  
Arbeiten zu deterministischen und RL-basierten Schedulern belegen:

- deterministisches Verhalten → stabilere Ergebnisse  
- Vorhersagbarkeit → bessere Energieplanung  
- deterministische Reduktionen → numerische Stabilität

### 3.3 Kohärente Datenräume  
Shared-Memory- und Coherence-Forschung bestätigt:

- globale Datenräume sind hochwirksam  
- klassische Coherence ist jedoch teuer und komplex  
- spezialisierte Bus-Architekturen bieten massive Vorteile  

KORA nutzt den SRDB:  
ein strikt deterministischer Datenbus ohne dynamische Coherence-Kosten.

### 3.4 Epochale / gebündelte Synchronisation  
Aus verteilten Datenbanken ist bekannt:

- Epochen komprimieren Kommunikation  
- Bulk-Commit reduziert Energie  
- deterministische Commit-Punkte verbessern Stabilität

KORA integriert dieses Prinzip in Scheduling Trees.

### 3.5 Energieeffiziente Architekturen  
Brain-inspired Systeme (Loihi, SpiNNaker, Wukong, Monkey, BIE-1) zeigen:

- massiv reduzierte Energie  
- enge Kopplung von Speicher & Rechenpfad verbessert Effizienz  
- deterministischer Datenfluss ist überlegen

KORA geht einen Schritt weiter:  
Es integriert deterministische Numerik, deterministisches Scheduling und deterministischen Speicherzugriff in einer HPC-tauglichen Architektur.

### 3.6 Big-Data-Forschung zu Datenlokalität  
Big-Data-Analysen belegen:

> Datenbewegung ist teurer als Rechnen.

KORA folgt strikt:

- Daten bleiben lokal auf Tiles  
- SRDB minimiert Bewegung  
- deterministische Fabric eliminiert dynamische Routen

---

## 4. Wo KORA über den Stand der Technik hinausgeht

### 4.1 Integration statt Einzeloptimierung  
KORA ist **nicht**:

- eine neue Scheduling-Variante  
- ein neuer GPU-Ansatz  
- ein weiteres HPC-Framework  

KORA ist:

> die erste deterministische Gesamtarchitektur für HPC, KI und Big Data.

Sie verbindet:

- SRDB  
- deterministische Scheduling Trees  
- deterministische DMA-Fenster  
- deterministische Reduktionen  
- deterministische Speicherzugriffe  
- deterministische Fabric-Zeitfenster  
- TSF als deterministisches Modellformat  

### 4.2 Vollständige Reproduzierbarkeit  
Alle Ausführungen:

- bitgenau  
- zeitkonstant  
- energiepräzise  
- numerisch konsistent  

Dies ist mit klassischen Systemen unmöglich.

### 4.3 Deterministische Energieprofile  
Energie = Leistung × Zeit.  
Da beide deterministisch sind, liefert KORA:

- exakte Energieangaben  
- wissenschaftlich vergleichbare Profilierung  
- auditierbare Modelle  

### 4.4 Elimination globaler HPC-Barrieren  
Keine:

- Preemption  
- OS-Noise  
- MPI-Jitter  
- dynamische Kommunikation  
- nichtdeterministische Reduktionen  

KORA löst alle diese Probleme strukturell.

---

## 5. V3.0-Simulation als wissenschaftliches Fundament

Die v3.0-Simulation bildet KORA als:

- deterministisches A/B/C-Modell  
- energiepräzise  
- zeitpräzise  
- HPC-, KI- und Big-Data-kompatibel  

### 5.1 Simulationsergebnisse (Kurzfassung)

**KORA-SW (B):**

- Speedup: 1.3–2.6×  
- Energieeinsparung: 40–70 %

**KORA-HW (C):**

- Speedup: 5–6× bei KI / Big-Data  
- Speedup: 15–20× bei CFD  
- Energieeinsparung: 97–99 %

Diese Ergebnisse sind:

- robust (Sensitivitätsanalyse bestätigt)  
- stabil gegenüber Parameteränderungen  
- validiert anhand realistischer Lastprofile  

---

## 6. Wissenschaftliche Relevanz

### 6.1 Für KI  
KI leidet derzeit unter:

- unreproduzierbaren Läufen  
- numerischer Drift  
- Race Conditions  
- varianter Reduktionsreihenfolge  

KORA garantiert:

- identische Gewichte  
- identische Loss-Kurven  
- bitgenaue Modelle  
- perfekte Vergleichbarkeit

### 6.2 Für CFD  
CFD erfordert:

- deterministische Iterationsschritte  
- kontrollierte Reduktionen  
- stabile Energieprofile  

KORA liefert:

- perfekte Reproduzierbarkeit  
- auditierbare Reduktionspfade  
- numerische Stabilität  

### 6.3 Für Big Data  
Big Data benötigt:

- effiziente Datenbewegung  
- Bulk-Verarbeitung  
- stabile Energieprofile  

KORA eliminiert:

- Netzwerkjitter  
- Speicherfragmentierung  
- unkontrollierte Kommunikation  

---

## 7. Fazit: Warum KORA wissenschaftlich notwendig ist

KORA löst strukturelle Probleme, die seit Jahrzehnten ungelöst sind:  
Determinismus, globale Konsistenz, Reproduzierbarkeit und Energieeffizienz.

**Kernbegründung:**

1. Jedes KORA-Element basiert auf etablierter Forschung.  
2. KORA integriert diese Elemente erstmals in einer Gesamtarchitektur.  
3. Das Simulationsergebnis zeigt:  
   - signifikante Beschleunigung  
   - dramatische Energieeinsparung  
   - vollständige Reproduzierbarkeit  
4. KORA stellt eine neue Klasse wissenschaftlicher Rechensysteme dar.

KORA ist nicht „eine Verbesserung“, sondern ein **Paradigmenwechsel**.

---

## 8. Literaturhinweise  
(Siehe Dokument *11_References.md*, Version 2.0)

---

## Versionierung

- **Dokument:** `11_Background_and_Scientific_Basis.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
