# Dataset Documentation

## 📊 Overview

This document provides comprehensive information about all datasets used in the Pakistan Data Twin Dashboard.

## 📁 Dataset Structure

```
datasets_cleaned/
├── Economy/        # Economic indicators (16 files)
├── Education/      # Educational data
├── Energy/         # Energy sector data
└── Health/         # Healthcare data
```

---

## 🏦 Economy Datasets

### 1. Pakistan_GDP.csv
**Description**: Pakistan's Gross Domestic Product in current US dollars

**Columns**:
- `Date`: Year (1999-2025)
- `GDP (current US$)`: GDP value in billions USD

**Usage**: 
- Main GDP trend visualization
- LSTM forecasting input
- Economic growth analysis

**Source**: World Bank, State Bank of Pakistan

**Sample Data**:
```
Date,GDP (current US$)
1999,73.6B
2000,74.0B
...
2025,450.2B
```

---

### 2. Pakistan_GDP_2000-2025.csv
**Description**: Detailed GDP breakdown by sectors and growth rates

**Columns**:
- `Observation Date`: Date of observation
- `Series name`: Type of GDP metric
- `Observation Value`: Value in Million PKR or percentage

**Series Types**:
- Growth Rate of Real Gross Domestic Product
- Commodity Producing Sector (a+b)
- Agricultural Sector
- Industrial Sector
- Services Sector

**Usage**:
- GDP composition pie charts
- Sectoral analysis
- Growth rate calculations

**Source**: Pakistan Bureau of Statistics

---

### 3. Export_of_Goods_&_Services.csv
**Description**: Total exports of goods and services

**Columns**:
- `Date`: Monthly date
- `Value`: Export value in Million USD

**Time Period**: 2003-2024

**Usage**:
- Export trend analysis
- Trade balance calculations
- Economic performance indicators

**Source**: State Bank of Pakistan

---

### 4. Export_By_Commodities.csv
**Description**: Export values by commodity categories

**Columns**:
- `Date`: Monthly date
- `Value`: Export value in Thousand USD

**Usage**:
- Commodity export trends
- LSTM export forecasting
- Sector-specific analysis

**Source**: Pakistan Bureau of Statistics

---

### 5. Workers_Remittance.csv
**Description**: Monthly remittances from overseas Pakistani workers

**Columns**:
- `Date`: Monthly date
- `Value`: Remittance value in Million USD

**Time Period**: 2001-2024

**Usage**:
- Remittance trend analysis
- Foreign exchange inflow tracking
- Economic stability indicators

**Source**: State Bank of Pakistan

---

### 6. Total_Foreign_Investment.csv
**Description**: Foreign Direct Investment and Portfolio Investment

**Columns**:
- `Date`: Monthly date
- `Value`: Investment value in Million USD

**Usage**:
- FDI trend analysis
- Investment climate assessment
- Economic confidence indicators

**Source**: State Bank of Pakistan

---

### 7. Pakistan_Debt_and_Liabilities.csv
**Description**: Government debt breakdown by categories

**Columns**:
- `Date`: Quarterly date
- `Series_Name`: Type of debt
- `Value`: Debt value in Million PKR

**Debt Categories**:
- Total Debt and Liabilities (sum I to IX)
- Gross Public Debt (sum I to III)
- Government Domestic Debt
- Government External Debt
- PSE Debt
- IMF Debt

**Usage**:
- Debt analysis dashboard
- LSTM debt forecasting
- Fiscal policy assessment

**Source**: Ministry of Finance, State Bank of Pakistan

---

### 8. Exchange_Rates.csv
**Description**: Exchange rate indices

**Columns**:
- `Date`: Monthly date
- `Series_Name`: Type of exchange rate
- `Value`: Index value (Base: 2010=100)

**Series Types**:
- Nominal Effective Exchange Rate (NEER)
- Real Effective Exchange Rate (REER)

**Usage**:
- Currency strength analysis
- Trade competitiveness
- Inflation-adjusted rates

**Source**: State Bank of Pakistan

---

### 9. Pk_Imports_Payments.csv
**Description**: Import payments for freight and insurance

**Columns**:
- `Date`: Monthly date
- `Value`: Payment value in Thousand USD

**Usage**:
- Import cost analysis
- Trade balance calculations
- Logistics cost tracking

**Source**: State Bank of Pakistan

---

### 10. Net-balance-PKR-Exports.csv
**Description**: Net export balance in Pakistani Rupees

**Columns**:
- `Date`: Annual date
- `Value`: Net balance in Million PKR

**Usage**:
- Trade surplus/deficit analysis
- Economic performance metrics
- Currency impact assessment

**Source**: Pakistan Bureau of Statistics

---

### 11. Net-balance-USD-Exports.csv
**Description**: Net export balance in US Dollars

**Columns**:
- `Date`: Annual date
- `Value`: Net balance in Million USD

**Usage**:
- International trade analysis
- Foreign exchange earnings
- Economic competitiveness

**Source**: Pakistan Bureau of Statistics

---

### 12. Pakistan-CPI_Annual.csv
**Description**: Consumer Price Index (Annual)

**Columns**:
- `Date`: Annual date
- `CPI_Value`: Index value

**Usage**:
- Inflation tracking
- Purchasing power analysis
- Economic stability indicators

**Source**: Pakistan Bureau of Statistics

---

### 13. Agriculture-Sector.csv
**Description**: Agricultural sector growth rates

**Columns**:
- `Date`: Quarterly date
- `Value`: Growth rate percentage

**Usage**:
- Sectoral performance analysis
- GDP contribution tracking
- Agricultural policy assessment

**Source**: Pakistan Bureau of Statistics

---

### 14. Services-Export.csv
**Description**: Service sector export values

**Columns**:
- `Date`: Monthly date
- `Value`: Export value in Million USD

**Usage**:
- Service sector analysis
- LSTM service export forecasting
- Economic diversification tracking

**Source**: State Bank of Pakistan

---

### 15. Service-Sectors-Monthly.csv
**Description**: Monthly service sector performance

**Columns**:
- `Date`: Monthly date
- `Value`: Sector value/growth

**Usage**:
- Service sector trends
- Monthly performance tracking
- Economic activity indicators

**Source**: Pakistan Bureau of Statistics

---

### 16. GDP_Quarterly_With_Constant_Prices.csv
**Description**: Quarterly GDP at constant prices

**Columns**:
- `Date`: Quarterly date
- `Value`: GDP value in constant prices

**Usage**:
- Real GDP analysis
- Inflation-adjusted growth
- Quarterly trend analysis

**Source**: Pakistan Bureau of Statistics

---

## 🎓 Education Datasets

### Computer Science Faculty Data
**Location**: `datasets_raw/Education/computer-science-intellectual-capital.csv`

**Description**: Faculty information from Pakistani universities

**Columns**:
- `Designation`: Academic position
- `Terminal Degree`: Highest qualification
- `Province University Located`: Geographic location
- `University Currently Teaching`: Institution name
- `Country`: Country of degree

**Usage**:
- Faculty distribution analysis
- Qualification trends
- Geographic mapping
- University rankings

**Source**: Higher Education Commission

---

## ⚡ Energy Datasets

**Status**: Datasets to be added

**Planned Data**:
- Energy production by source
- Consumption patterns
- Renewable energy capacity
- Power generation statistics

---

## 🏥 Health Datasets

**Status**: Datasets to be added

**Planned Data**:
- Healthcare indicators
- Disease prevalence
- Hospital infrastructure
- Public health metrics

---

## 📊 Data Quality & Preprocessing

### Cleaning Process

1. **Missing Values**: Handled through interpolation or removal
2. **Outliers**: Identified and treated appropriately
3. **Formatting**: Standardized date formats and column names
4. **Validation**: Cross-checked with official sources
5. **Normalization**: Scaled for ML model input

### Data Validation

- **Completeness**: All required fields present
- **Accuracy**: Values within expected ranges
- **Consistency**: Uniform formatting across datasets
- **Timeliness**: Most recent data available
- **Reliability**: Verified against official sources

### Update Frequency

| Dataset Category | Update Frequency |
|-----------------|------------------|
| GDP Data | Quarterly/Annual |
| Trade Data | Monthly |
| Debt Data | Quarterly |
| Exchange Rates | Monthly |
| Inflation | Annual |
| Education | Annual |

---

## 🔄 Data Pipeline

```
Raw Data Sources
    ↓
Data Collection (Web scraping, APIs, Downloads)
    ↓
Data Cleaning (Jupyter Notebooks)
    ↓
Cleaned Datasets (CSV files)
    ↓
Feature Engineering
    ↓
Model Training (LSTM)
    ↓
Predictions & Forecasts
    ↓
Visualization (Streamlit Dashboard)
```

---

## 📈 Data Usage Statistics

- **Total Datasets**: 16 (Economy) + 1 (Education)
- **Total Records**: 100,000+
- **Time Span**: 1999-2025 (26 years)
- **File Size**: ~50 MB total
- **Update Cycle**: Quarterly

---

## 🔗 Data Relationships

### Primary Relationships

1. **GDP ↔ Exports**: Economic growth correlation
2. **Debt ↔ GDP**: Debt-to-GDP ratio
3. **Remittances ↔ Exchange Rates**: Currency impact
4. **Inflation ↔ Exchange Rates**: Price stability
5. **Sectoral GDP ↔ Total GDP**: Composition analysis

### Derived Metrics

- **GDP Growth Rate**: Year-over-year percentage change
- **Trade Balance**: Exports - Imports
- **Debt-to-GDP Ratio**: Total Debt / GDP
- **Per Capita GDP**: GDP / Population
- **Export Growth**: Year-over-year export change

---

## 📝 Data Citation

When using this data, please cite:

```
Pakistan Data Twin Dashboard (2024)
Data Sources: State Bank of Pakistan, Pakistan Bureau of Statistics,
World Bank, Higher Education Commission
Available at: [Repository URL]
```

---

**Next**: [LSTM Forecasting Models](03_LSTM_MODELS.md)
