Configuration
--------------

Replace `.env.example` with real `.env`, changing placeholders

```
SECRET_KEY=changeme
POSTGRES_PORT=5432
POSTGRES_DB=financial_record
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/financial_record
```

Run in Docker
-------------

### !! Note:

If you want to run app in `Docker`, change host in `DATABASE_URL` in `.env` file to name of docker db service:

`DATABASE_URL=postgresql://postgres:postgres@db:5432/financial_record`

Run project in Docker:

    $ make docker_build

or 

    $ docker-compose up --build


Stop project in Docker:

    $ make docker_down



Web routes
----------
All routes are available on ``/`` or ``/redoc`` paths with Swagger or ReDoc.


Case steps
----------

after docker-compose up  go to http://localhost:5001 to swagger ui

1. Create user with /api/v1/user/create-user endpoint
2. Login with /api/v1/user/login endpoint
3. add financial records with upload endpoint /api/v1/financial-records/upload with file 04-01-Financial Sample Data-1.csv
4. get sum of gross sales 
5. register other user and try to see other user's financial records





Project structure
-----------------
Files related to application are in the ``main`` directory.
Application parts are:
```text
main
├── __init__.py
├── api
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       ├── router.py
│       └── routes
│           ├── __init__.py
│           ├── status.py
│           ├── financial_records.py
│           └── user.py
├── app.py
├── core
│   ├── __init__.py
│   ├── config.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── logging.py
│   ├── security.py
│   └── settings
│       ├── __init__.py
│       ├── app.py
│       └── base.py
├── db
│   ├── __init__.py
│   ├── base.py
│   ├── base_class.py
│   ├── migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── dfb75cfbf652_create_tables.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── financial_records.py
│   │   └── users.py
│   └── session.py
├── models
│   ├── __init__.py
│   ├── financial_record.py
│   └── user.py
├── schemas
│   ├── __init__.py
│   ├── response.py
│   ├── status.py
│   ├── financial_records.py
│   └── user.py
├── services
│   ├── __init__.py
│   └── user.py
└── utils
    ├── __init__.py
    └── financial_records.py
```
