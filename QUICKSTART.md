# Quick Start Guide / 快速入门指南

## English Version

### Prerequisites
```bash
# Make sure Python 3.6+ is installed
python3 --version

# Install required packages
pip install -r requirements.txt
```

### Running the Analysis
```bash
# Run the complete analysis
python3 analyze_battery_data.py
```

### Output
All analysis results will be saved in the `output/` directory:
- Capacity degradation plots for each battery
- Voltage-current curves
- Temperature analysis
- Impedance analysis (Nyquist plots)
- Battery comparison plot

### Viewing Results
Open the PNG files in the `output/` directory to view the analysis results.

---

## 中文版本

### 前置要求
```bash
# 确保已安装 Python 3.6+
python3 --version

# 安装所需的包
pip install -r requirements.txt
```

### 运行分析
```bash
# 运行完整分析
python3 analyze_battery_data.py
```

### 输出结果
所有分析结果将保存在 `output/` 目录中：
- 每个电池的容量衰减图
- 电压-电流曲线
- 温度分析
- 阻抗分析（Nyquist图）
- 电池对比图

### 查看结果
打开 `output/` 目录中的PNG文件查看分析结果。

---

## Example Usage / 使用示例

### Using the BatteryDataAnalyzer class in your own code:

```python
from analyze_battery_data import BatteryDataAnalyzer

# Analyze a single battery
analyzer = BatteryDataAnalyzer('B0053.mat')

# Run complete analysis
analyzer.run_complete_analysis(output_dir='my_output')

# Or run individual analyses
analyzer.analyze_structure()
analyzer.generate_summary_statistics()
analyzer.plot_capacity_degradation()
analyzer.plot_voltage_current_curves()
analyzer.plot_temperature_analysis()
analyzer.plot_impedance_analysis()

# Extract discharge cycles for custom analysis
discharge_cycles = analyzer.extract_discharge_cycles()
for cycle in discharge_cycles:
    print(f"Cycle {cycle['cycle_index']}: Capacity = {cycle['capacity']:.4f} Ahr")
```

### Comparing multiple batteries:

```python
from analyze_battery_data import compare_batteries

# Compare all batteries
mat_files = ['B0053.mat', 'B0054.mat', 'B0055.mat', 'B0056.mat']
compare_batteries(mat_files, output_dir='comparison_output')
```

## Tips / 提示

1. The analysis script automatically finds all `.mat` files in the current directory
2. Large image files (300 DPI) are generated - suitable for publications
3. All plots use professional styling with grid lines and proper labels
4. The script handles missing data gracefully
5. Complex impedance data is properly handled for Nyquist plots

## Troubleshooting / 故障排除

### Error: "No module named 'scipy'"
```bash
pip install scipy numpy matplotlib pandas
```

### Error: "Permission denied"
```bash
# Make the script executable
chmod +x analyze_battery_data.py
```

### Output directory doesn't exist
The script automatically creates the `output/` directory if it doesn't exist.
