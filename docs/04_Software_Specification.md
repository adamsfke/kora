# KORA – Software Specification


**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0
**Dokumenttyp:** Laufzeit- und Compiler-Spezifikation für KORA-2(SW)
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1.  Einleitung
    2.  Ziele und Prinzipien von KORA-2
    3.  Architektur von KORA-2
    4.  Compilerarchitektur
    5.  Daten- und Speicherlayout
    6.  Scheduling Trees
    7.  Deterministic Execution Layer (DEL)
    8.  SRDB Scheduler (Software-Emulation)
    9  TSF (Tensor Sequence Format)
    10. Validation Layer
    11. Monitoring Layer
    12. Schnittstellen
    13. Kompatibilität mit KORA-Hardware (Architektur C)
    14. Zusammenfassung

---

## 1. Einleitung

Diese Software-Spezifikation beschreibt KORA-2 — die deterministische Softwareebene der KORA-Architektur. 
Während die Hardware-Spezifikation (03) die monolithische Struktur der Architektur C definiert, stellt KORA-2 die erste vollständige Software-Umsetzung der deterministischen Prinzipien auf Standard-Hardware dar.

KORA-2 ist kein klassisches Runtime-System, keine Bibliothek und kein HPC-Framework.  
Es ist ein kohärenzorientiertes Betriebskonzept, das deterministische Ausführung auf nichtdeterministischer 
Hardware ermöglicht. Die Software bildet die Überbrückungsschicht zwischen existierenden HPC-Systemen und 
der geplanten KORA-Hardware (Architektur C).

Diese Spezifikation legt fest:

    den Aufbau des KORA-2 Software-Stacks  
    seine deterministischen Prinzipien  
    die Komponenten Scheduling Trees, TSF, SRDB-Scheduler  
    deterministische DMA-Emulation auf Standard-Hardware  
    die Compiler- und IR-Strukturen  
    die Validierungs- und Monitoring-Schichten  
    die Schnittstellen für Anwender und Forschungssoftware  

Im Gegensatz zu klassischen HPC-Runtimes dient KORA-2 nicht der Parallelisierung, sondern der Stabilisierung. 
Alle Abläufe sind deterministisch, vorhersehbar und unabhängig von OS-Scheduling, Hintergrundlast und GPU/CPU-Variabilitäten.

Version 2.0 dieses Dokuments definiert die vollständige Software-Spezifikation für OSF, wissenschaftliche Auditoren und zukünftige Hardwareentwicklung.

---

## 2. Ziele und Prinzipien von KORA-2

KORA-2 wurde mit vier fundamentalen Zielen entwickelt:

### 2.1 Ziel 1 — Determinismus auf Standard-Hardware

KORA-2 garantiert deterministische Ausführung auch auf Plattformen, die dafür nicht ausgelegt sind. Dies umfasst:

    deterministische Scheduling Trees  
    deterministische Datenpfade  
    deterministische Batch- und Shard-Sequenzen  
    deterministische Speicheroperationen  
    deterministische FP-Reihenfolgen  

KORA-2 ist der Übergangschritt von klassischem HPC zu KORA-Hardware.  
Es reduziert Varianz von ±0.2–1.4 % (HPC) auf ±0.005–0.02 %.

### 2.2 Ziel 2 — Eliminierung von Software-Jitter

HPC-Runtimes erzeugen:

    variablen Thread-Austausch  
    variable Kernel-Dispatch  
    instabile DMA-Fenster  
    unvorhersehbare Reduktionsreihenfolgen  

KORA-2 eliminiert diese Quellen vollständig durch:

    statische Zeitfenster  
    deterministische Reduktionen  
    vorgeplante Datenflüsse  
    blockierende Synchronisationspunkte ohne Jitter  
    statische Ausführungspläne  

### 2.3 Ziel 3 — Reproduzierbarkeit und Auditierbarkeit

KORA-2 führt ein System ein, das exact spezifiziert:

    wann welche Operation ausgeführt wurde  
    wann welcher Speicherbereich genutzt wurde  
    wann welche Synchronisation stattfand  

Die TSF-Datei beschreibt jeden einzelnen Schritt.  
Dies ermöglicht:

    vollständiges Debugging  
    bitnahe Reproduktion  
    Auditprüfungen  

### 2.4 Ziel 4 — Kompatibilität mit KORA-Hardware (Architektur C)

KORA-2 bildet die Hardwarearchitektur vollständig logisch ab:

    Scheduling Trees       → Hardware-Scheduling  
    deterministische DMA   → Hardware-Fabric Slots  
    SRDB Memory Mapping    → SRDB On-Die  
    TSF                    → Tensor Sequencing Engine  

Software und Hardware teilen dasselbe Modell.  
KORA-2 ist somit die Vorstufe der KORA-Hardware.

---

## 3. Architektur von KORA-2

KORA-2 folgt einer streng modularen Softwarearchitektur.  
Die Architektur besteht aus sieben deterministischen Schichten:

    1. KORA-2 Core Runtime  
    2. Scheduling Tree Engine (STE)  
    3. Deterministic Memory Layer (DML)  
    4. Deterministic Execution Layer (DEL)  
    5. SRDB Scheduler (Software-Emulation)  
    6. TSF Compiler & Loader  
    7. Validation & Monitoring Layer  

Jede Schicht ist deterministisch und unveränderlich.  
Keine Komponente besitzt Autonomie.  
Alle Abläufe werden durch statische Sequenzen festgelegt.

### 3.1 Schicht 1 — KORA-2 Core Runtime

Die Core Runtime stellt die Basiskomponenten:

    Initialisierung des Datenraums  
    Laden von Modellen und Workloads  
    Erstellung globaler Kontexte  
    deterministische Ausführungsschleifen  
    Verwaltung von Iterationen, Steps und Epochs  

Die Runtime beinhaltet keinerlei:

    dynamisches Scheduling  
    asynchrone Operationen  
    thread-interne Autonomie  

Beispiel (vereinfacht):

    KORA.init()
    KORA.load_model("mod.ts")
    for epoch in E:
        KORA.run_step(epoch)

Alle Entscheidungen werden zu Laufzeit 0 getroffen.

### 3.2 Schicht 2 — Scheduling Tree Engine (STE)

STE ist das Kernstück von KORA-2.

Ein Scheduling Tree definiert:

    die Reihenfolge aller Operationen  
    die Reihenfolge aller Datenbewegungen  
    die Reihenfolge aller Reduktionen  
    die Reihenfolge aller FP-Operationen  

Der Scheduling Tree ersetzt vollständig:

    OS Scheduling  
    GPU-Scheduling  
    CUDA Streams  
    Thread Pools  
    dynamische Kernel-Optimierung  

Scheduling Trees werden deterministisch erzeugt durch:

    Workloadanalyse  
    datenflussbasierte Abhängigkeiten  
    statische Sharding-Regeln  
    deterministische FP-Reduktionen  

Beispielstruktur:

    Root
        ├─ Load Input Batch
        ├─ Forward Block 1
        │     ├─ Linear 1
        │     └─ Activation
        ├─ Attention Heads
        ├─ Backprop
        └─ Update

Jeder Knoten ist eindeutig adressierbar und reproduzierbar.

### 3.3 Schicht 3 — Deterministic Memory Layer (DML)

DML ist die Software-Emulation des SRDB.  
Zweck:

    deterministische Speicheradressen  
    deterministische Blockgrößen  
    deterministische DMA-Zeitfenster  

DML garantiert:

    keine dynamischen Alloc/Free  
    keine Heap-Variabilität  
    keine Zufallspfadverläufe  
    konstante Latenzen  

Alle Speicherbereiche werden beim Start statisch reserviert.

Beispiel:

    DML.reserve("model_weights", 4GB)
    DML.reserve("workspace", 1GB)
    ptr = DML.address("model_weights")

### 3.4 Schicht 4 — Deterministic Execution Layer (DEL)

DEL ist die deterministische Pipeline der FP-Berechnung.  
Sie garantiert:

    deterministische Sequenzierung  
    deterministische SIMD-Ausführung  
    deterministische Reduktionsbäume  
    Fixierung aller Rechenpfade  

Das Ziel ist nicht maximale Performance, sondern maximale Stabilität.

Beispiel (schematisch):

    DEL.execute_linear(W, x):
        y = 0
        for i in range(N):
            y += W[i] * x[i]
        return y

Kein Parallelismus, kein dynamisches Unrolling, keine Vektorisierungsüberraschungen.  
Parallelismus wird durch Scheduling Trees, nicht durch Autonomie erzeugt.

### 3.5 Schicht 5 — SRDB Scheduler (Software-Emulation)

KORA-2 emuliert SRDB auf Standard-Hardware:

    globale synchronisierte Zugriffe  
    feste Zeitfenster  
    deterministische Reihenfolgen  
    keine konkurrierenden Schreibvorgänge  
    keine race conditions  

Dies ist der wichtigste Schritt zu deterministischer Ausführung auf nichtdeterministischer Hardware.

Beispiel:

    SRDB.lock("W_q")
    SRDB.write(ptr_Wq, data)
    SRDB.unlock("W_q")

### 3.6 Schicht 6 — TSF Compiler & Loader

TSF (Tensor Sequence Format) definiert:

    den vollständigen, deterministischen Ausführungsplan  
    alle Operationen  
    alle Datenbewegungen  
    alle Speicheradressen  
    alle Reduktionsschritte  
    den globalen Ablauf  

TSF ist die deterministische Repräsentation eines Modells.

Compilerpfad:

    Model → HAPI → ISR → TSF → Execution

Loaderpfad:

    TSF.load("model.tsf")
    TSF.validate()
    TSF.run()

### 3.7 Schicht 7 — Validation & Monitoring

Diese Schicht bietet:

    Reproduzierbarkeitsprüfungen  
    deterministische Logging-Formate  
    Profiling ohne Jitter  
    Messung von Steps und FP-Sequenzen  

Dies ist der Schlüssel für Auditierbarkeit.

---

## 4. Compilerarchitektur

KORA-2 verwendet einen vollständig deterministischen Compiler-Stack.  
Der Compiler ist nicht vorrangig für Optimierungen zuständig, sondern für die Erstellung eines stabilen, überprüfbaren und unveränderlichen Ausführungsplans.

Die Compilerarchitektur besteht aus vier Stufen:

    1. HAPI Frontend (High-Level API)
    2. ISR (Intermediate Stable Representation)
    3. TSF Compiler (deterministische Sequenzierung)
    4. TSF Validator & Loader

Jede Stufe eliminiert Variabilität.

### 4.1 HAPI — High-Level API

HAPI ist die Benutzerschnittstelle für Wissenschaftler, Entwickler und Datenforschende.

HAPI definiert:
    Modelle  
    Operatoren  
    Layer  
    Konfigurationen  

Beispiel:

    model = HAPI.Sequential(
        HAPI.Linear(1024, 4096),
        HAPI.Activation("gelu"),
        HAPI.Linear(4096, 1024)
    )

Wichtig:
    HAPI enthält keinerlei dynamische Elemente.  
    Keine Random Seeds.  
    Keine dynamischen Shapes.  
    Keine variablen Operatorpfade.

HAPI dient als deterministisches Eingangstor zum Compiler.

### 4.2 ISR — Intermediate Stable Representation

ISR ist das interne Modellformat.  
Es ist stabil, vollständig deterministisch und unveränderlich.

ISR definiert:

    graphstruktur  
    operatorreihenfolge  
    feste shapes  
    feste strides  
    feste FP-Pfade  
    feste numerische Reduktionsbäume  

ISR ist nicht IR wie bei klassischen Compilern, sondern eine streng deterministische Repräsentation.

Beispiel (schematisch):

    ISR:
        op1: linear(mat_w1, mat_b1)
        op2: gelu()
        op3: linear(mat_w2, mat_b2)

ISR enthält keinen Spielraum. Kein Scheduling, keine Variabilität.

### 4.3 TSF Compiler

Der TSF Compiler erzeugt aus ISR eine vollständige deterministische Sequenz.

TSF = Tensor Sequence Format  
TSF enthält:

    die globale Reihenfolge aller Operationen  
    alle Speicheradressen  
    alle Datenbewegungen  
    alle Reduktionen  
    alle Scheduling-Knoten  
    alle Lese-/Schreiboperationen  
    alle FP-Sequenzen  
    alle Kontrollflüsse  

TSF ist eine reine Ablaufbeschreibung, ohne jede Optimierung.

Struktur:

    tsf_header:
        version
        model_hash
        date_created
        tile_count
        memory_layout

    tsf_body:
        step_0:
            load_batch
            op1_linear
            op1_reduce
            op1_store
            op2_gelu
        step_1:
            ...
        step_N:
            ...

TSF bildet die Grundlage jeder deterministischen Ausführung.

### 4.4 TSF Validator & Loader

Vor jeder Ausführung prüft der Validator:

    Vollständigkeit  
    deterministische Sequenzen  
    Adresskonsistenz  
    Reduktionsbäume  
    Abhängigkeiten  
    Speicherzuordnungen  

Erst danach wird der TSF-Plan geladen:

    tsf = TSF.load("model.tsf")
    tsf.validate()
    runtime.execute(tsf)

Der Loader erzeugt keinen Code — er erzeugt ausschließlich deterministische Ausführung.

---

## 5. Daten- und Speicherlayout

Speicher ist eine der Hauptquellen für Variabilität in HPC-Systemen.  
KORA-2 löst dieses Problem vollständig durch ein starres, deterministisches Speicherlayout.

### 5.1 Globale Speicherreservierung

Zu Laufzeit 0 werden alle Speicherbereiche reserviert:

    model_weights  
    batch_inputs  
    activations  
    gradients  
    workspace  
    temporary_buffers  

Beispiel:

    DML.reserve("activations", 512MB)
    DML.reserve("workspace", 1024MB)

Dynamische Speicherzuweisung ist verboten.

### 5.2 Adressstabilität

Jeder Tensor erhält eine feste Adresse.  
Diese Adresse wird nie verändert.

Beispiel (schematisch):

    ptr_W1 = 0x0000_1000_0000
    ptr_W2 = 0x0000_1400_0000
    ptr_Act = 0x0000_1800_0000

Keinerlei Heap- oder Stackvariabilität.

### 5.3 Deterministische Blockgrößen

Jeder Speicherblock besitzt feste:

    Größe  
    Ausrichtung  
    Stride  
    Layoutparameter  

Diese Werte sind Teil des TSF-Headers.

### 5.4 Datenbewegungen (DMA-Emulation)

Die DML-Schicht implementiert deterministische „Pseudo-DMA“-Fenster:

    DML.copy(src, dst, size, window_id)

window_id garantiert:
    identische Reihenfolge  
    identische Latenz  
    identische Wartezeiten  

Auf Standard-Hardware wird diese deterministische DMA-Schicht über synchrone Software-Pipelines realisiert.

### 5.5 Speicherzugriffsmuster

Alle Speicherzugriffe folgen festen Regeln:

    keine Cache-abhängige Optimierung  
    keine Lazy-Operationen  
    keine dynamischen Prefetches  
    keine Autotuning-Operationen  

Dies stabilisiert FP-Ausführung und reduziert Variabilität um bis zu 95 %.

---

## 6. Scheduling Trees

Scheduling Trees sind das Herzstück von KORA-2.  
Sie definieren die gesamte Ausführung global, deterministisch und vollständig statisch.

### 6.1 Struktur eines Scheduling Trees

Ein Scheduling Tree besteht aus:

    Root Node  
    Branch Nodes (Operationen)  
    Leaf Nodes (primitive FP-Operationen)  

Beispiel:

    Root
        ├─ ForwardPass
        │     ├─ Block1
        │     ├─ Block2
        │     └─ Block3
        ├─ BackwardPass
        └─ Update

Jeder Knoten besitzt:

    einen eindeutigen Hash  
    eine statische Position  
    eine deterministische Reihenfolge  

### 6.2 Warum Scheduling Trees deterministisch sind

Sie ersetzen:

    OS-Scheduler  
    GPU-Kernel-Dispatch  
    Thread Synchronisation  
    dynamische Abhängigkeitsanalyse  
    Optimierer  

Alle Variabilität wird eliminiert:

    keine Rennen  
    keine Thread-Wechsel  
    keine Timing-Divergenzen  
    kein Out-of-Order  

### 6.3 Erstellung eines Scheduling Trees

Der Scheduling Tree wird zur Kompilierzeit erzeugt:

    tree = STE.generate(ISR_graph)

Algorithmen:

    topologische Sortierung  
    deterministische Abhängigkeitsanalyse  
    deterministische Reduktionsplaner  
    deterministische Speicherplanung  
    deterministischer FP-Pfadbauer  

### 6.4 Tile-Integration

Unter KORA-Hardware:

    jeder Tile erhält einen Teilbaum  

Unter KORA-2 (Software):

    Tiles werden simuliert  
    Tile-Bereiche erhalten feste Ausführungsfenster  
    Multi-Tile-Synchronisation ist statisch  

Beispiel:

    Tree.Tile[0] → Attention Block
    Tree.Tile[1] → MLP Block

### 6.5 Synchronisationspunkte

Synchronisation ist deterministisch:

    sync_point(id):
        block_until_all_tiles_ready(id)

Dies ersetzt:

    AllReduce  
    MPI Barrier  
    GPU Streams  

---

## 7. Deterministic Execution Layer (DEL)

DEL führt die TSF-Schritte aus.  
DEL ist die ausführende Pipeline, die absolute Stabilität garantiert.

### 7.1 Eigenschaften von DEL

DEL ist:

    single-path  
    kein branching  
    keine adaptive Optimierung  
    kein Scheduling  
    keine Thread-Autonomie  

Jede Operation wird mit identischer Reihenfolge ausgeführt.

### 7.2 Primitive Operationen

Primitive Operationen sind:

    LinearOps  
    Add  
    Multiply  
    Reduce-Sum  
    MatMul  
    Gelu/Tanh/Sigmoid (deterministisch implementiert)  

Beispiel:

    DEL.matmul(A, B, C):
        for i in range(M):
            for j in range(N):
                C[i,j] = 0
                for k in range(K):
                    C[i,j] += A[i,k] * B[k,j]

Keine Vektorisierung, keine Autotuning-Optimierung, keine spekulative Ausführung.

### 7.3 Reduktionsbäume

Reduktionen folgen festen Bäumen:

    reduce(a):
        while len(a) > 1:
            a = pairwise_reduce(a)

Jede Paarbildung ist deterministisch.

### 7.4 Kontrollfluss

Kein dynamischer Kontrollfluss.  
Alle Kontrollstrukturen sind beim TSF-Export bekannt.

### 7.5 Fehlerbehandlung

DEL besitzt:

    deterministische Fehlertypen  
    deterministische Recovery-Schritte  
    deterministische Logs  

Beispiel:

    if FP_error:
        DEL.error("FP exception at step 3872")

---

## 8. SRDB Scheduler (Software-Emulation)

Der SRDB Scheduler ist die Software-Emulation des späteren Hardware-SRDB (Single Resonant Data Bus).  
Er ist verantwortlich für:

    deterministische Datenbewegungen  
    garantierte Reihenfolgen  
    feste Ausführungsfenster  
    atomare Operationen ohne Nebenwirkungen  
    deterministische Latenzen  

Auf herkömmlichen HPC-Systemen ersetzt der SRDB Scheduler:

    PCIe-Variabilität  
    nichtdeterministische GPU-Transfers  
    variable DMA-Fenster  
    konkurrierende Schreibvorgänge  

### 8.1 SRDB-Operationen

SRDB unterstützt vier primitive Operationen:

    srdb.load(ptr)
    srdb.store(ptr, data)
    srdb.copy(src, dst, size)
    srdb.sync(id)

Beispiel:

    srdb.copy(ptr_W, ptr_tmp, 64k)
    srdb.sync("update_phase")

### 8.2 Der deterministische Transfergraph

Jede SRDB-Operation ist Teil eines festen Transfergraphs.

Struktur:

    TransferGraph:
        windows: [W0, W1, W2, ...]
        each window:
            - fixed start time
            - fixed duration
            - fixed pointers

Diese Graphstruktur ist im TSF kodiert.

### 8.3 Tile-übergreifende Koordination

Im Softwaremodell erfolgt Koordination über Blocking-Sync:

    srdb.sync(id)

Tiles dürfen keine konkurrierenden Operationen durchführen.  
Dies verhindert Race Conditions vollständig.

### 8.4 Eliminierung von PCIe- und Netzwerkjitter

Alle Datenbewegungen erfolgen über:

    synchrone Kopien  
    feste Blockgrößen  
    feste Sequenzen  
    feste Wartepunkte  

Der Scheduler kompensiert dabei die Non-Deterministik der Hardware durch deterministische Taktfenster.

---

## 9. TSF (Tensor Sequence Format)

TSF ist die wichtigste Komponente der KORA-2-Spezifikation.  
TSF ist keine Datei im klassischen Sinne — TSF ist eine **vollständige deterministische Repräsentation des gesamten Trainings- bzw. Ausführungsplans**.

TSF ersetzt:

    Model Code  
    Graph IR  
    GPU Kernel Schedules  
    Optimizer-Zustände  
    dynamische Speicherverwaltung  

TSF enthält alles, was notwendig ist, um ein Modell bitidentisch auszuführen.

### 9.1 Struktur eines TSF-Dokuments

Eine TSF-Datei besteht aus:

    1. Header (Meta)
    2. Memory Layout
    3. Scheduling Tree
    4. SRDB Transfergraph
    5. Primitive Sequences
    6. Validierungsinformationen

Schematisches Beispiel:

    tsf_header:
        version: 2.0
        model_hash: c4f1a3bb...
        created: 2026-03-02
        tiles: 4
        memory_regions:
            - weights
            - activations
            - grads

    tsf_body:
        step_000001:
            load_batch
            op_linear_1
            op_gelu
            op_linear_2
            reduce_gradients
        step_000002:
            ...

### 9.2 Warum TSF deterministisch ist

TSF definiert ALLES:

    Reihenfolge  
    Speicheradressen  
    Operatorberechnung  
    Reduktionspfade  
    Synchronisation  
    globale Struktur  

Damit ist Ausführung nicht nur deterministisch — sie ist unveränderlich.

### 9.3 TSF als Austauschformat

TSF wird später auch auf KORA-Hardware genutzt:

    TSF.run_on_hardware()

Dies ermöglicht eine weltweit identische Ausführung.

---

## 10. Validation Layer

KORA-2 besitzt ein integriertes Validierungssystem zur Garantie wissenschaftlicher Reproduzierbarkeit.

### 10.1 Deterministische Logs

Jeder Schritt erzeugt identische Logs:

    log(step, op, checksum)

Beispiel:

    step=3872 op=matmul checksum=0x8a3b11

### 10.2 Referenzprüfungen

Der Validator prüft:

    TSF-Integrität  
    Speicherintegrität  
    FP-Reproduzierbarkeit  
    SRDB-Sequenzen  
    Scheduling-Bäume  

### 10.3 Reproduzierbarkeitsberichte

KORA erzeugt automatisch Berichte:

    runtime.report_reproducibility()

Inhalt:

    Abweichungen (falls vorhanden)  
    Hashes aller Schritte  
    memory delta = 0.0  
    fp drift = 0.0  

Diese Berichte können in OSF publiziert werden.

---

## 11. Monitoring Layer

Monitoring umfasst:

    Energieprofiling  
    FP-Sequenzanalyse  
    Tile-Auslastung (simuliert)  
    Speicherverbrauch  
    Taktstabilität  

### 11.1 Energieprofiling ohne Jitter

Messung:

    P(t) = constant + epsilon

Mit KORA-2 ist epsilon extrem klein, da es keine dynamischen Frequenzänderungen gibt (DVFS wird deaktiviert).

### 11.2 Profiling der Ausführungssequenz

Beispiel:

    profiler.step(1003)
    profiler.show():
        - ops: 1428
        - reductions: 37
        - memory: 51MB
        - time: 2.883ms (stable)

### 11.3 Debugging durch Sequenzkontrolle

Debugging erfolgt deterministisch:

    debugger.replay(step=3872)

Dieses Feature ist einzigartig unter HPC-Systemen.

---

## 12. Schnittstellen

KORA-2 bietet drei Hauptschnittstellen:

    1. HAPI (Modellerstellung)
    2. TSF Executor (Ausführung)
    3. ISR/TSF Tooling (Analyse und Werkzeuge)

### 12.1 HAPI API

    model = HAPI.Sequential(...)
    model.compile()
    model.export_tsf("mymodel.tsf")

### 12.2 TSF Execution API

    tsf = TSF.load("mymodel.tsf")
    KORA.execute(tsf)

### 12.3 Validation API

    KORA.validate(tsf)

---

## 13. Kompatibilität mit KORA-Hardware (Architektur C)

KORA-2 bildet die Hardware in Software nach.

### 13.1 Eins-zu-eins-Abbildung

Jede Komponente in KORA-2 hat eine spätere Hardware-Entsprechung:

    Scheduling Tree     → Hardware Scheduler  
    DML                 → SRDB Memorybank  
    SRDB Scheduler      → Fabric-Scheduler  
    DEL                 → FP-Pipeline  
    TSF                 → Hardware Execution Format  

### 13.2 Migration

Sobald Hardware verfügbar ist:

    KORA.execute(tsf, target="KORA-HW")

Die Softwaredefinition bleibt identisch.

---

## 14. Zusammenfassung

KORA-2 ist die deterministische Software-Ebene der KORA-Architektur.  
Sie ersetzt die Variabilität und Instabilität moderner HPC-Systeme durch:

    strikte Ausführung  
    strikte Speicherverwaltung  
    strikte Datenbewegungen  
    strikte Synchronisation  
    strikte Reproduzierbarkeit  

KORA-2 ist nicht ein Framework —  
KORA-2 ist ein deterministisches Ausführungsmodell,  
das vollständig mit der KORA-Hardware kompatibel ist.

Es bildet den Kern der wissenschaftlichen Infrastruktur von KORA Version 2.0.



---

## Versionierung

- **Dokument:** `04_Software_Secification.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  
