#!/bin/bash
set -e

# TODO: Use Docker secrets for the passwords
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER backend WITH PASSWORD 'hello';
	CREATE DATABASE sensors;
	GRANT ALL PRIVILEGES ON DATABASE sensors TO backend;
	\c sensors boss
	GRANT ALL ON SCHEMA public TO backend;
EOSQL