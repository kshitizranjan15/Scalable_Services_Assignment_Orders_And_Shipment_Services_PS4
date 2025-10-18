# ECI Orders & Shipping API

A lightweight FastAPI service that exposes Orders and Shipments endpoints. Data is loaded from CSV files and persisted into MySQL databases.

## Repository layout

- `.env` — environment variables for DB connection (not committed)
- `requirements.txt` — Python dependencies
- `main.py` — FastAPI app and route handlers
- `db_utils.py` — DB connection helper
- `db_setup.py` — create databases/tables and load CSVs
- `csv_files/`
  - `Orders.csv`
  - `Order_Items.csv`
  - `Shipments.csv`
- `orders_services_and_shipment/` — project package
- `orders_services_and_shipments_apis/` — request collection (Bruno)

## Overview

- Orders service: create and fetch orders and their items.
- Shipments service: create and fetch shipments.
- Data is stored in two MySQL databases: `order_db` and `shipping_db`.
- `db_setup.py` contains utilities to create databases/tables and load the CSVs.

## Requirements

- Python 3.10+
- MySQL server (local or remote)
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the repo root containing your DB connection values. Typical variables:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`

The helper in `db_utils.py` reads these environment variables to build DB connections.

## Load CSVs into MySQL

1. Ensure MySQL is running and accessible with the credentials in `.env`.
2. Run the setup script to create databases/tables and load CSV data:

```bash
python db_setup.py
```

The script will create `order_db` and `shipping_db` (if missing), create the tables, and bulk-insert the CSV data from `csv_files/`.

## Run the API

Start the FastAPI server locally:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Alternatively, you can run the module directly:

```bash
python main.py
```
# ECI Orders & Shipping API

A lightweight FastAPI service that exposes Orders and Shipments endpoints. Data is loaded from CSV files and persisted into MySQL databases.

## Repository layout

- `.env` — environment variables for DB connection (not committed)
- `requirements.txt` — Python dependencies
- `main.py` — FastAPI app and route handlers
- `db_utils.py` — DB connection helper
- `db_setup.py` — create databases/tables and load CSVs
- `csv_files/`
  - `Orders.csv`
  - `Order_Items.csv`
  - `Shipments.csv`
- `orders_services_and_shipment/` — project package
- `orders_services_and_shipments_apis/` — request collection (Bruno)

## Overview

- Orders service: create and fetch orders and their items.
- Shipments service: create and fetch shipments.
- Data is stored in two MySQL databases: `order_db` and `shipping_db`.
- `db_setup.py` contains utilities to create databases/tables and load the CSVs.

## Requirements

- Python 3.10+
- MySQL server (local or remote)
- Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the repo root containing your DB connection values. Typical variables:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`

The helper in `db_utils.py` reads these environment variables to build DB connections.

## Load CSVs into MySQL

1. Ensure MySQL is running and accessible with the credentials in `.env`.
2. Run the setup script to create databases/tables and load CSV data:

```bash
python db_setup.py
```

The script will create `order_db` and `shipping_db` (if missing), create the tables, and bulk-insert the CSV data from `csv_files/`.

## Run the API

Start the FastAPI server locally:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Alternatively, you can run the module directly:

```bash
python main.py
```

OpenAPI (interactive docs) will be available at: `http://127.0.0.1:8000/docs`.

## API Endpoints

All routes are defined in `main.py`.

Orders

- `GET /orders?limit={n}` — list orders (default `limit=10`)
- `GET /orders/{order_id}` — get order details including items
- `POST /orders` — insert a new order (JSON payload must match the `Order` Pydantic model in `main.py`)

Shipments

- `GET /shipments?limit={n}` — list shipments (default `limit=10`)
- `GET /shipments/{shipment_id}` — get a shipment by ID
- `POST /shipments` — insert a new shipment (JSON payload must match the `Shipment` Pydantic model in `main.py`)

Request examples are included in the `orders_services_and_shipments_apis/` collection.

## Examples

Example minimal `POST /orders` payload (match fields exactly):

```json
{
  "order_id": 123,
  "customer_id": 456,
  "order_total": 99.99,
  "order_status": "PENDING",
  "payment_status": "UNPAID",
  "items": [
    { "product_id": 1, "sku": "SKU-001", "quantity": 2, "unit_price": 19.99 }
  ]
}
```

Example minimal `POST /shipments` payload:

```json
{
  "shipment_id": 1,
  "order_id": 123,
  "carrier": "DHL",
  "status": "SHIPPED",
  "tracking_no": "TRACK123"
}
```

## Notes & Caveats

- CSV loading uses pandas and inserts rows directly; very large CSVs may take time.
- Primary keys (`order_id`, `shipment_id`) are expected to be unique. Duplicate keys will raise DB errors.
- Pydantic models in `main.py` set sensible defaults (e.g., timestamps). Ensure client payloads use compatible formats (ISO 8601 for datetimes).
- Error responses may include DB error messages for easier debugging in development. Avoid exposing detailed DB errors in production.

## Useful files

- `main.py` — FastAPI app (models and routes)
- `db_utils.py` — DB connection helper
- `db_setup.py` — DB creation and CSV loader
- `csv_files/` — source CSV data
- `orders_services_and_shipments_apis/` — request examples

## License

No license specified. Add a `LICENSE` file if you want to make the project open source.