# Your Anime List

A Python and MySQL project that imports anime and user-list data from the [MyAnimeList API](https://myanimelist.net/apiconfig/references/api/v2) into a relational database. It is intended as a learning project for SQL/MySQL, database design, triggers, stored procedures, scheduled events, and reporting.

## Features

- Fetch anime details, seasonal anime, and a user's anime list from MyAnimeList.
- Store anime, genres, studios, accounts, and user-list entries in MySQL.
- Use relational tables and foreign keys to model anime/genre/studio relationships.
- Use MySQL triggers, stored procedures, and an event to maintain derived values and process list changes.
- Generate HTML reports, including reports about studios, genres, and user scores.
- Include pytest tests for data-handling and database-manager code.

## Project layout

```text
.
├── database/
│   ├── ddl.sql
│   └── database structure/
├── reports/
├── src/
│   ├── database/
│   ├── logger/
│   ├── modules/
│   │   ├── main/
│   │   └── reporters/
│   ├── report_extractor/
│   └── report_maker/
├── tests/
├── .env.example
└── requirements.txt
```

## Requirements

- Python 3.10 or newer (the code uses modern union type syntax such as `int | None`).
- MySQL Server.
- A MyAnimeList API Client ID.
- Network access to the MyAnimeList API for live data retrieval and API integration tests.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shadmehr1984/your_anime_list_project.git
cd your_anime_list_project
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in the values:

```dotenv
# MySQL connection
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_DATABASE=your_anime_list
DB_PASSWORD=your_mysql_password

# MyAnimeList API
X_MAL_CLIENT_ID=your_myanimelist_client_id
```

Create a Client ID in your MyAnimeList API settings. Keep the actual `.env` file and credentials private; do not commit them to Git.

The current database connector reads the database connection settings from these environment variables. Ensure the MySQL user has the privileges required by your chosen setup.

### 5. Initialize the database

The schema is defined in `database/ddl.sql`. Review it before executing it and use a disposable development database when setting up the project.

> **Warning: data loss.** The current `database/ddl.sql` starts with `DROP DATABASE IF EXISTS your_anime_list`. Running it deletes the existing database with that name and its data before recreating it. Do not run the migration script against a database containing data you need to keep.

The repository also contains `src/database/migrate.py`, but its import path and execution behavior should be checked against your environment before using it. Run project scripts from the repository root unless the script's imports have been adjusted.

MySQL scheduled events require the server's event scheduler to be enabled if you want the project's scheduled log-processing event to run.

## Running the project

The repository currently provides Python modules for loading data and generating reports rather than a documented command-line entry point.

The main modules are:

- `src/modules/main/data_handling.py` — calls the MyAnimeList API.
- `src/modules/main/load_data_into_database.py` — loads anime and user-list data into MySQL.
- `src/modules/main/database_manager.py` — database operations.
- `src/modules/reporters/` — report-specific queries and HTML report generation.

Because the database connection is initialized when `database_manager` is imported, configure `.env` and ensure MySQL is reachable before importing modules that use it.

## Tests

Tests use pytest. Run them from the repository root:

```bash
python -m pytest
```

Some tests call the live MyAnimeList API and are marked with `need_vpn`; they require network access and valid API configuration. The database-manager tests connect to MySQL and modify table contents, so **run them only against a dedicated test database with disposable data**, never a production or personal database.

## Notes and known limitations

- The current API request code and pagination behavior may need adjustment for different responses and API limits.
- The report generator currently contains a machine-specific Windows output path; update it for your local environment before generating reports.
- The migration SQL is destructive as noted above.
- The project is a learning project and should be reviewed and tested before being used with important data.

## License

No license file is currently documented in the repository. Unless a license is added, reuse and redistribution permissions are not explicitly granted.
