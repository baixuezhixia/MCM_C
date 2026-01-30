# Li-ion Battery Data Analysis / 锂离子电池数据分析

[中文文档 / Chinese Documentation](README_CN.md)

This repository contains analysis tools and results for Li-ion battery degradation experiments. The dataset includes test data from four Li-ion batteries (#53-56) subjected to various operational profiles at 4°C ambient temperature.

## Dataset Description

### Battery Test Specifications
- **Batteries**: Four Li-ion batteries (#53, #54, #55, #56)
- **Ambient Temperature**: 4°C
- **Operational Profiles**: Charge, Discharge, and Impedance (EIS)

#### Charge Protocol
- **Mode**: Constant Current (CC) at 1.5A until 4.2V
- **Then**: Constant Voltage (CV) mode until current drops to 20mA

#### Discharge Protocol
- **Load Current**: Fixed at 2A
- **Stop Voltages**:
  - Battery #53: 2.0V
  - Battery #54: 2.2V
  - Battery #55: 2.5V
  - Battery #56: 2.7V

#### Impedance Measurement
- **Method**: Electrochemical Impedance Spectroscopy (EIS)
- **Frequency Range**: 0.1Hz to 5kHz

### Test Duration
- Experiments continued until capacity reduced to 1.4 Ahr (30% fade)
- Note: Some discharge runs show very low capacity (reasons not fully analyzed)

## Data Files

| File | Description |
|------|-------------|
| `B0053.mat` | Battery #53 test data |
| `B0054.mat` | Battery #54 test data |
| `B0055.mat` | Battery #55 test data |
| `B0056.mat` | Battery #56 test data |
| `README_53_54_55_56.txt` | Original data description |

## Data Structure

Each `.mat` file contains a top-level structure array with cycle data:

### Cycle Fields
- `type`: Operation type (charge, discharge, or impedance)
- `ambient_temperature`: Ambient temperature (°C)
- `time`: Date and time of cycle start (MATLAB date vector format)
- `data`: Measurement data structure

### Data Fields by Type

#### Charge Data
- `Voltage_measured`: Battery terminal voltage (V)
- `Current_measured`: Battery output current (A)
- `Temperature_measured`: Battery temperature (°C)
- `Current_charge`: Charger current (A)
- `Voltage_charge`: Charger voltage (V)
- `Time`: Time vector (seconds)

#### Discharge Data
- `Voltage_measured`: Battery terminal voltage (V)
- `Current_measured`: Battery output current (A)
- `Temperature_measured`: Battery temperature (°C)
- `Current_load`: Load current (A)
- `Voltage_load`: Load voltage (V)
- `Time`: Time vector (seconds)
- `Capacity`: Battery capacity (Ahr) for discharge to 2.7V

#### Impedance Data
- `Sense_current`: Current in sense branch (A)
- `Battery_current`: Current in battery branch (A)
- `Current_ratio`: Ratio of currents
- `Battery_impedance`: Battery impedance (Ω) from raw data
- `Rectified_impedance`: Calibrated and smoothed impedance (Ω)
- `Re`: Estimated electrolyte resistance (Ω)
- `Rct`: Estimated charge transfer resistance (Ω)

## Analysis Script

### Installation

```bash
pip install scipy numpy matplotlib pandas
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

### Usage

Run the complete analysis:

```bash
python3 analyze_battery_data.py
```

This will:
1. Load all battery data files
2. Analyze data structure and generate statistics
3. Create visualizations for each battery
4. Generate comparison plots across all batteries
5. Save all results in the `output/` directory

## Analysis Results

The script generates comprehensive analysis including:

### 1. Capacity Degradation Analysis
- Tracks battery capacity over discharge cycles
- Identifies capacity fade patterns
- Individual plots for each battery
- Comparison plot across all batteries

### 2. Voltage-Current Curves
- Charge voltage vs. time curves
- Discharge voltage vs. time curves
- Multiple cycles overlaid for comparison

### 3. Temperature Analysis
- Temperature profiles during charge
- Temperature profiles during discharge
- Temperature range and variation analysis

### 4. Impedance Analysis (EIS)
- Nyquist plots (Real vs. Imaginary impedance)
- Impedance evolution over cycles
- Electrolyte and charge transfer resistance

### 5. Summary Statistics
For each battery:
- Total number of cycles by type
- Capacity statistics (initial, final, fade %)
- Temperature statistics (mean, min, max, std)

## Key Findings

### Battery Comparison

| Battery | Initial Capacity | Final Capacity | Capacity Fade | Fade % |
|---------|------------------|----------------|---------------|---------|
| B0053   | 1.0691 Ahr      | 0.0000 Ahr    | 1.0691 Ahr   | 100.00% |
| B0054   | 0.7399 Ahr      | 0.0000 Ahr    | 0.7399 Ahr   | 100.00% |
| B0055   | 0.7990 Ahr      | 0.9908 Ahr    | -0.1918 Ahr  | -24.00% |
| B0056   | 0.7853 Ahr      | 1.1291 Ahr    | -0.3438 Ahr  | -43.78% |

**Note**: Negative fade percentages for B0055 and B0056 indicate capacity recovery, which is unusual and may require further investigation.

### Cycle Statistics

| Battery | Total Cycles | Discharge | Charge | Impedance |
|---------|--------------|-----------|---------|-----------|
| B0053   | 137          | 56        | 55      | 26        |
| B0054   | 253          | 103       | 102     | 48        |
| B0055   | 252          | 102       | 102     | 48        |
| B0056   | 252          | 102       | 102     | 48        |

## Output Files

All analysis results are saved in the `output/` directory:

```
output/
├── B0053_capacity_degradation.png
├── B0053_impedance.png
├── B0053_temperature.png
├── B0053_voltage_curves.png
├── B0054_capacity_degradation.png
├── B0054_impedance.png
├── B0054_temperature.png
├── B0054_voltage_curves.png
├── B0055_capacity_degradation.png
├── B0055_impedance.png
├── B0055_temperature.png
├── B0055_voltage_curves.png
├── B0056_capacity_degradation.png
├── B0056_impedance.png
├── B0056_temperature.png
├── B0056_voltage_curves.png
└── battery_comparison.png
```

## Further Analysis

Potential areas for further investigation:

1. **Capacity Recovery**: Why do batteries #55 and #56 show capacity increase?
2. **Low Capacity Cycles**: Investigate discharge runs with very low capacity
3. **Temperature Effects**: Analyze correlation between temperature and capacity fade
4. **Impedance Growth**: Study how impedance evolves with battery degradation
5. **State of Health Prediction**: Develop models to predict remaining useful life

## Dependencies

- Python 3.6+
- scipy (for reading MATLAB files)
- numpy (for numerical computations)
- matplotlib (for visualization)
- pandas (for data analysis)

## License

This dataset and analysis code are provided for research and educational purposes.

## References

For more information about the battery test methodology and dataset, please refer to the original data source.
