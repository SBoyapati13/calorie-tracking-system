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
    goal INT
);

CREATE TABLE IF NOT EXISTS daily_calories (
    date DATE PRIMARY KEY,
    total_calories INT DEFAULT 0
);

-- Trigger to update daily_calories table when a new meal is added
DELIMITER //
CREATE TRIGGER after_meal_insert
AFTER INSERT ON meals
FOR EACH ROW
BEGIN
    INSERT INTO daily_calories (date, total_calories)
    VALUES (DATE(NEW.datetime), NEW.calories)
    ON DUPLICATE KEY UPDATE total_calories = total_calories + NEW.calories;
END;//

-- Trigger to update daily_calories table when a meal is deleted
CREATE TRIGGER after_meal_delete
AFTER DELETE ON meals
FOR EACH ROW
BEGIN
    UPDATE daily_calories
    SET total_calories = total_calories - OLD.calories
    WHERE date = DATE(OLD.datetime);

    -- Optionally, remove the entry from daily_calories if the total becomes 0
    IF (SELECT total_calories FROM daily_calories WHERE date = DATE(OLD.datetime)) = 0 THEN
        DELETE FROM daily_calories WHERE date = DATE(OLD.datetime);
    END IF;
END;//

-- Trigger to update daily_calories table when a meal is updated
CREATE TRIGGER after_meal_update
AFTER UPDATE ON meals
FOR EACH ROW
BEGIN
    -- Update total_calories for the old date
    UPDATE daily_calories
    SET total_calories = total_calories - OLD.calories
    WHERE date = DATE(OLD.datetime);

    -- Add total_calories for the new date
    INSERT INTO daily_calories (date, total_calories)
    VALUES (DATE(NEW.datetime), NEW.calories)
    ON DUPLICATE KEY UPDATE total_calories = total_calories + NEW.calories;

    --Clean up zero calorie days from the old date

    IF (SELECT total_calories FROM daily_calories WHERE date = DATE(OLD.datetime)) = 0 THEN
        DELETE FROM daily_calories WHERE date = DATE(OLD.datetime);
    END IF;

END;//

DELIMITER ;
