#!/bin/bash
# manage-backups.sh
#
# This script helps manage database backups by providing options to
# list, delete, and archive backup files.

BACKUP_DIR="./backups"

# Function to show help
function show_help {
    echo "Database Backup Management Tool"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  list              List all available backups"
    echo "  delete [FILE]     Delete a specific backup file"
    echo "  archive           Create a compressed archive of all backups"
    echo "  clean [DAYS]      Remove backups older than DAYS days (default: 30)"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 delete backups/postscore_20230501_120000.dump"
    echo "  $0 archive"
    echo "  $0 clean 7"
}

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory $BACKUP_DIR not found!"
    exit 1
fi

# Check command line arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

# Process commands
case "$1" in
    list)
        echo "Available backups:"
        echo "-----------------"
        if [ -z "$(ls -A $BACKUP_DIR)" ]; then
            echo "No backups found in $BACKUP_DIR"
        else
            find $BACKUP_DIR -type f -name "postscore_*.dump" -o -name "postscore_*.sql" | sort
        fi
        ;;
        
    delete)
        if [ -z "$2" ]; then
            echo "Error: No backup file specified for deletion"
            echo "Usage: $0 delete [FILE]"
            exit 1
        fi
        
        if [ -f "$2" ]; then
            echo "Deleting backup file: $2"
            rm -f "$2"
            echo "File deleted successfully"
        else
            echo "Error: File $2 not found"
            exit 1
        fi
        ;;
        
    archive)
        ARCHIVE_FILE="postscore_backups_$(date +%Y%m%d).tar.gz"
        echo "Creating archive: $ARCHIVE_FILE"
        tar -czf $ARCHIVE_FILE $BACKUP_DIR
        echo "Archive created successfully"
        ;;
        
    clean)
        DAYS=${2:-30}  # Default to 30 days if not specified
        echo "Removing backups older than $DAYS days..."
        find $BACKUP_DIR -name "postscore_*.dump" -type f -mtime +$DAYS -delete
        find $BACKUP_DIR -name "postscore_*.sql" -type f -mtime +$DAYS -delete
        echo "Cleanup completed"
        ;;
        
    help)
        show_help
        ;;
        
    *)
        echo "Error: Unknown command '$1'"
        show_help
        exit 1
        ;;
esac

exit 0 