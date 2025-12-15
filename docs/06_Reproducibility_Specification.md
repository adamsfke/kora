# KORA - Reproducibility Specification  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Wissenschaftliche Spezifikation – deterministische Reproduzierbarkeit in KORA
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Einleitung
    2.  Motivation: Die Reproduzierbarkeitskrise der Wissenschaft
    3.  Definition: Was bedeutet Reproduzierbarkeit in KORA?
    4.  Reproduzierbarkeitsprofile der KORA-Architekturen
    5.  KORA Reproducibility Model (KRM)
    6.  TSF: Der Reproduzierbarkeitsvertrag
    7.  Golden Runs
    8.  Checksums, Hashes und FP-Stabilität
    9.  Reproduzierbarkeitsmetriken
    10. Failure Modes
    11. Validation Procedures
    12. Reproducibility Reports
    13. Scientific Audit Mode
    14. Deterministic Debugging
    15. Multi-System Reproduzierbarkeit
    16. Cross-Generation Stability
    17. Architekturebenen der Reproduzierbarkeit
    18. Interoperabilität und Reproduzierbarkeit
    19. Dokumentations- und Archivierungspflichten
    20. Sicherheitsaspekte
    21. Empfehlungen für Reproduzierbarkeitsrichtlinien
    22. Schlussfolgerung
    23. Glossar

---

## 1. Einleitung

Reproduzierbarkeit ist das fundamentale wissenschaftliche Prinzip hinter KORA.  
Während traditionelle HPC- und GPU-Systeme auf hoher Parallelität, dynamischem Scheduling und 
nichtdeterministischen Ausführungsmustern beruhen, definiert KORA einen vollkommen neuen Ansatz: 
wissenschaftliche Erkenntnisse müssen nicht nur schnell, sondern exakt reproduzierbar sein.

Die Reproduzierbarkeitslogik von KORA ist vollständig architekturzentriert.  
Sie ergibt sich aus der Eliminierung nichtdeterministischer Systemzustände und wird durch deterministische 
Software- und Hardwarekomponenten garantiert. Diese Spezifikation beschreibt:

    die Definition wissenschaftlicher Reproduzierbarkeit  
    die Reproduzierbarkeitsebenen der KORA-Architekturen A/B/C  
    deterministische Ausführungspfade in KORA-2  
    TSF als Reproduzierbarkeitsvertrag  
    das KORA Reproducibility Model (KRM)  
    Golden Runs, Checksums und FP-Driftmodelle  
    Validierungs- und Auditmechanismen  
    Failure Modes und Sicherheitsmechanismen  

Dieses Dokument ist ein Pflichtbaustein der KORA-Version 2.0 und dient als Referenz für wissenschaftliche 
Peer Reviews, OSF-Veröffentlichungen, auditorische Prüfungen sowie regulatorische Nutzung (z. B. Medizin, Klima, Verkehr).

---

## 2. Motivation: Die Reproduzierbarkeitskrise der Wissenschaft

In modernen HPC- und KI-Systemen besteht ein grundlegendes Problem:  
Identische Modelle liefern unter identischen Umständen unterschiedliche Ergebnisse.  
Dies ist kein Softwarefehler, sondern eine Architekturkonsequenz.

Ursachen:
    Thread-Variabilität  
    dynamischer Kernel-Dispatch  
    nichtdeterministische Reduktionen  
    Cache-Kohärenzvariabilität  
    Netzwerk- und PCIe-Jitter  
    variable DMA-Fenster  
    adaptives Taktverhalten (DVFS)  

Konsequenzen:
    wissenschaftliche Modelle sind nicht stabil  
    Ergebnisse lassen sich nicht verifizieren  
    Paper lassen sich nicht reproduzieren  
    Debugging wird immer schwieriger  
    KI verliert regulatorisch an Akzeptanz  

KORA bricht dieses Paradigma:  
Es ersetzt dynamische, nichtdeterministische Systeme durch deterministische Architekturen, 
die Ergebnisse bitgenau wiederholbar machen.

---

## 3. Definition: Was bedeutet Reproduzierbarkeit in KORA?

KORA definiert Reproduzierbarkeit auf mehreren Ebenen.  
Die klassische Definition „identische Inputs → identische Outputs“ ist unzureichend, 
da viele Systeme scheinbar deterministisch sind, aber intern variieren.

KORA definiert Reproduzierbarkeit als:

    Ein Modell liefert bitidentische Ergebnisse,
    unabhängig von:
        Hardware,
        Auslastung,
        Thread-Zuständen,
        Betriebssystem,
        Reihenfolge der Operationen,
        Scheduling,
        DMA-Fenstern,
        Cache-Zuständen,
        zeitabhängigen Effekten.

Reproduzierbarkeit ist also nicht das Ergebnis von Softwarekontrolle,  
sondern eine Eigenschaft der **Architektur**.

### 3.1 Vier Ebenen der Reproduzierbarkeit

KORA unterscheidet vier Ebenen:

#### Ebene 1 — Ergebnisreproduzierbarkeit  
Das Endergebnis ist identisch.

#### Ebene 2 — Sequenzreproduzierbarkeit  
Alle Zwischenergebnisse sind identisch.

#### Ebene 3 — Pfadreproduzierbarkeit  
Alle internen Operationen werden in identischer Reihenfolge ausgeführt.

#### Ebene 4 — Bitreproduzierbarkeit (höchste Stufe)  
Jeder Schritt, jede Operation, jedes Speicherbyte ist identisch.

KORA strebt Ebene 4 an.

### 3.2 FP-Drift vs. deterministische FP-Pipelines

In GPU-Systemen kann FP-Differenzierung im Bereich von:

    ±0.1–1.4 %

auftreten, abhängig von Reihenfolgen, Threads, Reduktionen oder Kernelparametern.

In KORA-2:

    ±0.005–0.02 %

Durch deterministische Sequenzen und Reduktionsbäume.

In KORA-Hardware:

    0.000 %

Durch deterministische FP-Pipelines und SRDB.

---

## 4. Reproduzierbarkeitsprofile der KORA-Architekturen

KORA definiert drei Architekturprofile:

    A — HPC/GPU (baseline)  
    B — KORA-SW (Software deterministisch)  
    C — KORA-HW (Hardware deterministisch)  

### 4.1 Architektur A (HPC/GPU)

Nichtdeterministisch aufgrund von:

    Warp-Divergenz  
    OS-Scheduling  
    konkurrierenden DMA-Fenstern  
    Floating-Point-Ladder-Effekten  
    Cache-Invalidierungen  

Reproduzierbarkeit:
    ±0.2–1.4 % Variabilität

### 4.2 Architektur B (KORA-SW)

Reduziert Variabilität durch:

    deterministische Scheduling Trees  
    deterministische Speicheradressen  
    deterministische Reduktionen  
    feste Execution-Windows  
    deaktivierte DVFS-Routen  
    synchrone Transferpfade  

Reproduzierbarkeit:
    ±0.005–0.02 % Variabilität

### 4.3 Architektur C (KORA-HW)

Eliminiert Variabilität durch:

    keine Interrupts  
    keine Caches  
    keine dynamischen Threads  
    keine variablen DMA-Fenster  
    deterministische Hardware-Fabric  
    deterministische FP-Pipeline  

Reproduzierbarkeit:
    0.000 % — bitidentisch

---

## 5. KORA Reproducibility Model (KRM)

Das KORA Reproducibility Model (KRM) ist das zentrale mathematische Modell,  
das Reproduzierbarkeit aus Architekturparametern ableitet.

KRM modelliert Reproduzierbarkeit als Funktion der Overheads:

R_var = g(T_sync, T_sched, T_irq, T_bus, T_cs)

Interpretation:

    wenn Overheads existieren → Varianz existiert  
    wenn Overheads stabil sind → Varianz ist klein  
    wenn Overheads eliminiert sind → Varianz ist 0  

Damit ist Reproduzierbarkeit nicht empirisch, sondern logisch bestimmbar.

### 5.1 KRM-Parameter

KRM verwendet drei Kernparameter:

    structural variance (σ_structural)  
    execution variance (σ_exec)  
    FP variance (σ_fp)  

σ_total = σ_structural + σ_exec + σ_fp

KORA-HW → alle σ = 0.

### 5.2 Reproduzierbarkeitsgrenzen

Für wissenschaftliche Nutzung definiert KORA:

    σ_total ≤ 0.02 %   (Software Minimum)  
    σ_total = 0.00 %   (Hardware Minimum)  

KRM beschreibt, wie diese Grenzen erreicht und kontrolliert werden.

---

## 6. TSF: Der Reproduzierbarkeitsvertrag

TSF ist der Kernmechanismus, der Reproduzierbarkeit garantiert.  
Eine TSF-Datei beschreibt:

    alle Operationen  
    alle Speicheradressen  
    alle Datenbewegungen  
    alle Reduktionen  
    alle Kontrollflüsse  
    alle FP-Pfade  
    alle Synchronisationen  
    alle Scheduling-Punkte  

TSF ist daher ein **Reproduzierbarkeitsvertrag zwischen Modell und Maschine**.

### 6.1 Warum TSF Reproduzierbarkeit garantiert

Ohne TSF:  
    Modell beschreibt nur „was“, nicht „wie“.

Mit TSF:  
    Modell beschreibt „was“, „wie“, „wann“, „wo“, „in welcher Reihenfolge“.

TSF ist vollständig deterministisch.

### 6.2 TSF-Hashing

Der TSF-Header enthält:

    model_hash  
    tsf_hash  
    sequence_hash  
    fp_hash  

Damit kann ein vollständiger Golden Run validiert werden.

---

## 7. Golden Runs

Ein Golden Run ist:

    eine vollständige deterministische Referenzausführung  
    die Grundlage für alle Vergleiche  
    der wissenschaftliche Prüfstein  

Ein Golden Run erzeugt:

    Checksums pro Operation  
    zeitliche Sequenzdaten  
    Speicherprüfsummen  
    Reduktionspfadprüfungen  
    FP-Verifikationen  

Golden Runs können getauscht und auf beliebigen Maschinen geprüft werden.

### 7.1 Golden Run Format

Struktur:

    golden_run/
        steps/
            000001.chk
            000002.chk
        summary.txt
        tsf_hash.txt
        fp_consistency.txt

### 7.2 Golden Run Validation

Eine Validierung ist erfolgreich, wenn:

    alle Checksums identisch sind  
    alle FP-Werte identisch sind  
    alle Speicherbereiche identisch sind  

Golden Runs sind OSF-kompatibel und können archiviert werden.

---

## 8. Checksums, Hashes und FP-Stabilität

Checksums sind die technische Grundlage für Reproduzierbarkeitsprüfungen.  
KORA nutzt ein mehrstufiges Prüfsystem, das sicherstellt, dass nicht nur Ergebnisse,  
sondern auch intern ausgeführte Operationen bitidentisch sind.

### 8.1 Operation Checksums

Jede primitive Operation erzeugt eine Prüfsumme:

    checksum = hash(op_type, inputs, outputs, fp_state)

Diese Prüfsumme wird gespeichert und im Golden Run validiert.

Beispiel:

    step=1287 op=matmul checksum=0x8a3b11ffb2

Operation Checksums garantieren Sequenzreproduzierbarkeit (Ebene 2).

### 8.2 State Checksums

Am Ende jedes Steps wird ein vollständiger Speicherhash erzeugt:

    state_hash = hash(memory_region_state)

Hashbereiche:

    aktivierungen  
    gewichtsspeicher  
    gradientspeicher  
    temporärpuffer  

State Checksums garantieren Pfadreproduzierbarkeit (Ebene 3).

### 8.3 FP-Stabilitätsprüfungen

KORA-2 erzwingt deterministische FP-Reihenfolgen.  
Daher wird FP-Stabilität explizit geprüft:

    fp_hash = hash(fp_sequence)

Hiermit wird sichergestellt, dass:

    alle Additionen  
    alle Multiplikationen  
    alle Reduktionen  

in identischer Reihenfolge stattfinden.

FP-Stabilität ist das Fundament der bitgenauen Reproduzierbarkeit.

### 8.4 TSF-spezifische Hashes

Der TSF-Header enthält vier Hash-Werte:

    model_hash
    tsf_hash
    sequence_hash
    fp_hash

Wenn zwei TSF-Dateien denselben tsf_hash besitzen, sind sie funktional identisch.

### 8.5 Vergleichslogik (Judge-Modul)

Das Validation Layer beinhaltet ein „Judge“-Modul:

    if checksum_ref != checksum_run:
        report_error(step, op)

    if fp_hash_ref != fp_hash_run:
        report_error("FP drift detected")

Dadurch wird jeder Drift sofort sichtbar.

---

## 9. Reproduzierbarkeitsmetriken

KORA definiert ein eigenständiges Metriksystem zur Evaluation von Reproduzierbarkeit.

Es umfasst vier Kennzahlen:

    1. δ_op   (Operation Drift)
    2. δ_fp   (Floating-Point Drift)
    3. δ_mem  (Memory Region Drift)
    4. δ_seq  (Sequenzdrift über Steps)

Alle Kennzahlen werden so definiert, dass sie bei perfekter Reproduzierbarkeit 0.0 ergeben.

### 9.1 Operation Drift (δ_op)

δ_op misst Abweichungen einzelner Operationen:

    δ_op = sum(|checksum_i - checksum_i_ref|)

KORA-HW:
    δ_op = 0

KORA-2:
    δ_op < 10^-10

HPC/GPU:
    δ_op kann > 10^3 sein (Zustandsraum groß)

### 9.2 Floating-Point Drift (δ_fp)

δ_fp misst numerische Drift:

    δ_fp = max(|fp_value - fp_value_ref|)

KORA-HW:
    δ_fp = 0

KORA-2:
    δ_fp ≤ 2e-4

HPC/GPU:
    δ_fp bis zu 1e-1  

### 9.3 Memory Drift (δ_mem)

δ_mem vergleicht Speicherbereiche:

    δ_mem = hash(mem_run) XOR hash(mem_ref)

KORA-HW und KORA-2 garantieren identische Speicherzustände.

### 9.4 Sequenz Drift (δ_seq)

δ_seq beschreibt, ob die Ausführungsreihenfolge identisch ist:

    δ_seq = 1, falls Reihenfolge abweicht
           0, falls Reihenfolge exakt ist

KORA-2 und KORA-HW garantieren δ_seq = 0.

---

## 10. Failure Modes

Deterministische Ausführung ist stark, aber nicht unfehlbar.  
KORA beschreibt alle Failure Modes explizit, damit Wissenschaftler diese erkennen und protokollieren können.

### 10.1 Failure Mode 1 — FP Drift (Software)

Kann auftreten, wenn:

    Hardware-FP-Einheiten instabil sind  
    externe Bibliotheken verwendet werden  
    Scheduling Trees falsch erzeugt wurden  

KORA-2 meldet:

    FP drift detected at step 3382

### 10.2 Failure Mode 2 — Scheduling Drift

Kann auftreten durch:

    unzulässige dynamische Operationen  
    externe Threads  
    Nicht-KORA-Code innerhalb eines KORA-Pipelineschritts  

Meldung:

    Scheduling mismatch at step 1947

### 10.3 Failure Mode 3 — Memory Drift

Typische Ursachen:

    Speicherbereich überschrieben  
    Race Condition in Fremdcode  
    nicht deterministische Alloc/Free Vorgänge  

KORA meldet:

    Memory delta != 0 at step 512

### 10.4 Failure Mode 4 — Invalid TSF

Ein TSF kann ungültig sein bei:

    unvollständigen Sequenzen  
    fehlerhaften Abhängigkeiten  
    Inkonsistenzen in Adressräumen  
    Hash-Mismatch  

Fehler:

    TSF validation failed: hash mismatch

### 10.5 Failure Mode 5 — Hardware-Layer-Drift (nur für Architektur C)

Nicht relevant für Software, aber für später:

    defekte Fabric-Lanes  
    spannungsbedingte Fehlrechnungen  
    defekte FP-Einheiten  

KORA-HW meldet:

    hardware slot deviation at tile 3

---

## 11. Validation Procedures

KORA definiert ein vollständiges Validierungsprotokoll, das von allen wissenschaftlichen 
Einrichtungen genutzt werden kann, um Modelle sicher zu validieren.

### 11.1 Pre-Run Validation

Vor der Ausführung:

    TSF.validate()
    TSF.check_hashes()
    SchedulingTree.check()
    MemoryLayout.check()

Ergebnis:

    ready_for_execution = True

### 11.2 In-Run Validation

Während der Ausführung:

    jede Operation wird gehasht  
    jede Speicherregion überwacht  
    jede Reduktion geprüft  
    jede Sequenz gegen Referenz abgeglichen  

KORA-2 führt ein Shadow-Log, das parallel zum Hauptlauf erzeugt wird.

### 11.3 Post-Run Validation

Nach der Ausführung:

    Prüfen aller checksum_files  
    Prüfen des finalen state_hash  
    Vergleich mit Golden Run  
    Erstellen eines Reproducibility Reports  

### 11.4 OSF-kompatible Validierung

Struktur:

    reproducing/
        tsf/
        golden_run/
        reports/
        drift_analysis.json

Diese Struktur wird für OSF akzeptiert und erleichtert Peer Review.

---

## 12. Reproducibility Reports

Jeder KORA-Lauf erzeugt automatisch einen Reproduzierbarkeitsbericht.

Beispiel:

    reproducibility_report:
        tsf_hash: c4f1a3bb91
        steps: 12873
        δ_op: 0
        δ_fp: 0
        δ_seq: 0
        δ_mem: 0
        status: PASS

Die Berichte enthalten zusätzlich Metadaten:

    Hardware
    KORA Version
    TSF Version
    RNG Status (sollte immer 0 sein)
    Compiler Hash
    Runtime Hash

Die Berichte sind revisionssicher.

---

## 13. Scientific Audit Mode

KORA bietet einen speziellen „Audit Mode“, der von Journalen, Universitäten und regulatorischen Institutionen genutzt werden kann.

### 13.1 Eigenschaften des Audit Modes

    extrem striktes Logging  
    zusätzliche Prüfsummen  
    detaillierte Sequenzdaten  
    strengere TSF-Prüfungen  
    Takt-Pinning  
    vollständige Ausschaltung von DVFS  
    vollständige Abschaltung von Hyperthreading  

### 13.2 Audit Mode Reports

Der Audit Mode erzeugt:

    audit_steps.json  
    audit_fp.json  
    audit_memory.json  
    audit_sequence.json  

Diese Dateien ermöglichen vollständige Nachvollziehbarkeit.

---

## 14. Deterministic Debugging

Debugging ist in KORA deterministisch.

### 14.1 Replay Debugging

    debugger.replay(step=3129)

Spielt jeden Schritt identisch ab.

### 14.2 Breakpoints

Breakpoints sind deterministisch:

    debugger.break_at(step=4000)

### 14.3 State Freeze

Der Zustand kann eingefroren werden:

    debugger.freeze(step=1200)

Dies ist bei HPC unmöglich.

---

## 15. Multi-System Reproduzierbarkeit

Ein Hauptziel von KORA ist, dass Modelle über:

    unterschiedliche Maschinen  
    unterschiedliche Hardware  
    unterschiedliche Zeitpunkte  

identisch reproduzierbar bleiben.

KORA-2 ermöglicht:

    runs on machine A identical to runs on machine B  
    runs in 2026 identisch zu runs in 2036  
    runs auf unterschiedlicher Hardware identisch  

Über TSF und deterministische Sequenzen bleibt alles konsistent.

---

## 16. Cross-Generation Stability

Ein wesentliches Ziel von KORA ist die Stabilität wissenschaftlicher Modelle über Hardwaregenerationen hinweg.  
Während klassische Systeme bei jeder neuen GPU-Generation Änderungen im Verhalten, in numerischen Details und in Speicherarchitekturen aufweisen, bleibt KORA deterministisch und generationenstabil.

### 16.1 Stabilität über Software- und Hardwareversionen

KORA garantiert:

    identische TSF-Datei → identisches Ergebnis  
    identische Ablaufsequenz → identische FP-Reihenfolge  
    identisches Speicherlayout → identische Reduktionen  

Dabei spielt keine Rolle:

    ob das Modell 2026 oder 2036 ausgeführt wird  
    ob Softwareversionen wechseln  
    ob Hardwaregenerationen wechseln  

Nur TSF bestimmt das Ergebnis.  
Nichts anderes.

### 16.2 Migrationsgarantie

Beim Übergang von KORA-2 (Software) zu KORA-HW (Architektur C) gilt:

    TSR_compatibility = True  
    FP-pipelines werden bitgenau abgebildet  
    Scheduling Trees bleiben 1:1 erhalten  
    Speicheradressen bleiben stabil  

Dies macht KORA einzigartig im Vergleich zu HPC-Systemen, bei denen Generationenwechsel Reproduzierbarkeit zerstören.

---

## 17. Architekturebenen der Reproduzierbarkeit

KORA beschreibt Reproduzierbarkeit auf drei Architekturebenen:

### 17.1 Ebene 1: Logische Ebene (TSF)

    TSF definiert Operationen, Reihenfolgen, Speicher, Reduktionen  
    Die logische Ebene ist unveränderlich  

### 17.2 Ebene 2: Softwareebene (KORA-2)

    scheduling trees  
    deterministic memory layer (DML)  
    deterministic execution layer (DEL)  
    SRDB simulation  

Die Softwareebene bildet die logische Ebene exakt ab.

### 17.3 Ebene 3: Hardwareebene (KORA-HW)

    keine Interrupts  
    keine variablen DMA-Fenster  
    kein OS  
    keine dynamische Beschleunigung  

Die Hardwareebene eliminiert alle Residualvariationen.

Diese drei Ebenen erzeugen zusammen ein vollständig deterministisches Ökosystem.

---

## 18. Interoperabilität und Reproduzierbarkeit

KORA erlaubt Interoperabilität auf zwei Arten:

### 18.1 Interoperabilität zwischen Maschinen

Jede Maschine, die TSF ausführt — egal ob HPC, KORA-2 oder KORA-HW — liefert identische Ergebnisse.  
Dies ist ein revolutionärer Unterschied zu heutigen Systemen.

### 18.2 Interoperabilität zwischen Versionen

Solange:

    tsf_hash identisch  
    sequence_hash identisch  

ist, bleibt das Modell reproduzierbar.

### 18.3 Interoperabilität zwischen Forschungsgruppen

Forschungsteams können TSF-Dateien austauschen:

    Institut A generiert TSF  
    Institut B führt TSF aus  
    Ergebnisse sind identisch  

Dies schafft eine neue Grundlage für wissenschaftliche Zusammenarbeit.

---

## 19. Dokumentations- und Archivierungspflichten

KORA empfiehlt — und für regulatorische Anwendungen fordert — klare Archivierungsrichtlinien.

### 19.1 Pflichtartefakte

Folgende Artefakte müssen archiviert werden:

    TSF-Datei  
    Golden Run  
    Reproducibility Report  
    Systemkonfiguration  
    KORA-Version  
    FP-Konfiguration  

### 19.2 Aufbewahrungsdauer

Für wissenschaftliche Arbeiten:

    mindestens 10 Jahre

Für regulatorische Berichte (z. B. Medizin, Verkehr):

    mindestens 25 Jahre

### 19.3 Archivformat

OSF, Zenodo oder ein institutseigenes Archiv.

---

## 20. Sicherheitsaspekte

Reproduzierbarkeit ist nicht nur eine wissenschaftliche Anforderung — sie ist auch ein Sicherheitsmechanismus.

### 20.1 Tamper Resistance

Jede Abweichung im Modell führt zu:

    hash mismatch  
    sequence mismatch  
    memory mismatch  

Die kleinste Manipulation wird sichtbar.

### 20.2 Trusted Execution (Architektur C)

Da KORA-HW ohne OS, Interrupts, DMA-Variabilität und dynamischen Scheduler arbeitet, ist sie inhärent sicher:

    keine Rootkits  
    keine Scheduling-Angriffe  
    keine Drift-Angriffe  
    keine Speicherrennen  

### 20.3 Revision Safety

Alle Ergebnisse sind reproduzierbar, messbar, belegbar.

---

## 21. Empfehlungen für Reproduzierbarkeitsrichtlinien

KORA empfiehlt Forschungsinstituten folgende Standards:

### 21.1 Mindestanforderungen

    deterministische Modelle  
    Nutzung von TSF  
    Golden Run vor Veröffentlichung  
    Reproducibility Report veröffentlichen  
    Speicher- und Sequenzhashes archivieren  

### 21.2 Erweiterte Anforderungen

    Audit Mode  
    sequentielle Prüfsummen  
    FP-Stabilität über alle Schichten  
    archivierte TSF sowie ISR  

### 21.3 Regulatorische Anforderungen

Für medizinische oder sicherheitskritische KI:

    Audit Mode Pflicht  
    Hash-basierte FP-Stabilitätsprüfung  
    vollständiges Scheduling Logging  
    Speicherung aller Golden Runs  

---

## 22. Schlussfolgerung

Diese Spezifikation beschreibt die vollständige Reproduzierbarkeitslogik des KORA-Projekts in Version 2.0.  
Sie definiert:

    Reproduzierbarkeitsbegriffe  
    Reproduzierbarkeitsmetriken  
    deterministische Softwaremechanismen  
    deterministische Hardwaremechanismen  
    TSF als Reproduzierbarkeitsvertrag  
    Validierungsmechanismen  
    Auditverfahren  
    Sicherheitsaspekte  

KORA macht wissenschaftliche Modelle langfristig stabil, bitgenau reproduzierbar und auditierbar.  
Damit bildet KORA die Grundlage einer neuen Klasse wissenschaftlicher Rechenarchitekturen:  
kohärent, deterministisch und strukturell zuverlässig.

---

## 23. Glossar

Bitreproduzierbarkeit  
    höchste Form der Reproduzierbarkeit, bei der jedes Bit identisch ist.

Deterministische DMA-Fenster  
    feste Zeitfenster mit identischen Übertragungsparametern.

Golden Run  
    vollständige deterministische Referenzausführung zur Validierung.

KRM  
    KORA Reproducibility Model.

Scheduling Tree  
    deterministische Struktur der gesamten Ausführung.

Sequenzdrift  
    Abweichung der Ausführungsreihenfolge.

TSF  
    Tensor Sequence Format, deterministisches Ausführungsformat.

State Drift  
    Abweichung in Speicherbereichen einer Ausführung.

---

## Versionierung

- **Dokument:** `06_Reproducibility_Specification.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
