#!/bin/bash
set -e

# This script runs as the postgres user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create golf_api role if it doesn't exist
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'golf_api') THEN
            CREATE ROLE golf_api WITH LOGIN PASSWORD '$GOLF_API_PASSWORD';
        END IF;
    END
    \$\$;

    -- Grant necessary privileges to golf_api
    ALTER ROLE golf_api WITH SUPERUSER;
    
    -- Create schemas and grant access
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO golf_api;
    GRANT ALL PRIVILEGES ON SCHEMA public TO golf_api;
    
    -- Set golf_api as the owner of the public schema
    ALTER SCHEMA public OWNER TO golf_api;
EOSQL

echo "Golf API user has been created and configured successfully!" 