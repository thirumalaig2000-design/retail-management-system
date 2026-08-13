# SmartStock Retail Management System

Production-style retail management platform for inventory, purchasing, POS, sales, payments, invoices, reporting, and auditability.

## Final Delivery Summary

SmartStock is a fully built retail management system with JWT authentication, role-based access control, master data management, inventory tracking, purchases, POS and sales, payments, invoices, dashboards, reports, audit logs, and super-admin system settings.

Verification:

- Backend checks, migrations, and tests passed
- Frontend dependency install and production build passed
- Deployment-oriented settings, static file support, and Railway startup config are in place
- Postman collection and local environment template are included

## What’s Included

- Authentication, JWT refresh, logout, profile, and role-based access control
- Product, category, customer, and supplier management
- Inventory tracking, stock adjustments, and transaction history
- Purchases, stock receiving, POS, sales, payments, and invoices
- Dashboards, reports, gross profit tracking, audit logs, and system settings
- Responsive Material UI frontend with protected routes and role-aware navigation
- PostgreSQL-backed services, validation, and transactional business logic

## Delivery Milestones

Built across eight phases covering environment setup, authentication, master data, inventory, purchases and POS, reporting and dashboards, audit and settings, verification, and deployment prep.

## Core Stack

- Frontend: React, Vite, JavaScript, Material UI, Axios, React Router, Recharts
- Backend: Django, Django REST Framework, SimpleJWT
- Database: PostgreSQL

## Project Layout

```text
smartstock-retail/
├─ backend/
│  ├─ config/
│  ├─ apps/
│  ├─ manage.py
│  ├─ requirements.txt
│  ├─ .env.example
│  └─ .env
├─ frontend/
│  ├─ src/
│  ├─ package.json
│  └─ vite.config.js
├─ postman/
├─ Procfile
├─ .gitignore
└─ README.md
```

## Data Model Snapshot

SmartStock uses a relational PostgreSQL schema centered on:

- `accounts_role`
- `accounts_user`
- `categories_category`
- `products_product`
- `customers_customer`
- `suppliers_supplier`
- `inventory_inventory`
- `inventory_stocktransaction`
- `purchases_purchase`
- `purchases_purchaseitem`
- `sales_sale`
- `sales_saleitem`
- `sales_payment`
- `sales_invoice`
- `audit_logs_auditlog`
- `system_settings_systemsetting`

Key relationships:

- `User` belongs to a `Role`
- `Product` links to `Category`
- `Inventory` tracks one `Product`
- `StockTransaction` records every stock movement
- `Purchase` owns `PurchaseItem` rows and updates stock when received
- `Sale` owns `SaleItem`, `Payment`, and `Invoice`
- `AuditLog` records sensitive business actions
- `SystemSetting` stores non-secret configuration only

## Master Data APIs

- `GET /api/products/`
- `POST /api/products/`
- `GET /api/products/{id}/`
- `PATCH /api/products/{id}/`
- `DELETE /api/products/{id}/`
- `GET /api/categories/`
- `POST /api/categories/`
- `GET /api/customers/`
- `POST /api/customers/`
- `GET /api/suppliers/`
- `POST /api/suppliers/`

## Authentication APIs

- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/roles/`
- `GET /api/users/`
- `POST /api/users/`
- `GET /api/users/{id}/`
- `PATCH /api/users/{id}/`
- `POST /api/users/{id}/deactivate/`

## Inventory APIs

- `GET /api/inventory/`
- `GET /api/inventory/{id}/`
- `GET /api/inventory/transactions/`
- `GET /api/inventory/low-stock/`
- `POST /api/inventory/adjust/`

## Purchases and Sales APIs

- `GET /api/purchases/`
- `POST /api/purchases/`
- `POST /api/purchases/{id}/receive/`
- `GET /api/sales/`
- `POST /api/sales/`
- `POST /api/sales/{id}/complete/`
- `GET /api/payments/`
- `GET /api/invoices/`

## Dashboard and Reports APIs

- `GET /api/dashboard/`
- `GET /api/reports/sales/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/reports/products/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/reports/payments/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/reports/inventory/`, `/low-stock/`, `/purchases/`, and `/profit/` (Admin and Super Admin)

## Audit and Settings APIs

- `GET /api/audit-logs/`
- `GET /api/settings/`
- `PATCH /api/settings/{id}/`
- `GET /api/security/review/`

## Configuration

Use `backend/.env.example` and `frontend/.env.example` as the templates.

Backend example:

```env
DB_NAME=retail_management_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
FRONTEND_URL=http://localhost:5173
ALLOWED_HOSTS=localhost,127.0.0.1
JWT_ACCESS_TOKEN_LIFETIME=30
JWT_REFRESH_TOKEN_LIFETIME=1
DATABASE_URL=
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
STATIC_ROOT=backend/staticfiles
```

Frontend example:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Run Locally

Backend:

```bash
cd backend
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py migrate
..\venv\Scripts\python.exe manage.py test
```

Frontend:

```bash
cd frontend
npm install
npm run build
```

Demo credentials seeded by `seed_data`:

- `superadmin@smartstock.local` / `SmartStock!123`
- `admin@smartstock.local` / `SmartStock!123`
- `cashier@smartstock.local` / `SmartStock!123`

Seed command:

```bash
cd backend
..\venv\Scripts\python.exe manage.py seed_data
```

## Verification

- `git status`
- `git branch --show-current`
- `git remote -v`
- `python --version`
- `node --version`
- `npm --version`
- `git --version`
- `pg_isready -h localhost -p 5432` was unavailable on PATH
- PostgreSQL service was confirmed running through Windows Services
- `manage.py check`
- `manage.py makemigrations --dry-run --check`
- `manage.py migrate`
- `manage.py showmigrations`
- `manage.py test`
- `manage.py seed_data`
- `npm install`
- `npm run build`
- `pip install -r backend/requirements.txt`

## Implementation Notes

- The PostgreSQL password is stored only in `backend/.env` for local development.
- No production credentials are committed.
- The frontend now includes login, route protection, and role-aware dashboards.
- Audit logs and system settings are now fully wired through the backend and frontend.

## Railway Deployment

### Railway and Cloudflare Pages setup

Deploy the two applications as separate services from the same repository:

- **Railway backend service:** set **Root Directory** to `backend`. The committed
  `backend/railway.toml` installs the Python application through Railpack, runs
  migrations and static-file collection before deploy, starts Gunicorn, and uses
  `/api/health/` as its health check.
- **Cloudflare Pages frontend project:** set **Root Directory** to `frontend`,
  use build command `npm run build`, and set build output directory to `dist`.
  The committed `frontend/public/_redirects` file keeps React client-side routes
  such as `/admin/dashboard` working after a direct refresh.

Set `VITE_API_BASE_URL` on Cloudflare Pages to `https://<railway-backend-domain>/api`.
After Cloudflare provides its public URL, add that exact HTTPS origin to the
Railway backend's `FRONTEND_URL`, `CORS_ALLOWED_ORIGINS`, and
`CSRF_TRUSTED_ORIGINS` values.

Set these values on Railway:

- `DEBUG=False`
- `SECRET_KEY=<production-secret>`
- `DATABASE_URL=<railway-postgres-url>` or the individual PostgreSQL fields below
- `ALLOWED_HOSTS=<railway-app-domain>,<custom-domain>`
- `FRONTEND_URL=<deployed-frontend-origin>`
- `CORS_ALLOWED_ORIGINS=<deployed-frontend-origin>`
- `CSRF_TRUSTED_ORIGINS=<deployed-frontend-origin>`
- `SECURE_SSL_REDIRECT=True`
- `SECURE_HSTS_SECONDS=31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- `SECURE_HSTS_PRELOAD=True`

Then run:

1. `python manage.py migrate`
2. `python manage.py collectstatic`
3. `gunicorn config.wsgi:application`

### Suggested Values

```env
DEBUG=False
SECRET_KEY=<production-secret>
DATABASE_URL=<railway-postgres-url>
ALLOWED_HOSTS=<railway-app-domain>,<custom-domain>
FRONTEND_URL=<deployed-frontend-origin>
CORS_ALLOWED_ORIGINS=<deployed-frontend-origin>
CSRF_TRUSTED_ORIGINS=<deployed-frontend-origin>
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

If Railway provides only the individual PostgreSQL fields, use:

```env
DB_NAME=<railway-db-name>
DB_USER=<railway-db-user>
DB_PASSWORD=<railway-db-password>
DB_HOST=<railway-db-host>
DB_PORT=<railway-db-port>
```

## API Testing

- Collection: [`postman/SmartStock API.postman_collection.json`](postman/SmartStock%20API.postman_collection.json)
- Environment: [`postman/SmartStock Local.postman_environment.json`](postman/SmartStock%20Local.postman_environment.json)

## Quick Smoke Test

Use this after starting the backend and frontend to confirm the core flows are healthy.

| Role | What to check |
| --- | --- |
| Super Admin | Log in, open Dashboard, open Audit Logs, update one non-secret Setting, confirm Reports load |
| Admin | Log in, open Dashboard, create or edit a master-data record, open Inventory, confirm Reports load |
| User | Log in, open Dashboard, use POS, complete a sale, confirm the invoice appears |

Pass criteria: login works, dashboards load, role checks hold, and sale completion creates stock, payment, and invoice records.
