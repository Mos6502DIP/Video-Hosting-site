-- Drop the Users table if it exists
DROP TABLE IF EXISTS Users;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    profile_picture_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Added timestamp for record creation
);

-- Drop the Videos table if it exists
DROP TABLE IF EXISTS Videos;

-- Create the Videos table
CREATE TABLE IF NOT EXISTS Videos (
    video_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each video
    user_id INTEGER,                           -- ID of the user who uploaded the video
    title TEXT NOT NULL,                       -- Title of the video
    description TEXT,                          -- Description of the video
    file_path TEXT NOT NULL,                   -- File path or URL of the video
    thumbnail_path TEXT,                       -- File path or URL of the video's thumbnail
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date and time of upload
    views INTEGER DEFAULT 0,                   -- Number of views
    likes INTEGER DEFAULT 0,                   -- Number of likes
    dislikes INTEGER DEFAULT 0,                -- Number of dislikes
    duration INTEGER,                          -- Duration of the video in seconds
    FOREIGN KEY (user_id) REFERENCES Users(id) -- Link to the users table
);

-- Drop the Videos table if it exists
DROP TABLE IF EXISTS VideoVerification;

-- Create the VideoVerification table
CREATE TABLE IF NOT EXISTS VideoVerification (
    verification_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each verification entry
    video_id INTEGER,                                 -- ID of the video that needs verification
    verifier_id INTEGER,                              -- ID of the user who verified the video
    status TEXT NOT NULL DEFAULT 'pending',           -- Status of the verification ('pending', 'verified', 'rejected')
    verification_date TIMESTAMP,                      -- Date and time of verification
    comments TEXT,                                    -- Optional comments from the verifier
    FOREIGN KEY (video_id) REFERENCES Videos(video_id), -- Link to the Videos table
    FOREIGN KEY (verifier_id) REFERENCES Users(id)       -- Link to the Users table for verifier
);


-- Query to check if the data has been inserted correctly
SELECT * FROM Users;