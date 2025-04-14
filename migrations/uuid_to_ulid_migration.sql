BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 13eea4ac64ad

CREATE OR REPLACE FUNCTION uuid_to_ulid(uuid_val TEXT) RETURNS TEXT AS $$
    DECLARE
        -- Use the UUID as a seed for a deterministic ULID
        -- This ensures foreign keys remain consistent
        result TEXT;
    BEGIN
        -- If the input is already in ULID format (26 chars), return as is
        IF LENGTH(uuid_val) = 26 THEN
            RETURN uuid_val;
        END IF;
        
        -- Convert UUID to a deterministic ULID-like value
        -- Use parts of the UUID to create something that looks like a ULID
        -- Real ULIDs have timestamp component, but we're creating deterministic values
        result := REPLACE(uuid_val, '-', '') || 'ULID';
        -- Ensure it's 26 characters long (ULID length)
        RETURN SUBSTRING(result, 1, 26);
    END;
    $$ LANGUAGE plpgsql;;

ALTER TABLE tee_boxes 
            DROP CONSTRAINT IF EXISTS tee_boxes_course_id_fkey;

ALTER TABLE rounds 
            DROP CONSTRAINT IF EXISTS rounds_course_id_fkey;

ALTER TABLE rounds 
            DROP CONSTRAINT IF EXISTS rounds_player_id_fkey;

ALTER TABLE tee_box_holes 
            DROP CONSTRAINT IF EXISTS tee_box_holes_tee_box_id_fkey;

ALTER TABLE rounds 
            DROP CONSTRAINT IF EXISTS rounds_tee_box_id_fkey;

ALTER TABLE round_holes 
            DROP CONSTRAINT IF EXISTS round_holes_tee_box_hole_id_fkey;

ALTER TABLE round_holes 
            DROP CONSTRAINT IF EXISTS round_holes_round_id_fkey;

ALTER TABLE round_holes
    DROP CONSTRAINT IF EXISTS unique_round_hole_per_round;

UPDATE courses 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

UPDATE tee_boxes
            SET course_id = uuid_to_ulid(course_id)
            WHERE LENGTH(course_id) != 26;

UPDATE rounds
            SET course_id = uuid_to_ulid(course_id)
            WHERE LENGTH(course_id) != 26;

UPDATE players 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

UPDATE rounds
            SET player_id = uuid_to_ulid(player_id)
            WHERE LENGTH(player_id) != 26;

UPDATE tee_boxes 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

UPDATE tee_box_holes
            SET tee_box_id = uuid_to_ulid(tee_box_id)
            WHERE LENGTH(tee_box_id) != 26;

UPDATE rounds
            SET tee_box_id = uuid_to_ulid(tee_box_id)
            WHERE LENGTH(tee_box_id) != 26;

UPDATE tee_box_holes 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

UPDATE round_holes
            SET tee_box_hole_id = uuid_to_ulid(tee_box_hole_id)
            WHERE LENGTH(tee_box_hole_id) != 26;

UPDATE rounds 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

UPDATE round_holes
            SET round_id = uuid_to_ulid(round_id)
            WHERE LENGTH(round_id) != 26;

UPDATE round_holes 
        SET id = uuid_to_ulid(id)
        WHERE LENGTH(id) != 26;

ALTER TABLE tee_boxes
            ADD CONSTRAINT tee_boxes_course_id_fkey
            FOREIGN KEY (course_id) REFERENCES courses(id);

ALTER TABLE rounds
            ADD CONSTRAINT rounds_course_id_fkey
            FOREIGN KEY (course_id) REFERENCES courses(id);

ALTER TABLE rounds
            ADD CONSTRAINT rounds_player_id_fkey
            FOREIGN KEY (player_id) REFERENCES players(id);

ALTER TABLE tee_box_holes
            ADD CONSTRAINT tee_box_holes_tee_box_id_fkey
            FOREIGN KEY (tee_box_id) REFERENCES tee_boxes(id);

ALTER TABLE rounds
            ADD CONSTRAINT rounds_tee_box_id_fkey
            FOREIGN KEY (tee_box_id) REFERENCES tee_boxes(id);

ALTER TABLE round_holes
            ADD CONSTRAINT round_holes_tee_box_hole_id_fkey
            FOREIGN KEY (tee_box_hole_id) REFERENCES tee_box_holes(id);

ALTER TABLE round_holes
            ADD CONSTRAINT round_holes_round_id_fkey
            FOREIGN KEY (round_id) REFERENCES rounds(id);

ALTER TABLE round_holes
    ADD CONSTRAINT unique_round_hole_per_round
    UNIQUE (round_id, tee_box_hole_id);

DROP FUNCTION IF EXISTS uuid_to_ulid(TEXT);

INSERT INTO alembic_version (version_num) VALUES ('13eea4ac64ad') RETURNING alembic_version.version_num;

COMMIT;

