-- Fix Player table schema mismatches
-- Convert handicap from VARCHAR to FLOAT
ALTER TABLE players ALTER COLUMN handicap TYPE FLOAT USING handicap::float;

-- Convert ghin_number from INTEGER to VARCHAR
ALTER TABLE players ALTER COLUMN ghin_number TYPE VARCHAR;

-- Increase hashed_password field length from 50 to 128
ALTER TABLE players ALTER COLUMN hashed_password TYPE VARCHAR(128);

-- Add created_on column if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT FROM information_schema.columns 
    WHERE table_name = 'players' AND column_name = 'created_on'
  ) THEN
    ALTER TABLE players ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
  END IF;
END $$;

-- Set NOT NULL constraints for required fields
ALTER TABLE players ALTER COLUMN is_active SET DEFAULT TRUE;
ALTER TABLE players ALTER COLUMN is_super SET DEFAULT FALSE; 