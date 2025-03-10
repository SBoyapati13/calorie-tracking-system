import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image, ImageTk
import io

load_dotenv()

class CalorieTracker:
    def __init__(self, master):
        self.master = master
        master.title("Calorie Tracking System")
        master.geometry("400x600")

        self.db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.db.cursor()

        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        self.add_meal_tab = ttk.Frame(self.notebook)
        self.view_meals_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_meal_tab, text="Add Meal")
        self.notebook.add(self.view_meals_tab, text="View Meals")
        self.notebook.add(self.stats_tab, text="Statistics")

        self.create_add_meal_widgets()
        self.create_view_meals_widgets()
        self.create_stats_widgets()

    def create_add_meal_widgets(self):
        ttk.Label(self.add_meal_tab, text="Enter meal details:").pack(pady=10)

        ttk.Label(self.add_meal_tab, text="Meal Name:").pack()
        self.meal_entry = ttk.Entry(self.add_meal_tab)
        self.meal_entry.pack()

        ttk.Label(self.add_meal_tab, text="Calories:").pack()
        self.calories_entry = ttk.Entry(self.add_meal_tab)
        self.calories_entry.pack()

        ttk.Button(self.add_meal_tab, text="Add Meal", command=self.add_meal).pack(pady=10)

        ttk.Button(self.add_meal_tab, text="Set Daily Target", command=self.set_daily_target).pack(pady=10)

    def create_view_meals_widgets(self):
        self.meals_tree = ttk.Treeview(self.view_meals_tab, columns=("Meal", "Calories"), show="headings")
        self.meals_tree.heading("Meal", text="Meal")
        self.meals_tree.heading("Calories", text="Calories")
        self.meals_tree.pack(pady=10, fill="both", expand=True)

        ttk.Button(self.view_meals_tab, text="View Today's Meals", command=self.view_meals).pack(pady=10)

    def create_stats_widgets(self):
        ttk.Button(self.stats_tab, text="View Weekly Chart", command=self.view_weekly_chart).pack(pady=10)
        ttk.Button(self.stats_tab, text="Export Data", command=self.export_data).pack(pady=10)

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
                self.view_meals()
            except ValueError:
                messagebox.showerror("Error", "Calories must be a number")
        else:
            messagebox.showerror("Error", "Please enter both meal and calories")

    def view_meals(self):
        for item in self.meals_tree.get_children():
            self.meals_tree.delete(item)

        today = date.today()
        query = "SELECT meal, calories FROM meals WHERE date = %s"
        self.cursor.execute(query, (today,))
        results = self.cursor.fetchall()

        total_calories = 0
        for meal, calories in results:
            self.meals_tree.insert("", "end", values=(meal, calories))
            total_calories += calories

        target_query = "SELECT target FROM daily_targets WHERE date = %s"
        self.cursor.execute(target_query, (today,))
        target_result = self.cursor.fetchone()

        if target_result:
            daily_target = target_result[0]
            remaining_calories = daily_target - total_calories
            self.meals_tree.insert("", "end", values=("Total Calories", total_calories))
            self.meals_tree.insert("", "end", values=("Daily Target", daily_target))
            self.meals_tree.insert("", "end", values=("Remaining Calories", remaining_calories))
        else:
            self.meals_tree.insert("", "end", values=("Total Calories", total_calories))
            self.meals_tree.insert("", "end", values=("No daily target set", ""))

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

    def export_data(self):
        query = "SELECT date, meal, calories FROM meals ORDER BY date"
        df = pd.read_sql(query, self.db)
        
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

root = tk.Tk()
app = CalorieTracker(root)
root.mainloop()
