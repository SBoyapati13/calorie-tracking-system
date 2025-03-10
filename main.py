import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import date
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

load_dotenv()

class CalorieTracker:
    def __init__(self, master):
        self.master = master
        master.title("Calorie Tracking System")

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.db.cursor()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Enter meal details:")
        self.label.pack()

        self.meal_entry = tk.Entry(self.master)
        self.meal_entry.pack()

        self.calories_entry = tk.Entry(self.master)
        self.calories_entry.pack()

        self.add_button = tk.Button(self.master, text="Add Meal", command=self.add_meal)
        self.add_button.pack()

        self.view_button = tk.Button(self.master, text="View Today's Meals", command=self.view_meals)
        self.view_button.pack()

        self.set_target_button = tk.Button(self.master, text="Set Daily Target", command=self.set_daily_target)
        self.set_target_button.pack()

        self.view_chart_button = tk.Button(self.master, text="View Weekly Chart", command=self.view_weekly_chart)
        self.view_chart_button.pack()

    def add_meal(self):
        meal = self.meal_entry.get()
        calories = self.calories_entry.get()

        if meal and calories:
            try:
                calories = int(calories)
                today = date.today()
                query = "INSERT INTO meals (date, meal, calories) VALUES (%s, %s, %s)"
                values = (today, meal, calories)
                self.cursor.execute(query, values)
                self.db.commit()
                messagebox.showinfo("Success", "Meal added successfully!")
                self.meal_entry.delete(0, tk.END)
                self.calories_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Calories must be a number")
        else:
            messagebox.showerror("Error", "Please enter both meal and calories")

    def view_meals(self):
        today = date.today()
        query = "SELECT meal, calories FROM meals WHERE date = %s"
        self.cursor.execute(query, (today,))
        results = self.cursor.fetchall()

        if results:
            meal_list = "\n".join([f"{meal}: {calories} calories" for meal, calories in results])
            total_calories = sum(calories for _, calories in results)
            
            target_query = "SELECT target FROM daily_targets WHERE date = %s"
            self.cursor.execute(target_query, (today,))
            target_result = self.cursor.fetchone()
            
            if target_result:
                daily_target = target_result[0]
                remaining_calories = daily_target - total_calories
                messagebox.showinfo("Today's Meals", f"{meal_list}\n\nTotal Calories: {total_calories}\nDaily Target: {daily_target}\nRemaining Calories: {remaining_calories}")
            else:
                messagebox.showinfo("Today's Meals", f"{meal_list}\n\nTotal Calories: {total_calories}\nNo daily target set.")
        else:
            messagebox.showinfo("Today's Meals", "No meals logged for today")

    def set_daily_target(self):
        target = simpledialog.askinteger("Set Daily Target", "Enter your daily calorie target:")
        if target:
            today = date.today()
            query = "INSERT INTO daily_targets (date, target) VALUES (%s, %s) ON DUPLICATE KEY UPDATE target = %s"
            values = (today, target, target)
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Success", f"Daily target set to {target} calories")

    def view_weekly_chart(self):
        end_date = date.today()
        start_date = end_date - timedelta(days=6)
        
        query = """
        SELECT date, SUM(calories) as total_calories
        FROM meals
        WHERE date BETWEEN %s AND %s
        GROUP BY date
        ORDER BY date
        """
        self.cursor.execute(query, (start_date, end_date))
        results = self.cursor.fetchall()
        
        dates = [result[0] for result in results]
        calories = [result[1] for result in results]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(dates, calories)
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Calories")
        ax.set_title("Weekly Calorie Intake")
        plt.xticks(rotation=45)
        
        chart_window = tk.Toplevel(self.master)
        chart_window.title("Weekly Calorie Chart")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

root = tk.Tk()
app = CalorieTracker(root)
root.mainloop()