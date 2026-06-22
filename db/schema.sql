PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT
);

CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT
);

CREATE TABLE balancesheet (
    company_id TEXT,
    year TEXT,
    total_assets REAL,
    total_liabilities REAL,
    PRIMARY KEY(company_id, year),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE profitandloss (
    company_id TEXT,
    year TEXT,
    sales REAL,
    operating_profit REAL,
    net_profit REAL,
    PRIMARY KEY(company_id, year),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    company_id TEXT,
    year TEXT,
    cash_flow REAL,
    PRIMARY KEY(company_id, year),
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    company_id TEXT,
    price_date TEXT,
    close_price REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE market_cap (
    company_id TEXT,
    year TEXT,
    market_cap REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE financial_ratios (
    company_id TEXT,
    year TEXT,
    roe REAL,
    roce REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE peer_groups (
    company_id TEXT,
    peer_company TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE analysis (
    company_id TEXT,
    analysis_text TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);