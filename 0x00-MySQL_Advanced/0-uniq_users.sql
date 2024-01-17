-- Create a table of users
-- Has 3 rows ID, EMAI and NAME

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255)
);
