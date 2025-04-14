![logo](./logo.png)

# POSTScore
POSTScore is a simple REST API that allows golfers to track their scores.

## Installation
### Docker 

- clone repo
```
$ cd ./postscore
$  docker compose up --build -d
```

### Uvicorn
- install FastAPI - https://github.com/tiangolo/fastapi?tab=readme-ov-file#installation
- clone repo
```
$ cd ./postscore/app
$ pip install -r requirements.txt
$ uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555 
```

## Usage
### Documentation 
Once running, you can access the OpenAPI documention from http://localhost:5555/docs

## Database Management

### Backup and Restore

The project includes a comprehensive database backup and restore system in the `data_backup` directory. This system provides tools for:

- Creating full database backups
- Extracting schema definitions
- Managing seed data
- Database reset and restoration
- Scheduled backup automation

To use the backup system:

```bash
# Navigate to the data_backup directory
cd data_backup

# Create a full backup
./backup-db.sh

# Extract the current schema
./schema-only.sh

# Extract seed data
./seed-data.sh

# Manage existing backups
./manage-backups.sh list
```

For detailed instructions, see the [Database Backup README](./data_backup/README.md).

### Backup Schedule Recommendation

- Daily: Run scheduled backups via cron
- Weekly: Archive older backups
- Before deployments: Create a full backup
- After schema changes: Update schema and seed files
