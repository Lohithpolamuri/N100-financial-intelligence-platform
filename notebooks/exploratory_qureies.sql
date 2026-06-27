-- 1. Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Top 10 Companies
SELECT *
FROM companies
LIMIT 10;

-- 3. Companies with Highest Market Cap
SELECT company_id,
market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 4. Highest Net Profit
SELECT company_id,
year,
net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 5. Highest Revenue
SELECT company_id,
year,
sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 6. Highest Total Assets
SELECT company_id,
year,
total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

-- 7. Companies by Sector
SELECT broad_sector,
COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC;

-- 8. Average ROE
SELECT AVG(return_on_equity_pct)
FROM financial_ratios;

-- 9. Stock Price Records
SELECT COUNT(*)
FROM stock_prices;

-- 10. Companies Having Peer Groups
SELECT COUNT(DISTINCT company_id)
FROM peer_groups;