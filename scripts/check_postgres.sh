#!/usr/bin/env bash

set -euo pipefail

: "${ACTA_TEST_DATABASE_URL:?Define ACTA_TEST_DATABASE_URL before running this check}"

case "$ACTA_TEST_DATABASE_URL" in
    postgresql://*:*@*/*|postgresql+psycopg://*:*@*/*) ;;
    *)
        echo "ACTA_TEST_DATABASE_URL must include scheme, credentials, host, port and database" >&2
        exit 1
        ;;
esac

command -v psql >/dev/null 2>&1 || {
    echo "psql is required but was not found in PATH" >&2
    exit 1
}

command -v pg_isready >/dev/null 2>&1 || {
    echo "pg_isready is required but was not found in PATH" >&2
    exit 1
}

echo "PostgreSQL client: $(psql --version)"
pg_isready

psql --pset=pager=off "$ACTA_TEST_DATABASE_URL" \
    -v ON_ERROR_STOP=1 \
    -c "SELECT current_user, current_database(), current_setting('server_version');"

disposable_database="acta_cd_check_${RANDOM}_$$"

cleanup() {
    psql "$ACTA_TEST_DATABASE_URL" \
        -v ON_ERROR_STOP=1 \
        -c "DROP DATABASE IF EXISTS \"${disposable_database}\";" \
        >/dev/null
}

trap cleanup EXIT

psql "$ACTA_TEST_DATABASE_URL" \
    -v ON_ERROR_STOP=1 \
    -c "CREATE DATABASE \"${disposable_database}\";" \
    >/dev/null

echo "Created disposable database: ${disposable_database}"

psql "$ACTA_TEST_DATABASE_URL" \
    -v ON_ERROR_STOP=1 \
    -c "DROP DATABASE \"${disposable_database}\";" \
    >/dev/null

trap - EXIT
echo "Dropped disposable database: ${disposable_database}"
echo "PostgreSQL P2-T01 verification passed"