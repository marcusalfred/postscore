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

### Uvicorn (local)
```bash
cd postscore/app
pip install -r requirements.txt
cp ../example.env .env   # fill in DB credentials
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage
### API Documentation
Once running, visit http://localhost:8000/docs for the interactive OpenAPI docs.

### Documentation Site
A full documentation site lives in the `docs/` directory, built with [Fumadocs](https://fumadocs.vercel.app).

```bash
cd docs
npm install
npm run dev   # http://localhost:3000/docs
```

Covers getting started, authentication, and API reference (generated from the live OpenAPI spec).

## Testing

Tests use pytest with an in-memory SQLite database — no running server or database required.

### Setup

```bash
cd postscore/app
python -m venv ../.venv
source ../.venv/bin/activate   # Windows: ..\.venv\Scripts\activate
pip install -r requirements.txt
```

### Run all tests

```bash
pytest tests/
```

### Run a specific test file

```bash
pytest tests/test_auth.py
pytest tests/test_courses.py
pytest tests/test_players.py
pytest tests/test_rounds.py
pytest tests/test_round_holes.py
```

### End-to-end round test

The e2e test simulates a full 18-hole round — signup, login, course setup, scoring all holes, and verifying final stats. Run with `-s` to see the play-by-play output:

```bash
pytest tests/test_e2e_round.py -v -s
```

Example output:
```
1. PLAYER SIGNUP     → Player created (id, name, handicap)
2. LOGIN             → JWT token issued
3. CREATE COURSE     → Pines Golf Club created
4. ADD TEE BOXES     → White tees, 18 holes
5. START ROUND       → Round ID assigned, player linked
6. SCORING           → Hole-by-hole: par, score, to-par, GIR, fairway, running total
7. ROUND WITH HOLES  → Total score and all 18 holes confirmed
8. ROUND STATS       → Score, GIR %, fairways %, avg putts, penalties
```

### Test coverage

| File | What it covers |
|---|---|
| `test_auth.py` | Signup, duplicate email, login, wrong password, `/me` |
| `test_courses.py` | Course CRUD, tee box uniqueness per course |
| `test_players.py` | Player list/get/patch, ownership enforcement |
| `test_rounds.py` | Round creation, 404, duplicate hole prevention |
| `test_round_holes.py` | Hole create/get/patch/delete, duplicate prevention |
| `test_e2e_round.py` | Full 18-hole round flow end-to-end |

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
