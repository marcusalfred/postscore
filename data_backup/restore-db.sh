#!/bin/bash
# restore-db.sh

# Check if backup file parameter was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file>"
    echo "Please provide the path to the backup file (.dump or .sql)"
    exit 1
fi

BACKUP_FILE=$1

# Check if file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file $BACKUP_FILE not found"
    exit 1
fi

echo "Restoring database from $BACKUP_FILE..."

# Determine file type and use appropriate restore method
if [[ "$BACKUP_FILE" == *.dump ]]; then
    # Custom format backup - use pg_restore
    echo "Detected custom format backup, using pg_restore..."
    podman exec -i postscore_db pg_restore -U postgres -d postgres -c -v < "$BACKUP_FILE"
elif [[ "$BACKUP_FILE" == *.sql ]]; then
    # Plain SQL backup - use psql
    echo "Detected SQL backup, using psql..."
    podman exec -i postscore_db psql -U postgres -d postgres < "$BACKUP_FILE"
else
    echo "Unknown backup format. Please use .dump or .sql extension."
    exit 1
fi

echo "Database restore completed from $BACKUP_FILE" 