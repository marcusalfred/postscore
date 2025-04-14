#!/bin/bash
# schema-only.sh

# Set up directory
SCHEMA_DIR="."
SCHEMA_FILE="${SCHEMA_DIR}/schema.sql"

# Extract schema only
echo "Extracting database schema..."
podman exec -it postscore_db pg_dump -U postgres -d postscore --schema-only > $SCHEMA_FILE

echo "Schema updated at $SCHEMA_FILE"
