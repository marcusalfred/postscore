#!/bin/bash
# backup_db.sh

# Set variables
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/postscore_${DATE}.dump"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create a comprehensive backup in custom format
echo "Creating database backup..."
podman exec -it postscore_db pg_dump -U postgres -d postscore -Fc > $BACKUP_FILE

# Create a plain SQL backup too (optional)
podman exec -it postscore_db pg_dump -U postgres -d postscore > "${BACKUP_DIR}/postscore_${DATE}.sql"

echo "Backup created at $BACKUP_FILE"
echo "SQL backup created at ${BACKUP_DIR}/postscore_${DATE}.sql" 