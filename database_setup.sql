CREATE DATABASE IF NOT EXISTS calorie_tracker;
USE calorie_tracker;

CREATE TABLE IF NOT EXISTS meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datetime DATETIME,
    meal VARCHAR(255),
    calories INT
);

CREATE INDEX idx_datetime ON meals(datetime);

CREATE TABLE IF NOT EXISTS calorie_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    goal INT,
    UNIQUE KEY unique_goal (goal)
);
