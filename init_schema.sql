-- Create tables for PostScore application

-- Players table
CREATE TABLE IF NOT EXISTS players (
    id VARCHAR(26) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    zip VARCHAR(50),
    handicap FLOAT,
    ghin_number VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    hashed_password VARCHAR(128),
    is_super BOOLEAN DEFAULT FALSE,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE IF NOT EXISTS courses (
    id VARCHAR(26) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    address VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    zip VARCHAR(50),
    website VARCHAR(50),
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tee boxes table
CREATE TABLE IF NOT EXISTS tee_boxes (
    id VARCHAR(26) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    course_id VARCHAR(26) NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    rating FLOAT,
    slope INTEGER,
    yardage INTEGER,
    hex VARCHAR(50),
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_tee_box_course_name ON tee_boxes(course_id, name);

-- Tee box holes table
CREATE TABLE IF NOT EXISTS tee_box_holes (
    id VARCHAR(26) PRIMARY KEY,
    tee_box_id VARCHAR(26) NOT NULL REFERENCES tee_boxes(id) ON DELETE CASCADE,
    hole_number INTEGER NOT NULL,
    par INTEGER NOT NULL,
    yardage INTEGER NOT NULL,
    handicap INTEGER NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Rounds table
CREATE TABLE IF NOT EXISTS rounds (
    id VARCHAR(26) PRIMARY KEY,
    course_id VARCHAR(26) NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    tee_box_id VARCHAR(26) NOT NULL REFERENCES tee_boxes(id) ON DELETE CASCADE,
    player_id VARCHAR(26) NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    total_score INTEGER,
    holes INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Round holes table
CREATE TABLE IF NOT EXISTS round_holes (
    id VARCHAR(26) PRIMARY KEY,
    round_id VARCHAR(26) NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    tee_box_hole_id VARCHAR(26) NOT NULL REFERENCES tee_box_holes(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    gir BOOLEAN,
    fairway VARCHAR(50),
    putts INTEGER,
    penalties INTEGER,
    sand BOOLEAN,
    water BOOLEAN,
    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(round_id, tee_box_hole_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_players_email ON players(email);
CREATE INDEX IF NOT EXISTS idx_courses_name ON courses(name);
CREATE INDEX IF NOT EXISTS idx_tee_boxes_course_id ON tee_boxes(course_id);
CREATE INDEX IF NOT EXISTS idx_tee_box_holes_tee_box_id ON tee_box_holes(tee_box_id);
CREATE INDEX IF NOT EXISTS idx_rounds_player_id ON rounds(player_id);
CREATE INDEX IF NOT EXISTS idx_rounds_course_id ON rounds(course_id);
CREATE INDEX IF NOT EXISTS idx_round_holes_round_id ON round_holes(round_id); 