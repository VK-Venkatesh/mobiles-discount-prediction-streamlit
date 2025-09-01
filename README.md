# Mobiles Discount Prediction (Flipkart + Amazon)

> **End‑to‑end data product:** Web scraping → Data validation & cleaning → Unified e‑commerce dataset → EDA & feature engineering → Discount prediction model → Streamlit app

![status-badge](https://img.shields.io/badge/status-active-brightgreen) ![python](https://img.shields.io/badge/Python-3.10%2B-blue) ![license](https://img.shields.io/badge/License-MIT-lightgrey) ![build](https://img.shields.io/badge/CI-GitHub%20Actions-blueviolet)

---

## 📌 Project Overview

This repository contains a **production‑ready, reproducible pipeline** that collects smartphone listings from **Flipkart** and **Amazon** (target: **≥ 500 mobiles per platform**), performs rigorous **data cleaning & validation**, merges both sources into a single **`ecommerce_final.csv`** dataset, and trains a model to **predict discount percentage / deal price**. A minimal **Streamlit app** is included for interactive exploration and inference.

**Core deliverables**

* Robust web scrapers for Flipkart & Amazon
* Automated validation (schema + data quality checks)
* Clean, tidy per‑platform datasets and a unified final dataset
* EDA notebooks + feature engineering
* ML pipeline to predict `Discount_%` (and optionally final price)
* Streamlit app to demo predictions

---

## 🗂️ Repository Structure

```
Mobiles_Discount-Prediction-Streamlit/
├── data/
│   ├── raw/
│   │   ├── flipkart_mobiles_raw.jsonl
│   │   └── amazon_mobiles_raw.jsonl
│   ├── interim/
│   │   ├── flipkart_mobiles_interim.parquet
│   │   └── amazon_mobiles_interim.parquet
│   └── processed/
│       ├── flipkart_mobiles_clean.csv
│       ├── amazon_mobiles_clean.csv
│       └── ecommerce_final.csv
├── notebooks/
│   └── Mobile_Discount_Price_Prediction.ipynb
├── src/
│   ├── scrapers/
│   │   ├── flipkart_scraper.py
│   │   └── amazon_scraper.py
│   ├── data/
│   │   ├── clean_merge.py
│   │   └── validate_schema.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── app/
│       └── app.py
├── tests/
│   ├── test_schema.py
│   └── test_utils.py
├── requirements.txt
├── environment.yml
├── Makefile
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

> The **`notebooks/Mobile_Discount_Price_Prediction.ipynb`** notebook documents EDA, preprocessing decisions, and model experiments.

---

## 🧾 Data Dictionary (Unified Schema)

Each record represents a mobile phone listing. After cleaning, both sources conform to **one schema**:

| Column             | Type     | Description                                          |
| ------------------ | -------- | ---------------------------------------------------- |
| `brand`            | string   | Phone brand (normalized casing; e.g., "Samsung")     |
| `model`            | string   | Model name normalized (e.g., "Galaxy S23 8GB/128GB") |
| `ram_gb`           | float    | RAM in GB                                            |
| `rom_gb`           | float    | Storage in GB                                        |
| `display_size_in`  | float    | Screen size (inches)                                 |
| `battery_mah`      | int      | Battery capacity (mAh)                               |
| `rear_cam_mp`      | float    | Rear camera megapixels (max / primary)               |
| `front_cam_mp`     | float    | Front camera megapixels                              |
| `processor`        | string   | Chipset/processor family                             |
| `rating`           | float    | Average user rating                                  |
| `rating_count`     | int      | Number of ratings                                    |
| `review_count`     | int      | Number of reviews                                    |
| `mrp`              | float    | Listed MRP (₹)                                       |
| `price`            | float    | Current listed price (₹)                             |
| `discount_percent` | float    | `(mrp - price)/mrp * 100`                            |
| `platform`         | category | `flipkart` or `amazon`                               |
| `url`              | string   | Product detail URL                                   |
| `scrape_ts`        | datetime | Scrape timestamp (UTC)                               |

> **Target(s)** for modeling: `discount_percent` (primary), and optionally `price`.

---

## 🕸️ Data Collection (Web Scraping)

* **Volume:** Aim for **≥ 500 unique mobiles** per platform (Flipkart & Amazon).
* **Method:** Requests + parsing (or Selenium for dynamic sections); polite crawling with user‑agent rotation and throttling.
* **Keys captured:** Title, brand, model, specs (RAM/ROM, display, battery, cameras, processor), price components, ratings, counts, URL.
* **De‑duplication:** Normalize (brand, model, RAM, ROM) and drop near‑duplicates by URL & title fingerprints.

**Run scrapers**

```bash
# Flipkart
python -m src.scrapers.flipkart_scraper \
  --pages 50 --min_items 500 --out data/raw/flipkart_mobiles_raw.jsonl

# Amazon
python -m src.scrapers.amazon_scraper \
  --pages 50 --min_items 500 --out data/raw/amazon_mobiles_raw.jsonl
```

> Configure secrets (proxies, keys if any) via **`.env`** (copy from `.env.example`). Respect site terms and robots; for research/learning only.

---

## 🧹 Cleaning & ✅ Validation

Cleaning and validation bring both sources to the **unified schema** above.

**Major steps**

1. **Type Coercion:** Parse numerics from strings (e.g., `"8 GB" → 8`).
2. **Unit Normalization:** Inches, mAh, MP; strip symbols; convert ₹.
3. **Brand/Model Canonicalization:** Regex + rules to unify brand/model tokens.
4. **Price Logic:** Ensure `mrp ≥ price`; recompute `discount_percent`.
5. **Outlier & Anomaly Checks:** Winsorize extreme prices/specs; flag negatives/zeros.
6. **Deduplication:** Title fingerprinting + key tuple `(brand, model, ram_gb, rom_gb)`.
7. **Schema Validation:** `pandera`/`pydantic`; optional `Great Expectations` suite.
8. **Missingness Handling:** Impute or drop based on thresholds; document decisions.

**Run cleaning & merge**

```bash
# Validate + clean per-platform
python -m src.data.clean_merge \
  --flipkart data/raw/flipkart_mobiles_raw.jsonl \
  --amazon  data/raw/amazon_mobiles_raw.jsonl \
  --out_dir data/processed

# Outputs
#  - data/processed/flipkart_mobiles_clean.csv
#  - data/processed/amazon_mobiles_clean.csv
#  - data/processed/ecommerce_final.csv
```

**Automated checks** (examples)

* No nulls in `brand`, `model`, `price`, `platform`, `url`
* `0 < discount_percent < 95`
* `3 ≤ display_size_in ≤ 8`, `1000 ≤ battery_mah ≤ 10000`
* `rating ∈ [0, 5]`, counts ≥ 0

---

## 🧪 EDA & Feature Engineering

Use the notebook to explore distributions and relationships:

* **Univariate:** Histograms/boxplots (price, discount, ratings)
* **Bivariate:** Price vs specs, discount vs platform/brand
* **Multivariate:** Correlation heatmap; feature importance

**Feature ideas**

* `price_per_gb = price / (ram_gb + rom_gb/4)` (proxy value metric)
* `camera_score = 0.7*rear_cam_mp + 0.3*front_cam_mp`
* `brand_tier` (A/B/C based on median price)
* `popularity = log1p(rating_count)`
* One‑hot encode `platform`, top‑K `brand`, hash `processor`

---

## 🤖 Modeling

Goal: **predict `discount_percent`** given specs & context.

**Pipeline**

* Train/val/test split with time‑aware holdout by `scrape_ts`
* Preprocess: imputation, scaling (numeric), encoding (categorical)
* Models: LinearReg, RandomForest, XGBoost/LightGBM; compare via cross‑val
* Metrics: **MAE**, **RMSE**, **R²**; calibration plots
* Persist best model as `artifacts/model.pkl` + `artifacts/preprocess.pkl`

**Train & evaluate**

```bash
python -m src.models.train \
  --data data/processed/ecommerce_final.csv \
  --target discount_percent \
  --out_dir artifacts

python -m src.models.evaluate \
  --data data/processed/ecommerce_final.csv \
  --model artifacts/model.pkl
```

---

## 🖥️ Streamlit App

Quick interactive UI to inspect the dataset and run predictions.

```bash
streamlit run src/app/app.py
```

Features:

* Filters by brand/specs
* Visuals (price vs specs, discount distributions)
* On‑the‑fly prediction panel

---

## 🚀 Getting Started

**Option A – venv + pip**

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Option B – Conda**

```bash\ nconda env create -f environment.yml
conda activate mobiles-discount
```

**Environment**

* Copy `.env.example` → `.env` and set variables if needed (proxies, app secrets)

**Make it easy**

```bash
make scrape     # runs both scrapers with sensible defaults
make process    # cleaning + merge + schema checks
make train      # train best model
make app        # launch streamlit
```

---

## ✅ Reproducibility & Quality

* **Fixed random seeds** for splits & models
* **Versioned artifacts** in `/artifacts`
* **Unit tests** for schema/utilities (`pytest`)
* **Pre‑commit hooks**: black, isort, flake8
* **CI**: GitHub Actions workflow for tests & lint

---

## 📈 Results (example placeholders)

* `MAE` ≈ *x.xx* %, `RMSE` ≈ *y.yy* %, `R²` ≈ *0.zz*
* Feature importance: specs > popularity > brand\_tier > platform

> Replace with your actual metrics from `evaluate.py`.

---

## 🔐 Ethics & Compliance

* Respect site ToS and robots; throttle and randomize requests.
* For research/educational use. Do **not** overload source sites.
* Remove PII and comply with platform policies.

---

## 🧭 Roadmap

* [ ] Add scheduling for periodic scraping
* [ ] Great Expectations data docs
* [ ] Hyperparameter search with Optuna
* [ ] Model monitoring (drift + data quality)
* [ ] Dockerfile + deploy on Streamlit Cloud/Render

---

## 🤝 Contributing

PRs welcome! Please open an issue to discuss major changes.

---

## 🧾 License

Released under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgements

Thanks to Flipkart and Amazon for publicly visible catalog pages used strictly for learning and research purposes.

---

## 🔗 Quick Commands (Copy‑Paste)

```bash
# 1) Scrape
python -m src.scrapers.flipkart_scraper --pages 50 --min_items 500 --out data/raw/flipkart_mobiles_raw.jsonl
python -m src.scrapers.amazon_scraper  --pages 50 --min_items 500 --out data/raw/amazon_mobiles_raw.jsonl

# 2) Clean + merge
python -m src.data.clean_merge --flipkart data/raw/flipkart_mobiles_raw.jsonl --amazon data/raw/amazon_mobiles_raw.jsonl --out_dir data/processed

# 3) Train + evaluate
python -m src.models.train --data data/processed/ecommerce_final.csv --target discount_percent --out_dir artifacts
python -m src.models.evaluate --data data/processed/ecommerce_final.csv --model artifacts/model.pkl

# 4) App
streamlit run src/app/app.py
```
