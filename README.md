# ACE Intelligence System

**Team:** Jujutsu Query  
**Project:** 2nd Annual Datathon Project 2025 | Macaulay Honors College × Metropolitan Transit Authority

## Project Mission

To develop an **Adaptive Enforcement Intelligence System** that moves beyond reactive violation tracking to proactively recommend enforcement deployment for maximizing bus speed and reliability.

## Project Overview

The ACE Intelligence System leverages data analytics and machine learning to optimize Automated Camera Enforcement (ACE) deployment across NYC's bus network. By analyzing patterns in violation data, bus speeds, and ridership, our system identifies enforcement blind spots and recommends strategic deployment to maximize public transit efficiency.

## Repository Structure

```
ACE_Intelligence_System/
├── data_pipeline.py                    # Core data loading and processing pipeline
├── General_Analytics/                  # General system-wide analysis
│   └── 01_Performance_Paradox_Analysis.ipynb
├── Cuny_Analytics/                     # CUNY-specific corridor analysis
│   └── 02_CUNY_Corridor_Deep_Dive.ipynb
├── Dashboards/                         # Interactive visualization dashboards
└── README.md                          # Project documentation
```

## Key Features

### 🚌 Performance Paradox Detection
Identifies routes where high enforcement activity doesn't correlate with speed improvements, enabling strategic reallocation of resources.

### 🎓 CUNY Corridor Analysis
Specialized analysis of enforcement gaps around CUNY campuses during peak academic hours, ensuring reliable transit for students.

### 📊 Adaptive Intelligence
Machine learning-driven recommendations that evolve with changing traffic patterns and enforcement effectiveness.

### 🗺️ Geospatial Analytics
Interactive mapping and spatial analysis to visualize enforcement coverage and identify optimization opportunities.

## Data Sources

- **MTA Bus Speeds Data**: Real-time and historical bus performance metrics
- **ACE Enforcement Data**: Automated camera enforcement violation records
- **Route & Schedule Data**: Bus route configurations and timing data
- **Ridership Data**: Passenger volume and boarding patterns

## Team Jujutsu Query

Our interdisciplinary team combines expertise in data science, urban planning, and transportation analytics to tackle NYC's bus lane enforcement challenges through innovative data-driven solutions.

## Getting Started

1. **Setup Environment**
   ```bash
   pip install pandas numpy matplotlib seaborn plotly geopandas folium jupyter
   ```

2. **Load Data**
   ```python
   from data_pipeline import MTADataPipeline
   pipeline = MTADataPipeline(data_directory="data/")
   master_data = pipeline.create_master_dataframe()
   ```

3. **Run Analysis**
   - Open `General_Analytics/01_Performance_Paradox_Analysis.ipynb` for system-wide analysis
   - Open `Cuny_Analytics/02_CUNY_Corridor_Deep_Dive.ipynb` for CUNY-focused analysis

## Contributing

This project is part of the 2025 MTA Datathon. For questions or collaboration opportunities, please contact Team Jujutsu Query.

---

*Advancing NYC transit efficiency through intelligent enforcement optimization.*
