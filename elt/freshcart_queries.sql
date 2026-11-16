-- Snowflake-style FreshCart ELT additions required by Part B.
-- Run after the supplied FreshCart baseline notebook creates the schemas.

-- B3: append this expression inside ARRAY_CONSTRUCT_COMPACT(...).
-- IFF(currency NOT IN ('INR', 'USD'), 'unsupported_currency', NULL)

-- B5: sixth quality check (must return zero rows).
SELECT COUNT(*) AS null_amount_with_nonnull_source_amount
FROM gold.fct_orders
WHERE amount_inr IS NULL AND amount IS NOT NULL;

-- B5 alternative checks:
SELECT COUNT(*) AS negative_loyalty_points
FROM gold.fct_orders
WHERE loyalty_points < 0;

SELECT COUNT(*) AS future_orders
FROM silver.orders_dedup
WHERE order_date > CURRENT_DATE();

-- B4: new SCD2 event, inserted before rerunning the supplied pipeline.
INSERT INTO MOCK_CRM_TIER_EVENTS
    (customer_id, email, tier, effective_from)
VALUES
    ('CUST-02', 'arjun.k@yahoo.in', 'Gold', '2026-08-15');

