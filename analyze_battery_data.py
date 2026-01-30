#!/usr/bin/env python3
"""
Battery Data Analysis Script
Analyzes Li-ion battery test data from MATLAB .mat files (B0053-B0056)

This script provides comprehensive analysis of battery charge, discharge, and impedance cycles.
"""

import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

class BatteryDataAnalyzer:
    """Class to analyze Li-ion battery test data"""
    
    def __init__(self, mat_file):
        """
        Initialize the analyzer with a MATLAB file
        
        Args:
            mat_file (str): Path to the .mat file
        """
        self.mat_file = mat_file
        self.battery_id = os.path.basename(mat_file).replace('.mat', '')
        self.data = None
        self.cycles = None
        self.load_data()
        
    def load_data(self):
        """Load MATLAB .mat file"""
        print(f"\n{'='*60}")
        print(f"Loading data from {self.battery_id}")
        print(f"{'='*60}")
        self.data = scipy.io.loadmat(self.mat_file, simplify_cells=True)
        self.cycles = self.data[self.battery_id]['cycle']
        print(f"Total cycles loaded: {len(self.cycles)}")
        
    def get_cycle_types(self):
        """Get statistics about cycle types"""
        types = {}
        for cycle in self.cycles:
            cycle_type = cycle['type']
            types[cycle_type] = types.get(cycle_type, 0) + 1
        return types
    
    def analyze_structure(self):
        """Analyze and print data structure"""
        print(f"\n--- Data Structure Analysis ---")
        cycle_types = self.get_cycle_types()
        print(f"Cycle types: {cycle_types}")
        
        # Analyze first cycle of each type
        for cycle_type in ['charge', 'discharge', 'impedance']:
            for i, cycle in enumerate(self.cycles):
                if cycle['type'] == cycle_type:
                    print(f"\n{cycle_type.upper()} cycle example (cycle {i}):")
                    print(f"  Ambient temperature: {cycle['ambient_temperature']}°C")
                    if 'data' in cycle:
                        print(f"  Data fields: {list(cycle['data'].keys())}")
                        # Print first few values of each field
                        for field in cycle['data'].keys():
                            data_array = np.array(cycle['data'][field])
                            if data_array.size > 0:
                                print(f"    {field}: shape={data_array.shape}, "
                                      f"range=[{np.min(data_array):.3f}, {np.max(data_array):.3f}]")
                    break
    
    def extract_discharge_cycles(self):
        """Extract all discharge cycles and their capacities"""
        discharge_data = []
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'discharge':
                data = cycle['data']
                if 'Capacity' in data:
                    capacity = np.array(data['Capacity'])
                    if capacity.size > 0:
                        max_capacity = np.max(capacity)
                        discharge_data.append({
                            'cycle_index': i,
                            'capacity': max_capacity,
                            'voltage': np.array(data.get('Voltage_measured', [])),
                            'current': np.array(data.get('Current_measured', [])),
                            'temperature': np.array(data.get('Temperature_measured', [])),
                            'time': np.array(data.get('Time', []))
                        })
        return discharge_data
    
    def plot_capacity_degradation(self, output_dir='output'):
        """Plot battery capacity degradation over discharge cycles"""
        os.makedirs(output_dir, exist_ok=True)
        
        discharge_cycles = self.extract_discharge_cycles()
        if not discharge_cycles:
            print("No discharge cycles with capacity data found")
            return
        
        capacities = [d['capacity'] for d in discharge_cycles]
        cycle_numbers = list(range(1, len(capacities) + 1))
        
        plt.figure(figsize=(10, 6))
        plt.plot(cycle_numbers, capacities, 'o-', linewidth=2, markersize=6)
        plt.xlabel('Discharge Cycle Number', fontsize=12)
        plt.ylabel('Capacity (Ahr)', fontsize=12)
        plt.title(f'{self.battery_id}: Battery Capacity Degradation', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, f'{self.battery_id}_capacity_degradation.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()
        
        return capacities
    
    def plot_voltage_current_curves(self, output_dir='output', num_cycles=5):
        """Plot voltage-current curves for charge and discharge cycles"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Plot discharge voltage curves
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Discharge cycles
        discharge_count = 0
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'discharge' and discharge_count < num_cycles:
                data = cycle['data']
                if 'Voltage_measured' in data and 'Time' in data:
                    voltage = np.array(data['Voltage_measured'])
                    time = np.array(data['Time'])
                    if voltage.size > 0 and time.size > 0:
                        axes[0].plot(time / 3600, voltage, label=f'Cycle {i}', linewidth=2)
                        discharge_count += 1
        
        axes[0].set_xlabel('Time (hours)', fontsize=12)
        axes[0].set_ylabel('Voltage (V)', fontsize=12)
        axes[0].set_title('Discharge Voltage vs Time', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Charge cycles
        charge_count = 0
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'charge' and charge_count < num_cycles:
                data = cycle['data']
                if 'Voltage_measured' in data and 'Time' in data:
                    voltage = np.array(data['Voltage_measured'])
                    time = np.array(data['Time'])
                    if voltage.size > 0 and time.size > 0:
                        axes[1].plot(time / 3600, voltage, label=f'Cycle {i}', linewidth=2)
                        charge_count += 1
        
        axes[1].set_xlabel('Time (hours)', fontsize=12)
        axes[1].set_ylabel('Voltage (V)', fontsize=12)
        axes[1].set_title('Charge Voltage vs Time', fontsize=13, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.battery_id}: Voltage Curves', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, f'{self.battery_id}_voltage_curves.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()
    
    def plot_temperature_analysis(self, output_dir='output'):
        """Plot temperature during charge and discharge cycles"""
        os.makedirs(output_dir, exist_ok=True)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Discharge temperature
        discharge_count = 0
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'discharge' and discharge_count < 5:
                data = cycle['data']
                if 'Temperature_measured' in data and 'Time' in data:
                    temp = np.array(data['Temperature_measured'])
                    time = np.array(data['Time'])
                    if temp.size > 0 and time.size > 0:
                        axes[0].plot(time / 3600, temp, label=f'Cycle {i}', linewidth=2)
                        discharge_count += 1
        
        axes[0].set_xlabel('Time (hours)', fontsize=12)
        axes[0].set_ylabel('Temperature (°C)', fontsize=12)
        axes[0].set_title('Discharge Temperature', fontsize=13, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Charge temperature
        charge_count = 0
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'charge' and charge_count < 5:
                data = cycle['data']
                if 'Temperature_measured' in data and 'Time' in data:
                    temp = np.array(data['Temperature_measured'])
                    time = np.array(data['Time'])
                    if temp.size > 0 and time.size > 0:
                        axes[1].plot(time / 3600, temp, label=f'Cycle {i}', linewidth=2)
                        charge_count += 1
        
        axes[1].set_xlabel('Time (hours)', fontsize=12)
        axes[1].set_ylabel('Temperature (°C)', fontsize=12)
        axes[1].set_title('Charge Temperature', fontsize=13, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.suptitle(f'{self.battery_id}: Temperature Analysis', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, f'{self.battery_id}_temperature.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()
    
    def plot_impedance_analysis(self, output_dir='output'):
        """Plot impedance data (EIS)"""
        os.makedirs(output_dir, exist_ok=True)
        
        impedance_cycles = []
        for i, cycle in enumerate(self.cycles):
            if cycle['type'] == 'impedance':
                data = cycle['data']
                if 'Battery_impedance' in data:
                    impedance = np.array(data['Battery_impedance'])
                    if impedance.size > 0:
                        impedance_cycles.append({
                            'cycle': i,
                            'impedance': impedance,
                            'rectified': np.array(data.get('Rectified_impedance', [])),
                            'Re': data.get('Re', None),
                            'Rct': data.get('Rct', None)
                        })
        
        if not impedance_cycles:
            print("No impedance data found")
            return
        
        # Plot first few impedance measurements
        plt.figure(figsize=(10, 6))
        for i, imp_data in enumerate(impedance_cycles[:10]):
            impedance = imp_data['impedance']
            if impedance.size > 0:
                # Real vs Imaginary impedance (Nyquist plot)
                if impedance.dtype == np.complex128 or np.iscomplexobj(impedance):
                    plt.plot(np.real(impedance), -np.imag(impedance), 'o-', 
                             label=f'Cycle {imp_data["cycle"]}', markersize=4)
        
        plt.xlabel('Real Impedance (Ω)', fontsize=12)
        plt.ylabel('-Imaginary Impedance (Ω)', fontsize=12)
        plt.title(f'{self.battery_id}: Nyquist Plot (EIS)', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        output_file = os.path.join(output_dir, f'{self.battery_id}_impedance.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Saved: {output_file}")
        plt.close()
    
    def generate_summary_statistics(self):
        """Generate summary statistics"""
        print(f"\n--- Summary Statistics for {self.battery_id} ---")
        
        cycle_types = self.get_cycle_types()
        print(f"\nTotal cycles: {len(self.cycles)}")
        for cycle_type, count in cycle_types.items():
            print(f"  {cycle_type}: {count}")
        
        # Discharge capacity statistics
        discharge_cycles = self.extract_discharge_cycles()
        if discharge_cycles:
            capacities = [d['capacity'] for d in discharge_cycles]
            print(f"\nDischarge Capacity Statistics:")
            print(f"  Number of discharge cycles: {len(capacities)}")
            print(f"  Initial capacity: {capacities[0]:.4f} Ahr")
            print(f"  Final capacity: {capacities[-1]:.4f} Ahr")
            print(f"  Capacity fade: {capacities[0] - capacities[-1]:.4f} Ahr "
                  f"({100 * (capacities[0] - capacities[-1]) / capacities[0]:.2f}%)")
            print(f"  Average capacity: {np.mean(capacities):.4f} Ahr")
            print(f"  Min capacity: {np.min(capacities):.4f} Ahr")
            print(f"  Max capacity: {np.max(capacities):.4f} Ahr")
        
        # Temperature statistics
        all_temps = []
        for cycle in self.cycles:
            if 'data' in cycle and 'Temperature_measured' in cycle['data']:
                temp = np.array(cycle['data']['Temperature_measured'])
                if temp.size > 0:
                    all_temps.extend(temp.flatten())
        
        if all_temps:
            print(f"\nTemperature Statistics:")
            print(f"  Mean: {np.mean(all_temps):.2f}°C")
            print(f"  Min: {np.min(all_temps):.2f}°C")
            print(f"  Max: {np.max(all_temps):.2f}°C")
            print(f"  Std: {np.std(all_temps):.2f}°C")
    
    def run_complete_analysis(self, output_dir='output'):
        """Run all analysis functions"""
        print(f"\n{'='*60}")
        print(f"Running Complete Analysis for {self.battery_id}")
        print(f"{'='*60}")
        
        self.analyze_structure()
        self.generate_summary_statistics()
        
        print(f"\nGenerating visualizations...")
        self.plot_capacity_degradation(output_dir)
        self.plot_voltage_current_curves(output_dir)
        self.plot_temperature_analysis(output_dir)
        self.plot_impedance_analysis(output_dir)
        
        print(f"\n{'='*60}")
        print(f"Analysis complete for {self.battery_id}")
        print(f"{'='*60}\n")


def compare_batteries(mat_files, output_dir='output'):
    """Compare multiple batteries"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print("Comparing All Batteries")
    print(f"{'='*60}")
    
    battery_data = {}
    for mat_file in mat_files:
        analyzer = BatteryDataAnalyzer(mat_file)
        discharge_cycles = analyzer.extract_discharge_cycles()
        if discharge_cycles:
            capacities = [d['capacity'] for d in discharge_cycles]
            battery_id = analyzer.battery_id
            battery_data[battery_id] = capacities
    
    # Plot comparison
    plt.figure(figsize=(12, 7))
    for battery_id, capacities in battery_data.items():
        cycle_numbers = list(range(1, len(capacities) + 1))
        plt.plot(cycle_numbers, capacities, 'o-', linewidth=2, markersize=6, label=battery_id)
    
    plt.xlabel('Discharge Cycle Number', fontsize=12)
    plt.ylabel('Capacity (Ahr)', fontsize=12)
    plt.title('Battery Capacity Comparison (All Batteries)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'battery_comparison.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")
    plt.close()
    
    # Print comparison table
    print("\n--- Capacity Comparison Table ---")
    print(f"{'Battery':<12} {'Initial':<10} {'Final':<10} {'Fade':<10} {'Fade %':<10}")
    print("-" * 52)
    for battery_id, capacities in battery_data.items():
        initial = capacities[0]
        final = capacities[-1]
        fade = initial - final
        fade_pct = 100 * fade / initial
        print(f"{battery_id:<12} {initial:<10.4f} {final:<10.4f} {fade:<10.4f} {fade_pct:<10.2f}")


def main():
    """Main function to run the analysis"""
    # Find all .mat files in the current directory
    import glob
    mat_files = sorted(glob.glob('/home/runner/work/MCM_C/MCM_C/B*.mat'))
    
    if not mat_files:
        print("No .mat files found!")
        return
    
    print(f"Found {len(mat_files)} battery data files:")
    for f in mat_files:
        print(f"  - {os.path.basename(f)}")
    
    output_dir = '/home/runner/work/MCM_C/MCM_C/output'
    
    # Analyze each battery individually
    for mat_file in mat_files:
        analyzer = BatteryDataAnalyzer(mat_file)
        analyzer.run_complete_analysis(output_dir)
    
    # Compare all batteries
    if len(mat_files) > 1:
        compare_batteries(mat_files, output_dir)
    
    print("\n" + "="*60)
    print("ALL ANALYSIS COMPLETE")
    print(f"Results saved in: {output_dir}/")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
