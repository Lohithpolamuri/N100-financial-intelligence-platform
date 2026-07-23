# 📈 N100 Financial Intelligence Dashboard

## Project Overview

The **N100 Financial Intelligence Dashboard** is an interactive financial analytics platform built using **Python, Streamlit, SQLite, Pandas, and Plotly**. It provides comprehensive analysis of companies in the Nifty 100 index through an easy-to-use multipage dashboard.

The application enables users to explore company fundamentals, compare peers, screen companies based on financial metrics, analyze trends, study sector performance, evaluate capital allocation patterns, access annual reports, and review valuation insights.

The project focuses on delivering fast, reliable, and user-friendly financial analysis while handling missing data, partial historical records, and large datasets efficiently.

## Features

- Interactive Streamlit dashboard with 8 analytical screens
- Company financial profile with KPIs and trend analysis
- Financial screener with multiple filtering options
- Peer comparison across financial metrics
- Historical trend analysis using interactive charts
- Sector-wise performance analysis
- Capital allocation pattern visualization
- Annual report access
- Valuation analysis with FCF Yield and valuation flags
- Fast cached database queries for improved performance

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- OpenPyXL

## Project Structure

```text
N100_financial_intelligence/
│── src/
│   ├── analytics/
│   └── dashboard/
│       ├── app.py
│       ├── utils/
│       └── pages/
│
│── output/
│── scripts/
│── tests/
│── db/
│── README.md
│── requirements
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/Lohithpolamuri/N100-financial-intelligence-platform.git
```

2. Install dependencies

```bash
pip install -r requirements
```

## Run the Dashboard

Run the Streamlit dashboard from the project root directory:

```bash
PYTHONPATH=$PWD streamlit run src/dashboard/app.py
```

> **Note:** The `PYTHONPATH=$PWD` prefix ensures that the `src` package is correctly resolved when running the application.
```

## Dashboard Screens

### 1. Home
Displays market summary, financial KPIs, sector distribution, and top quality companies.

### 2. Company Profile
Shows company information, financial metrics, historical trends, and performance charts.

### 3. Screener
Filters companies using financial metrics and exports results as CSV.

### 4. Peer Comparison
Compares selected companies across key financial ratios.

### 5. Trend Analysis
Visualizes multi-year financial trends with interactive charts.

### 6. Sector Analysis
Analyzes sector performance using charts and summary statistics.

### 7. Capital Allocation
Displays capital allocation patterns and cash flow classifications.

### 8. Annual Reports
Provides quick access to company annual report links.

## Analytics Modules

- Financial Ratio Engine
- Company Screener
- Peer Comparison Engine
- Trend Analysis
- Sector Analysis
- Capital Allocation Analysis
- Valuation Engine

## Output Files

- valuation_summary.xlsx
- valuation_flags.csv
- screener_output.xlsx
- peer_comparison.xlsx
- capital_allocation.csv

## Performance

- Dashboard supports 92 Nifty companies.
- Company Profile screen loads in under 2 seconds.
- Cached database queries improve dashboard responsiveness.
- Handles missing and partial historical data gracefully.

## Future Improvements

- Live stock market integration
- Real-time financial data updates
- Portfolio tracker
- User authentication
- AI-based financial insights

## Author

**Lohith Polamuri**

B.Tech CSE (Data Science)

Vaagdevi College of Engineering

Financial Intelligence Dashboard  Project