-- tb_portfolio definition

CREATE TABLE tb_portfolio (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT(200) NOT NULL,
	desc_msg TEXT(2000),
	crt_dt TEXT(200) NOT NULL,
	update_dt TEXT(200) NOT NULL
, is_del TEXT NOT NULL);

-- tb_sec_account definition

CREATE TABLE tb_sec_account (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	crt_dt TEXT NOT NULL
, is_del TEXT NOT NULL);

-- tb_cash_account definition

CREATE TABLE tb_cash_account (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	currency_type TEXT(10) NOT NULL,
	crt_dt TEXT(200) NOT NULL
, is_del TEXT NOT NULL);

-- tb_portfolio_sec_account_rel definition

CREATE TABLE tb_portfolio_sec_account_rel (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	portfolio_id INTEGER NOT NULL,
	sec_account_id INTEGER NOT NULL,
	is_del TEXT NOT NULL,
	crt_dt TEXT NOT NULL
);

-- tb_sec_cash_account_rel definition

CREATE TABLE tb_sec_cash_account_rel (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	sec_id INTEGER NOT NULL,
	cash_id INTEGER NOT NULL,
	is_del TEXT NOT NULL,
	crt_dt TEXT NOT NULL
);