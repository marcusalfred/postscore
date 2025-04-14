#!/bin/bash
# backup_db.sh

# Set variables
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/postscore_${DATE}.dump"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create backup
podman exec -it postscore_db pg_dump -U postgres -d postscore -Fc > $BACKUP_FILE

echo "Backup created at $BACKUP_FILE"