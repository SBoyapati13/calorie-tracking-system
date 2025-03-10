CREATE DATABASE IF NOT EXISTS calorie_tracker;
USE calorie_tracker;

CREATE TABLE IF NOT EXISTS meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    meal VARCHAR(255),
    calories INT
);

CREATE INDEX idx_date ON meals(date);

CREATE TABLE IF NOT EXISTS calorie_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    goal INT,
    UNIQUE KEY unique_goal (goal)
);
