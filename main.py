import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

class CalorieTracker:
    def __init__(self, master):
        self.master = master
        master.title("Calorie Tracking System")

        # Connect to MySQL database
        try:
            self.db = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            self.cursor = self.db.cursor(buffered=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            master.destroy()
            return

        # Create GUI elements
        self.label = tk.Label(master, text="Enter meal details:")
        self.label.pack()

        self.meal_entry = tk.Entry(master)
        self.meal_entry.pack()

        self.calories_entry = tk.Entry(master)
        self.calories_entry.pack()

        self.add_button = tk.Button(master, text="Add Meal", command=self.add_meal)
        self.add_button.pack()

        self.view_button = tk.Button(master, text="View Today's Meals", command=self.view_meals)
        self.view_button.pack()

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
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error adding meal: {err}")
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
            messagebox.showinfo("Today's Meals", f"{meal_list}\n\nTotal Calories: {total_calories}")
        else:
            messagebox.showinfo("Today's Meals", "No meals logged for today")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieTracker(root)
    root.mainloop()
