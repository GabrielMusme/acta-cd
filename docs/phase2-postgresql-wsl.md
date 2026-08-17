# PostgreSQL 16+ local setup for Phase 2

This guide provisions the PostgreSQL verification environment required by P2-T01
on WSL Ubuntu/Debian. PostgreSQL is the normative database engine for Phase 2;
SQLite is not an equivalent test substitute.

## 1. Install PostgreSQL

Install PostgreSQL 16 or newer and its client tools using the official PGDG
repository, or use the PostgreSQL packages provided by the WSL distribution.
Verify that both required commands are available:

```bash
psql --version
pg_isready --version
```

Start PostgreSQL after opening a WSL shell:

```bash
sudo service postgresql start
```

If WSL is configured with `systemd`, `sudo systemctl start postgresql` is also
valid. Check readiness with:

```bash
pg_isready -h "${POSTGRES_HOST:-localhost}" -p "${POSTGRES_PORT:-5432}"
```

## 2. Create the local role and databases

Keep the password only in the local shell environment. Do not place it in this
repository, `.env` files tracked by Git, or shell commands copied into project
documentation.

Set these values in `~/.bashrc` and reload them with `source ~/.bashrc`:

```bash
export POSTGRES_USER="acta_cd_test"
export POSTGRES_PASSWORD="replace-with-a-local-password"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="acta_cd"

export ACTA_DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export ACTA_TEST_DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/acta_cd_test"
```

Create the role and its databases once. The role needs `CREATEDB` because the
P2-T01 verification creates and drops a disposable database:

```bash
sudo -u postgres psql <<SQL
CREATE ROLE ${POSTGRES_USER} LOGIN PASSWORD '${POSTGRES_PASSWORD}' CREATEDB;
CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};
CREATE DATABASE acta_cd_test OWNER ${POSTGRES_USER};
SQL
```

If the role or databases already exist, run equivalent `ALTER ROLE` and
`CREATE DATABASE` commands only for the missing objects instead of repeating
the block unchanged.

If a password contains `@`, `:`, `/`, `#`, or other URL-reserved characters,
URL-encode it in the two `ACTA_*_DATABASE_URL` values. `psql` still accepts the
unencoded value through `PGPASSWORD` when connecting with separate options.

## 3. Verify P2-T01

From the repository root:

```bash
source ~/.bashrc
./scripts/check_postgres.sh
```

The check verifies `psql`, `pg_isready`, the PostgreSQL server version, the
configured test connection, and creation plus removal of a disposable test
database. It prints no password.

The required environment contract is:

- `ACTA_DATABASE_URL`: application database connection URL;
- `ACTA_TEST_DATABASE_URL`: integration-test database connection URL.

These values must be supplied by the user's environment and must not be
committed to Git.