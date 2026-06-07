# 🇬🇧 UK Census 2021 — Population & Employment Analysis Pipeline

> **MSc Advanced Data Science & Artificial Intelligence — Group Project**
> A fully automated data pipeline that ingests, cleans, transforms, analyses, and visualises UK Census 2021 data to answer five research questions on population ageing and employment inequality.

---

## 📊 Research Questions

| # | Question | Key Finding |
|---|---|---|
| RQ1 | Does working-age population % influence employment rate? | Weak positive correlation (r = 0.30) |
| RQ2 | Which areas have the oldest populations? | North Norfolk (35.3%) leads; national avg 20.9% |
| RQ3 | What is the distribution of dependency ratios? | 289 areas above 0.70; national avg 0.81 |
| RQ4 | Does education attainment affect employment? | Moderate positive correlation (r = 0.47) |
| RQ5 | Is there regional employment inequality within population bands? | 15–20% gap between min and max in every band |

---

## 🗂️ Project Structure

```
uk-census-pipeline/
├── src/
│   ├── ingest.py          # Load CSVs from input directory
│   ├── clean.py           # Standardise columns, handle missing values
│   ├── transform.py       # Feature engineering per dataset
│   ├── analyze.py         # Answer all 5 research questions
│   └── visualise.py       # Generate matplotlib charts
├── input/                 # Place raw Census CSV files here
│   ├── TS001.csv          # Population demographics
│   ├── TS007.csv          # Age by single year
│   ├── TS066.csv          # Labour market / economic activity
│   └── TS067.csv          # Qualifications
├── output/
│   └── charts/            # Auto-generated PNG charts
├── main.py                # Pipeline entry point
└── requirements.txt
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/LikhithaKhaspa/uk-census-pipeline.git
cd uk-census-pipeline
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Add Census data
Download the datasets from the [ONS Census 2021 website](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic) and place them in the `input/` folder:

| File | Dataset | Description |
|---|---|---|
| `TS001.csv` | TS001 | Demography — total population |
| `TS007.csv` | TS007 | Age by single year |
| `TS066.csv` | TS066 | Economic activity status |
| `TS067.csv` | TS067 | Highest level of qualification |

### 4. Run the full pipeline
```bash
python main.py
```

---

## 🔄 Pipeline Stages

```
Stage 1 — Ingest      Load all CSVs from input/
    ↓
Stage 2 — Clean       Standardise columns, fix types, fill missing values
    ↓
Stage 3 — Transform   Feature engineering (age groups, rates, ratios)
    ↓
Stage 4 — Analyse     Answer 5 research questions, compute correlations
    ↓
Stage 5 — Visualise   Save charts to output/charts/
```

### Feature Engineering

| Dataset | Derived Features |
|---|---|
| TS007 | `pct_working_age`, `pct_elderly`, `dependency_ratio` |
| TS066 | `employment_rate`, `unemployment_rate` |
| TS067 | `qualification_rate`, `no_qual_rate` |

---

## 📈 Output Charts

| Chart | Description |
|---|---|
| `rq1_employment_by_working_age.png` | Employment rate by working-age population quartile |
| `rq2_elderly_population.png` | Top 10 most elderly local authorities |
| `rq3_dependency_ratio.png` | Top 10 highest dependency ratios |
| `rq4_education_employment.png` | Education attainment vs employment rate |
| `rq5_regional_inequality.png` | Employment range within population size bands |

### Sample Results

**RQ2 — Top 10 oldest areas (% aged 66+)**

| Area | % Elderly |
|---|---|
| North Norfolk | 35.3% |
| Rother | 34.2% |
| East Devon | 31.8% |
| East Lindsey | 31.6% |
| Dorset | 31.3% |

**RQ5 — Employment gap within population bands**

Every population band shows a 15–20 percentage point gap between the lowest and highest employment rates, demonstrating persistent regional inequality regardless of area size.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| pandas | Data loading, cleaning, transformation |
| numpy | Numerical computation |
| matplotlib | Chart generation |
| re (stdlib) | Column name standardisation |

---

## 📦 Installation

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 📁 Data Sources

All data is sourced from the **UK Office for National Statistics (ONS) Census 2021**:

- [TS001 — Demography](https://www.ons.gov.uk/datasets/TS001)
- [TS007 — Age by single year of age](https://www.ons.gov.uk/datasets/TS007)
- [TS066 — Economic activity status](https://www.ons.gov.uk/datasets/TS066)
- [TS067 — Highest level of qualification](https://www.ons.gov.uk/datasets/TS067)

> **Note:** Raw CSV files are excluded from this repository due to ONS licensing. Download them directly from the links above and place them in the `input/` folder.

---

## 👥 Contributors

MSc Advanced Data Science & Artificial Intelligence — Group Project Team

---

## 📄 License

This project is for academic purposes. Census data © Office for National Statistics, licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
