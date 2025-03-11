import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta, date
import mysql.connector
import os
from dotenv import load_dotenv
import matplotlib.dates as mdates

load_dotenv()

class CalorieVisualizer:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cursor = self.db.cursor(buffered=True)

    def get_data(self, days):
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        query = """
            SELECT date, total_calories
            FROM daily_calories
            WHERE date BETWEEN %s AND %s
            ORDER BY date
        """
        self.cursor.execute(query, (start_date, end_date))
        return self.cursor.fetchall()

    def plot_calories(self, frame, days):
        data = self.get_data(days)
        dates = [row[0] for row in data]
        calories = [row[1] for row in data]

        # Convert dates to Matplotlib dates
        mpl_dates = mdates.date2num(dates)

        fig, ax = plt.subplots(figsize=(8, 6))  # Adjusted for better fit
        ax.bar(mpl_dates, calories, width=0.8)  # width for better spacing

        ax.set_xlabel("Date")
        ax.set_ylabel("Calories")
        ax.set_title(f"Calorie Intake Over the Last {days} Days")

        # Format the x-axis to show dates
        date_format = mdates.DateFormatter("%Y-%m-%d")
        ax.xaxis.set_major_formatter(date_format)

        # Ensure date labels are readable
        fig.autofmt_xdate()

        # Set x-axis ticks to show each date
        ax.set_xticks(mpl_dates)

        # Make sure the labels are within the graph
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

        plt.close(fig)  # close the figure

    def plot_weekly_calories(self, frame):
        self.plot_calories(frame, 7)

    def plot_monthly_calories(self, frame):
        self.plot_calories(frame, 30)
