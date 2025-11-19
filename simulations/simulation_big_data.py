#!/usr/bin/env python3
"""
KORA Big-Data-Verarbeitung Simulation

Simuliert Verarbeitung eines 5D-Datensatzes (Klimamodell-ähnlich)
auf drei Architekturen:
- A: Standard (klassisches HPC-System)
- B: KORA-Software (auf Standard-Hardware)
- C: KORA-Hardware (spezialisierter Chip)

Autoren: Frank Meyer
Lizenz: CC-BY-SA 4.0
Version: 1.0 (November 2025)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Erstelle Ausgabe-Verzeichnis
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)


def simulate_big_data_processing():
    """
    Hauptsimulation für Big-Data-Verarbeitung
    """
    
    print("=" * 70)
    print("KORA BIG-DATA-VERARBEITUNG SIMULATION")
    print("=" * 70)
    print()
    
    # 1. DATENSATZ-DEFINITION
    print("1. DATENSATZ-DEFINITION")
    print("-" * 70)
    
    n_x = 180
    n_y = 360
    n_z = 20
    t = 1000
    v = 5
    
    N = n_x * n_y * n_z * t * v
    print(f"Dimensionen: {n_x} × {n_y} × {n_z} × {t} × {v}")
    print(f"Gesamte Datenpunkte: N = {N:,}")
    
    k = 10  # Operationen pro Datenpunkt
    p = 3   # Pipeline-Durchläufe
    
    O_base = N * k * p
    print(f"Operationen pro Punkt: k = {k}")
    print(f"Pipeline-Durchläufe: p = {p}")
    print(f"Gesamt-Operationen: O_base = {O_base:,.0f}")
    print()
    
    # 2. ARCHITEKTUR-PARAMETER
    print("2. ARCHITEKTUR-PARAMETER")
    print("-" * 70)
    
    architectures = {
        'A': {
            'name': 'Standard (Baseline)',
            'r_irq': 500,
            'r_cs': 2000,
            'm_bus': 3.0,
            'color': 'red',
        },
        'B': {
            'name': 'KORA-Software',
            'r_irq': 50,
            'r_cs': 200,
            'm_bus': 1.5,
            'color': 'blue',
        },
        'C': {
            'name': 'KORA-Hardware',
            'r_irq': 5,
            'r_cs': 20,
            'm_bus': 1.1,
            'color': 'green',
        },
    }
    
    for arch, params in architectures.items():
        print(f"{arch} ({params['name']}):")
        print(f"  r_irq = {params['r_irq']} (Interrupts pro Mio Ops)")
        print(f"  r_cs  = {params['r_cs']} (Kontextwechsel pro Mio Ops)")
        print(f"  m_bus = {params['m_bus']} (Bus-Overhead-Multiplikator)")
    print()
    
    # 3. ZEITKONSTANTEN
    print("3. ZEITKONSTANTEN")
    print("-" * 70)
    
    time_constants = {
        't_op': 1.0,    # Nanosekunden pro Operation
        't_bus': 3.0,   # Nanosekunden pro Bus-Transfer
        't_cs': 100.0,  # Nanosekunden pro Kontextwechsel
        't_irq': 300.0, # Nanosekunden pro Interrupt
    }
    
    for key, value in time_constants.items():
        print(f"{key} = {value} ns")
    print()
    
    # 4. LEISTUNGSPARAMETER
    power = {
        'P_dynamic': 1.0,  # Watt (dynamisch)
        'P_static': 0.5,   # Watt (statisch)
    }
    P_total = power['P_dynamic'] + power['P_static']
    print(f"4. LEISTUNGSPARAMETER")
    print("-" * 70)
    print(f"P_dynamic = {power['P_dynamic']} W")
    print(f"P_static  = {power['P_static']} W")
    print(f"P_total   = {P_total} W")
    print()
    
    # 5. BERECHNUNG FÜR JEDE ARCHITEKTUR
    print("5. BERECHNUNGEN")
    print("-" * 70)
    print()
    
    results = []
    
    for arch_name, params in architectures.items():
        print(f"=== Architektur {arch_name} ({params['name']}) ===")
        
        # Overhead-Komponenten
        O_millions = O_base / 1e6
        
        I_X = params['r_irq'] * O_millions
        C_X = params['r_cs'] * O_millions
        B_X = params['m_bus'] * N
        
        print(f"Interrupts (I):       {I_X:,.0f}")
        print(f"Kontextwechsel (C):   {C_X:,.0f}")
        print(f"Bus-Operationen (B):  {B_X:,.0f}")
        
        # Qualitätsmetriken
        KVI = I_X + 0.1 * C_X
        FG = C_X / O_base
        DI = 1 / (I_X + C_X)
        
        print(f"\nQualitätsmetriken:")
        print(f"  KVI (Kohärenz-Verlust): {KVI:.2e}")
        print(f"  FG (Fragmentierung):    {FG:.6f}")
        print(f"  DI (Determinismus):     {DI:.2e}")
        
        # Laufzeit
        T_compute = O_base * time_constants['t_op']
        T_bus = B_X * time_constants['t_bus']
        T_cs = C_X * time_constants['t_cs']
        T_irq = I_X * time_constants['t_irq']
        
        T_total_ns = T_compute + T_bus + T_cs + T_irq
        T_total_s = T_total_ns / 1e9
        
        print(f"\nLaufzeit-Komponenten:")
        print(f"  Compute: {T_compute/1e9:.2f} s ({T_compute/T_total_ns*100:.1f}%)")
        print(f"  Bus:     {T_bus/1e9:.2f} s ({T_bus/T_total_ns*100:.1f}%)")
        print(f"  Context: {T_cs/1e9:.2f} s ({T_cs/T_total_ns*100:.1f}%)")
        print(f"  IRQ:     {T_irq/1e9:.2f} s ({T_irq/T_total_ns*100:.1f}%)")
        print(f"  TOTAL:   {T_total_s:.2f} s")
        
        # Energie
        E_total = P_total * T_total_s
        
        print(f"\nEnergie: {E_total:.2f} Ws (Joule)")
        print()
        
        results.append({
            'Architecture': arch_name,
            'Name': params['name'],
            'Interrupts': I_X,
            'ContextSwitches': C_X,
            'BusOps': B_X,
            'KVI': KVI,
            'FG': FG,
            'DI': DI,
            'Time_s': T_total_s,
            'Energy_Ws': E_total,
            'Color': params['color'],
        })
    
    df = pd.DataFrame(results)
    
    # Normierung auf Architektur A
    baseline = df[df['Architecture'] == 'A'].iloc[0]
    df['KVI_norm'] = df['KVI'] / baseline['KVI']
    df['FG_norm'] = df['FG'] / baseline['FG']
    df['DI_norm'] = df['DI'] / baseline['DI']
    df['Time_norm'] = df['Time_s'] / baseline['Time_s']
    df['Energy_norm'] = df['Energy_Ws'] / baseline['Energy_Ws']
    
    # 6. ERGEBNISSE
    print("=" * 70)
    print("6. ZUSAMMENFASSUNG DER ERGEBNISSE")
    print("=" * 70)
    print()
    
    print("NORMIERTE WERTE (Architektur A = 1.0):")
    print("-" * 70)
    print(df[['Architecture', 'Name', 'Time_norm', 'Energy_norm', 'KVI_norm', 'DI_norm']].to_string(index=False))
    print()
    
    print("ABSOLUTE VERBESSERUNGEN:")
    print("-" * 70)
    for idx, row in df.iterrows():
        if row['Architecture'] != 'A':
            time_improvement = (1 - row['Time_norm']) * 100
            energy_improvement = (1 - row['Energy_norm']) * 100
            kvi_improvement = (1 - row['KVI_norm']) * 100
            di_improvement = (row['DI_norm'] - 1) * 100
            
            print(f"{row['Architecture']} ({row['Name']}):")
            print(f"  Zeit:        {time_improvement:+.1f}% (schneller)")
            print(f"  Energie:     {energy_improvement:+.1f}% (weniger)")
            print(f"  Kohärenz:    {kvi_improvement:+.1f}% (besser)")
            print(f"  Determinismus: {di_improvement:+.1f}% (besser)")
            print()
    
    # 7. VISUALISIERUNG
    create_visualizations(df)
    
    # 8. EXPORT
    output_file = OUTPUT_DIR / "big_data_results.csv"
    df.to_csv(output_file, index=False)
    print(f"Ergebnisse gespeichert: {output_file}")
    
    return df


def create_visualizations(df):
    """
    Erstellt Visualisierungen der Ergebnisse
    """
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('KORA Big-Data-Simulation: Ergebnisse', fontsize=16, fontweight='bold')
    
    # Plot 1: Laufzeit
    ax1 = axes[0, 0]
    bars1 = ax1.bar(df['Architecture'], df['Time_s'], color=df['Color'], alpha=0.7)
    ax1.set_ylabel('Laufzeit (Sekunden)')
    ax1.set_title('Laufzeit-Vergleich')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Werte auf Balken
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}s',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Energie
    ax2 = axes[0, 1]
    bars2 = ax2.bar(df['Architecture'], df['Energy_Ws'], color=df['Color'], alpha=0.7)
    ax2.set_ylabel('Energie (Joule)')
    ax2.set_title('Energieverbrauch-Vergleich')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}J',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: Qualitätsmetriken (normiert)
    ax3 = axes[1, 0]
    x = np.arange(len(df))
    width = 0.25
    
    bars_kvi = ax3.bar(x - width, df['KVI_norm'], width, label='KVI (Kohärenz)', alpha=0.7)
    bars_fg = ax3.bar(x, df['FG_norm'], width, label='FG (Fragmentierung)', alpha=0.7)
    bars_di = ax3.bar(x + width, 1/df['DI_norm'], width, label='1/DI (inv. Determinismus)', alpha=0.7)
    
    ax3.set_ylabel('Normierter Wert (A = 1.0)')
    ax3.set_title('Qualitätsmetriken (niedriger = besser)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(df['Architecture'])
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_yscale('log')
    
    # Plot 4: Relative Verbesserung
    ax4 = axes[1, 1]
    
    improvements = []
    labels = []
    
    for idx, row in df.iterrows():
        if row['Architecture'] != 'A':
            time_imp = (1 - row['Time_norm']) * 100
            energy_imp = (1 - row['Energy_norm']) * 100
            improvements.append([time_imp, energy_imp])
            labels.append(row['Architecture'])
    
    improvements = np.array(improvements)
    x_pos = np.arange(len(labels))
    
    ax4.bar(x_pos - 0.2, improvements[:, 0], 0.4, label='Zeit', alpha=0.7, color='steelblue')
    ax4.bar(x_pos + 0.2, improvements[:, 1], 0.4, label='Energie', alpha=0.7, color='darkgreen')
    
    ax4.set_ylabel('Verbesserung (%)')
    ax4.set_title('Relative Verbesserung vs. Standard')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(labels)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    
    output_file = OUTPUT_DIR / "big_data_visualization.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Visualisierung gespeichert: {output_file}")
    
    plt.show()


if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  KORA BIG-DATA SIMULATION                                          ║")
    print("║  Kohärenzorientierte Rechenarchitektur für Big-Data-Langläufer     ║")
    print("║                                                                    ║")
    print("║  Autoren: Frank Meyer                                              ║")
    print("║  Lizenz: CC-BY-SA 4.0                                              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    try:
        results = simulate_big_data_processing()
        
        print("\n")
        print("=" * 70)
        print("SIMULATION ERFOLGREICH ABGESCHLOSSEN")
        print("=" * 70)
        print()
        print("Ausgabe-Dateien:")
        print(f"  - {OUTPUT_DIR}/big_data_results.csv")
        print(f"  - {OUTPUT_DIR}/big_data_visualization.png")
        print()
        
    except Exception as e:
        print(f"\nFEHLER: {e}")
        import traceback
        traceback.print_exc()
