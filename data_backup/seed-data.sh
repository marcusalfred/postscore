#!/bin/bash
# seed-data.sh

# Set up directory
SEED_DIR="."

# Extract key tables as seed data
echo "Extracting seed data from key tables..."
podman exec -it postscore_db pg_dump -U postgres -d postscore --table=courses --data-only > ${SEED_DIR}/seed_courses.sql
podman exec -it postscore_db pg_dump -U postgres -d postscore --table=tee_boxes --data-only > ${SEED_DIR}/seed_tee_boxes.sql
podman exec -it postscore_db pg_dump -U postgres -d postscore --table=tee_box_holes --data-only > ${SEED_DIR}/seed_tee_box_holes.sql

# Add more tables as needed
# podman exec -it postscore_db pg_dump -U postgres -d postscore --table=players --data-only > ${SEED_DIR}/seed_players.sql
# podman exec -it postscore_db pg_dump -U postgres -d postscore --table=rounds --data-only > ${SEED_DIR}/seed_rounds.sql

echo "Seed data created in ${SEED_DIR}/seed_*.sql files"
