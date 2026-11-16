# FreshCart ELT

Use the supplied FreshCart notebook as the baseline, save it in this directory,
and apply `freshcart_queries.sql` for B3--B5. The expected baseline is:

| Layer/check | Expected |
|---|---:|
| Bronze rows after one run | 8 |
| Clean silver rows | 6 |
| Quarantine rows | 2 (`ORD-1004`, `ORD-1006`) |
| Deduplicated orders | 4 |
| Gold total | 4 orders, INR 7,785.00, 126 points |

Snowflake account credentials and screenshots are intentionally not stored in Git.

