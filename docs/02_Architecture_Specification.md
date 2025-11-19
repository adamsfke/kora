# KORA – Architektur-Spezifikation

## Kohärenzorientierte Rechenarchitektur für Big-Data-Langläufer

**Autoren:** Frank Meyer  
**Version:** 1.0 (November 2025)  
**Dokumenttyp:** Technische Spezifikation

---

## Inhaltsverzeichnis

1. Architektonische Grundprinzipien
2. KORA-Core (Orchestrator)
3. Compute-Worker (Recheneinheiten)
4. KORA-Net-Layer (I/O-Abschirmung)
5. SRDB (Single Resonance Data Bus)
6. Scheduling-Mechanismen
7. Fehlertoleranz und Redundanz
8. Hardware-Implementierung
9. Software-Stack
10. Vergleich mit verwandten Architekturen

---

## 1. Architektonische Grundprinzipien

### 1.1 Designphilosophie

KORA basiert auf der Erkenntnis, dass moderne Rechnerarchitekturen für **Interaktivität** optimiert sind, während Big-Data-Langläufer **Kohärenz und Durchsatz** benötigen. Die Architektur implementiert drei fundamentale Prinzipien:

**Prinzip 1: Globale Kohärenz durch zentrale Orchestrierung**
```
Klassische Systeme:
- Jeder Prozess/Thread hat lokale Sicht auf Daten
- Synchronisation über komplexe Protokolle
- Emergente Inkonsistenzen möglich

KORA:
- Ein KORA-Core mit globaler Sicht (SRDB)
- Alle Worker greifen auf denselben Datenraum zu
- Kohärenz ist strukturell garantiert, nicht nachträglich erzwungen
```

**Prinzip 2: Determinismus durch Unterbrechungsfreiheit**
```
Klassische Systeme:
- Preemptive Multitasking (Interrupts 500-3000/s)
- Timing-abhängiges Verhalten
- Non-deterministische Ergebnisse

KORA:
- Batch-Processing ohne Unterbrechungen
- Statisches oder vorhersagbares Scheduling
- Bit-identische Reproduzierbarkeit
```

**Prinzip 3: Spezialisierung durch Architektur-Reduktion**
```
Klassische Systeme:
- General-Purpose-Fähigkeiten (Desktop, Server, HPC)
- Komplexe Hardware (Out-of-Order, Branch-Prediction, Multi-Level-Cache)
- Overhead für Features, die Big-Data nicht nutzt

KORA:
- Spezialisiert auf strukturierte Datenverarbeitung
- Vereinfachte Hardware (In-Order, kein Speculative Execution)
- Effizienz durch Verzicht auf Universalität
```

### 1.2 Systemüberblick

```
┌───────────────────────────────────────────────────────────────┐
│                      KORA-SYSTEM                              │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              KORA-Net-Layer                              │ │
│  │  (Epochen-basierte I/O-Bündelung, keine IRQs)            │ │
│  └───────────────────┬──────────────────────────────────────┘ │
│                      │ Gebündelte Daten                       │
│                      ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              KORA-Core (Orchestrator)                    │ │
│  │  - Deterministisches Scheduling                          │ │
│  │  - SRDB-Verwaltung (globales Datenmodell)                │ │
│  │  - Task-Generierung und Validierung                      │ │
│  └───────────────────┬──────────────────────────────────────┘ │
│                      │ Task-Queue                             │
│                      ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              SRDB (Global Coherent Memory)               │ │
│  │  Single Resonance Data Bus – alle sehen gleichen Zustand │ │
│  └─────────┬─────────┬─────────┬─────────┬──────────────────┘ │
│            │         │         │         │                    │
│  ┌─────────▼────┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────────┐           │
│  │  Worker-Tile │ │Worker │ │Worker │ │  ...256   │           │
│  │  (Vektor-ALU)│ │Tile 2 │ │Tile 3 │ │           │           │
│  │  Scratchpad  │ │       │ │       │ │           │           │
│  └─────────┬────┘ └──┬────┘ └──┬────┘ └──┬────────┘           │
│            │         │         │         │                    │
│            └─────────┴─────────┴─────────┘                    │
│                      │ Result-Queue                           │
│                      ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         Result-Aggregation (im KORA-Core)                │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘

Datenfluss: Extern → Net-Layer → Core → SRDB → Worker → Core → Extern
Keine Interrupts zwischen Worker und Core während Berechnung
```

### 1.3 Abgrenzung zu klassischen Architekturen

| Eigenschaft | Klassisch (MPI/GPU-Cluster) | KORA |
|-------------|----------------------------|------|
| **Scheduling** | Dynamisch, preemptive | Statisch, deterministisch |
| **Interrupts** | 500-3000/s | <10/s (nur epochenbasiert) |
| **Speichermodell** | Distributed, Cache-Hierarchie | Global kohärent (SRDB) |
| **Worker-Autonomie** | Hoch (eigenes Scheduling) | Keine (passiv) |
| **Synchronisation** | Asynchron, Message-Passing | Synchron, Task-Queue |
| **Reproduzierbarkeit** | Probabilistisch (±0,1-0,3%) | Deterministisch (bit-identisch) |
| **Interaktivität** | Jederzeit unterbrechbar | Nur in Epochen |
| **Ziel-Optimierung** | Latenz, Responsiveness | Durchsatz, Kohärenz |

---

## 2. KORA-Core (Orchestrator)

### 2.1 Funktion und Verantwortlichkeiten

Der KORA-Core ist der zentrale Kontrollpunkt des Systems. Im Gegensatz zu verteilten Systemen, wo jeder Node Autonomie besitzt, konzentriert KORA alle Scheduling- und Kohärenzentscheidungen in einer Instanz.

**Kernaufgaben:**

1. **Globales Datenmodell verwalten (SRDB-Hüter)**
   - Kennt vollständigen Zustand aller Daten
   - Entscheidet über Speicher-Layout und -Zugriff
   - Validiert Datenkonsistenz vor/nach Berechnungen

2. **Deterministisches Scheduling**
   - Generiert Task-Wellen (homogene Tasks für Worker)
   - Zuteilung basierend auf Daten-Lokalität, nicht dynamischer Last
   - Kein preemptives Scheduling während Task-Ausführung

3. **Epochen-Management**
   - Definiert Zeitpunkte für externe I/O
   - Bündelt Netzwerk-/Dateisystem-Zugriffe
   - Verhindert spontane Interrupts

4. **Fehler-Detektion und Recovery**
   - Überwacht Worker-Health (Timeout, NaN-Propagation)
   - Kann fehlerhafte Tasks neu zuteilen
   - Checkpoint-Verwaltung für Rollback

### 2.2 Implementierung

**Phase 1 (Software auf Standard-Hardware):**
```c
// Pseudo-Code: KORA-Core als User-Space-Scheduler

struct KORACore {
    SRDB* global_data;
    WorkerPool* workers;
    TaskQueue* pending_tasks;
    ResultQueue* completed_results;
    EpochTimer* io_epoch;
};

void kora_core_run(KORACore* core) {
    // Initialisierung
    srdb_load_data(core->global_data);
    validate_problem_definition(core->global_data);
    
    while (!computation_complete(core)) {
        // Phase 1: Task-Generierung
        generate_task_wave(core->pending_tasks, core->global_data);
        
        // Phase 2: Worker-Zuteilung (deterministisch)
        for (int i = 0; i < core->pending_tasks->size; i++) {
            Task* task = &core->pending_tasks->tasks[i];
            int worker_id = deterministic_assign(task, core->workers);
            worker_submit_task(core->workers, worker_id, task);
        }
        
        // Phase 3: Warten auf Completion (KEIN INTERRUPT)
        // Worker signalisieren via Memory-Mapped Flag, nicht IRQ
        while (!all_workers_done(core->workers)) {
            // Busy-Wait oder Low-Frequency-Poll (100 Hz)
            usleep(10000); // 10ms
        }
        
        // Phase 4: Result-Collection (gebündelt)
        collect_results(core->completed_results, core->workers);
        
        // Phase 5: SRDB-Update
        srdb_update(core->global_data, core->completed_results);
        
        // Phase 6: Epochen-I/O (falls fällig)
        if (epoch_due(core->io_epoch)) {
            handle_external_io(core);
        }
    }
    
    // Finalisierung
    srdb_export_results(core->global_data);
}
```

**Phase 3 (Hardware-Implementierung):**
```
KORA-Core als dedizierter Prozessor:
- RISC-ähnlicher ISA (einfach, deterministisch)
- Keine Out-of-Order-Execution
- Keine Branch-Prediction (für Determinismus)
- Große Register-Datei für SRDB-Metadaten
- Hardware-Timer für Epochen
- DMA-Controller für Task/Result-Transfers

Vorteile:
- Scheduling-Entscheidungen in <1 Zyklus (statt ms)
- Kein OS-Overhead
- Energie-Effizienz durch Einfachheit
```

### 2.3 Scheduling-Strategien

**Statisches Scheduling (bevorzugt):**
```
Voraussetzung: Workload ist strukturiert und vorhersagbar

Algorithmus:
1. Analysiere Datenabhängigkeiten (Build Dependency Graph)
2. Partitioniere Daten in homogene Blöcke
3. Weise jedem Worker gleich große Blöcke zu
4. Schedule ist vor Ausführung vollständig bekannt

Vorteil:
- Perfekt deterministisch
- Kein Runtime-Overhead
- Maximale Cache-Lokalität planbar

Nachteil:
- Benötigt homogene Tasks (Laufzeitvarianz schlecht)
```

**Dynamisches Scheduling (Fallback):**
```
Falls Workload inhomogen (z.B. Sparse-Matrizen, Graphen):

Algorithmus:
1. Work-Stealing Queue pro Worker
2. Workers melden "fertig" via Flag (nicht IRQ)
3. Core pollt Flags und rebalanciert bei Bedarf
4. Rebalancing nur an definierten Synchronisationspunkten

Vorteil:
- Bessere Load-Balance bei heterogenen Tasks

Nachteil:
- Verliert Determinismus (Timing-abhängig)
- Sollte vermieden werden wenn möglich
```

### 2.4 Core-Skalierung für Cluster

In Phase 2 (Cluster-Erweiterung) wird ein **Hierarchisches Core-Modell** benötigt:

```
┌─────────────────────────────────────┐
│      Cluster-KORA-Core              │
│  (orchestriert Node-Cores)          │
└──────────┬──────────┬───────────────┘
           │          │
    ┌──────▼────┐  ┌──▼────────┐
    │ Node-Core │  │ Node-Core │
    │ (Node 1)  │  │ (Node 2)  │
    └──────┬────┘  └──┬────────┘
           │          │
      Workers 1-256  Workers 257-512
```

**Cluster-Core:**
- Verwaltet globales SRDB (repliziert oder partitioniert)
- Teilt Tasks auf Node-Cores zu
- Synchronisiert Epochen clusterweitt

**Node-Core:**
- Wie Einzelrechner-Core, aber empfängt Tasks von Cluster-Core
- Verwaltet lokales SRDB-Fragment

---

## 3. Compute-Worker (Recheneinheiten)

### 3.1 Designprinzipien

Worker in KORA sind **bewusst passiv** – sie besitzen keine Scheduling-Autonomie. Dies ist fundamental anders als in klassischen Systemen, wo jeder Core/Thread eigenständig agiert.

**Passive Worker-Eigenschaften:**

1. **Kein eigenes Betriebssystem**: Worker laufen ohne OS-Scheduler
2. **Kein Interrupt-Handling**: Können nicht unterbrochen werden
3. **Kein Speicher-Management**: Arbeiten auf vordefinierten Scratchpads
4. **Deterministisch**: Gleiche Task → gleiche Laufzeit (±Taktzyklen)

### 3.2 Worker-Architektur

**Logische Struktur eines Workers:**

```
┌──────────────────────────────────────┐
│         Worker-Tile N                │
├──────────────────────────────────────┤
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  Task-Queue (Read-Only FIFO)    │ │ ← Vom Core gefüllt
│  └────────┬────────────────────────┘ │
│           │                          │
│  ┌────────▼────────────────────────┐ │
│  │  Execution Unit                 │ │
│  │  - Vektor-ALU (SIMD)            │ │
│  │  - FP64/FP32/INT-Operationen    │ │
│  │  - Keine Kontrollfluss-Logik    │ │
│  └────────┬────────────────────────┘ │
│           │                          │
│  ┌────────▼────────────────────────┐ │
│  │  Local Scratchpad (SRAM)        │ │
│  │  - 256 KB - 1 MB                │ │
│  │  - Software-Managed (kein Cache)│ │
│  └────────┬────────────────────────┘ │
│           │                          │
│  ┌────────▼────────────────────────┐ │
│  │  Result-Queue (Write-Only FIFO) │ │ → Zum Core zurück
│  └─────────────────────────────────┘ │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │  Status-Flags (Memory-Mapped)   │ │
│  │  - BUSY / IDLE                  │ │
│  │  - ERROR (NaN, Overflow)        │ │
│  └─────────────────────────────────┘ │
│                                      │
└──────────────────────────────────────┘
```

**Ausführungslogik (Hardware-Level):**

```assembly
; Pseudo-Assembly für Worker-Tile

worker_loop:
    ; 1. Warte auf Task (Memory-Mapped Flag statt Interrupt)
    POLL task_queue_flag
    BEQ task_queue_flag, 0, worker_loop
    
    ; 2. Lade Task-Daten vom SRDB in Scratchpad
    DMA_LOAD scratchpad, task_data_addr, task_size
    
    ; 3. Führe Operation aus (z.B. Matrix-Multiplikation)
    VLOAD v0, scratchpad[0]    ; Vektor laden
    VLOAD v1, scratchpad[64]
    VMUL v2, v0, v1            ; Vektor-Multiplikation
    VADD v3, v2, v2            ; Akkumulation
    VSTORE scratchpad[128], v3 ; Ergebnis speichern
    
    ; 4. Schreibe Ergebnis in Result-Queue
    DMA_STORE result_queue, scratchpad[128], result_size
    
    ; 5. Setze Status-Flag (Core pollt dieses, kein IRQ)
    STORE worker_status, IDLE
    
    ; 6. Wiederhole
    JMP worker_loop
```

### 3.3 Worker-Typen für verschiedene Workloads

**Typ 1: Vektor-Worker (Standard)**
```
Optimiert für: Dense Matrizen, strukturierte Gitter
Hardware: SIMD-Einheiten (AVX-512-ähnlich)
Beispiel: Klimamodell-Stencil-Operationen
```

**Typ 2: Tensor-Worker (KI)**
```
Optimiert für: Matrix-Multiplikation, Convolutions
Hardware: Tensor-Cores (wie NVIDIA)
Beispiel: Neural-Network-Training
```

**Typ 3: Custom-Worker (Domänenspezifisch)**
```
Optimiert für: FFT, Sparse-Matrix, Graph-Traversierung
Hardware: FPGA-Pipelines mit Custom-Logic
Beispiel: Molekulardynamik-Kraftberechnungen
```

### 3.4 Worker-Kommunikation untereinander

**Problem:** Viele HPC-Workloads erfordern Daten-Austausch zwischen Workern (z.B. Halo-Exchange bei Gitter-Simulationen).

**KORA-Lösung: Keine direkte Kommunikation**

```
Klassisch (MPI):
Worker 1 ↔ Worker 2 (direkter Message-Passing)
Problem: Non-deterministisch, Overhead

KORA:
Worker 1 → Core (via Result-Queue)
Core synchronisiert
Core → Worker 2 (via Task-Queue mit aktualisierten Daten)

Vorteil: Deterministisch, Core hat globale Sicht
Nachteil: Latenz (aber bei Langläufern irrelevant)
```

**Optimierung für häufige Kommunikation:**

Wenn Halo-Exchange jede Iteration nötig ist (wie bei CFD):

```
Option 1: Bulk-Synchronous-Parallel (BSP)-Modell
- Core orchestriert globale Barrier-Points
- Alle Worker schreiben Results
- Core updated SRDB
- Nächste Task-Welle startet

Option 2: Software-Pipelined Halo-Exchange
- Worker berechnen zuerst innere Zellen (keine Kommunikation)
- Während innere Zellen rechnen, Core distribuiert Boundary-Daten
- Worker berechnen dann Boundary-Zellen
```

---

## 4. KORA-Net-Layer (I/O-Abschirmung)

### 4.1 Problem der asynchronen I/O

Klassische Systeme behandeln I/O als **asynchrone Events**:
- Netzwerkpaket kommt an → sofortiger Interrupt
- Dateisystem-Operation fertig → Callback/Signal
- Sensor sendet Daten → spontane Verarbeitung

Dies fragmentiert Berechnungen und zerstört Determinismus.

### 4.2 Epochen-basiertes I/O-Modell

KORA behandelt I/O als **periodische Epochen**:

```
Zeitstrahl:
│← Compute-Epoche (10s) →│← I/O-Epoche (100ms) →│← Compute →│...

Während Compute-Epoche:
- Kein externes I/O
- Worker rechnen unterbrechungsfrei
- Externe Daten werden gebuffert (nicht processed)

Während I/O-Epoche:
- Alle Worker pausieren
- Core holt gebufferte Daten
- Core schreibt Checkpoints / Logs
- Core sendet Results an Netzwerk
```

**Epochen-Längen (konfigurierbar):**

| Workload-Typ | Compute-Epoche | I/O-Epoche |
|--------------|----------------|------------|
| Klimamodell | 60s | 1s |
| KI-Training | 10s | 0,5s |
| CFD-Simulation | 30s | 0,2s |
| Echtzeit-CFD | 1s | 0,1s |

**Trade-off:** Längere Compute-Epochen → höhere Effizienz, aber länger ohne externe Feedback

### 4.3 Netzwerk-Handling

**Standard-Netzwerk-Stack (TCP/IP):**
```
Problem:
- Interrupt pro Paket (1000-10000/s bei 10 Gbit/s)
- Non-deterministisches Timing
- CPU-Overhead 20-40%
```

**KORA-Netzwerk-Stack:**
```
Komponente 1: RDMA-fähige NIC mit eigenem Buffer
- NIC empfängt Pakete ohne CPU-Interrupt
- Schreibt Daten direkt in reservierten Memory-Bereich
- Setzt Memory-Mapped-Flag (kein IRQ)

Komponente 2: Net-Layer-Dämon (auf separater Core)
- Pollt Flag alle 10-100ms (epochenabhängig)
- Validiert/Parst gebufferte Daten
- Übergibt gebündelt an KORA-Core

Komponente 3: Deterministische Protokoll-Schicht
- Sequenznummern für alle Messages
- Timeout/Retry mit festen Intervallen (nicht dynamisch)
- Keine spontanen ACKs (gebündelt in I/O-Epoche)
```

**Energieeinsparung:**
- Standard: 1000 IRQ/s × 10.000 Zyklen = 10 Mio Zyklen/s Overhead
- KORA: 10 Polls/s × 1.000 Zyklen = 10.000 Zyklen/s Overhead
- **Faktor 1000 weniger Overhead**

### 4.4 Dateisystem-Integration

**Problem:** Klassische Dateisysteme (ext4, XFS) sind für interaktive Nutzung optimiert, nicht für deterministische Batch-I/O.

**KORA-Dateisystem-Strategie:**

```
Option 1: RAM-Disk für Zwischenergebnisse
- Alle Daten während Berechnung in RAM
- Nur bei Epochen-Checkpoints auf Disk schreiben
- Minimiert Dateisystem-Interaktion

Option 2: Direct I/O mit vorallokierten Files
- File-Layout vor Berechnung festgelegt
- DMA-Transfers ohne Dateisystem-Cache
- Deterministische Write-Reihenfolge

Option 3: Log-Structured Filesystem
- Append-Only-Writes (sequenziell, vorhersagbar)
- Keine In-Place-Updates (vermeidet Fragmentierung)
- Beispiel: F2FS im Deterministic-Mode
```

---

## 5. SRDB (Single Resonance Data Bus)

### 5.1 Konzept

SRDB ist das **globale, kohärente Datenmodell** von KORA. Im Gegensatz zu verteilten Speichersystemen mit Cache-Hierarchien existiert **eine zentrale Wahrheit**.

**Metapher:**
```
Klassisch: Jeder hat eine Kopie des Dokuments, Änderungen werden synchronisiert
KORA: Alle arbeiten am gleichen Dokument gleichzeitig (Google Docs-ähnlich)
```

### 5.2 Speicherorganisation

**Logische Struktur:**

```
SRDB
├── Global State (Core-verwaltet)
│   ├── Metadaten (Grid-Dimensionen, Zeitschritte, Parameter)
│   └── Control-Flags (Iteration-Count, Convergence-Status)
│
├── Data Arrays (Worker-zugänglich)
│   ├── Input-Arrays (Read-Only für Worker)
│   ├── Output-Arrays (Write-Only für Worker)
│   └── Intermediate-Arrays (Read-Write, aber koordiniert)
│
└── Checkpoints (Epochen-Snapshots)
    ├── Checkpoint T=0 (Initial State)
    ├── Checkpoint T=1000
    └── ...
```

**Physische Implementierung (Phase-abhängig):**

**Phase 1 (Software auf Standard-Hardware):**
```c
// SRDB als großer Shared-Memory-Block
typedef struct {
    float* input_data;      // z.B. 100 GB
    float* output_data;     // z.B. 100 GB
    float* intermediate;    // z.B. 50 GB
    Metadata meta;
} SRDB;

// Allokation mit Huge Pages (reduziert TLB-Misses)
SRDB* srdb = mmap(NULL, 250GB, PROT_READ|PROT_WRITE, 
                  MAP_SHARED|MAP_HUGETLB, -1, 0);

// Worker greifen via Pointer zu (kein Copy)
worker_access(srdb->input_data + worker_offset);
```

**Phase 3 (Monolithische Hardware):**
```
SRDB als On-Chip High-Bandwidth Memory (HBM):
- 8× HBM3-Stacks direkt auf Die gebonded
- Kapazität: 128 GB (erweiterbar auf 256 GB)
- Bandbreite: 8 TB/s (alle Worker teilen sich)
- Latenz: <100ns (vs. 300ns für externen DRAM)

Vorteil:
- Keine Cache-Kohärenz nötig (alle sehen gleichen Speicher)
- Deterministische Latenz (kein NUMA-Effekt)
- Energieeffizienz (kurze Wege, niedriger Voltage)
```

### 5.3 Speicherzugriffsmuster

**Problem:** Wenn alle Worker gleichzeitig auf SRDB zugreifen, entsteht Contention (Memory-Bandwidth-Limit).

**KORA-Lösung: Strukturierte Zugriffsmuster**

```
Prinzip 1: Räumliche Partitionierung
- Jeder Worker bekommt exklusiven Speicherbereich
- Beispiel: Gitter in 256 Blöcke geteilt, Worker N bearbeitet Block N
- Kein Konflikt, da unterschiedliche Adressen

Prinzip 2: Zeitliche Partitionierung (bei Read-Write-Sharing)
- Time-Division-Multiplexing: Worker greifen in festen Slots zu
- Beispiel: Slot 0-3ms → Worker 0-63, Slot 4-7ms → Worker 64-127
- Deterministisch, kein Arbitrierungs-Overhead

Prinzip 3: Burst-Transfers
- Worker laden große Blöcke in Scratchpad (DMA)
- Arbeiten lokal auf Scratchpad
- Schreiben gebündelt zurück
- Minimiert Bus-Zugriffe
```

**Beispiel-Berechnung:**

```
Annahme: 256 Worker, je 10 GFLOP/s, Compute-Intensity 100 FLOP/Byte

Benötigte Bandbreite:
256 × 10 GFLOP/s ÷ 100 FLOP/Byte = 25,6 GB/s

HBM3-Bandbreite: 8 TB/s = 8.000 GB/s
Auslastung: 25,6 / 8.000 = 0,32%

→ Memory-Bandwidth ist KEIN Bottleneck für typische HPC-Workloads
```

**Hinweis:** Für Big-Data-Simulationen (wie die KORA-Klimamodell-Simulation mit 6,48 Mrd Datenpunkten und ~320s Laufzeit) ist die tatsächliche Bandbreiten-Nutzung oft noch niedriger, da Berechnungen compute-bound sind.

### 5.4 Kohärenz-Garantien

**KORA garantiert sequenzielle Konsistenz:**

```
Definition:
Alle Operationen erscheinen in einer globalen, totalen Ordnung,
konsistent mit der Programmreihenfolge jedes einzelnen Workers.

Praktisch:
1. Worker N schreibt X
2. Worker M liest X
→ Worker M sieht IMMER den Wert von Worker N (nie veraltet)

Im Gegensatz zu:
Eventual Consistency (NoSQL): M könnte veraltetes X sehen
Weak Consistency (GPU): M sieht X erst nach expliziter Synchronisation
```

**Implementierung:**

```
Software (Phase 1):
- Memory-Barriers nach jedem Worker-Result-Write
- Core wartet explizit auf alle Worker (Barrier-Synchronisation)

Hardware (Phase 3):
- Alle Worker schreiben auf gleichen physischen Speicher (HBM)
- Keine Caches → keine Kohärenz-Probleme
- Oder: Write-Through-Caches mit Hardware-Snooping (einfacher als Multi-Chip)
```

---

## 6. Scheduling-Mechanismen

### 6.1 Task-Granularität

**Trade-off:**
- **Grobe Tasks** (z.B. ganzer Gitter-Block): Weniger Overhead, aber schlechte Load-Balance
- **Feine Tasks** (z.B. einzelne Zellen): Perfekte Load-Balance, aber hoher Overhead

**KORA-Ansatz: Adaptive Granularität basierend auf Workload**

```
Homogene Workloads (Klimamodell, Dense-Matrix):
- Grobe Tasks (1.000-10.000 Operationen pro Task)
- Statische Zuteilung
- Minimaler Overhead

Heterogene Workloads (Sparse-Matrix, Graph):
- Mittlere Granularität (100-1.000 Operationen)
- Dynamisches Rebalancing an Epochen-Grenzen
- Akzeptabler Overhead für bessere Balance
```

### 6.2 Scheduling-Algorithmen im Detail

**Algorithmus 1: Block-Cyclic-Distribution (Standard für strukturierte Daten)**

```python
def block_cyclic_schedule(data_grid, num_workers):
    """
    Verteilt strukturiertes Gitter zyklisch auf Worker
    Optimiert für Cache-Lokalität und Load-Balance
    """
    block_size = calculate_block_size(data_grid, num_workers)
    
    for block_id in range(total_blocks):
        worker_id = block_id % num_workers
        task = create_task(data_grid, block_id, block_size)
        assign_to_worker(worker_id, task)
    
    return schedule  # Deterministisch, vorhersagbar

# Vorteil: Perfekt balanced wenn Blöcke homogen
# Nachteil: Suboptimal bei heterogenen Daten
```

**Algorithmus 2: Dependency-Aware-Scheduling (für iterative Solver)**

```python
def dependency_schedule(tasks, dependency_graph, num_workers):
    """
    Berücksichtigt Datenabhängigkeiten zwischen Tasks
    Erstellt Wellen von unabhängigen Tasks
    """
    levels = topological_sort(dependency_graph)
    
    for level in levels:
        # Alle Tasks in diesem Level sind unabhängig
        independent_tasks = tasks[level]
        
        # Verteile gleichmäßig auf Worker
        for i, task in enumerate(independent_tasks):
            worker_id = i % num_workers
            assign_to_worker(worker_id, task)
        
        # Barrier: Warte auf Completion aller Tasks dieses Levels
        wait_for_level_completion()
    
    return schedule

# Beispiel: Gauss-Seidel-Iteration
# Level 0: Alle rot-markierten Zellen (unabhängig)
# Level 1: Alle schwarz-markierten Zellen (abhängig von Level 0)
```

**Algorithmus 3: Work-Stealing (Fallback für heterogene Workloads)**

```python
def work_stealing_schedule(tasks, num_workers):
    """
    Dynamisches Load-Balancing: Idle Workers stehlen Tasks
    NUR an Epochen-Grenzen, nicht kontinuierlich
    """
    # Initiale Verteilung
    for i, task in enumerate(tasks):
        worker_queues[i % num_workers].append(task)
    
    # Workers arbeiten ab
    while not all_done():
        # An Epochen-Grenze: Rebalancing
        if epoch_boundary():
            for worker in workers:
                if worker.queue_empty() and not worker.stealing:
                    victim = find_busiest_worker()
                    if victim.queue_size > 1:
                        stolen_task = victim.queue.pop()
                        worker.queue.append(stolen_task)
    
    return execution_trace

# Deterministisch WENN:
# - Stealing nur an definierten Zeitpunkten
# - Victim-Auswahl nach festen Regeln (z.B. höchste ID)
# Sonst: Non-deterministisch (sollte vermieden werden)
```

### 6.3 Synchronisationsmodelle

**Bulk-Synchronous-Parallel (BSP) – KORA-Standard**

```
Struktur:
┌─ Superstep 1 ───┐  ┌─ Superstep 2 ───┐  ┌─ Superstep 3 ───┐
│ Worker 0: Comp  │  │ Worker 0: Comp  │  │ Worker 0: Comp  │
│ Worker 1: Comp  │  │ Worker 1: Comp  │  │ Worker 1: Comp  │
│ ...             │  │ ...             │  │ ...             │
│ Worker 255:Comp │  │ Worker 255:Comp │  │ Worker 255:Comp │
└────────┬────────┘  └───────┬─────────┘  └──────┬──────────┘
         │ Barrier           │ Barrier           │ Barrier
         ▼                   ▼                   ▼
    Synchronisation     Synchronisation     Synchronisation
    (SRDB-Update)       (SRDB-Update)       (SRDB-Update)

Eigenschaften:
- Alle Worker starten/enden gleichzeitig
- Kommunikation nur an Barriers
- Perfekt deterministisch
- Idle-Zeit wenn Worker unterschiedlich schnell
```

**Pipelined-Execution (Optimierung für geringe Idle-Zeit)**

```
Idee: Überlappen von Compute und Kommunikation

Beispiel: Stencil-Berechnung mit Halo-Exchange
┌────────────────────────────────────────┐
│ Worker N                               │
├────────────────────────────────────────┤
│ Phase 1: Berechne innere Zellen        │ ← Keine Kommunikation nötig
│          (können sofort starten)       │
│                                        │
│ Parallel: Core distribuiert Halo-Daten │ ← Während Worker rechnen
│                                        │
│ Phase 2: Berechne Rand-Zellen          │ ← Benötigt Halo-Daten
│          (warten auf Core-Update)      │
└────────────────────────────────────────┘

Vorteil: Reduziert Barrier-Idle-Zeit um 30-50%
Nachteil: Komplexere Scheduling-Logik
```

---

## 7. Fehlertoleranz und Redundanz

### 7.1 Fehlerarten in KORA

**Transiente Fehler (Soft Errors):**
- Kosmische Strahlung → Bit-Flip in Memory/Register
- Häufigkeit: ~1 Fehler pro GB-RAM pro Jahr
- KORA-Risiko: Höher bei großem SRDB (100+ GB)

**Permanente Fehler (Hard Errors):**
- Defekter Worker-Tile (Yield-Problem bei großen Dies)
- Speicher-Defekt in HBM
- Core-Ausfall (selten, aber kritisch)

**Software-Fehler:**
- NaN-Propagation (Division durch Null, Overflow)
- Algorithmus-Bugs (außerhalb KORA-Kontrolle)
- Fehlerhafte Problemdefinition

### 7.2 Fehlererkennungsmechanismen

**1. Worker-Health-Monitoring**

```c
// KORA-Core pollt Worker-Status jede Epoche
void check_worker_health(KORACore* core) {
    for (int i = 0; i < core->num_workers; i++) {
        WorkerStatus status = read_worker_status(i);
        
        if (status.timeout) {
            // Worker hängt → Task neu zuteilen
            reschedule_task(core, i);
        }
        
        if (status.error_flag) {
            // NaN oder Overflow detektiert
            log_error(i, status.error_code);
            if (critical_error(status)) {
                rollback_to_checkpoint(core);
            }
        }
    }
}
```

**2. SRDB-Integritätschecks**

```c
// Nach jedem Superstep: Validiere Daten
void validate_srdb(SRDB* srdb) {
    // Plausibilitäts-Checks
    for (int i = 0; i < srdb->size; i++) {
        if (isnan(srdb->data[i]) || isinf(srdb->data[i])) {
            flag_corruption(i);
        }
        
        // Domänenspezifisch: z.B. Temperatur -273°C..10000°C
        if (srdb->data[i] < PHYS_MIN || srdb->data[i] > PHYS_MAX) {
            flag_suspicious(i);
        }
    }
    
    // Checksum-Validierung (optional, teuer)
    uint64_t checksum = calculate_checksum(srdb);
    if (checksum != srdb->expected_checksum) {
        trigger_ecc_correction();
    }
}
```

**3. ECC-Memory (Hardware-Level)**

```
Phase 3-Hardware: SRDB-HBM mit ECC
- Single-Bit-Errors: Automatisch korrigiert
- Double-Bit-Errors: Detektiert, aber nicht korrigierbar

Worker-Tiles: Redundante Berechnung (optional)
- Kritische Tasks werden von 2 Workern parallel berechnet
- Ergebnisse verglichen, bei Diskrepanz: Mehrheits-Voting
- Overhead: 2×, aber garantiert Korrektheit
```

### 7.3 Checkpoint-Strategie

**Coordinated Checkpointing (KORA-Standard)**

```
Prinzip:
Alle Worker pausieren gleichzeitig (an Epochen-Grenze)
→ SRDB-Snapshot ist global konsistent

Algorithmus:
1. Core sendet CHECKPOINT-Signal an alle Worker
2. Worker beenden aktuellen Task
3. Core schreibt SRDB auf persistenten Speicher
4. Checkpoint-Marker gesetzt (Iteration N, Timestamp)
5. Workers fahren fort

Checkpoint-Frequenz:
- Adaptiv basierend auf Kosten/Nutzen
- Kostenfunktion: C = Checkpoint_Time × Frequency
- Nutzenfunktion: B = Avg_Work_Lost_On_Failure / MTBF
- Optimal: C = B
```

**Beispiel-Berechnung:**

```
Annahme:
- SRDB-Größe: 200 GB
- Schreib-Bandbreite: 10 GB/s
- Checkpoint-Zeit: 20s
- Berechnung pro Iteration: 60s
- MTBF (Mean Time Between Failures): 1000 Stunden

Ohne Checkpoints:
- Durchschnittlich verlorene Arbeit: 500 Stunden
- Neustart: 500 Stunden verschwendet

Checkpoint alle 10 Iterationen (600s):
- Verlorene Arbeit bei Failure: Maximal 600s
- Checkpoint-Overhead: 20s / 600s = 3,3%
- Erwartete Zeitersparnis bei Failure: 499,84 Stunden

→ 3,3% Overhead rechtfertigt sich bereits bei 0,2% Failure-Rate
```

**Incremental Checkpointing (Optimierung)**

```
Problem: Checkpoint-Zeit wächst mit SRDB-Größe

Lösung: Nur geänderte Seiten schreiben
1. Memory-Pages als Copy-On-Write markieren
2. Tracking welche Pages seit letztem Checkpoint verändert
3. Nur dirty Pages schreiben

Beispiel:
- SRDB: 200 GB (50.000 Pages à 4 MB)
- Typisch geändert pro Iteration: 10% = 20 GB
- Incremental-Checkpoint: 2s statt 20s (10× schneller)
```

### 7.4 Redundanz in Monolithischer Hardware

**Problem:** Ein 2.500 mm² Die hat niedrigere Yield als mehrere kleine Dies.

**KORA-Lösung: N+K-Redundanz**

```
Design: 256 Worker-Tiles + 16 Reserve-Tiles = 272 Tiles total

Während Fertigung:
1. Wafer-Test identifiziert defekte Tiles
2. Defekte Tiles werden in Hardware-Mapping deaktiviert
3. Reserve-Tiles ersetzen defekte Tiles

Beispiel:
- 10 defekte Tiles → 10 Reserve aktiviert → 256 funktionierende
- System ist voll funktional

Yield-Verbesserung (bei 0,09 Defekte/cm²):
Ohne Redundanz (256 Tiles, alle müssen funktionieren):
  Yield ≈ 5,0% (nur 50 von 1000 Dies nutzbar)

Mit Redundanz (272 Tiles, bis zu 16 defekt tolerierbar):
  Yield ≈ 73,9% (739 von 1000 Dies nutzbar)

→ Redundanz erhöht Yield um Faktor 15
```

**Runtime-Redundanz (optional für kritische Anwendungen)**

```
Triple-Modular-Redundancy (TMR):
- Jeder Task wird von 3 Workern parallel berechnet
- Majority-Voting: Ergebnis, das 2 von 3 liefern, ist korrekt
- Overhead: 3×, aber toleriert 1 defekten Worker pro Task-Gruppe

Anwendung:
- Finanzberechnungen (regulatorische Anforderungen)
- Sicherheitskritische Simulationen (Luft-/Raumfahrt)
- Wissenschaft mit extremen Genauigkeitsanforderungen
```

---

## 8. Hardware-Implementierung

### 8.1 Phasenweise Evolution

**Phase 1: Software auf Standard-Hardware (2025-2027)**

```
Hardware:
- Standard-Server: 2× Intel Xeon / AMD EPYC
- 8× NVIDIA A100 / AMD MI300 GPUs
- 512 GB DDR5-RAM (SRDB in System-Memory)
- 10/25 Gbit/s Ethernet (RDMA-fähig)

Software-Stack:
- KORA-Core: C/C++ User-Space-Scheduler
- Worker: CUDA/ROCm Kernels
- SRDB: Shared Memory (mmap mit Huge Pages)
- Net-Layer: Modifizierter RDMA-Stack

Limitierungen:
- OS-Overhead trotz Optimierung (15-20%)
- PCIe-Latenz GPU↔CPU (200-500ns)
- Cache-Kohärenz zwischen CPUs
```

**Phase 2: Multi-Chip-Module (MCM) (2027-2029)**

```
Hardware:
- 4-8 KORA-Tiles pro Package (Chiplet-Architektur)
- Jeder Tile: KORA-Core-Logic + 32 Worker-Units
- Inter-Tile-Interconnect: Proprietär, SERDES-basiert (nicht PCIe)
- Shared HBM2e (64 GB pro Package)

Design:
┌─────────────────────────────────────┐
│         MCM-Package                 │
├─────────────────────────────────────┤
│  ┌────────┐  ┌────────┐             │
│  │ Tile 0 │──│ Tile 1 │             │ ← Inter-Tile-Link
│  └───┬────┘  └───┬────┘             │
│      │           │                  │
│  ┌───▼───────────▼──────┐           │
│  │   Interconnect-Hub   │           │
│  └───┬──────────────────┘           │
│      │                              │
│  ┌───▼──────────────────┐           │
│  │   HBM2e Controller   │           │
│  └──────────────────────┘           │
│         ▲  ▲  ▲  ▲                  │
│     HBM-Stack (4× 16 GB)            │
└─────────────────────────────────────┘

Vorteile vs. Phase 1:
- 50% höhere Bandbreite (Tile↔HBM)
- 70% niedrigere Latenz (kein PCIe)
- 40% weniger Energie (kürzere Wege)

Limitierungen:
- Inter-Tile-Kommunikation noch nicht optimal
- Yield-Probleme bei >100 mm² Tiles
```

**Phase 3: Monolithischer Die (2029-2033)**

```
Spezifikation:
┌───────────────────────────────────────────────────┐
│                KORA-Monolith (2.500 mm²)          │
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────────────────────────────────┐ │
│  │    KORA-Core-Cluster (4× Cores)              │ │
│  │    - Scheduling-Logic                        │ │
│  │    - SRDB-Controller                         │ │
│  │    - DMA-Engines                             │ │
│  └────────────┬─────────────────────────────────┘ │
│               │                                   │
│  ┌────────────▼─────────────────────────────────┐ │
│  │    Global Interconnect (1024-bit Bus)        │ │
│  │    8 TB/s Bandwidth, Latency <10ns           │ │
│  └─┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┘ │
│    │  │  │  │  │  │  │  │  │  │  │  │  │  │  │    │
│   ┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐┌▼┐   │
│   │W││W││W││W││W││W││W││W││W││W││W││W││W││W││W│   │
│   │0││1││2││3││..││││││││││││ ...      ││255│ │   │
│   └─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘   │
│                                                   │
│  ┌──────────────────────────────────────────────┐ │
│  │    HBM3 Controller (8-Channel)               │ │
│  └─┬────┬────┬────┬────┬────┬────┬────┬─────────┘ │
│    │    │    │    │    │    │    │    │           │
│   ┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐┌▼──┐        │
│   │HBM││HBM││HBM││HBM││HBM││HBM││HBM││HBM│        │
│   │ 0 ││ 1 ││ 2 ││ 3 ││ 4 ││ 5 ││ 6 ││ 7 │        │
│   └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘        │
│         128 GB HBM3, 8 TB/s Total                 │
└───────────────────────────────────────────────────┘

Prozess: 3nm oder 2nm (TSMC/Samsung)
Leistung: 800-1.200 W TDP
Taktfrequenz: 1,5-2 GHz (niedrig für Effizienz)
```

### 8.2 Worker-Tile-Mikroarchitektur

**Einzelner Worker-Tile (10-15 mm²)**

```
┌───────────────────────────────────────┐
│        Worker-Tile                    │
├───────────────────────────────────────┤
│                                       │
│  ┌──────────────────────────────────┐ │
│  │  Instruction Decode (Simple)     │ │  ← Kein Out-of-Order
│  └───────────┬──────────────────────┘ │
│              │                        │
│  ┌───────────▼──────────────────────┐ │
│  │  Vector-ALU (512-bit SIMD)       │ │  ← 16× FP32 oder 8× FP64
│  │  - FMA-Units (Fused-Multiply-Add)│ │
│  │  - Special-Functions (sqrt, exp) │ │
│  └───────────┬──────────────────────┘ │
│              │                        │
│  ┌───────────▼──────────────────────┐ │
│  │  Local Scratchpad (512 KB)       │ │  ← Software-Managed
│  │  - 8-Way Banked                  │ │  ← Paralleler Zugriff
│  │  - Dual-Port (Read + Write)      │ │
│  └───────────┬──────────────────────┘ │
│              │                        │
│  ┌───────────▼──────────────────────┐ │
│  │  DMA-Engine                      │ │  ← Load/Store zu SRDB
│  └──────────────────────────────────┘ │
│                                       │
│  ┌──────────────────────────────────┐ │
│  │  Status/Control Registers        │ │  ← Memory-Mapped
│  └──────────────────────────────────┘ │
│                                       │
└───────────────────────────────────────┘

Peak-Performance: 20-40 GFLOP/s (FP64)
Fläche: 12 mm² @ 3nm
Leistung: 3-5 W @ 1,8 GHz
```

**Design-Vereinfachungen vs. Standard-CPU-Core:**

| Feature | Standard-Core | KORA-Worker |
|---------|---------------|-------------|
| Out-of-Order-Execution | Ja (komplex) | Nein (In-Order) |
| Branch-Prediction | Ja (Tournament) | Minimal (Static) |
| Multi-Level-Cache | L1/L2/L3 | Nur Scratchpad |
| Virtual Memory | Ja (TLB, Page-Walk) | Nein (Physical nur) |
| Interrupts | Ja (komplex) | Nein |
| Context-Switch-Support | Ja (State-Save) | Nein |

**Flächeneinsparung durch Vereinfachung: ~60%**

### 8.3 Interconnect-Design

**Global Bus (Monolith-Phase)**

```
Architektur: Time-Division-Multiplexing (TDM)

Prinzip:
- Jeder Worker hat festen Zeitslot (z.B. 100ns)
- 256 Worker × 100ns = 25,6 µs pro Runde
- Keine Arbitrierung nötig (deterministisch)

Bus-Spezifikation:
- Breite: 1024 Bit (128 Bytes pro Transfer)
- Frequenz: 2 GHz
- Peak-Bandbreite: 256 GB/s pro Richtung (bidirektional)
- Latenz: <10ns (On-Die)

Vergleich zu PCIe Gen5 (Standard-System):
PCIe: 32 Lanes × 8 GT/s = 256 GB/s (ähnlich)
ABER: PCIe-Latenz 200-500ns (20-50× höher)
      PCIe-Arbitrierung non-deterministisch

KORA-Bus: Deterministisch, niedrige Latenz, keine Overhead
```

**Beispiel-Timing-Diagramm:**

```
Time →
  0ns     100ns   200ns   300ns   400ns   ...
│───────│───────│───────│───────│───────│
│ W0-Rd │ W1-Rd │ W2-Rd │ W3-Rd │ ...   │  ← Read-Slots
│───────│───────│───────│───────│───────│
│ W0-Wr │ W1-Wr │ W2-Wr │ W3-Wr │ ...   │  ← Write-Slots
└───────┴───────┴───────┴───────┴───────┘

Jeder Worker weiß seinen Slot → kein Konflikt möglich
```

### 8.4 Energieeffizienz-Maßnahmen

**1. Voltage-Frequency-Scaling (aber statisch, nicht dynamisch)**

```
Problem bei Standard-CPUs:
- DVFS (Dynamic Voltage and Frequency Scaling)
- Ändert Frequenz/Voltage je nach Last
- Non-deterministisch, Thermal-Zyklen (Materialstress)

KORA-Ansatz:
- Feste Frequenz während Berechnung (z.B. 1,8 GHz)
- Niedriger als Maximum (3 GHz) → 50% Energieeinsparung
- Keine Turbo-Boost-Varianz
- Deterministische Performance
```

**2. Clock-Gating (Worker-Ebene)**

```
Prinzip: Deaktiviere Takt für idle Workers

Implementierung:
if (worker_queue_empty(worker_id)) {
    disable_clock(worker_id);  // Hardware-Signal
    power_savings += 90%;       // Worker verbraucht nur Leakage
}

when (new_task_arrives(worker_id)) {
    enable_clock(worker_id);    // Wake-Up in <10ns
}

Energieeinsparung:
- Idle-Worker: 0,3 W (Leakage) statt 3 W (Active)
- Bei 50% Auslastung: 25% Gesamtenergieersparnis
```

**3. Scratchpad statt Cache (Energieeffizienz)**

```
Standard-Cache (L1/L2/L3):
- Assoziatives Lookup (hohe Energie)
- Kohärenz-Snooping (konstanter Energieverbrauch)
- Spekulatives Prefetching

KORA-Scratchpad:
- Direkter Adress-Zugriff (keine Suche)
- Kein Snooping nötig (Software-Managed)
- Kein Prefetching (explizite DMA-Transfers)

Energieeinsparung: 70-80% pro Memory-Zugriff
```

**4. Niedrige Taktfrequenz durch Parallelität**

```
Trade-off:
- Standard-GPU: Wenige Cores (100-200) bei 2-3 GHz
- KORA: Viele Cores (256+) bei 1,5-2 GHz

Energieformel: P ∝ f × V²
Bei niedrigerer Frequenz: Niedrigere Voltage möglich
1,5 GHz @ 0,7V vs. 3 GHz @ 1,0V
P(1,5 GHz) = 0,5 × 0,49 = 0,245 (75% Einsparung)

Gleicher Durchsatz durch mehr Parallelität (mehr Worker)
Aber: Fläche steigt linear, Energie sublinear
```

---

## 9. Software-Stack

### 9.1 Programmiermodell

**KORA bietet zwei Programmierebenen:**

**Level 1: High-Level-API (für Anwender)**

```python
from kora import KORARuntime, SRDB, Task

# 1. SRDB initialisieren
srdb = SRDB(size_gb=100)
srdb.load_data("climate_model_input.h5")

# 2. Problem definieren
@kora_task
def stencil_operation(data_block, neighbors):
    """Wird von jedem Worker ausgeführt"""
    result = 0.25 * (neighbors.north + neighbors.south +
                     neighbors.east + neighbors.west)
    return result

# 3. Berechnung starten (unterbrechungsfrei)
runtime = KORARuntime(num_workers=256)
runtime.run(stencil_operation, srdb, epochs=1000)

# 4. Ergebnisse exportieren
srdb.save_results("climate_model_output.h5")
```

**Level 2: Low-Level-API (für Performance-Optimierung)**

```c
// Direkte Kontrolle über Worker-Zuteilung und SRDB-Layout

#include <kora/core.h>
#include <kora/worker.h>

int main() {
    // SRDB mit spezifischem Memory-Layout
    SRDB* srdb = srdb_create(NUMA_NODE_0, 100GB);
    srdb_set_layout(srdb, BLOCK_CYCLIC, block_size=1MB);
    
    // Worker-Pool konfigurieren
    WorkerPool* workers = worker_pool_create(256);
    worker_pool_pin_cpus(workers, CPU_0_TO_255);
    
    // Manuelles Scheduling
    for (int epoch = 0; epoch < 1000; epoch++) {
        TaskQueue* tasks = generate_tasks(srdb, epoch);
        
        for (int i = 0; i < tasks->size; i++) {
            int worker_id = custom_schedule_policy(tasks[i]);
            worker_submit(workers, worker_id, tasks[i]);
        }
        
        // Explizite Barrier
        worker_pool_wait_all(workers);
        
        // SRDB-Update
        srdb_update_from_results(srdb, workers);
        
        // Optional: Checkpoint
        if (epoch % 100 == 0) {
            srdb_checkpoint(srdb, epoch);
        }
    }
    
    return 0;
}
```

### 9.2 Compiler und Toolchain

**KORA-Compiler-Stack:**

```
Source-Code (.c / .py)
     ↓
KORA-Frontend (clang-basiert)
- Analysiert Datenabhängigkeiten
- Detektiert parallelisierbare Schleifen
- Validiert Determinismus-Anforderungen
     ↓
KORA-Optimizer
- Loop-Tiling für Cache-Lokalität
- Task-Granularitäts-Optimierung
- SRDB-Layout-Planung
     ↓
KORA-Backend
- Code-Generation für Worker-ISA
- Scheduling-Plan-Generierung
- DMA-Transfer-Insertion
     ↓
KORA-Binary (.kora)
- Enthält: Worker-Code + Schedule + SRDB-Layout
- Kann von KORA-Core direkt geladen werden
```

**Compiler-Optimierungen (spezifisch für KORA):**

```c
// Beispiel: Automatisches Loop-Tiling

// User-Code:
for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
        C[i][j] = A[i][j] + B[i][j];
    }
}

// KORA-Compiler transformiert zu:
#define TILE_SIZE 64  // Passt in Worker-Scratchpad

for (int ii = 0; ii < N; ii += TILE_SIZE) {
    for (int jj = 0; jj < N; jj += TILE_SIZE) {
        // DMA-Transfer: Lade Tile in Scratchpad
        dma_load(scratchpad, &A[ii][jj], TILE_SIZE);
        dma_load(scratchpad + TILE_OFFSET, &B[ii][jj], TILE_SIZE);
        
        // Berechnung auf lokalem Scratchpad
        for (int i = ii; i < min(ii+TILE_SIZE, N); i++) {
            for (int j = jj; j < min(jj+TILE_SIZE, N); j++) {
                scratchpad_C[i-ii][j-jj] = 
                    scratchpad_A[i-ii][j-jj] + 
                    scratchpad_B[i-ii][j-jj];
            }
        }
        
        // DMA-Transfer: Schreibe Ergebnis zurück
        dma_store(&C[ii][jj], scratchpad_C, TILE_SIZE);
    }
}

// Vorteil: Alle Zugriffe auf lokalen Scratchpad (schnell, energieeffizient)
```

### 9.3 Debugging und Profiling

**Problem:** Ohne Unterbrechbarkeit ist klassisches Debugging unmöglich.

**KORA-Debugging-Strategie:**

**1. Dry-Run-Modus mit vollständigem Logging**

```python
# Aktiviere Debug-Modus für ersten Durchlauf
runtime = KORARuntime(num_workers=4, debug=True)  # Wenige Worker
runtime.enable_logging(level=VERBOSE)
runtime.run(my_task, srdb, epochs=10)  # Kurzer Test

# Analysiere Logs
runtime.print_task_trace()
runtime.validate_srdb_consistency()
runtime.check_for_race_conditions()

# Wenn erfolgreich: Produktionslauf ohne Debug
runtime = KORARuntime(num_workers=256, debug=False)
runtime.run(my_task, srdb, epochs=1000)
```

**2. Post-Mortem-Analyse via Checkpoints**

```c
// Bei Fehler: Rollback zu letztem Checkpoint
if (detect_error(srdb)) {
    Checkpoint* cp = load_checkpoint(last_valid_epoch);
    srdb_restore(srdb, cp);
    
    // Re-Run mit detailliertem Logging
    enable_verbose_logging();
    recompute_epoch(last_valid_epoch + 1);
    
    // Analysiere wo Fehler auftrat
    find_divergence_point();
}
```

**3. Determinismus-Validierung**

```python
# Führe gleiche Berechnung 2× aus
result1 = runtime.run(my_task, srdb, epochs=100)
result2 = runtime.run(my_task, srdb, epochs=100)

# Bit-genaue Vergleich
assert np.array_equal(result1, result2), "Non-determinism detected!"

# Wenn deterministisch: Produktionslauf ist garantiert reproduzierbar
```

**KORA-Profiler:**

```
kora-prof: Profiling-Tool für Performance-Analyse

Metriken:
- Worker-Auslastung (% Zeit in Compute vs. Idle)
- SRDB-Bandbreiten-Nutzung (% von Peak)
- Task-Verteilungs-Balance (Load-Imbalance-Faktor)
- Epochen-Overhead (% Zeit in I/O vs. Compute)

Ausgabe:
┌─────────────────────────────────────────────┐
│ KORA Profiling Report                       │
├─────────────────────────────────────────────┤
│ Total Runtime:        3.204 seconds         │
│ Compute Time:         2.890 seconds (90,2%) │
│ I/O Epochs:           0.314 seconds (9,8%)  │
│                                             │
│ Worker Utilization:                         │
│   Min:  87,3% (Worker 42)                   │
│   Avg:  91,5%                               │
│   Max:  94,2% (Worker 128)                  │
│   Load Imbalance: 6,9% (gut)                │
│                                             │
│ SRDB Bandwidth:                             │
│   Peak Available: 8.000 GB/s                │
│   Actual Used:      145 GB/s (1,8%)         │
│   Bottleneck: Keine (Compute-bound)         │
│                                             │
│ Recommendations:                            │
│ - Worker 42 hat 12% niedrigere Auslastung   │
│   → Task-Größe für diesen Worker anpassen   │
└─────────────────────────────────────────────┘
```

### 9.4 Integration mit bestehendem Code

**Wrapper für MPI-Code (Migration-Pfad):**

```c
// Klassischer MPI-Code
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    // Berechnung
    compute_local_data(rank);
    
    // Kommunikation
    MPI_Allreduce(local_result, global_result, ...);
    
    MPI_Finalize();
}

// KORA-Wrapper (minimale Änderungen)
#include <kora/mpi_compat.h>  // MPI-kompatible API

int main(int argc, char** argv) {
    KORA_MPI_Init(&argc, &argv);  // Initialisiert KORA statt MPI
    
    int rank, size;
    KORA_MPI_Comm_rank(KORA_COMM_WORLD, &rank);
    KORA_MPI_Comm_size(KORA_COMM_WORLD, &size);
    
    // Berechnung (unverändert)
    compute_local_data(rank);
    
    // Kommunikation (wird auf KORA-Epochen abgebildet)
    KORA_MPI_Allreduce(local_result, global_result, ...);
    
    KORA_MPI_Finalize();
}

// Hinter den Kulissen:
// - rank → Worker-ID
// - MPI_Allreduce → Epochen-synchronisierte Reduktion im Core
// - Deterministisch, keine echten MPI-Nachrichten
```

---

## 10. Vergleich mit verwandten Architekturen

### 10.1 KORA vs. Standard-HPC-Cluster (MPI)

| Aspekt | MPI-Cluster | KORA |
|--------|-------------|------|
| **Speichermodell** | Distributed (jeder Node eigener Memory) | Global kohärent (SRDB) |
| **Kommunikation** | Message-Passing (asynchron) | Epochen-synchronisiert |
| **Scheduling** | Dynamisch pro Node | Global deterministisch |
| **Reproduzierbarkeit** | Probabilistisch (±0,1-0,3%) | Bit-identisch |
| **Fehlertoleranz** | Checkpoint-Restart komplex | Koordiniertes Checkpointing |
| **Skalierung** | Tausende Nodes | Phase 1: Einzelknoten, Phase 2: 10-100 Nodes |
| **Programmierung** | MPI-API (explizite Kommunikation) | High-Level-Tasks |
| **Energie-Effizienz** | Baseline | 15-30% besser (Software), 80-95% besser (Hardware) |

**Wann MPI überlegen:**
- Extrem große Cluster (>1000 Nodes)
- Heterogene Hardware (CPUs + GPUs + FPGAs gemischt)
- Legacy-Code (Millionen Zeilen MPI-Anwendungen)

**Wann KORA überlegen:**
- Einzelknoten oder kleine Cluster
- Reproduzierbarkeit kritisch
- Energieeffizienz wichtiger als absolute Skalierung

### 10.2 KORA vs. GPU-Computing (CUDA/ROCm)

| Aspekt | GPU (CUDA) | KORA |
|--------|------------|------|
| **Architektur** | Tausende Threads, SIMT | Hunderte Worker, SIMD |
| **Scheduling** | Hardware-Scheduler (Warp-Scheduling) | Software (Core) |
| **Host-Device-Interaktion** | Explizite Transfers (PCIe) | Integriert (On-Die in Phase 3) |
| **Programmierung** | Kernel-basiert (C++/CUDA) | Task-basiert (Python/C) |
| **Kohärenz** | Keine (zwischen GPUs) | Global (SRDB) |
| **Determinismus** | Nein (Warp-Scheduling non-deterministisch) | Ja |
| **Einsatzbereich** | Matrix-Ops, Deep Learning | Strukturierte Big-Data, Simulationen |

**Wann GPU überlegen:**
- Extreme Parallelität (Millionen Threads)
- Matrix-lastige Workloads (ML-Training, Inferenz)
- Etabliertes Ökosystem (PyTorch, TensorFlow)

**Wann KORA überlegen:**
- Host-Device-Kommunikation ist Bottleneck
- Reproduzierbarkeit erforderlich
- Langläufer mit strukturierten Daten

### 10.3 KORA vs. Cerebras Wafer-Scale-Engine

| Aspekt | Cerebras WSE-3 | KORA (Phase 3) |
|--------|----------------|----------------|
| **Die-Größe** | 46.225 mm² (ganzer Wafer) | 2.500 mm² (großer Die) |
| **Cores** | 900.000 | 256 (aber größer, komplexer) |
| **On-Chip-Memory** | 44 GB | 128 GB (HBM-Integration) |
| **Preis** | $2-5 Millionen | $150.000-300.000 (geschätzt) |
| **Zielmarkt** | National Labs, Top-Hyperscaler | Forschungsinstitute, mittlere Hyperscaler |
| **Programmierung** | Custom-Toolchain | Standard C/Python + KORA-Extensions |
| **Fehlertoleranz** | Redundante Cores | N+K-Redundanz (16 Reserve-Tiles) |

**Gemeinsamkeiten:**
- Beide adressieren Fragmentierung durch Integration
- On-Chip-Kommunikation statt externe Links
- Spezialisiert für Langläufer

**Unterschiede:**
- Cerebras: Maximale Parallelität, maximaler Preis
- KORA: Balance zwischen Effizienz und Kosten

**Positionierung:**
Cerebras für Top 0,1%, KORA für Top 10%

### 10.4 KORA vs. FPGA-basierte Lösungen

| Aspekt | FPGA (z.B. Xilinx Versal) | KORA |
|--------|---------------------------|------|
| **Flexibilität** | Höchste (Hardware rekonfigurierbar) | Mittlere (Software-programmierbar) |
| **Performance** | Hoch (für spezifische Ops) | Hoch (für Langläufer generell) |
| **Entwicklungszeit** | Lang (HDL-Design, Synthese) | Kurz (C/Python-Code) |
| **Energieeffizienz** | Sehr hoch (Custom-Pipeline) | Hoch (Architektur-Optimierung) |
| **Kosten** | Mittel (FPGA-Boards) | Phase 1: Niedrig, Phase 3: Mittel-Hoch |

**Wann FPGA überlegen:**
- Sehr spezifische Operationen (z.B. FFT, Kryptographie)
- Hardware-Beschleunigung für Legacy-Protokolle
- Prototyping vor ASIC-Fertigung

**Wann KORA überlegen:**
- General-Purpose Big-Data (nicht ultra-spezialisiert)
- Schnelle Entwicklungszyklen
- Keine Hardware-Expertise im Team

### 10.5 KORA vs. Neuromorphe Systeme (Intel Loihi, IBM TrueNorth)

| Aspekt | Neuromorphe Chips | KORA |
|--------|-------------------|------|
| **Paradigma** | Event-Driven, Spiking-Neurons | Batch-Processing, Deterministic |
| **Energie-Effizienz** | Extrem (mW für Inferenz) | Hoch (W-Bereich) |
| **Anwendung** | Edge-AI, Sensorverarbeitung | Big-Data-Langläufer, HPC |
| **Programmierung** | Neuronal (Learning-basiert) | Imperativ (Code-basiert) |
| **Determinismus** | Nein (stochastisch) | Ja (perfekt) |

**Unterschiedliche Zieldomänen:**
- Neuromorphe: Real-time, low-power, adaptive
- KORA: Batch, high-throughput, deterministic

Keine direkte Konkurrenz, komplementär.

---

## 11. Offene Forschungsfragen

### 11.1 Skalierung auf große Cluster

**Problem:** KORA ist für Einzelknoten/kleine Cluster konzipiert. Skalierung auf 1000+ Nodes ist ungeklärt.

**Forschungsrichtungen:**

1. **Hierarchisches SRDB:**
   - Node-lokale SRDB-Fragmente
   - Cluster-weite Kohärenz nur an definierten Synchronisationspunkten
   - Trade-off: Globale Kohärenz vs. Skalierbarkeit

2. **Partitionierte Algorithmen:**
   - Domain-Decomposition mit minimaler Inter-Node-Kommunikation
   - Bulk-Synchronous-Parallel auf Cluster-Ebene
   - Optimierung: Welche Partitionierung minimiert Kommunikation?

3. **Deterministische Cluster-Netzwerke:**
   - Time-Triggered Ethernet für vorhersagbare Latenz
   - Keine spontanen Nachrichten, nur epochen-synchronisiert
   - Herausforderung: Implementierung auf Standard-Hardware

### 11.2 Adaptive Task-Granularität

**Problem:** Statisches Scheduling versagt bei heterogenen Workloads.

**Forschungsrichtungen:**

1. **Laufzeit-Profiling zur Granularitäts-Anpassung:**
   - Erste Epoche mit feiner Granularität (Profiling)
   - Analyse: Welche Tasks sind schnell/langsam?
   - Folge-Epochen: Passe Granularität dynamisch an

2. **Machine-Learning für Task-Vorhersage:**
   - Trainiere Modell: Task-Eigenschaften → Laufzeit
   - Nutze Vorhersage für bessere statische Zuteilung
   - Herausforderung: Overfitting bei neuen Workloads

### 11.3 Formale Verifikation

**Problem:** Determinismus ist behauptet, aber nicht mathematisch bewiesen.

**Forschungsrichtungen:**

1. **Model-Checking für KORA-Scheduler:**
   - Formale Spezifikation in TLA+ oder Coq
   - Beweis: Gleiche Eingabe → gleiche Ausgabe (immer)
   - Herausforderung: State-Space-Explosion bei 256 Workern

2. **Runtime-Verification:**
   - Instrumentierung für Trace-Validierung
   - Vergleiche Traces zwischen Runs
   - Automatische Divergenz-Detektion

### 11.4 Integration mit KI-Frameworks

**Problem:** PyTorch/TensorFlow erwarten asynchrones, dynamisches Scheduling.

**Forschungsrichtungen:**

1. **KORA-Backend für PyTorch:**
   - Übersetze PyTorch-Graphen in KORA-Tasks
   - Ersetzt cuDNN/NCCL durch KORA-Primitives
   - Herausforderung: Dynamische Graphen (z.B. RNNs)

2. **Batch-Compiler für statische Graphen:**
   - Nutze TorchScript oder ONNX für statische Analyse
   - Generiere KORA-Binary aus statischem Graphen
   - Training dann unterbrechungsfrei, reproduzierbar

---

## 12. Zusammenfassung und Ausblick

### 12.1 Architektonische Kernpunkte

KORA ist eine **kohärenz-orientierte Rechenarchitektur**, die durch strukturelle Entscheidungen Effizienz und Determinismus erreicht:

1. **KORA-Core als zentrale Orchestrierung** eliminiert verteilte Scheduling-Komplexität
2. **Passive Worker ohne Autonomie** verhindern non-deterministische Race-Conditions
3. **SRDB als globales Datenmodell** garantiert Kohärenz ohne komplexe Protokolle
4. **Epochen-basiertes I/O** schirmt gegen asynchrone Störungen ab
5. **Monolithische Hardware (Phase 3)** eliminiert Inter-Chip-Overhead fundamental

### 12.2 Technologische Herausforderungen

**Kurzfristig (Phase 1):**
- Software-Overhead auf Standard-Hardware minimieren
- Validierung: Können 15-30% Verbesserung erreicht werden?
- Adoption: Interesse von Forschungsinstituten wecken

**Mittelfristig (Phase 2):**
- MCM-Design mit akzeptablem Yield (>50%)
- Inter-Tile-Interconnect-Optimierung
- Toolchain-Reife (Compiler, Debugger, Profiler)

**Langfristig (Phase 3):**
- 2.500 mm² monolithischer Die bei 60-80% Yield
- Energie-Effizienz 80-95% besser als Standard
- Amortisation in 2-3 Jahren für Hyperscaler

### 12.3 Wissenschaftlicher Beitrag

KORA ist **keine inkrementelle Verbesserung**, sondern ein **systemischer Neuansatz**:

- **Nicht neu:** Batch-Processing, Determinismus, Kohärenz existierten in frühen Computern
- **Neu:** Integration dieser Prinzipien für moderne Big-Data-Workloads
- **Beitrag:** Zeigt, dass "Zurück zu den Wurzeln" für spezifische Domänen überlegen ist

Die Architektur demonstriert: **Komplexität ist nicht notwendig, Einfachheit skaliert besser** – wenn die Anwendungsdomäne klar definiert ist.

### 12.4 Vision für 2030+

Wenn KORA erfolgreich ist:

```
2027: KORA-Software ist Standard in 10+ Forschungsinstituten
2029: Erste monolithische KORA-Chips in Produktion
2031: KORA wird für Big-Data-Langläufer zum "Best Practice"
2033: Wafer-Scale-KORA für Exascale-Anwendungen
2035: KORA-Prinzipien beeinflussen nächste CPU/GPU-Generation
```

Wenn KORA scheitert, ist der Beitrag dennoch wertvoll:
- Empirische Daten über Trade-offs (Interaktivität vs. Kohärenz)
- Open-Source-Implementierung als Forschungsplattform
- Sensibilisierung für Reproduzierbarkeit in Scientific Computing

---

**Ende der Architektur-Spezifikation**

**Lizenz:** CC-BY-SA 4.0  
**Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
**Kontakt:** adamsfke@proton.me  
**Letzte Aktualisierung:** November 2025
