#!/bin/bash
# database-reset.sh

# Set up directories
BASE_DIR="."
EXTRAS_DIR="../extras"

# Check if schema exists
if [ ! -f "${BASE_DIR}/schema.sql" ]; then
    echo "Error: Schema file not found. Run schema-only.sh first."
    exit 1
fi

# Check if seed data exists
if [ ! -f "${BASE_DIR}/seed_courses.sql" ] || [ ! -f "${BASE_DIR}/seed_tee_boxes.sql" ] || [ ! -f "${BASE_DIR}/seed_tee_box_holes.sql" ]; then
    echo "Error: Seed data files not found. Run seed-data.sh first."
    exit 1
fi

echo "Dropping and recreating database..."
# Drop and recreate database
podman exec -it postscore_db psql -U postgres -c "DROP DATABASE IF EXISTS postscore;"
podman exec -it postscore_db psql -U postgres -c "CREATE DATABASE postscore;"

echo "Applying schema..."
# Apply schema
podman exec -it postscore_db psql -U postgres -d postscore -f "${BASE_DIR}/schema.sql"

echo "Loading seed data..."
# Load seed data
podman exec -it postscore_db psql -U postgres -d postscore -f "${BASE_DIR}/seed_courses.sql"
podman exec -it postscore_db psql -U postgres -d postscore -f "${BASE_DIR}/seed_tee_boxes.sql"
podman exec -it postscore_db psql -U postgres -d postscore -f "${BASE_DIR}/seed_tee_box_holes.sql"

# Check if admin user script exists
if [ -f "${EXTRAS_DIR}/fix_super_user.sql" ]; then
    echo "Creating admin user..."
    # Create admin user if needed
    podman exec -it postscore_db psql -U postgres -d postscore -f "${EXTRAS_DIR}/fix_super_user.sql"
else
    echo "Warning: Admin user script not found at ${EXTRAS_DIR}/fix_super_user.sql"
fi

echo "Database reset complete with schema and seed data"
