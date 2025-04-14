-- Check if Admin user exists
DO $$
DECLARE
    user_exists BOOLEAN;
    user_id TEXT;
BEGIN
    -- Check if the user exists
    SELECT EXISTS(SELECT 1 FROM players WHERE email = 'admin@example.com') INTO user_exists;
    
    IF user_exists THEN
        -- Update existing user
        UPDATE players 
        SET 
            is_active = TRUE,
            is_super = TRUE,
            handicap = 10.0,
            zip = '12345',
            ghin_number = '1234567',
            -- Using a pre-hashed bcrypt password: 'adminpassword'
            hashed_password = '$2a$12$1X.GQIzB5Vz1N0ReR92kJ.Ky5/pfR.zK6Bqy91F2zfYUPvAATQsmW'
        WHERE email = 'admin@example.com'
        RETURNING id INTO user_id;
        
        RAISE NOTICE 'Updated user with ID: %', user_id;
    ELSE
        -- Create new user
        INSERT INTO players (
            id, name, email, zip, handicap, ghin_number, 
            is_active, is_super, hashed_password, created_on
        ) VALUES (
            -- Using ULID-like format
            '01JRPCAAAAAAAAAAAAAAAAAAA', 
            'Admin User', 
            'admin@example.com', 
            '12345', 
            10.0, 
            '1234567', 
            TRUE, 
            TRUE, 
            -- Using a pre-hashed bcrypt password: 'adminpassword'
            '$2a$12$1X.GQIzB5Vz1N0ReR92kJ.Ky5/pfR.zK6Bqy91F2zfYUPvAATQsmW',
            NOW()
        )
        RETURNING id INTO user_id;
        
        RAISE NOTICE 'Created user with ID: %', user_id;
    END IF;
END $$; 