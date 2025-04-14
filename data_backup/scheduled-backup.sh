#!/bin/bash
# scheduled-backup.sh
#
# This script is intended to be run as a scheduled job (e.g., via cron)
# to create regular backups and manage backup retention.

# Set variables
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/postscore_${DATE}.dump"
RETENTION_DAYS=30  # How many days to keep backups

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create a comprehensive backup in custom format
echo "Creating scheduled database backup..."
podman exec -it postscore_db pg_dump -U postgres -d postscore -Fc > $BACKUP_FILE

# Check if backup was successful
if [ $? -ne 0 ]; then
    echo "Error: Backup failed!"
    exit 1
fi

echo "Backup created at $BACKUP_FILE"

# Clean up old backups
echo "Cleaning up backups older than $RETENTION_DAYS days..."
find $BACKUP_DIR -name "postscore_*.dump" -type f -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "postscore_*.sql" -type f -mtime +$RETENTION_DAYS -delete

# Show remaining backups
BACKUP_COUNT=$(find $BACKUP_DIR -name "postscore_*.dump" | wc -l)
echo "Currently storing $BACKUP_COUNT backups in $BACKUP_DIR" 