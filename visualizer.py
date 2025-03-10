import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class CalorieVisualizer:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.db.cursor(buffered=True)

    def get_weekly_data(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)
        query = "SELECT date, SUM(calories) FROM meals WHERE date BETWEEN %s AND %s GROUP BY date ORDER BY date"
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def plot_weekly_calories(self):
        data = self.get_weekly_data()
        dates = [row[0] for row in data]
        calories = [row[1] for row in data]

        plt.figure(figsize=(10, 6))
        plt.bar(dates, calories)
        plt.title("Weekly Calorie Intake")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("weekly_calories.png")
        plt.close()

if __name__ == "__main__":
    visualizer = CalorieVisualizer()
    visualizer.plot_weekly_calories()
