#!/usr/bin/env python3
"""
KORA Simulation Engine v3.0

Realmodell mit:
- Compute (FLOPs)
- Memory (Bandbreite / Latenz)
- Communication (Interconnect)
- Synchronisation (globale Barrieren)

Drei Architekturen:
    A: Standard HPC/KI-Cluster
    B: KORA-SW (optimierte SW auf Standard-HW)
    C: KORA-HW Monolith

Fünf Workloads:
    BERT    : FLOP-limitiert
    BD_S    : Big-Data Small (lokales ETL)
    BD_L    : Big-Data Large (Cluster-ETL)
    CFD_M   : CFD Medium (Engineering-Fall)
    CFD_L   : CFD Large (Klima/Wetter, 24h-Fall)

Hinweis:
- Pro Workload wird ein Kalibrierfaktor S_W berechnet, so dass
  Architektur A (Standard) die angegebene Referenzzeit exakt trifft.
- Die relativen Unterschiede A/B/C stammen aus den Architekturparametern.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


# ---------------------------------------------------------------------------
# Datenklassen
# ---------------------------------------------------------------------------

@dataclass
class Architecture:
    name: str
    key: str

    # Compute
    compute_throughput: float   # FLOPs/s oder Ops/s (für FLOP-Term)
    compute_overhead: float     # dimensionslos, z.B. 1.9

    # Memory
    mem_bw_seq: float           # GB/s (sequentiell, effektiv)
    mem_bw_rnd: float           # GB/s (random, effektiv)
    mem_latency_ns: float       # ns (mittlere Zugriffs-Latenz)

    # Interconnect / Communication
    net_bw_gb: float            # GB/s (effektiv)
    net_latency_us: float       # µs (pro Nachricht)

    # Synchronisation
    sync_latency_ms: float      # ms (globale Barrier)

    # Energie / Reproduzierbarkeit
    power_base: float           # W (inkl. Kühlung)
    r_bit: float                # Bit-Reproduzierbarkeit [0..1]
    r_run: float                # effektive Runs (1.10 = 10% Zusatzläufe)


@dataclass
class Workload:
    name: str
    key: str

    # FLOPs-basierter Anteil (Compute)
    flops_total: float          # FLOPs (0 möglich, wenn irrelevant)

    # Datenvolumen (für Memory-Term)
    data_bytes: float           # Bytes (gesamt, grobe Abschätzung)

    # Kommunikationsparameter (pro Iteration)
    n_iter: int                 # Iterationszahl (0, wenn nicht iterativ modelliert)
    n_msg_per_iter: int         # Anzahl Nachrichten pro Iteration
    msg_bytes_per_iter: float   # Bytes Gesamtvolumen pro Iteration

    # Synchronisation
    n_sync_total: int           # Anzahl globaler Barrieren (gesamt)

    # Referenzzeit (Architektur A)
    ref_time_s: float           # reale Referenzzeit in s


@dataclass
class SimulationResult:
    workload_key: str
    arch_key: str
    workload_name: str
    arch_name: str

    t_compute: float            # [s]
    t_mem: float                # [s]
    t_comm: float               # [s]
    t_sync: float               # [s]

    t_total: float              # [s] (vor r_run)
    t_eff: float                # [s] (inkl. r_run)

    energy: float               # [J] (vor r_run)
    energy_eff: float           # [J] (inkl. r_run)

    speedup: float              # relative Beschleunigung vs A
    energy_saving: float        # relative Energieersparnis vs A (0..1)

    r_bit: float
    r_run: float


# ---------------------------------------------------------------------------
# Architektur-Definitionen (realistisch, aber anpassbar)
# ---------------------------------------------------------------------------

def get_architectures_v3() -> Dict[str, Architecture]:
    """
    Definiert die drei Architekturen für das v3.0-Realmodell.
    Werte sind konservativ gewählt und direkt kommentiert.
    """

    # Annahme: eine Node-Konfiguration auf HPC-Niveau

    archs: Dict[str, Architecture] = {}

    # A: Standard HPC/KI-Cluster
    archs["A"] = Architecture(
        name="Standard HPC/KI-Cluster",
        key="A",

        # Compute: wie in v2.0
        compute_throughput=0.8e15,   # FLOPs/s sustained
        compute_overhead=1.9,        # 40–60% Overhead -> Faktor ~1.9

        # Memory (effektive Bandbreiten, konservativ)
        mem_bw_seq=200.0,            # GB/s
        mem_bw_rnd=30.0,             # GB/s
        mem_latency_ns=100.0,        # ns

        # Interconnect (effektiv, keine Peak-Werte)
        net_bw_gb=3.0,               # GB/s, realistisch mit Contention
        net_latency_us=80.0,         # µs, Allreduce/CFD-relevant

        # Synchronisation (globale Barrier-Kosten)
        sync_latency_ms=20.0,        # ms

        # Power & Reproduzierbarkeit
        power_base=8600.0,           # W
        r_bit=0.4,
        r_run=1.10,
    )

    # B: KORA-SW auf Standard-HW
    archs["B"] = Architecture(
        name="KORA-SW (optimierte Software)",
        key="B",

        # Compute: etwas bessere Auslastung
        compute_throughput=0.88e15,  # +10%
        compute_overhead=1.3,        # stark reduzierte Overheads

        # Memory
        mem_bw_seq=240.0,            # GB/s
        mem_bw_rnd=40.0,             # GB/s
        mem_latency_ns=60.0,         # ns

        # Interconnect
        net_bw_gb=4.0,               # GB/s
        net_latency_us=40.0,         # µs

        # Synchronisation
        sync_latency_ms=8.0,         # ms

        # Power & Reproduzierbarkeit
        power_base=6900.0,           # W
        r_bit=0.8,
        r_run=1.02,
    )

    # C: KORA-HW Monolith (realistisch kalibriert)
    archs["C"] = Architecture(
        name="KORA-HW Monolith",
        key="C",

        # Compute: ~3x A, aber nicht perfekt
        compute_throughput=2.4e15,
        compute_overhead=1.10,

        # Memory: deutlich besser als A, aber nicht „magisch“
        mem_bw_seq=320.0,      # GB/s
        mem_bw_rnd=60.0,       # GB/s
        mem_latency_ns=25.0,   # ns

        # Interconnect: on-die / lokal, aber mit realen Latenzen
        net_bw_gb=16.0,        # GB/s
        net_latency_us=10.0,   # µs

        # Synchronisation: sehr schnell, aber nicht 0
        sync_latency_ms=1.0,   # ms

        # Power & Reproduzierbarkeit
        power_base=1200.0,     # W (inkl. Kühlung)
        r_bit=1.0,
        r_run=1.00,
    )


    return archs


# ---------------------------------------------------------------------------
# Workload-Definitionen
# ---------------------------------------------------------------------------

def get_workloads_v3() -> Dict[str, Workload]:
    """
    Definiert die fünf Workloads inkl. realer Referenzzeiten für A.
    FLOPs und Volumina sind so gewählt, dass sie konsistent mit v2.0 bleiben.
    """

    DAY = 24 * 3600.0

    w: Dict[str, Workload] = {}

    # 1) BERT-Large (FLOP-limitiert)
    w["BERT"] = Workload(
        name="BERT-Large Training",
        key="BERT",
        flops_total=4.224e20,
        data_bytes=0.0,          # Memory wird hier vernachlässigt
        n_iter=0,
        n_msg_per_iter=0,
        msg_bytes_per_iter=0.0,
        n_sync_total=0,
        ref_time_s=3.5 * DAY,    # ~3,5 Tage
    )

    # 2) Big-Data Small
    # 6.48e9 Elemente @8 Byte ≈ 52 GB
    w["BD_S"] = Workload(
        name="Big-Data Small (lokales ETL)",
        key="BD_S",
        flops_total=0.0,         # FLOPs spielen hier praktisch keine Rolle
        data_bytes=52.0 * (1024**3),
        n_iter=1,                # eine logische „Pass“-Iteration
        n_msg_per_iter=0,        # lokale ETL, keine Cluster-Comm
        msg_bytes_per_iter=0.0,
        n_sync_total=0,
        ref_time_s=80.0,
    )

    # 3) Big-Data Large
    # 1 TB als Cluster-ETL
    w["BD_L"] = Workload(
        name="Big-Data Large (Cluster-ETL)",
        key="BD_L",
        flops_total=0.0,
        data_bytes=1.0 * (1024**4),  # 1 TiB
        n_iter=1,
        n_msg_per_iter=2000,         # Shuffles, Partition Joins etc.
        msg_bytes_per_iter=64.0 * (1024**2),  # 64 MB pro Iteration
        n_sync_total=2000,           # globale Barrieren im Job
        ref_time_s=1800.0,           # 30 Minuten
    )

    # 4) CFD Medium (2h)
    w["CFD_M"] = Workload(
        name="CFD Medium (Engineering)",
        key="CFD_M",
        flops_total=5.0e13,         # wie in v2 (100M * 500 * 1000)
        data_bytes=30.0 * (1024**3),# 30 GB State
        n_iter=500,
        n_msg_per_iter=1000,        # konservativ
        msg_bytes_per_iter=60.0 * (1024**2),  # 60 MB pro Iteration
        n_sync_total=30000,         # Barrieren
        ref_time_s=7200.0,          # 2h
    )

    # 5) CFD Large (24h)
    w["CFD_L"] = Workload(
        name="CFD Large (Klima/Wetter)",
        key="CFD_L",
        flops_total=1.0e15,         # 20x Medium (ungefähr)
        data_bytes=600.0 * (1024**3),# 600 GB
        n_iter=2000,
        n_msg_per_iter=3000,        # höherer Parallelitätsgrad
        msg_bytes_per_iter=80.0 * (1024**2),  # 80 MB pro Iteration
        n_sync_total=80000,
        ref_time_s=DAY,             # 24h
    )

    return w


# ---------------------------------------------------------------------------
# Hilfsfunktionen für Zeitanteile
# ---------------------------------------------------------------------------

def compute_time_compute(workload: Workload, arch: Architecture) -> float:
    """
    Compute-Term: FLOPs / Durchsatz * Overhead.
    Für Workloads ohne FLOPs (Big-Data) ergibt sich 0.
    """
    if workload.flops_total <= 0 or arch.compute_throughput <= 0:
        return 0.0
    t_ideal = workload.flops_total / arch.compute_throughput
    return t_ideal * arch.compute_overhead


def compute_time_mem(workload: Workload, arch: Architecture) -> float:
    """
    Memory-Term:
    grob: T_mem = Datenvolumen / effektive Bandbreite.
    Wir nehmen eine Mischung aus sequentiellem und random Access an,
    je nach Workload-Typ (hier sehr einfach gehalten).
    """

    if workload.data_bytes <= 0:
        return 0.0

    # Sehr einfache Heuristik:
    # BERT: FLOP-limitiert -> Memory nur sekundär
    # Big-Data: 80% random, 20% sequential
    # CFD: 60% random, 40% sequential

    if workload.key.startswith("BD_"):
        frac_rnd = 0.8
    elif workload.key.startswith("CFD_"):
        frac_rnd = 0.6
    else:
        # BERT & andere: konservativ
        frac_rnd = 0.5

    frac_seq = 1.0 - frac_rnd

    bw_eff = (
        frac_seq * arch.mem_bw_seq +
        frac_rnd * arch.mem_bw_rnd
    )  # GB/s

    if bw_eff <= 0:
        return 0.0

    data_gb = workload.data_bytes / (1024**3)
    return data_gb / bw_eff


def compute_time_comm(workload: Workload, arch: Architecture) -> float:
    """
    Communication-Term:
    T_comm = n_iter * ( n_msg * L_net + V / BW_net )
    für Workloads ohne n_iter oder n_msg -> 0
    """

    if workload.n_iter <= 0 or workload.n_msg_per_iter <= 0:
        return 0.0

    # Latenz-Anteil
    L = arch.net_latency_us * 1e-6   # in s
    lat_per_iter = workload.n_msg_per_iter * L

    # Daten-Anteil
    if arch.net_bw_gb <= 0:
        data_per_iter = 0.0
    else:
        bw = arch.net_bw_gb * (1024**3)  # Bytes/s
        data_per_iter = workload.msg_bytes_per_iter / bw

    t_per_iter = lat_per_iter + data_per_iter
    return workload.n_iter * t_per_iter


def compute_time_sync(workload: Workload, arch: Architecture) -> float:
    """
    Synchronisations-Term:
    T_sync = N_sync * L_sync
    """

    if workload.n_sync_total <= 0:
        return 0.0

    L = arch.sync_latency_ms * 1e-3  # in s
    return workload.n_sync_total * L


# ---------------------------------------------------------------------------
# Kalibrierung pro Workload (damit A = Referenzzeit)
# ---------------------------------------------------------------------------

def compute_scaling_factor_v3(workload: Workload, arch_A: Architecture) -> float:
    """
    Berechnet S_W so, dass Architektur A mit dem Realmodell
    die angegebene Referenzzeit ref_time_s erhält.
    """
    t_c = compute_time_compute(workload, arch_A)
    t_m = compute_time_mem(workload, arch_A)
    t_o = compute_time_comm(workload, arch_A)
    t_s = compute_time_sync(workload, arch_A)

    t_raw = t_c + t_m + t_o + t_s

    if t_raw <= 0:
        return 1.0

    return workload.ref_time_s / t_raw


# ---------------------------------------------------------------------------
# Hauptsimulation
# ---------------------------------------------------------------------------

def simulate_pair_v3(
    workload: Workload,
    arch: Architecture,
    scaling_factor: float,
) -> SimulationResult:
    """
    Simuliert eine (Workload, Architektur)-Kombination mit dem Realmodell v3.0.
    """

    t_c = compute_time_compute(workload, arch)
    t_m = compute_time_mem(workload, arch)
    t_o = compute_time_comm(workload, arch)
    t_s = compute_time_sync(workload, arch)

    # Skalierung mit S_W (aus Architektur A)
    t_c *= scaling_factor
    t_m *= scaling_factor
    t_o *= scaling_factor
    t_s *= scaling_factor

    t_total = t_c + t_m + t_o + t_s
    t_eff = t_total * arch.r_run

    energy = t_total * arch.power_base
    energy_eff = energy * arch.r_run

    return SimulationResult(
        workload_key=workload.key,
        arch_key=arch.key,
        workload_name=workload.name,
        arch_name=arch.name,
        t_compute=t_c,
        t_mem=t_m,
        t_comm=t_o,
        t_sync=t_s,
        t_total=t_total,
        t_eff=t_eff,
        energy=energy,
        energy_eff=energy_eff,
        speedup=1.0,         # wird im Vergleich gesetzt
        energy_saving=0.0,   # wird im Vergleich gesetzt
        r_bit=arch.r_bit,
        r_run=arch.r_run,
    )


def add_comparative_metrics_v3(results_for_workload: Dict[str, SimulationResult]) -> None:
    """
    Ergänzt Speedup und Energieersparnis (vs. Architektur A).
    """
    ref = results_for_workload["A"]
    t_ref = ref.t_eff
    e_ref = ref.energy_eff

    for r in results_for_workload.values():
        r.speedup = t_ref / r.t_eff if r.t_eff > 0 else 0.0
        r.energy_saving = 1.0 - (r.energy_eff / e_ref) if e_ref > 0 else 0.0


def run_all_simulations_v3() -> List[SimulationResult]:
    """
    Führt die v3.0-Simulation für alle Workloads und Architekturen aus.
    """
    archs = get_architectures_v3()
    workloads = get_workloads_v3()
    results: List[SimulationResult] = []

    arch_A = archs["A"]

    for w in workloads.values():
        s_w = compute_scaling_factor_v3(w, arch_A)

        res_for_w: Dict[str, SimulationResult] = {}

        for arch in archs.values():
            r = simulate_pair_v3(w, arch, s_w)
            res_for_w[arch.key] = r

        add_comparative_metrics_v3(res_for_w)
        results.extend(res_for_w.values())

    return results


def print_results_v3(results: List[SimulationResult]) -> None:
    """
    Einfache Konsolenausgabe der Ergebnisse (mit Zeitanteilen).
    Zeiten in Stunden, Energie in kWh.
    """
    header = (
        f"{'Workload':10s} {'Arch':4s} "
        f"{'t_eff[h]':>9s} {'E_eff[kWh]':>11s} "
        f"{'Speedup':>8s} {'E-Save[%]':>10s} "
        f"{'C%':>6s} {'M%':>6s} {'O%':>6s} {'S%':>6s}"
    )
    print(header)
    print("-" * len(header))

    for r in results:
        t_h = r.t_eff / 3600.0
        e_kwh = r.energy_eff / 3600.0 / 1000.0

        # Anteil in %
        if r.t_total > 0:
            c_pct = 100.0 * r.t_compute / r.t_total
            m_pct = 100.0 * r.t_mem / r.t_total
            o_pct = 100.0 * r.t_comm / r.t_total
            s_pct = 100.0 * r.t_sync / r.t_total
        else:
            c_pct = m_pct = o_pct = s_pct = 0.0

        es_pc = 100.0 * r.energy_saving

        print(
            f"{r.workload_key:10s} {r.arch_key:4s} "
            f"{t_h:9.3f} {e_kwh:11.3f} "
            f"{r.speedup:8.3f} {es_pc:10.1f} "
            f"{c_pct:6.1f} {m_pct:6.1f} {o_pct:6.1f} {s_pct:6.1f}"
        )


if __name__ == "__main__":
    results_all = run_all_simulations_v3()
    print_results_v3(results_all)
