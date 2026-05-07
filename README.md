# SNAP Meal Gap Analysis - 2020

> **An ETL pipeline and multi-dataset analysis revealing regional food insecurity disparities across the US by combining SNAP meal gap data with racial demographics and financial health indicators.**

---

## The Problem

Millions of Americans face a daily meal gap — the difference between food needed and food they can afford — yet the scale and distribution of this crisis is poorly understood at a regional level. SNAP (Supplemental Nutrition Assistance Program) data alone doesn't tell the full story: without overlaying racial demographics and financial health indicators like median income, unemployment, and poverty rates, it's impossible to see *who* is most affected, *where* the burden is heaviest, and *why* certain regions consistently fall short. This project bridges that gap by integrating three separate datasets into a unified, queryable pipeline that surfaces actionable insights for policymakers and researchers.

---

## The Solution

A full ETL pipeline that ingests raw SNAP, demographic, and financial data from **MongoDB**, transforms and enriches it with derived metrics and regional mappings, stores the cleaned output in **PostgreSQL**, and produces a suite of visualisations and a merged analytical dashboard — enabling cross-dimensional analysis of food insecurity across US counties and regions.

---

## Tech Stack

| Component | Technology |
|---|---|
| Raw Storage | MongoDB Atlas |
| Data Processing | Python, Pandas, NumPy |
| Scaling / ML | scikit-learn (Min-Max Scaling) |
| Structured Storage | PostgreSQL + SQLAlchemy |
| Visualisation | Matplotlib, Seaborn |
| Environment | Jupyter Notebook |

---

## Pipeline Overview

```
MongoDB Atlas
  ├── snap_meal_gap
  ├── race_and_ethnicity        ──► Spark/Pandas ETL ──► PostgreSQL ──► Analysis & Visualisation
  └── financial_health_metrics
```

**ETL steps:**
- Extract all three collections from MongoDB into Pandas DataFrames
- Clean: handle missing values, remove duplicates, standardise column formats
- Enrich: derive `cost_per_capita`, `total_gap_cost`, `normalized_cost_per_meal`, region mapping
- Remove outliers via IQR method
- Load cleaned data into PostgreSQL via SQLAlchemy
- Filter and merge PUMA demographic/financial data by matching county names to SNAP counties

---

## Key Findings

- The **South accounts for 44.3%** of total national gap costs; the Midwest follows at 35.5%
- **Population size is the strongest driver** of total gap cost (correlation: 0.68) — not cost per meal alone
- The **South and Midwest** have the highest counts of counties exceeding the Thrifty Food Plan (TFP) cost
- **Higher meal costs consistently increase the percent gap cost** regardless of region
- The West and Northeast have higher average meal costs but smaller populations, resulting in lower overall burden

---

## Repository Structure

```
├── Main.py                              # MongoDB ingestion script
├── SNAP_Mean_Gap_2020_Analysis.ipynb    # Core ETL pipeline + SNAP analysis
├── Merged_Dataset_Analysis_Dashboard.ipynb  # Multi-dataset merged analysis
└── SNAP_Meal_Gap_Analysis_Report.docx   # Full written report
```

---

## Getting Started

### Prerequisites

```bash
pip install pymongo pandas numpy matplotlib seaborn scikit-learn sqlalchemy psycopg2-binary
```

### Setup

1. Download the three source JSON files and upload to your MongoDB Atlas cluster
2. Update the `mongo_uri` in `Main.py` with your credentials and run it to populate collections
3. Update the PostgreSQL connection string in the notebook
4. Run `SNAP_Mean_Gap_2020_Analysis.ipynb` for the core ETL and SNAP-level analysis
5. Run `Merged_Dataset_Analysis_Dashboard.ipynb` for cross-dataset insights

---

## Datasets Used

| Dataset | Source | Key Fields |
|---|---|---|
| SNAP Meal Gap 2020 | Feeding America / Kaggle | `county_state`, `meal_gap`, `cost_per_meal`, `snap_participation` |
| PUMA Race & Ethnicity | US Census (PUMA) | `puma10_name`, racial composition by region |
| PUMA Financial Health | US Census (PUMA) | `median_income`, `unemployment_rate`, `poverty_level` |
