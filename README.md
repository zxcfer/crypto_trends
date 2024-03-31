# Botin

C:\bin\mariadb-10.5.3-winx64\bin\mysqld --datadir=/wamp/data --console --init-file=C:\wamp\data\my.ini --skip-grant-tables

## Setup project

1. Install python requirements 

```bash
pip install -r requirements.txt
```

2. Create database and set credentials in `.env` file.

## alembic setup

https://www.compose.com/articles/schema-migrations-with-alembic-python-and-postgresql/

### Setup alembic

2. Set set `target_metadata = models.Base.metadata` in file `./alembic/env.py`
3. Add project directory to the Python path: `set PYTHONPATH=/dev/f21/price_monitor`

### Migrate

```bash
export PYTHONPATH=/home/xlavecat/app/price_monitor

alembic revision --autogenerate -m "create tables"
alembic upgrade --sql d37c7fb77a0b > sql/wawa.sql
alembic upgrade d37c7fb77a0b
```

## Server

- Connection:

```bash
ssh -L 3307:localhost:3306 xlavecat@punchao.com
```

### Crontab

```bash
*/1 * * * * X=/home/fer/app/price_monitor; . $X/.env; python3 $X/get_prices.py >> /tmp/get_prices.out 2>> /tmp/get_prices.err
```