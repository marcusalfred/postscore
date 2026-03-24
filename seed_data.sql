-- Insert test data for PostScore application

-- Insert test players
INSERT INTO players (id, name, email, zip, handicap, ghin_number, is_active, hashed_password, is_super)
VALUES 
    ('player1', 'Test User 1', 'test1@example.com', '12345', 10.5, '123456', TRUE, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE),
    ('player2', 'Test User 2', 'test2@example.com', '23456', 15.2, '234567', TRUE, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE),
    ('admin1', 'Admin User', 'admin@example.com', '34567', 5.0, '345678', TRUE, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Insert test courses
INSERT INTO courses (id, name, address, city, state, zip, website)
VALUES 
    ('course1', 'Test Golf Club', '123 Fairway Drive', 'Golf City', 'CA', '12345', 'https://testgolfclub.com'),
    ('course2', 'Pine Valley Golf Course', '456 Pine Street', 'Forest Hills', 'NY', '23456', 'https://pinevalley.com')
ON CONFLICT (id) DO NOTHING;

-- Insert test tee boxes
INSERT INTO tee_boxes (id, name, course_id, rating, slope, yardage, hex)
VALUES 
    ('teebox1', 'Blue', 'course1', 72.5, 130, 6800, '#0000FF'),
    ('teebox2', 'White', 'course1', 70.0, 125, 6400, '#FFFFFF'),
    ('teebox3', 'Blue', 'course2', 73.2, 135, 6900, '#0000FF'),
    ('teebox4', 'White', 'course2', 70.8, 128, 6500, '#FFFFFF')
ON CONFLICT (id) DO NOTHING;

-- Insert test tee box holes (18 holes for each tee box)
INSERT INTO tee_box_holes (id, tee_box_id, hole_number, par, yardage, handicap)
VALUES 
    -- Course 1 Blue Tees (Front 9)
    ('hole1_1', 'teebox1', 1, 4, 410, 5),
    ('hole1_2', 'teebox1', 2, 3, 175, 17),
    ('hole1_3', 'teebox1', 3, 5, 550, 1),
    ('hole1_4', 'teebox1', 4, 4, 420, 3),
    ('hole1_5', 'teebox1', 5, 4, 380, 13),
    ('hole1_6', 'teebox1', 6, 3, 195, 15),
    ('hole1_7', 'teebox1', 7, 4, 405, 7),
    ('hole1_8', 'teebox1', 8, 5, 530, 9),
    ('hole1_9', 'teebox1', 9, 4, 435, 11),
    -- Course 1 Blue Tees (Back 9)
    ('hole1_10', 'teebox1', 10, 4, 425, 4),
    ('hole1_11', 'teebox1', 11, 3, 185, 16),
    ('hole1_12', 'teebox1', 12, 5, 545, 2),
    ('hole1_13', 'teebox1', 13, 4, 415, 6),
    ('hole1_14', 'teebox1', 14, 4, 395, 14),
    ('hole1_15', 'teebox1', 15, 3, 180, 18),
    ('hole1_16', 'teebox1', 16, 4, 430, 8),
    ('hole1_17', 'teebox1', 17, 5, 525, 10),
    ('hole1_18', 'teebox1', 18, 4, 445, 12),

    -- Course 1 White Tees (Front 9)
    ('hole2_1', 'teebox2', 1, 4, 390, 5),
    ('hole2_2', 'teebox2', 2, 3, 160, 17),
    ('hole2_3', 'teebox2', 3, 5, 520, 1),
    ('hole2_4', 'teebox2', 4, 4, 400, 3),
    ('hole2_5', 'teebox2', 5, 4, 360, 13),
    ('hole2_6', 'teebox2', 6, 3, 175, 15),
    ('hole2_7', 'teebox2', 7, 4, 385, 7),
    ('hole2_8', 'teebox2', 8, 5, 500, 9),
    ('hole2_9', 'teebox2', 9, 4, 415, 11),
    -- Course 1 White Tees (Back 9)
    ('hole2_10', 'teebox2', 10, 4, 405, 4),
    ('hole2_11', 'teebox2', 11, 3, 165, 16),
    ('hole2_12', 'teebox2', 12, 5, 515, 2),
    ('hole2_13', 'teebox2', 13, 4, 395, 6),
    ('hole2_14', 'teebox2', 14, 4, 375, 14),
    ('hole2_15', 'teebox2', 15, 3, 160, 18),
    ('hole2_16', 'teebox2', 16, 4, 410, 8),
    ('hole2_17', 'teebox2', 17, 5, 495, 10),
    ('hole2_18', 'teebox2', 18, 4, 425, 12),

    -- Course 2 Blue Tees (Front 9)
    ('hole3_1', 'teebox3', 1, 4, 420, 7),
    ('hole3_2', 'teebox3', 2, 3, 180, 15),
    ('hole3_3', 'teebox3', 3, 5, 560, 3),
    ('hole3_4', 'teebox3', 4, 4, 430, 1),
    ('hole3_5', 'teebox3', 5, 4, 390, 11),
    ('hole3_6', 'teebox3', 6, 3, 190, 17),
    ('hole3_7', 'teebox3', 7, 4, 415, 5),
    ('hole3_8', 'teebox3', 8, 5, 540, 9),
    ('hole3_9', 'teebox3', 9, 4, 445, 13),
    -- Course 2 Blue Tees (Back 9)
    ('hole3_10', 'teebox3', 10, 4, 435, 2),
    ('hole3_11', 'teebox3', 11, 3, 175, 16),
    ('hole3_12', 'teebox3', 12, 5, 555, 4),
    ('hole3_13', 'teebox3', 13, 4, 425, 6),
    ('hole3_14', 'teebox3', 14, 4, 405, 12),
    ('hole3_15', 'teebox3', 15, 3, 185, 18),
    ('hole3_16', 'teebox3', 16, 4, 440, 8),
    ('hole3_17', 'teebox3', 17, 5, 535, 10),
    ('hole3_18', 'teebox3', 18, 4, 455, 14),

    -- Course 2 White Tees (Front 9)
    ('hole4_1', 'teebox4', 1, 4, 400, 7),
    ('hole4_2', 'teebox4', 2, 3, 165, 15),
    ('hole4_3', 'teebox4', 3, 5, 530, 3),
    ('hole4_4', 'teebox4', 4, 4, 410, 1),
    ('hole4_5', 'teebox4', 5, 4, 370, 11),
    ('hole4_6', 'teebox4', 6, 3, 170, 17),
    ('hole4_7', 'teebox4', 7, 4, 395, 5),
    ('hole4_8', 'teebox4', 8, 5, 510, 9),
    ('hole4_9', 'teebox4', 9, 4, 425, 13),
    -- Course 2 White Tees (Back 9)
    ('hole4_10', 'teebox4', 10, 4, 415, 2),
    ('hole4_11', 'teebox4', 11, 3, 155, 16),
    ('hole4_12', 'teebox4', 12, 5, 525, 4),
    ('hole4_13', 'teebox4', 13, 4, 405, 6),
    ('hole4_14', 'teebox4', 14, 4, 385, 12),
    ('hole4_15', 'teebox4', 15, 3, 165, 18),
    ('hole4_16', 'teebox4', 16, 4, 420, 8),
    ('hole4_17', 'teebox4', 17, 5, 505, 10),
    ('hole4_18', 'teebox4', 18, 4, 435, 14)
ON CONFLICT (id) DO NOTHING;

-- Insert test rounds
INSERT INTO rounds (id, course_id, tee_box_id, player_id, total_score, holes, start_time, end_time)
VALUES 
    ('round1', 'course1', 'teebox1', 'player1', 85, 18, CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day' + INTERVAL '4 hours'),
    ('round2', 'course2', 'teebox3', 'player2', 92, 18, CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days' + INTERVAL '4 hours')
ON CONFLICT (id) DO NOTHING;

-- Insert test round holes (18 holes for each round)
INSERT INTO round_holes (id, round_id, tee_box_hole_id, score, gir, fairway, putts, penalties, sand, water)
VALUES 
    -- Round 1 holes (Front 9)
    ('round1_1', 'round1', 'hole1_1', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round1_2', 'round1', 'hole1_2', 4, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round1_3', 'round1', 'hole1_3', 6, TRUE, 'center', 2, 0, FALSE, FALSE),
    ('round1_4', 'round1', 'hole1_4', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_5', 'round1', 'hole1_5', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round1_6', 'round1', 'hole1_6', 3, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_7', 'round1', 'hole1_7', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_8', 'round1', 'hole1_8', 5, TRUE, 'center', 2, 0, FALSE, FALSE),
    ('round1_9', 'round1', 'hole1_9', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    -- Round 1 holes (Back 9)
    ('round1_10', 'round1', 'hole1_10', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_11', 'round1', 'hole1_11', 3, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_12', 'round1', 'hole1_12', 6, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round1_13', 'round1', 'hole1_13', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_14', 'round1', 'hole1_14', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round1_15', 'round1', 'hole1_15', 4, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round1_16', 'round1', 'hole1_16', 4, TRUE, 'center', 1, 0, FALSE, FALSE),
    ('round1_17', 'round1', 'hole1_17', 5, TRUE, 'center', 2, 0, FALSE, FALSE),
    ('round1_18', 'round1', 'hole1_18', 4, TRUE, 'center', 1, 0, FALSE, FALSE),

    -- Round 2 holes (Front 9)
    ('round2_1', 'round2', 'hole3_1', 6, FALSE, 'left', 3, 0, TRUE, FALSE),
    ('round2_2', 'round2', 'hole3_2', 4, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_3', 'round2', 'hole3_3', 7, FALSE, 'center', 3, 1, FALSE, TRUE),
    ('round2_4', 'round2', 'hole3_4', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round2_5', 'round2', 'hole3_5', 5, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_6', 'round2', 'hole3_6', 4, FALSE, 'center', 2, 0, FALSE, FALSE),
    ('round2_7', 'round2', 'hole3_7', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round2_8', 'round2', 'hole3_8', 6, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_9', 'round2', 'hole3_9', 5, FALSE, 'center', 2, 0, FALSE, FALSE),
    -- Round 2 holes (Back 9)
    ('round2_10', 'round2', 'hole3_10', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round2_11', 'round2', 'hole3_11', 4, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_12', 'round2', 'hole3_12', 7, FALSE, 'center', 3, 1, FALSE, TRUE),
    ('round2_13', 'round2', 'hole3_13', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round2_14', 'round2', 'hole3_14', 5, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_15', 'round2', 'hole3_15', 4, FALSE, 'center', 2, 0, FALSE, FALSE),
    ('round2_16', 'round2', 'hole3_16', 5, FALSE, 'left', 2, 0, FALSE, FALSE),
    ('round2_17', 'round2', 'hole3_17', 6, FALSE, 'right', 2, 0, FALSE, FALSE),
    ('round2_18', 'round2', 'hole3_18', 5, FALSE, 'center', 2, 0, FALSE, FALSE)
ON CONFLICT (id) DO NOTHING; 