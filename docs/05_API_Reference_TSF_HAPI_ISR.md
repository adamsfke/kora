# KORA - API Reference – TSF, HAPI, ISR  

**Autoren:** Frank Meyer  
**Version:** 2.0 (November 2025)  
**Lizenz:** CC-BY-SA 4.0  
**Dokumenttyp:** API-Referenz  
**Status:** Konzeptphase

---

***Inhaltsverzeichnis***

    1. Einleitung
    2. TSF — Tensor Sequence Format
    3. ISR — Intermediate State Representation
    4. HAPI — Hardware Abstraction & Processing Interface
    5. Zusammenspiel TSF – ISR – HAPI
    6.  SF – Erweiterte Instruktionsreferenz
    7.  SF – Vollständige Opcode-Tabelle
    8.  SR – Validierungs- und Hash-Mechanismen
    9.  SR – Validierungsalgorithmus
    10. HAPI – Statuscodes
    11. HAPI – Vollständige Funktionsreferenz
    12. Vollständiger Ablauf: TSF → HAPI → ISR
    13. Abschluss
    14. Deterministische Garantien über alle Ebenen
    15. Versionierung von TSF-, ISR- und HAPI-Dateien
    16. Fehlertoleranz und deterministische Fehlerklassen
    17. Golden Runs und Validierung
    18. Beispiel: Schrittweiser Ablauf (vollständig)
    19. Kompatibilität zu Architektur B und C
    20. Sicherheit und Auditierbarkeit
    21. Zusammenfassung

---

## 1. Einleitung
Dieses Dokument spezifiziert die drei zentralen API-Schichten der KORA-Architektur:

    TSF  – Tensor Sequence Format
    ISR  – Intermediate State Representation
    HAPI – Hardware Abstraction & Processing Interface

Gemeinsam bilden sie den vollständigen deterministischen Ausführungsstack von KORA.  
TSF definiert die Operationen, ISR den Zustand, und HAPI die Bindung an deterministische Hardware (Architektur C) sowie deren Emulation (Architektur B).

Ziel dieser Spezifikation:

    • deterministische Ausführung
    • vollständige Reproduzierbarkeit
    • hardwareunabhängige Modellbeschreibung
    • auditierbare Daten- und Ausführungswege
    • durchgängige Konsistenz zwischen Software und Hardware

Gültig für:

    Architecture B – KORA-SW (Softwaredeterminismus)
    Architecture C – KORA-HW (Hardwaredeterminismus)

---

## 2. TSF — Tensor Sequence Format

TSF ist das deterministische Modellformat von KORA.  
Es beschreibt jede Operation, jeden Speicherzugriff, jede Reduktion und jede Synchronisation vollständig und explizit.  
Keine impliziten Layouts. Keine dynamischen Kernel. Keine nichtdeterministische Parallelität.

TSF ersetzt:

    • Graph-IR
    • nichtdeterministische Kernel-Aufrufe
    • dynamische Reduktionen
    • implizite Scheduling-Entscheidungen

TSF ist:

    • sequentiell
    • deterministisch
    • vollständig auditierbar
    • hardwareunabhängig

### 2.1 TSF-Fundamentalprinzipien

    1. Jede Operation ist vollständig spezifiziert.
    2. Jeder Speicherzugriff ist explizit.
    3. Jede Reduktion ist deterministisch (Tree-ID + Order-ID).
    4. Jede Synchronisation ist explizit.
    5. Der globale Zustand ist aus TSF ableitbar (ISR).
    6. Keine impliziten Layout- oder Optimierungsentscheidungen.

### 2.2 TSF-Dateiheader

    TSF_VERSION:     2.0
    ARCH_PROFILE:    B | C
    MODEL_NAME:      <string>
    GLOBAL_SEED:     <uint64>
    OP_COUNT:        <uint64>
    TENSOR_COUNT:    <uint64>
    REDUCTION_TREES: <uint32>

### 2.3 TSF-Tensor-Deklaration

    TENSOR <ID>:
        dtype: float32 | float64 | int32 | int64
        shape: [d1, d2, ...]
        init: ZERO | RAND_SEEDED(<uint64>) | CONST(<value>)
        address: <uint64>
        layout: ROW_MAJOR

### 2.4 TSF-Operationen (Kerninstruktionen)

Alle Operationen folgen:

    OP <SEQ_ID>:
        type: <OP_TYPE>
        in:  [<tensor_ids>]
        out: [<tensor_ids>]
        fp_mode: STRICT | RELAXED
        order: <uint64>

OP_TYPE-Kategorien:

    elementwise.add
    elementwise.mul
    matmul
    conv2d
    reduce.sum
    reduce.max
    reduce.mean
    reshape
    transpose
    gather
    scatter
    activation.relu
    activation.softmax
    loss.crossentropy
    optimizer.adam.update
    scheduler.step

### 2.5 Deterministische Reduktionen

    REDUCTION:
        tree_id: <uint32>
        order_id: <uint64>
        fanin: 2 | 4 | 8
        seq: [<seq_ids>]

Jede Reduktion ist bitgenau deterministisch.

### 2.6 Synchronisation

    SYNC <SEQ_ID>:
        barrier: GLOBAL | TILE_LOCAL
        fence:   READ | WRITE | READWRITE

### 2.7 Deterministische Speicher- und Transferoperationen

    TRANSFER:
        src: <tensor_id>
        dst: <tensor_id>
        window: <dma_window_id>

### 2.8 Abschlussbedingungen

    END_STATE_HASH: <uint256>
    FP_HASH:        <uint256>
    SEQ_HASH:       <uint256>

TSF ist damit ein vollständig reproduzierbarer Ausführungsvertrag.

---

## 3. ISR — Intermediate State Representation

ISR beschreibt den vollständigen Maschinenzustand zu jedem Zeitpunkt einer TSF-Ausführung.  
Sie dient zur:

    • Debugging-Nachvollziehbarkeit
    • Golden-Run-Verifizierung
    • Auditierbarkeit
    • deterministischen Fehleranalyse

### 3.1 ISR-Grundstruktur

    ISR:
        cycle: <uint64>
        active_tile: <uint32>
        seq_id: <uint64>
        fp_state: <fp registers>
        mem_map: <tensor_id -> address>
        tree_state: <reduction state>
        dma_state: <dma windows>
        hash_state: <uint256>

### 3.2 FP-Registerzustand

    FP_STATE:
        registers: [
            { mantissa: u64, exponent: u32, flags: {...} },
            ...
        ]
        rounding_mode: TIES_TO_EVEN

### 3.3 Tile-Zustand

    tile_state:
        pc: <uint64>
        regs: <vector registers>
        sync: <barrier state>

### 3.4 DMA-Fenster

    dma_window:
        id: <uint32>
        start_addr: <uint64>
        length: <uint64>
        open: TRUE | FALSE

### 3.5 Zustandshashes

    STATE_HASH = H(seq_id || fp_state || mem_map || tree_state || dma_state)

---

## 4. HAPI — Hardware Abstraction & Processing Interface

HAPI ist die deterministische Hardwareschnittstelle für:

    • Architektur C (native)
    • Architektur B (emuliert)

Ziele:

    • absolute Bitreproduzierbarkeit
    • feste Pipeline-Latenzen
    • deterministische Speicherverwaltung
    • deterministische DMA-Fenster
    • deterministische Tile-Zuweisung

### 4.1 Funktionsklassen

    1. Speicherverwaltung
    2. DMA-Kontrolle
    3. FP-Pipeline
    4. Tile-Ausführung
    5. Scheduling-Bindung

### 4.2 Speicherfunktionen

    addr = hapi_alloc(tensor_id, size, alignment)
    hapi_free(tensor_id)
    hapi_memcpy(dst, src, size)

### 4.3 DMA-Fenster

    hapi_dma_open(window_id, start, length)
    hapi_dma_close(window_id)

### 4.4 FP-Pipeline

    out = hapi_fp_op(opcode, a, b)
    hapi_fp_mode(STRICT | RELAXED)

### 4.5 Tile-Steuerung

    hapi_tile_run(tile_id, seq_id)
    hapi_tile_barrier(tile_id)

### 4.6 Scheduling

    hapi_schedule_bind(seq_id, tile_id)
    next_id = hapi_schedule_next(tile_id)

---

## 5. Zusammenspiel TSF – ISR – HAPI

Der KORA-Stack funktioniert wie folgt:

    TSF   = beschreibt die Operationen
    ISR   = beschreibt den Zustand
    HAPI  = führt deterministisch aus

Der Workflow:

1. TSF lädt Modell  
2. HAPI erzeugt deterministische Speicherzuordnung  
3. TSF bestimmt Operationen  
4. HAPI weist sie deterministisch zu  
5. ISR dokumentiert jeden Zustand  
6. State Hash verifiziert Reproduzierbarkeit

Das Ergebnis:

    absolute Deterministik  
    bitgenaue Ausführung  
    vollständige Auditierbarkeit  
	
---

## 6. TSF – Erweiterte Instruktionsreferenz

Dieser Abschnitt beschreibt alle Kerninstruktionen von TSF im Detail, einschließlich Syntax, semantischer Regeln und deterministischer Bindung.

### 6.1 Elementare Operationen

#### 6.1.1 elementwise.add

    OP <SEQ_ID>:
        type: elementwise.add
        in:  [A, B]
        out: [C]
        fp_mode: STRICT
        order: <uint64>

Regeln:
- A, B und C müssen gleiche Form besitzen
- Ergebnis ist deterministisch, da keine parallele Reduktion stattfindet

#### 6.1.2 elementwise.mul

    OP <SEQ_ID>:
        type: elementwise.mul
        in:  [A, B]
        out: [C]
        fp_mode: STRICT
        order: <uint64>

#### 6.1.3 matmul

    OP <SEQ_ID>:
        type: matmul
        in:  [A, B]
        out: [C]
        fp_mode: STRICT
        order: <uint64>

Regeln:
- Matmul ist intern als sequentielle FP-Operation definiert
- Keine Blockparallelität erlaubt (anders als bei GPU-Kerneln)
- Exakte FP-Pfad-Reihenfolge garantiert

### 6.2 Reduktionen (kritischer TSF-Bereich)

#### 6.2.1 reduce.sum

    OP <SEQ_ID>:
        type: reduce.sum
        in:  [A]
        out: [B]
        reduction:
            tree_id: <uint32>
            order_id: <uint64>
            fanin: 2 | 4 | 8
            seq: [<seq_ids>]

Regeln:
- Die Reihenfolge der Summation ist fixiert.
- Fan-In darf nicht dynamisch gewählt werden.
- Tree-ID ist global eindeutig.

#### 6.2.2 reduce.max

Wie reduce.sum, jedoch mit deterministischer Auswahlregel:

- Bei Gleichstand gewinnt der kleinere Index (Tie-Break).

#### 6.2.3 reduce.mean

Implementiert als:

    mean(x) = sum(x) / N

wobei sum(x) die deterministische reduce.sum-Operation ist.

### 6.3 Datenlayout-Operationen

#### 6.3.1 reshape

    OP <SEQ_ID>:
        type: reshape
        in:  [A]
        out: [B]

Bemerkung:
- Keine implizite Kopie; reinterpretation only.

#### 6.3.2 transpose

    OP <SEQ_ID>:
        type: transpose
        in:  [A]
        out: [B]

Keine Parallelisierung, deterministische Indextransformation.

### 6.4 Speicher- und Transferinstruktionen

#### 6.4.1 alloc

    OP <SEQ_ID>:
        type: memory.alloc
        tensor: T
        size: <bytes>
        alignment: 64

#### 6.4.2 free

    OP <SEQ_ID>:
        type: memory.free
        tensor: T

Das Freigeben löscht deterministisch den Tensorbereich (Zeroization).

#### 6.4.3 transfer

    OP <SEQ_ID>:
        type: memory.transfer
        src: A
        dst: B
        window: <dma_window_id>

Fenster wird durch HAPI garantiert (siehe Abschnitt HAPI).

---

## 7. TSF – Vollständige Opcode-Tabelle

Die folgende Tabelle definiert alle Instruktionen, die in TSF zulässig sind.

### 7.1 Liste der OP_TYPE-Werte

    elementwise.add
    elementwise.mul
    elementwise.sub
    elementwise.div
    matmul
    conv2d
    reduce.sum
    reduce.max
    reduce.mean
    reshape
    transpose
    gather
    scatter
    activation.relu
    activation.softmax
    loss.crossentropy
    optimizer.adam.update
    scheduler.step
    memory.alloc
    memory.free
    memory.transfer
    sync.barrier
    sync.fence

Jede Instruktion ist vollständig deterministisch beschrieben.  
Keine impliziten Argumente. Keine dynamischen Entscheidungen. Keine nichtdeterministische Parallelität.

---

## 8. ISR – Validierungs- und Hash-Mechanismen

ISR ist die deterministische Abbildung des Maschinenzustandes.  
Dieser Abschnitt definiert, wie ISR validiert und verifiziert wird.

### 8.1 Hashing des globalen Zustands

Nach jeder Operation:

    STATE_HASH(k) = H(
        seq_id ||
        fp_registers ||
        memory_map ||
        tree_state ||
        dma_state
    )

Der Hash dient drei Zwecken:

1. Golden Run Validierung  
2. Multi-Tile Konsistenzprüfung  
3. Debugging und Auditierbarkeit  

### 8.2 FP-Registerzustand

Beispielstruktur:

    FP_STATE:
        registers: [
            { mantissa: u64, exponent: u32, flags: {...} },
            ...
        ]
        rounding_mode: TIES_TO_EVEN

Regeln:
- Jeder FP-Schritt erzeugt einen deterministischen Zustand
- Flags sind integraler Bestandteil des Hashes

### 8.3 Speicherzuordnung

    mem_map:
        tensor_id -> physical_address

Diese Bindung ist fix, deterministisch und Teil der globalen Identität.

### 8.4 Reduktionszustand

    tree_state:
        active_nodes: [...]
        leaf_values: [...]
        combine_sequence: order_id

Garantiert vollständig rekonstruierbar.

---

## 9. ISR – Validierungsalgorithmus

Der Validierungsalgorithmus prüft:

1. Sequenzkonsistenz  
2. Speicherintegrität  
3. FP-Kohärenz  
4. Reduktionsstruktur  
5. DMA-Fensterzustand  

Algorithmus:

    function isr_validate(current_state, expected_state):
        if current_state.seq_id != expected_state.seq_id:
            return SEQ_MISMATCH

        if current_state.fp_state != expected_state.fp_state:
            return FP_MISMATCH

        if current_state.mem_map != expected_state.mem_map:
            return MEM_MISMATCH

        if current_state.tree_state != expected_state.tree_state:
            return TREE_MISMATCH

        if current_state.dma_state != expected_state.dma_state:
            return DMA_MISMATCH

        if hash(current_state) != expected_state.state_hash:
            return HASH_MISMATCH

        return OK

---

## 10. HAPI – Statuscodes

HAPI-Funktionen geben immer einen dieser deterministischen Statuscodes zurück:

    HAPI_OK
    HAPI_ERR_INVALID_ARGUMENT
    HAPI_ERR_OUT_OF_MEMORY
    HAPI_ERR_DMA_WINDOW_INVALID
    HAPI_ERR_FP_EXCEPTION
    HAPI_ERR_TILE_BUSY
    HAPI_ERR_SCHEDULING_CONFLICT
    HAPI_ERR_ILLEGAL_ADDRESS
    HAPI_ERR_ALIGNMENT
    HAPI_ERR_UNSUPPORTED_OPCODE

Diese Codes sind vollständig definierte Teilmenge –  
keine dynamischen Systemfehler, keine OS-bedingten Fehler.

---

## 11. HAPI – Vollständige Funktionsreferenz

### 11.1 Speicherverwaltung

#### hapi_alloc

    addr = hapi_alloc(tensor_id, size, alignment)

Regeln:
- Ausrichtung >= 64 Byte
- Adresse unveränderlich während Laufzeit

#### hapi_free

    hapi_free(tensor_id)

### 11.2 DMA-Fenster

#### hapi_dma_open

    hapi_dma_open(window_id, start_addr, length)

#### hapi_dma_close

    hapi_dma_close(window_id)

Fensteröffnungen sind deterministisch festgelegt.  
Keine dynamische Mobilität.

### 11.3 FP-Pipeline

#### hapi_fp_op

    out = hapi_fp_op(opcode, a, b)

Opcode erlaubt:
- add
- sub
- mul
- div
- fused_multiply_add

#### hapi_fp_mode

    hapi_fp_mode(STRICT | RELAXED)

STRICT = bitidentisch mit C-Architektur  
RELAXED = gleiche Reihenfolge, aber tolerant gegenüber Subnormal-Unterdrückung

### 11.4 Tile-Steuerung

#### hapi_tile_run

    hapi_tile_run(tile_id, seq_id)

#### hapi_tile_barrier

    hapi_tile_barrier(tile_id)

### 11.5 Scheduling-Bindung

#### hapi_schedule_bind

    hapi_schedule_bind(seq_id, tile_id)

Bindet Operation an festen Tile.

#### hapi_schedule_next

    next_id = hapi_schedule_next(tile_id)

Gibt deterministisch die nächste Operation auf diesem Tile zurück.

---

## 12. Vollständiger Ablauf: TSF → HAPI → ISR

1. TSF lädt Modell  
2. TSF deklariert Tensoren  
3. HAPI erstellt deterministische Speicherabbildung  
4. TSF sendet OP <SEQ_ID>  
5. HAPI führt Operation deterministisch aus  
6. ISR dokumentiert Zustand  
7. STATE_HASH geprüft  
8. Nächste Operation gemäß Scheduling Tree  
9. Am Ende:  
       FP_HASH  
       SEQ_HASH  
       END_STATE_HASH  
werden generiert.

---

## 13. Abschluss

TSF, ISR und HAPI bilden zusammen den deterministischen Ausführungsstack der KORA-Architektur. Sie garantieren:

- bitgenaue Wiederholbarkeit  
- deterministische Energieprofile  
- eindeutige Speicherzuordnung  
- auditierbare Ausführung  
- vollständige Hardware/Software-Kohärenz  

Dieses Dokument definiert Version 2.0 der API-Spezifikation und bildet die Grundlage für:

- deterministische KORA-SW-Implementierungen  
- zukünftige KORA-Hardware (Profil C)  
- wissenschaftliche Validierung  
- regulatorische Prüfpfade  

---

## 14. Deterministische Garantien über alle Ebenen

Dieses Kapitel fasst die deterministischen Eigenschaften zusammen, die durch die Kombination aus TSF, HAPI und ISR gewährleistet werden.

### 14.1 Operationale Deterministik
- Reihenfolge aller Operationen garantiert (SEQ_ID)
- Keine dynamischen Kernel-Dispatches
- Keine Parallelisierungsentscheidungen zur Laufzeit
- Keine race conditions
- Kein Scheduling-Jitter

### 14.2 Numerische Deterministik
- feste FP-Pipeline
- deterministischer Rundungsmodus (TIES_TO_EVEN)
- deterministische Reduktionsbäume
- deterministischer Umgang mit Subnormalzahlen (STRICT)
- bitidente FP-Ausgabe (Architektur C)

### 14.3 Speicher-Deterministik
- deterministische physische Adressen
- keine Caches
- keine dynamischen Zuordnungen
- DMA-Bereiche vollständig deterministisch geöffnet und geschlossen
- konstante Speicherlatenzen

### 14.4 Kommunikations-Deterministik
- feste DMA-Fenster
- feste Transferpfade
- keine variable Interconnect-Latenz
- keine dynamischen Routen

### 14.5 Ausführungs-Deterministik
- konstante Pipeline-Latenzen
- deterministische Tile-Zuweisung
- deterministische Synchronisation
- deterministische Befehlskette über TSF

---

## 15. Versionierung von TSF-, ISR- und HAPI-Dateien

TSF-, ISR- und HAPI-Dateien sind versioniert, um vollständige Kompatibilität und Prüfbarkeit zu sichern.

### 15.1 TSF-Versionierung
Jede TSF-Datei enthält:

    TSF_VERSION: 2.0
    ARCH_PROFILE: B | C
    MODEL_VERSION: <string>

Regeln:
- TSF-Version definiert das Dateiformat
- ARCH_PROFILE definiert die Zielarchitektur
- MODEL_VERSION ist beliebig

### 15.2 ISR-Versionierung

ISR speichert den Zustand:

    ISR_VERSION: 2.0
    STATE_HASH: <uint256>

Regeln:
- HASH ist der primäre Prüfschlüssel
- ISR-Version garantiert vollständige Strukturkompatibilität

### 15.3 HAPI-Versionierung

HAPI-Anfragen enthalten:

    HAPI_VERSION: 2.0

Dies stellt sicher, dass:

- Hardware und Software dieselbe Semantik nutzen
- deterministische Ausführung konsistent bleibt

---

## 16. Fehlertoleranz und deterministische Fehlerklassen

KORA erlaubt Fehler, aber nur **deterministische Fehler**.

### 16.1 Harte Fehler (deterministische Abbrüche)

    ERR_ILLEGAL_ADDRESS  
    ERR_FP_EXCEPTION  
    ERR_SCHEDULING_CONFLICT  
    ERR_ALIGNMENT  

Regeln:
- Fehler reproduzierbar
- kein undefiniertes Verhalten
- jedes Verhalten auditierbar

### 16.2 Weiche Fehler (deterministische Zustandsänderungen)

    ERR_DMA_WINDOW_INVALID  
    ERR_TILE_BUSY  

Regeln:
- Zustand bleibt wohldefiniert
- ISR dokumentiert den Zustand
- Wiederholung ergibt denselben Fehler

---

## 17. Golden Runs und Validierung

Ein Golden Run ist die Referenzausführung eines TSF-Modells und umfasst:

    1. TSF-Datei  
    2. ISR-Trace  
    3. END_STATE_HASH  
    4. FP_HASH  
    5. SEQ_HASH  

Die Validierung erfolgt durch:

    replay -> compare -> verify

### 17.1 Golden Run Erzeugung

    1. TSF laden  
    2. HAPI-Bindung erstellen  
    3. deterministische Ausführung  
    4. ISR erfassen  
    5. HASH generieren  
    6. Archivieren  

### 17.2 Golden Run Prüfung

    for each step:
        isr_validate(current_state, golden_state)
    verify(END_STATE_HASH)
    verify(FP_HASH)
    verify(SEQ_HASH)

Wenn alle Hashes identisch sind → Modell ist gültig.

---

## 18. Beispiel: Schrittweiser Ablauf (vollständig)

Ein Beispielablauf eines deterministischen TSF-Modells:

### 18.1 Beispiel-Tensoren

    TENSOR 1:
        dtype: float32
        shape: [1024, 1024]
        init: RAND_SEEDED(1234)
        address: 0x000000100000

    TENSOR 2:
        dtype: float32
        shape: [1024, 1024]
        init: ZERO
        address: 0x000000200000

    TENSOR 3:
        dtype: float32
        shape: [1024, 1024]
        address: 0x000000300000

### 18.2 Beispiel-Operationen

    OP 1:
        type: matmul
        in:  [1, 2]
        out: [3]
        fp_mode: STRICT
        order: 1

    OP 2:
        type: reduce.sum
        in:  [3]
        out: [4]
        reduction:
            tree_id: 1
            order_id: 42
            fanin: 4
            seq: [2, 3, 4, 5]
        fp_mode: STRICT
        order: 2

### 18.3 HAPI-Ausführung

HAPI erstellt deterministische Speicherzuordnung:

    addr(TENSOR 1) = 0x100000
    addr(TENSOR 2) = 0x200000
    addr(TENSOR 3) = 0x300000

Dann wird OP 1 auf Tile 0 gebunden:

    hapi_schedule_bind(seq_id=1, tile_id=0)
    hapi_tile_run(tile_id=0, seq_id=1)

ISR nach OP 1:

    seq_id: 1
    fp_registers: deterministic
    mem_map: stable
    state_hash: H1

OP 2:

    hapi_schedule_bind(seq_id=2, tile_id=0)
    hapi_tile_run(tile_id=0, seq_id=2)

ISR nach OP 2:

    seq_id: 2
    tree_state: deterministic
    state_hash: H2

### 18.4 Golden Run

Abschluss:

    FP_HASH: F
    SEQ_HASH: S
    END_STATE_HASH: H2

---

## 19. Kompatibilität zu Architektur B und C

### 19.1 Architektur B (Software)

- HAPI wird vollständig emuliert
- DMA-Fenster sind virtuelle Fenster
- FP-Pipeline wird simuliert
- STATE_HASH identisch zu Architektur C, solange STRICT verwendet wird

### 19.2 Architektur C (Hardware)

- HAPI ist die native Hardware-Schnittstelle
- alle Latenzen sind konstant
- alle PF-Pfade sind fix
- DMA ist fest verdrahtet
- TSF → HAPI → ISR erfolgt ohne Abweichung

---

## 20. Sicherheit und Auditierbarkeit

KORA ist nicht nur deterministisch, sondern auch:

### 20.1 auditierbar
Jeder Schritt ist reproduzierbar.

### 20.2 überprüfbar
Jeder Zustand ist prüfbar.

### 20.3 nachvollziehbar
TSF ist vollständig transparent.

### 20.4 sicher
Keine dynamische Code-Injektion,  
keine unkontrollierbaren Speicherbereiche.

---

## 21. Zusammenfassung

Dieses Dokument spezifiziert:

- TSF als deterministisches Modellformat  
- ISR als deterministische Zustandsrepräsentation  
- HAPI als deterministische Hardware-API  

Gemeinsam bilden sie die Grundlage für:

- reproduzierbare KI  
- reproduzierbare CFD  
- reproduzierbare Big-Data-Systeme  
- regulatorisch relevante Anwendungen  
- zukünftige KORA-Hardware (Profil C)

Dieses Modul schließt die softwareseitige Definition der KORA v2.0 Architektur ab.

---

## Versionierung

- **Dokument:** `05_API_Reference_TSF_HAPI_ISR.md`  
- **Version:** **2.0**  
- **Simulationsmodell:** **M3.0**  
- **Veröffentlichung:** November 2025  
- **Code-Repository:** https://github.com/adamsfke/kora  
- **Vollständige KORA-Dokumentation:** https://osf.io/8wyec  
- **Kontakt:** mailto:adamsfke@proton.me  

