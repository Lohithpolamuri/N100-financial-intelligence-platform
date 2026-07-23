# Project Retrospective
# Sprint 1 Retrospective

## Completed

- Environment setup
- Data cleaning
- Schema validation
- SQLite database creation
- Data loading
- Data quality review
- SQL exploration

## Challenges

- Header inconsistencies in Excel files
- SQLite loader debugging
- Foreign key validation

## Improvements

- Modular loader
- Better validation
- Automated audit generation

## Result

Sprint 1 completed successfully.
Sprint 2 Retrospective
Completed
Financial Ratio Engine
Profitability KPI calculations
Leverage & Efficiency KPI calculations
CAGR Engine
Cash Flow KPI Engine
Capital Allocation Engine
Financial Ratios table population (1102 records)
Capital Allocation report generation
Ratio Edge Case Log generation
KPI validation
Final testing (71 tests passed)
Challenges
Duplicate records in financial datasets
Data merge inconsistencies
Missing financial values
Cash flow validation
Edge case handling for KPI calculations
Improvements
Cleaned duplicate source data
Improved ratio calculation accuracy
Added edge case logging
Generated automated output reports
Strengthened validation and testing process
Result



---

# Sprint 2 Retrospective – Financial Ratio Engine

## Objective
Develop a financial ratio engine to compute key profitability and financial health metrics for Nifty 100 companies.

## Achievements
- Implemented profitability ratios including ROE, ROCE, Net Profit Margin and Operating Profit Margin.
- Added financial health metrics such as Debt-to-Equity, Free Cash Flow and CAGR calculations.
- Validated formulas with unit tests.
- Handled edge cases including zero denominators and negative equity.

## Challenges
- Different financial statement formats.
- Missing values for some companies.
- Handling divide-by-zero scenarios.

## Lessons Learned
- Formula validation is essential.
- Unit testing improves reliability.
- Modular analytics code simplifies future enhancements.

---

# Sprint 3 Retrospective – Dashboard Development

## Objective
Build an interactive Streamlit dashboard for financial analysis.

## Achievements
- Developed an 8-page Streamlit dashboard.
- Implemented Company Profile, Screener, Peer Comparison and Trend Analysis.
- Added Sector Analysis, Capital Allocation and Annual Reports pages.
- Integrated Plotly visualizations.
- Added database caching for faster performance.

## Challenges
- Designing responsive layouts.
- Optimizing SQL queries.
- Managing large datasets efficiently.

## Lessons Learned
- Caching significantly improves dashboard performance.
- Interactive visualizations enhance user experience.
- Modular page design simplifies maintenance.

---

# Sprint 4 Retrospective – Integration & QA

## Objective
Complete dashboard integration, valuation analysis and final testing.

## Achievements
- Implemented valuation engine with FCF Yield and valuation flags.
- Generated valuation_summary.xlsx and valuation_flags.csv.
- Performed integration testing across all dashboard pages.
- Verified application with multiple companies and edge cases.
- Added support for limited historical data messages.
- Confirmed Company Profile loads in under 2 seconds.

## UX Decisions
- Consistent navigation across all pages.
- Interactive charts using Plotly.
- Search and filtering for improved usability.
- Informative messages for limited historical data.

## Data Edge Cases
- Handled missing (`NaN`/`None`) values safely.
- Tested companies with partial historical data.
- Verified screener behavior for extreme filter values.

## Performance Findings
- Streamlit caching reduced database query time.
- Dashboard navigation is smooth.
- Company Profile consistently loads in under 2 seconds.

## Lessons Learned
- Integration testing identifies issues early.
- Proper data validation prevents runtime errors.
- Clean project structure improves maintainability.
- Performance optimization is important for a responsive dashboard.

---

