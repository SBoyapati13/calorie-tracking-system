import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime, timedelta
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

    def get_data(self, days):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        query = """
        SELECT DATE(datetime) as date, SUM(calories) as total_calories
        FROM meals
        WHERE DATE(datetime) BETWEEN %s AND %s
        GROUP BY DATE(datetime)
        ORDER BY DATE(datetime)
        """
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def plot_calories(self, days):
        data = self.get_data(days)
        dates = [row[0] for row in data]
        calories = [row[1] for row in data]

        plt.figure(figsize=(12, 6))
        plt.bar(dates, calories)
        plt.title(f"Calorie Intake Over the Last {days} Days")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"calorie_intake_{days}_days.png")
        plt.close()

    def plot_weekly_calories(self):
        self.plot_calories(7)

    def plot_monthly_calories(self):
        self.plot_calories(30)

if __name__ == "__main__":
    visualizer = CalorieVisualizer()
    visualizer.plot_weekly_calories()
    visualizer.plot_monthly_calories()