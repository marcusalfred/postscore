-- Add created_on timestamp column to players table
ALTER TABLE players ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() NOT NULL; 