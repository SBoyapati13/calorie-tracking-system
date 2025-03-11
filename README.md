# Calorie Tracking System

A Tkinter-based application for tracking daily calorie intake, setting goals, visualizing progress, and exporting data.

## Features

*   **Meal Management:**
    *   Add meals with details like name, calories, date, and time.
    *   View meals for a selected date.
    *   Delete unwanted meal entries.

*   **Goal Setting:**
    *   Set a daily calorie goal.
    *   View the current calorie goal.
    *   Track calories consumed vs. remaining through a pie chart.

*   **Data Visualization:**
    *   Visualize calorie intake through weekly and monthly bar graphs.

*   **Data Export:**
    *   Export meal data to a CSV file.
    *   Generate calorie reports for a specified period.

## Installation

1.  **Clone the Repository:**

    ```
    git clone <repository_url>
    cd calorie-tracking-system
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```
    pip install -r requirements.txt
    ```

4.  **Set up MySQL Database:**

    *   Ensure you have MySQL installed and running.
    *   Create a database named `calorie_tracker`.
    *   Run the SQL script in `database_setup.sql` to create necessary tables.

5.  **Configure Environment Variables:**

    *   Create a `.env` file in the project root.
    *   Add your MySQL connection details:

        ```
        DB_HOST=localhost
        DB_USER=your_mysql_username
        DB_PASSWORD=your_mysql_password
        DB_NAME=calorie_tracker
        ```

## Usage

1.  **Run the Application:**

    ```
    python main.py
    ```

2.  **Using the GUI:**

    *   **Meals Tab:** Add and view meal entries for a selected date.  Use the "Delete Selected" button to remove entries.

    *   **Visualize Tab:** View weekly and monthly calorie intake through bar graphs.

    *   **Goals Tab:** Set your daily calorie goal. The pie chart will visualize how much of your goal you've consumed.

    *   **Export Tab:** Export your data or generate a report.

## Database Setup

The application requires a MySQL database. The `database_setup.sql` file contains the SQL statements to create the necessary tables:

*   `meals`: Stores individual meal entries with date, time, description, and calorie information.
*   `calorie_goals`: Stores the history of calorie goals set by the user.

Remember to configure your MySQL credentials in the `.env` file.

## Requirements
All the requirements should be in the requirements.txt and make sure to do pip install -r requirements.txt.
## License

[MIT](LICENSE)
