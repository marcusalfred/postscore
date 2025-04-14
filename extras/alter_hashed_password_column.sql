-- Alter players table to increase hashed_password column length
ALTER TABLE players
ALTER COLUMN hashed_password TYPE VARCHAR(100); 