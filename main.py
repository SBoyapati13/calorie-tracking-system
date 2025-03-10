import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
from visualizer import CalorieVisualizer
import csv

load_dotenv()

class CalorieTracker:
    def __init__(self, master):
        self.master = master
        master.title("Calorie Tracking System")
        master.geometry("600x450")

        self.db = self.connect_to_database()
        if not self.db:
            master.destroy()
            return

        self.cursor = self.db.cursor(buffered=True)
        self.create_notebook()
        self.calorie_goal = self.get_calorie_goal()

    def connect_to_database(self):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.add_meal_tab = ttk.Frame(self.notebook)
        self.view_meals_tab = ttk.Frame(self.notebook)
        self.visualize_tab = ttk.Frame(self.notebook)
        self.goals_tab = ttk.Frame(self.notebook)
        self.export_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.add_meal_tab, text="Add Meal")
        self.notebook.add(self.view_meals_tab, text="View Meals")
        self.notebook.add(self.visualize_tab, text="Visualize")
        self.notebook.add(self.goals_tab, text="Goals")
        self.notebook.add(self.export_tab, text="Export")

        self.create_add_meal_tab()
        self.create_view_meals_tab()
        self.create_visualize_tab()
        self.create_goals_tab()
        self.create_export_tab()

    def create_add_meal_tab(self):
        frame = ttk.Frame(self.add_meal_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Meal:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.meal_entry = ttk.Entry(frame)
        self.meal_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Calories:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.calories_entry = ttk.Entry(frame)
        self.calories_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.datetime_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.datetime_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Time:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.time_entry = ttk.Entry(frame)
        self.time_entry.insert(0, "HH:MM")
        self.time_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(frame, text="Add Meal", command=self.add_meal).grid(row=4, column=0, columnspan=2, pady=10)

    def create_view_meals_tab(self):
        frame = ttk.Frame(self.view_meals_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.meals_text = tk.Text(frame, height=15, width=50)
        self.meals_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.meals_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.meals_text.configure(yscrollcommand=scrollbar.set)

        ttk.Button(frame, text="View Today's Meals", command=self.view_meals).grid(row=1, column=0, columnspan=2, pady=10)

    def create_visualize_tab(self):
        frame = ttk.Frame(self.visualize_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Visualize Weekly Calories", command=self.visualize_weekly_calories).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="Visualize Monthly Calories", command=self.visualize_monthly_calories).grid(row=1, column=0, pady=10)

    def create_goals_tab(self):
        frame = ttk.Frame(self.goals_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Set Calorie Goal", command=self.set_calorie_goal).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="View Calorie Goal", command=self.view_calorie_goal).grid(row=1, column=0, pady=10)

    def create_export_tab(self):
        frame = ttk.Frame(self.export_tab, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Export Data", command=self.export_data).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="Generate Report", command=self.generate_report).grid(row=1, column=0, pady=10)

    def add_meal(self):
        meal = self.meal_entry.get()
        calories = self.calories_entry.get()
        meal_date = self.datetime_entry.get_date()
        meal_time = self.time_entry.get()

        if meal and calories and meal_time:
            try:
                calories = int(calories)
                meal_datetime = datetime.combine(meal_date, datetime.strptime(meal_time, "%H:%M").time())
                query = "INSERT INTO meals (datetime, meal, calories) VALUES (%s, %s, %s)"
                self.cursor.execute(query, (meal_datetime, meal, calories))
                self.db.commit()
                messagebox.showinfo("Success", "Meal added successfully!")
                self.clear_entries()
                self.check_calorie_goal()
            except ValueError:
                messagebox.showerror("Error", "Calories must be a number and time must be in HH:MM format")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error adding meal: {err}")
        else:
            messagebox.showerror("Error", "Please enter meal, calories, and time")

    def clear_entries(self):
        self.meal_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM")

    def view_meals(self):
        today = date.today()
        query = "SELECT datetime, meal, calories FROM meals WHERE DATE(datetime) = %s ORDER BY datetime"
        self.cursor.execute(query, (today,))
        results = self.cursor.fetchall()

        self.meals_text.delete(1.0, tk.END)
        if results:
            for meal_datetime, meal, calories in results:
                self.meals_text.insert(tk.END, f"{meal_datetime.strftime('%I:%M %p')}: {meal} - {calories} calories\n")
            total_calories = sum(calories for _, _, calories in results)
            self.meals_text.insert(tk.END, f"\nTotal Calories: {total_calories}")
        else:
            self.meals_text.insert(tk.END, "No meals logged for today")

    def visualize_weekly_calories(self):
        visualizer = CalorieVisualizer()
        visualizer.plot_weekly_calories()
        messagebox.showinfo("Visualization", "Weekly calorie chart has been saved as 'calorie_intake_7_days.png'")

    def visualize_monthly_calories(self):
        visualizer = CalorieVisualizer()
        visualizer.plot_monthly_calories()
        messagebox.showinfo("Visualization", "Monthly calorie chart has been saved as 'calorie_intake_30_days.png'")

    def set_calorie_goal(self):
        goal = simpledialog.askinteger("Calorie Goal", "Enter your daily calorie goal:")
        if goal:
            self.calorie_goal = goal
            query = "INSERT INTO calorie_goals (goal) VALUES (%s) ON DUPLICATE KEY UPDATE goal = %s"
            self.cursor.execute(query, (goal, goal))
            self.db.commit()
            messagebox.showinfo("Success", f"Calorie goal set to {goal}")

    def view_calorie_goal(self):
        if self.calorie_goal:
            messagebox.showinfo("Calorie Goal", f"Your current daily calorie goal is {self.calorie_goal}")
        else:
            messagebox.showinfo("Calorie Goal", "No calorie goal set")

    def get_calorie_goal(self):
        query = "SELECT goal FROM calorie_goals ORDER BY id DESC LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_calorie_goal(self):
        if self.calorie_goal:
            today = date.today()
            query = "SELECT SUM(calories) FROM meals WHERE DATE(datetime) = %s"
            self.cursor.execute(query, (today,))
            result = self.cursor.fetchone()
            total_calories = result[0] if result[0] else 0
            if total_calories > self.calorie_goal:
                messagebox.showwarning("Goal Exceeded", f"You've exceeded your daily calorie goal of {self.calorie_goal}")

    def export_data(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            query = "SELECT datetime, meal, calories FROM meals ORDER BY datetime"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'Time', 'Meal', 'Calories'])
                for row in results:
                    writer.writerow([row[0].date(), row[0].strftime('%I:%M %p'), row[1], row[2]])

            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

    def generate_report(self):
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        query = """
        SELECT DATE(datetime) as date, SUM(calories) as total_calories
        FROM meals
        WHERE DATE(datetime) BETWEEN %s AND %s
        GROUP BY DATE(datetime)
        ORDER BY DATE(datetime)
        """
        self.cursor.execute(query, (start_date, end_date))
        results = self.cursor.fetchall()

        total_calories = sum(row[1] for row in results)
        avg_calories = total_calories / len(results) if results else 0

        report = f"Calorie Report ({start_date} to {end_date}):\n\n"
        report += f"Total Calories: {total_calories}\n"
        report += f"Average Daily Calories: {avg_calories:.2f}\n\n"
        report += "Daily Breakdown:\n"
        for row in results:
            report += f"{row[0]}: {row[1]} calories\n"

        messagebox.showinfo("30-Day Calorie Report", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieTracker(root)
    root.mainloop()
