import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class CalorieVisualizer:
    def __init__(self, db_connection):
        self.db = db_connection
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

    def plot_calories(self, frame, days):
        data = self.get_data(days)
        dates = [row[0] for row in data]
        calories = [row[1] for row in data]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(dates, calories)
        ax.set_title(f"Calorie Intake Over the Last {days} Days")
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories")
        plt.xticks(rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas.draw()

    def plot_weekly_calories(self, frame):
        self.plot_calories(frame, 7)

    def plot_monthly_calories(self, frame):
        self.plot_calories(frame, 30)