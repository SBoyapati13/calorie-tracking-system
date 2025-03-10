# Calorie Tracking System

An interactive calorie tracking system built with Python and MySQL, featuring a Tkinter GUI for efficient meal logging, calorie intake tracking, goal setting, and data analysis. Now with data visualization, reporting, and export capabilities!

## Features

- Log meals with calorie information and timestamps
- View daily meal logs with meal times and total calorie intake
- Visualize weekly calorie intake with a bar chart
- Set and track daily calorie goals
- Generate 30-day calorie reports
- Export data to CSV for further analysis
- Intuitive GUI for easy interaction
- MySQL database for persistent storage

## Installation

1. Clone the repository:

git clone https://github.com/SBoyapati13/calorie-tracking-system.git
cd calorie-tracking-system

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install required packages:

pip install -r requirements.txt

4. Set up the MySQL database:
- Create a database named `calorie_tracker`
- Run the SQL script in `database_setup.sql` to create the necessary table and index

5. Configure the `.env` file with your MySQL credentials:

DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=calorie_tracker

## Usage

Run the application:

python main.py

Use the GUI to add meals, view your daily calorie intake, visualize your weekly calorie intake, set and track calorie goals, generate reports, and export data.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)