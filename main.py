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

class CalorieTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calorie Tracking System")
        self.geometry("500x600")
        self.configure(padx=10, pady=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.db = self.connect_to_database()
        if not self.db:
            self.destroy()
            return

        self.cursor = self.db.cursor(buffered=True)
        self.calorie_goal = self.get_calorie_goal()
        self.create_widgets()

    def connect_to_database(self):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            self.show_message(f"Error connecting to database: {err}", "error")
            return None

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.meal_tab = ttk.Frame(self.notebook)
        self.visualize_tab = ttk.Frame(self.notebook)
        self.goals_tab = ttk.Frame(self.notebook)
        self.export_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.meal_tab, text="Meals")
        self.notebook.add(self.visualize_tab, text="Visualize")
        self.notebook.add(self.goals_tab, text="Goals")
        self.notebook.add(self.export_tab, text="Export")

        self.create_meal_tab()
        self.create_visualize_tab()
        self.create_goals_tab()
        self.create_export_tab()

    def create_meal_tab(self):
        frame = ttk.Frame(self.meal_tab, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Add Meal", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Meal:", "Calories:", "Date:", "Time:"]
        for i, label in enumerate(labels, start=1):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky="w", pady=5)

        self.meal_entry = ttk.Entry(frame)
        self.calories_entry = ttk.Entry(frame)
        self.datetime_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.time_entry = ttk.Entry(frame)
        self.time_entry.insert(0, "HH:MM")

        entries = [self.meal_entry, self.calories_entry, self.datetime_entry, self.time_entry]
        for i, entry in enumerate(entries, start=1):
            entry.grid(row=i, column=1, sticky="ew", pady=5)

        ttk.Button(frame, text="Add Meal", command=self.add_meal).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="View Meals", font=("Arial", 14, "bold")).grid(row=6, column=0, columnspan=2, pady=10)

        self.meals_tree = ttk.Treeview(frame, columns=("Date", "Time", "Meal", "Calories"), show="headings")
        self.meals_tree.grid(row=7, column=0, columnspan=2, sticky="nsew")

        for col in self.meals_tree["columns"]:
            self.meals_tree.heading(col, text=col)
            self.meals_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.meals_tree.yview)
        scrollbar.grid(row=7, column=2, sticky="ns")
        self.meals_tree.configure(yscrollcommand=scrollbar.set)

        self.view_date_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.view_date_entry.grid(row=8, column=0, pady=10, padx=5)
        ttk.Button(frame, text="View Meals", command=self.view_meals).grid(row=8, column=1, pady=10, padx=5)

        ttk.Button(frame, text="View Today's Meals", command=self.view_meals).grid(row=8, column=0, pady=10)
        ttk.Button(frame, text="Delete Selected", command=self.delete_meal).grid(row=8, column=1, pady=10)

    def create_visualize_tab(self):
        frame = ttk.Frame(self.visualize_tab, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Visualize Weekly Calories", command=self.visualize_weekly_calories).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="Visualize Monthly Calories", command=self.visualize_monthly_calories).grid(row=1, column=0, pady=10)

    def create_goals_tab(self):
        frame = ttk.Frame(self.goals_tab, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Set Calorie Goal", command=self.set_calorie_goal).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="View Calorie Goal", command=self.view_calorie_goal).grid(row=1, column=0, pady=10)

    def create_export_tab(self):
        frame = ttk.Frame(self.export_tab, padding="20")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)

        ttk.Button(frame, text="Export Data", command=self.export_data).grid(row=0, column=0, pady=10)
        ttk.Button(frame, text="Generate Report", command=self.generate_report).grid(row=1, column=0, pady=10)

    def add_meal(self):
        try:
            meal = self.meal_entry.get()
            calories = int(self.calories_entry.get())
            meal_date = self.datetime_entry.get_date()
            meal_time = datetime.strptime(self.time_entry.get(), "%H:%M").time()
            meal_datetime = datetime.combine(meal_date, meal_time)

            query = "INSERT INTO meals (datetime, meal, calories) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (meal_datetime, meal, calories))
            self.db.commit()
            self.show_message("Meal added successfully", "info")
            self.clear_entries()
            self.view_meals()
            self.check_calorie_goal()
        except ValueError:
            self.show_message("Please enter valid data for all fields", "error")
        except mysql.connector.Error as err:
            self.show_message(f"Error adding meal: {err}", "error")

    def clear_entries(self):
        self.meal_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM")

    def view_meals(self):
        self.meals_tree.delete(*self.meals_tree.get_children())
        selected_date = self.view_date_entry.get_date()
        query = "SELECT id, datetime, meal, calories FROM meals WHERE DATE(datetime) = %s ORDER BY datetime"
        self.cursor.execute(query, (selected_date,))
        results = self.cursor.fetchall()

        for row in results:
            meal_id, meal_datetime, meal, calories = row
            self.meals_tree.insert("", "end", values=(meal_datetime.strftime('%I:%M %p'), meal, calories), tags=(meal_id,))

    def delete_meal(self):
        selected_item = self.meals_tree.selection()
        if selected_item:
            meal_id = self.meals_tree.item(selected_item)['tags'][0]
            query = "DELETE FROM meals WHERE id = %s"
            self.cursor.execute(query, (meal_id,))
            self.db.commit()
            self.meals_tree.delete(selected_item)
            self.show_message("Meal deleted successfully", "info")
        else:
            self.show_message("Please select a meal to delete", "warning")

    def visualize_weekly_calories(self):
        visualizer = CalorieVisualizer()
        visualizer.plot_weekly_calories()
        self.show_message("Weekly calorie chart has been saved as 'calorie_intake_7_days.png'", "info")

    def visualize_monthly_calories(self):
        visualizer = CalorieVisualizer()
        visualizer.plot_monthly_calories()
        self.show_message("Monthly calorie chart has been saved as 'calorie_intake_30_days.png'", "info")

    def set_calorie_goal(self):
        goal = simpledialog.askinteger("Calorie Goal", "Enter your daily calorie goal:")
        if goal:
            self.calorie_goal = goal
            query = "INSERT INTO calorie_goals (goal) VALUES (%s) ON DUPLICATE KEY UPDATE goal = %s"
            self.cursor.execute(query, (goal, goal))
            self.db.commit()
            self.show_message(f"Calorie goal set to {goal}", "info")

    def view_calorie_goal(self):
        if self.calorie_goal:
            self.show_message(f"Your current daily calorie goal is {self.calorie_goal}", "info")
        else:
            self.show_message("No calorie goal set", "info")

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
                self.show_message(f"You've exceeded your daily calorie goal of {self.calorie_goal}", "warning")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            query = "SELECT datetime, meal, calories FROM meals ORDER BY datetime"
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Date', 'Time', 'Meal', 'Calories'])
                for row in results:
                    writer.writerow([row[0].date(), row[0].strftime('%I:%M %p'), row[1], row[2]])

            self.show_message(f"Data exported to {file_path}", "info")

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

        self.show_message(report, "info")

    def show_message(self, message, message_type):
        if message_type == "error":
            messagebox.showerror("Error", message)
        elif message_type == "info":
            messagebox.showinfo("Info", message)
        elif message_type == "warning":
            messagebox.showwarning("Warning", message)

if __name__ == "__main__":
    app = CalorieTracker()
    app.mainloop()
