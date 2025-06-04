# Table of contents
- public.investors
- public.trades
- public.stocks

## Table: public.investors
- Estimated rows: -1

### Code

```sql
CREATE TABLE public.investors (
    investor_id int4 DEFAULT nextval('"public".investors_investor_id_seq'::regclass) NOT NULL,
    name varchar(100) None NOT NULL,
    email varchar(100) None NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
);
```

### Sample Data
```sql
| investor_id | name | email | created_at |
| --- | --- | --- | --- |
| 1 | John Smith | john.smith@email.com | 2024-01-15T10:30:00 |
| 2 | Maria Garcia | maria.garcia@email.com | 2024-02-01T14:20:00 |
```

## Table: public.trades
- Estimated rows: -1

### Code

```sql
CREATE TABLE public.trades (
    trade_id int4 DEFAULT nextval('"public".trades_trade_id_seq'::regclass) NOT NULL,
    investor_id int4 None NULL,
    stock_id int4 None NULL,
    trade_date date None NOT NULL,
    quantity int4 None NOT NULL,
    price_per_share numeric(10,2) None NOT NULL,
    trade_type varchar(4) None NULL,
);
```

### Sample Data
```sql
| trade_id | investor_id | stock_id | trade_date | quantity | price_per_share | trade_type |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2024-03-15 | 100 | 150.50 | BUY |
| 2 | 2 | 2 | 2024-03-16 | 50 | 275.75 | SELL |
```

## Table: public.stocks
- Estimated rows: -1

### Code

```sql
CREATE TABLE public.stocks (
    stock_id int4 DEFAULT nextval('"public".stocks_stock_id_seq'::regclass) NOT NULL,
    symbol varchar(10) None NOT NULL,
    company_name varchar(255) None NOT NULL,
    sector varchar(100) None NULL,
    listed_since date None NULL,
);
```

### Sample Data
```sql
| stock_id | symbol | company_name | sector | listed_since |
| --- | --- | --- | --- | --- |
| 1 | AAPL | Apple Inc. | Technology | 1980-12-12 |
| 2 | MSFT | Microsoft Corporation | Technology | 1986-03-13 |
```

# Views 
