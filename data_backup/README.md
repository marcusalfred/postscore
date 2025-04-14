# Database Backup and Restore

This directory contains scripts for backing up and restoring the POSTscore PostgreSQL database.

## Scripts

- `backup-db.sh`: Creates a comprehensive backup of the database with a timestamp.
- `restore-db.sh`: Restores a database from a backup file.
- `schema-only.sh`: Extracts the database schema (structure only).
- `seed-data.sh`: Extracts seed data from key tables.
- `database-reset.sh`: Resets the database and reapplies schema and seed data.
- `scheduled-backup.sh`: Script for automated backups with retention management.
- `manage-backups.sh`: Tool for managing backups (list, delete, archive, clean).

## How to Use

### Creating a Full Backup

```bash
# Navigate to the data_backup directory
cd data_backup

# Run the backup script
./backup-db.sh
```

This will create two backup files in the `backups` directory:
- `postscore_YYYYMMDD_HHMMSS.dump`: A compressed backup in PostgreSQL's custom format
- `postscore_YYYYMMDD_HHMMSS.sql`: A plain SQL backup

### Restoring from a Backup

```bash
# Navigate to the data_backup directory
cd data_backup

# Restore from a custom format backup
./restore-db.sh backups/postscore_YYYYMMDD_HHMMSS.dump

# OR restore from a SQL backup
./restore-db.sh backups/postscore_YYYYMMDD_HHMMSS.sql
```

### Updating Schema Definition

```bash
# Navigate to the data_backup directory
cd data_backup

# Run the schema update script
./schema-only.sh
```

This will create a `schema.sql` file with the current database schema.

### Extracting Seed Data

```bash
# Navigate to the data_backup directory
cd data_backup

# Run the seed data script
./seed-data.sh
```

This will create SQL files for each key table:
- `seed_courses.sql`
- `seed_tee_boxes.sql`
- `seed_tee_box_holes.sql`

### Resetting the Database

```bash
# Navigate to the data_backup directory
cd data_backup

# Run the database reset script
./database-reset.sh
```

This will:
1. Drop and recreate the database
2. Apply the schema from `schema.sql`
3. Load seed data from the seed files
4. Create an admin user

### Setting Up Automated Backups

```bash
# Run scheduled backup manually
./scheduled-backup.sh

# Set up a cron job for daily backups at 2 AM
# Add this line to your crontab (crontab -e):
0 2 * * * /path/to/postscore/data_backup/scheduled-backup.sh
```

The scheduled backup script automatically removes backups older than 30 days.

### Managing Backups

The `manage-backups.sh` script provides several functions for managing your backups:

```bash
# List all backups
./manage-backups.sh list

# Delete a specific backup
./manage-backups.sh delete backups/postscore_20230501_120000.dump

# Create a compressed archive of all backups
./manage-backups.sh archive

# Clean up backups older than 7 days
./manage-backups.sh clean 7
```

## Backup Schedule Recommendation

- Daily: Run `scheduled-backup.sh` via cron for automated backups
- Weekly: Archive older backups using `manage-backups.sh archive`
- After major changes: Run `schema-only.sh` and `seed-data.sh` to update reference files
- Before deployments: Create a full backup using `backup-db.sh`

## Important Notes

- Make sure the POSTscore database container (`postscore_db`) is running before executing these scripts.
- Store backups in a secure location outside of the project directory for disaster recovery.
- Verify your backups regularly by restoring to a test environment.
- Consider copying backups to an off-site location for additional protection. 