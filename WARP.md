# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project type: Streamlit-based Python app for visualizing Pakistan socio-economic indicators using Plotly and pandas.

Quick start

- Create a virtualenv and install deps:

```bash path=null start=null
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Run the app (auto-reloads on code changes):

```bash path=null start=null
streamlit run src/app/main.py
```

- Run with options (matches devcontainer behavior):

```bash path=null start=null
streamlit run src/app/main.py \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  --server.port 8501
```

- Clear Streamlit cache (if data/code changes aren’t reflected):

```bash path=null start=null
streamlit cache clear
```

- Linting/tests: No linter or test framework is configured in this repo.

Data expectations

- Input CSVs live in data_processed/ and must be named:
  - Pakistan_GDP.csv
  - Pakistan_School_Enrollment.csv
  - Pakistan_Net_User.csv
- Expected columns per file: Country Name, Country Code, Indicator Name, Indicator Code, plus 4-digit year columns (>= 2000). Non-numeric year/value cells are dropped during ingestion.

High-level architecture

- src/app/main.py
  - Entry point for Streamlit UI. Sets page config, constructs sidebar navigation, and renders two pages: “Dashboard Overview” and “Forecasting & Modeling”.
  - Injects the project root into sys.path so imports like from src... work without packaging; keep this in place when running via streamlit.
  - Applies a common Plotly config (PLOTLY_CONFIG) and wires together data loading and chart rendering.

- src/config.py
  - Central metadata and paths. DATA_PATH points to data_processed/.
  - CATEGORY_MAPPING maps logical categories (GDP, Education, Health, Energy) to source files, labels, and y-axis units.
  - DASHBOARD_INDICATORS controls which categories surface as KPIs; FORECASTING_INDICATORS drives the radio selection on the forecasting page.

- src/data_loader.py
  - load_all_data() reads each referenced CSV under DATA_PATH, melts year columns (>= 2000) into long format, coerces to numeric, drops invalid rows, and caches results with st.cache_data.
  - Returns a dict[str, DataFrame] keyed by category, sharing the same long-form schema: [Country Name, Country Code, Indicator Name, Indicator Code, Year, Value].

- src/charts.py
  - create_plot_type(df, category, chart_type) produces themed Plotly figures for area (GDP), horizontal bar (Education), pie (latest-year share), and default line charts.
  - get_kpi_value(df, category) computes the latest value and YoY delta (GDP formatted with SI suffixes; percentages for others).
  - create_multi_axis_plot(data_dict) builds a combined figure using make_subplots: GDP as bars on the primary y-axis (left), percentage indicators as lines on the secondary y-axis (right, 0–100%).

Dev container notes (.devcontainer/devcontainer.json)

- Uses Python 3.11 image and auto-installs requirements. On attach, it runs:

```bash path=null start=null
streamlit run src/app/main.py --server.enableCORS false --server.enableXsrfProtection false
```

- Port 8501 is forwarded and labeled “Application”. You can mirror this setup locally with the command above.

Operational tips specific to this repo

- If you see “Data file not found” or empty visuals, ensure the three CSVs exist under data_processed/ with the expected columns and 4-digit year headers.
- The “Energy” category currently reuses the GDP file as a placeholder (see CATEGORY_MAPPING). Update mapping when a real dataset is available.
- The Forecasting page is a placeholder that reuses chart rendering; no model training code is present yet.
