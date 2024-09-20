-- Create the 'user' table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert a test user
INSERT INTO user (email, password)
VALUES ('test@example.com', '$2b$12$zqBJbzTVqL9jS4ROwjiu0eMhzWWf4WRCjeaWdcwdHleOyebWSWDh6'); -- Password: testpassword
