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

# Views 
