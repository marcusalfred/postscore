# UUID to ULID Migration Guide

This document provides comprehensive instructions for migrating your PostgreSQL database from UUIDs to ULIDs (Universally Unique Lexicographically Sortable Identifiers).

## Prerequisites

1. PostgreSQL database running with your application data
2. Database credentials with sufficient privileges to modify tables and constraints
3. Python environment with Alembic installed (`pip install alembic`)

## Environment Setup

1. Create a `.env` file based on the `example.env` template:
   ```
   DB_NAME=postscore
   DB_HOST=localhost
   DB_USER=golf_api
   DB_PASSWORD=your_password
   DB_PORT=5432
   ```

2. Ensure your database is accessible:
   ```bash
   # Test connection to PostgreSQL
   psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME
   ```

## Migration Options

### Option 1: Using Docker Compose (Recommended)

If using Docker, this is the simplest approach:

1. Start your PostgreSQL container:
   ```bash
   docker-compose up -d postgres
   ```

2. Apply the migration:
   ```bash
   # Connect to the container
   docker-compose exec postgres bash
   
   # Inside the container, run the migration
   psql -U $POSTGRES_USER -d $POSTGRES_DB -f /path/to/uuid_to_ulid_migration.sql
   ```

### Option 2: Using Alembic

1. Ensure Alembic is configured with your database URL:
   ```bash
   # Check alembic.ini
   cat alembic.ini | grep sqlalchemy.url
   
   # If needed, update with your connection string
   # sqlalchemy.url = postgresql://user:pass@localhost/dbname
   ```

2. Run the migration:
   ```bash
   alembic upgrade head
   ```

### Option 3: Manual SQL Execution

1. Execute the SQL script directly:
   ```bash
   psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -f migrations/uuid_to_ulid_migration.sql
   ```

## Verification

After applying the migration, verify that:

1. All IDs in your database tables are now in ULID format (26 characters)
2. Foreign key relationships are intact
3. The application can successfully read and write data

```sql
-- Example verification queries
SELECT id FROM courses LIMIT 5;
SELECT id FROM players LIMIT 5;

-- Check foreign key integrity
SELECT c.id, t.id, t.course_id 
FROM courses c 
JOIN tee_boxes t ON c.id = t.course_id 
LIMIT 5;
```

## Troubleshooting

### Common Issues

1. **Database Connection Problems**:
   - Verify your connection parameters in `.env`
   - Ensure PostgreSQL is running (`docker ps` or `pg_isready`)
   - Check network connectivity (`ping` or `telnet` to the database host)

2. **Permission Errors**:
   - Ensure your database user has sufficient privileges
   - For Docker, check that volume mounts are correct

3. **Foreign Key Constraint Failures**:
   - The migration temporarily disables constraints, but if interrupted, you may need to manually fix constraints
   - Use `\d tablename` in psql to inspect table definitions

## Rollback Strategy

This migration is **not reversible** using Alembic, since ULIDs cannot be reliably converted back to their original UUIDs.

If you need to revert:
1. Restore from a database backup taken before the migration
2. Alternatively, recreate your database from scratch with the original schema

## Next Steps

1. Ensure all application code is updated to use ULIDs
2. Update any external services or integrations that might expect UUIDs
3. Monitor application performance and database operations
4. Consider adopting ULIDs in other parts of your infrastructure for consistency

---

For more information about ULIDs, see the [ULID specification](https://github.com/ulid/spec). 