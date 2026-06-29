# Chandrayaan-2 Lunar South Polar Ice Detection & Rover Path Planning

**ISRO Bharatiya Antariksh Hackathon Challenge 8** — Subsurface Ice Detection & Landing Site Characterization

![Status](https://img.shields.io/badge/Status-In%20Progress-yellow) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

---

##  Project Overview

Automated detection and characterisation of subsurface water ice in lunar south polar regions using Chandrayaan-2 **DFSAR** (Dual Frequency Synthetic Aperture Radar) and **optical imagery**. The system identifies optimal landing sites and computes safe rover traversal paths, combining proximity to ice with terrain safety constraints.

**Primary Goal:** Locate and quantify subsurface ice deposits near Faustini, Haworth, and Shoemaker craters for future in-situ resource utilisation (ISRU).

---

##  Key Results

| Metric | Value |
|--------|-------|
| **Global South Pole Ice Volume** | **4.5 million m³** |
| **Uncertainty Range** | 1.78 — 7.13 million m³ (2%-8% concentration) |
| **High Confidence Ice Pixels** | 6,601 pixels (CPR > 1.0, SRD < 0.2) |
| **Data Coverage** | 12,237 × 12,794 (EAST) + 24,794 × 24,181 (WEST) pixels |
| **Pixel Resolution** | 25m (SAR), 200m (DEM) |

**Best Landing Sites Identified:**
- **EAST Swath:** Row 5540, Col 9511 (Score: 0.847)
- **WEST Swath:** Row 12193, Col 15360 (Score: 0.823)

---

##  Technical Approach

### **Week 1: Ice Detection Pipeline**
Input: Chandrayaan-2 DFSAR CPR & SRD products (PRADAN portal)

↓

Processing:

• Dual-criterion ice detection (CPR > 1.0 AND SRD < 0.2)

• Medium confidence screening (CPR > 0.8 AND SRD < 0.3)

• Validation vs. Sinha et al. 2026 (npj Space Exploration)

↓

Output:

✓ Ice probability maps (GeoTIFF)

✓ Ice volume estimates (4.5M m³)

✓ Per-crater CPR/SRD extraction (F2, H3, H1)

**Key Physics:**
- **CPR (Circular Polarization Ratio):** Radar backscatter strength (ice → CPR > 1.0)
- **SRD (Depolarization):** Volume scattering signature (ice → SRD < 0.2)
- **L-band penetration:** 5-10m subsurface
- **S-band penetration:** 3-5m subsurface

### **Week 2: Terrain Analysis**
Input:

• Ice probability maps (Week 1)

• Synthetic lunar DEM (200m resolution)

↓

Processing:

• Slope computation (Sobel gradient)

• Surface roughness (local std dev)

• PSR detection (permanently shadowed regions)

• Landing site scoring (ice + safety composite)

↓

Output:

✓ Slope maps (safe landing: <15°)

✓ Roughness maps (smooth terrain preferred)

✓ PSR masks (where ice is thermally stable)

✓ Landing site scores [0-1]

**Scoring Weights:**
- Ice proximity: 35%
- Slope safety: 30%
- Roughness: 20%
- PSR location: 15%

### **Week 3: Rover Path Planning** (In Progress)
Input: Landing site + slope hazard map

↓

Algorithm: A* pathfinding with cost function

↓

Output: Optimal traverse path + distance + estimated time

---

##  Directory Structure
chandrayaan2-lunar-ice/

├── README.md

├── requirements.txt

├── notebooks/

│   ├── 01_ice_detection.ipynb          # Week 1: CPR/SRD analysis

│   ├── 02_terrain_analysis.ipynb       # Week 2: Slope/roughness

│   └── 03_rover_path_planning.ipynb    # Week 3: A* algorithm

├── src/

│   ├── ice_detection.py                # CPR/SRD processing

│   ├── terrain_analysis.py             # Slope/roughness/PSR

│   ├── landing_site_scorer.py          # Composite scoring

│   ├── rover_path_planner.py           # A* pathfinding

│   └── utils.py                        # GDAL helpers, etc.

├── data/

│   ├── raw/                            # Downloaded DFSAR (8 ZIPs)

│   ├── processed/                      # Ice maps, slope, etc.

│   └── references/                     # Sinha et al. 2026, crater coords

├── output/

│   ├── ice_analysis/                   # Week 1 outputs

│   │   ├── ice_probability_east.tif

│   │   ├── ice_probability_west.tif

│   │   └── ice_analysis_.png

│   └── terrain_analysis/               # Week 2 outputs

│       ├── slope_.tif

│       ├── roughness_.tif

│       ├── landing_site_score_.tif

│       └── terrain_analysis_*.png

└── docs/

├── methodology.md                  # Technical details

├── data_sources.md                 # PRADAN, NASA PDS refs

└── references.bib                  # Sinha et al., LRO papers

---

## Quick Start

### **1. Clone Repository**
```bash
git clone https://github.com/sukuna-ice/chandrayaan2-lunar-ice.git
cd chandrayaan2-lunar-ice
```

### **2. Install Dependencies**
```bash
conda create -n lunar_ice python=3.9
conda activate lunar_ice
pip install -r requirements.txt
```

### **3. Download Data**
- **SAR Data (DFSAR):** https://pradan.issdc.gov.in/ch2
  - Filter: `SAR → ProcessingLevel Contains "derived" → South Pole`
  - Download: 2 ZIPs (mpcpspeast, mpcpspwest)
  - Extract to: `data/raw/`

### **4. Run Ice Detection**
```bash
python src/ice_detection.py
# Output: output/ice_analysis/ice_probability_*.tif
```

### **5. Run Terrain Analysis**
```bash
python src/terrain_analysis.py
# Output: output/terrain_analysis/landing_site_score_*.tif
```

### **6. Visualise in QGIS**
File → Open → output/terrain_analysis/landing_site_score_east.tif

Layer → Properties → Symbology → Stretched (Min-Max)

Colourmap: Spectral (reversed, green=safe)

---

## Dependencies
GDAL==3.6.0

numpy>=1.21.0

scipy>=1.7.0

matplotlib>=3.5.0

rasterio>=1.2.0

scikit-image>=0.19.0

See `requirements.txt` for the full list.

---

## Usage

### **Ice Detection Only**
```python
from src.ice_detection import detect_ice_dual_criterion

cpr_path = "data/raw/ch2_sar_ndxl_20250630mpcpspeast_d_cpr_xx_fp_xx_xxx.tif"
srd_path = "data/raw/ch2_sar_ndxl_20250630mpcpspeast_d_srd_xx_fp_xx_xxx.tif"

ice_high, ice_med, volume = detect_ice_dual_criterion(cpr_path, srd_path)
print(f"Ice volume: {volume:.2e} m³")
```

### **Landing Site Scoring**
```python
from src.landing_site_scorer import score_landing_sites

landing_score = score_landing_sites(ice_prob, slope, roughness, psr)
best_site = np.unravel_index(np.argmax(landing_score), landing_score.shape)
print(f"Best landing site: {best_site}")
```

---

## Data Sources

| Dataset | Source | Coverage | Resolution |
|---------|--------|----------|-----------|
| **DFSAR (CPR/SRD)** | PRADAN | South Pole | 25m |
| **OHRC Imagery** | PRADAN | South Pole | 0.25m |
| **LOLA DEM** | NASA PDS / Lunaserv | Lunar | 200m |
| **Crater Coords** | Sinha et al. 2026 | Reference | — |

**Key Reference:**
> Sinha, R. K., et al. (2026). "Subsurface ice in doubly shadowed craters as revealed by Chandrayaan-2 dual frequency synthetic aperture radar." *npj Space Exploration*, 2, 22.

---

## Methodology

### **Ice Detection Thresholds** (Sinha et al. 2026)
HIGH CONFIDENCE:  CPR > 1.0  AND  SRD < 0.2

MEDIUM CONFIDENCE: CPR > 0.8  AND  SRD < 0.3

NO ICE:           CPR < 0.8  OR   SRD > 0.3

### **Volume Estimation**
Ice Volume = Σ(ice pixels) × (pixel area) × (radar depth) × (ice concentration)
Parameters:

• Pixel area: 625 m² (25m × 25m)

• Radar depth: 5m (S-band penetration)

• Ice concentration: 2%-8% by volume
Result: 4.5 million m³ (best estimate, ±2.35M m³ uncertainty)

### **Landing Site Scoring Function**
Score = 0.35×Ice + 0.30×SlopeScore + 0.20×RoughnessScore + 0.15×PSR
where:

SlopeScore = max(0, 1 - slope/15°)

RoughnessScore = max(0, 1 - roughness/10m)

---

## Results Visualization

**Ice Probability Maps:**
- Red = no ice (CPR < 0.8)
- Yellow = medium confidence (0.8 < CPR < 1.0)
- Green = high confidence (CPR > 1.0)

**Landing Site Scores:**
- Red = hazardous (steep/rough)
- Yellow = moderate safety
- Green = optimal landing zone

**Terrain Hazard:**
- Dark = safe (<15° slope, smooth)
- Bright = hazardous (>25° slope, rough)

---

## Project Status

- [x] **Week 1:** Ice detection (CPR/SRD analysis)
  - ✅ Batch processing (both swaths)
  - ✅ Volume estimation
  - ✅ Validation vs. literature
  - ✅ Per-crater extraction

- [x] **Week 2:** Terrain analysis (slope/roughness/PSR)
  - ✅ DEM generation
  - ✅ Slope computation
  - ✅ PSR detection
  - ✅ Landing site scoring

- [ ] **Week 3:** Rover path planning (A* algorithm)
  - ⏳ Dijkstra/A* implementation
  - ⏳ Cost function (slope hazard + distance)
  - ⏳ Traverse path visualisation

- [ ] **Week 4:** Presentation & visualization
  - ⏳ QGIS maps
  - ⏳ Final report
  - ⏳ Hackathon presentation

---
## Citation

If you use this work, please cite:

```bibtex
@software{sukuna2026chandrayaan2,
  author = {Sukuna and Kaustav and Colleagues},
  title = {Chandrayaan-2 Lunar South Polar Ice Detection and Rover Path Planning},
  year = {2026},
  url = {https://github.com/sukuna-ice/chandrayaan2-lunar-ice},
  note = {ISRO Bharatiya Antariksh Hackathon Challenge 8}
}
```

---

## Contributing

Open issues for:
- Bug reports
- Feature requests
- Performance improvements
- Alternative algorithms

---

## Contact

- **GitHub:** @sauravjena1
- **Email:** 2404057@kiit.ac.in
- **KIIT Roll:** 2404057

---

## References

1. Sinha, R. K., et al. (2026). Subsurface ice in doubly shadowed craters. *npj Space Exploration*, 2, 22.
2. Mazarico, E., et al. (2011). Lunar Orbiter Laser Altimeter (LOLA) global gridded products. *LRO Data Node*.
3. Smith, D. E., et al. (2010). The lunar orbiter laser altimeter investigation on the lunar reconnaissance orbiter mission. *Space Science Reviews*.

---

**Last Updated:** June 29, 2026  
**Hackathon Date:** ~July 29, 2026  
**Days Remaining:** ~30 days
