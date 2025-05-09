# Expense Tracker

A modern, GUI-based Expense Tracker application built with Python, Tkinter, and MySQL. This project allows users to manage their expenses efficiently with a clean and intuitive interface. It supports adding, deleting, viewing, and analyzing expenses by category, with a minimal and attractive design.

---
## Features

- **Admin Login**: Secure login system for administrators.
- **Expense Management**:
    - Add new expenses with amount, category, description, and date.
    - Delete expenses using a unique expense ID.
    - View all expenses in a tabular format with category details.
- **Statistics**: Visualize expense distribution by category.
- **Database Integration**: Uses MySQL for persistent storage with automatic table initialization.
- **Modern UI**: Clean design with a minimal color palette (#2B2D42, #8D99AE, #EF233C, #EDF2F4), smooth typography, and hover effects.
- **Responsive Layout**: Organized tabs for different functionalities (Add Expense, View Expenses, Statistics).

---

## Screenshots

![login](https://github.com/darshitdudhaiya/Expense-Tacker/blob/main/Screenshots/Screenshot%202025-05-10%20001348.png)
![Add Expense](https://github.com/darshitdudhaiya/Expense-Tacker/blob/main/Screenshots/Screenshot%202025-05-10%20001434.png)
![View Expenses](https://github.com/darshitdudhaiya/Expense-Tacker/blob/main/Screenshots/Screenshot%202025-05-10%20001542.png)
![Statistics](https://github.com/darshitdudhaiya/Expense-Tacker/blob/main/Screenshots/Screenshot%202025-05-10%20001542.png)

---

## Requirements

- Python 3.6+
- MySQL Server
- Required Python packages:
    - `mysql-connector-python`
    - `tkinter` (usually included with Python)

---

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

2. **Set Up MySQL:**

- Ensure MySQL is installed and running.
- Create a database named `expense_tracker` (the application will initialize tables automatically).
- Update the database connection details in `expense_tracker.py` if your MySQL credentials 
differ:

```python
con = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
```

3. **Install Dependencies**:

```bash
pip install mysql-connector-python
```

4. **Run the Application**:

```bash
python expense_tracker.py
```

---

## Usage

1. **Login**:

- Default credentials: 
    - Username: `admin`
    - Password: `password123`

- Update credentials in the `admin` table if needed.

2. **Add Expense**:

- Navigate to the "Add Expense" tab.
- Enter the amount, category (e.g., Food, Transport), description, and date (YYYY-MM-DD).
- Click "ADD EXPENSE" to save.

3. **Delete Expense**:

- In the "Add Expense" tab, enter the expense ID (visible in the "View Expenses" tab).
- Click "DELETE EXPENSE" to remove it.

4. **View Expenses**:

- Go to the "View Expenses" tab to see all expenses in a table.
- Click "REFRESH" to update the list.

5. **View Statistics**:

- In the "Statistics" tab, click "VIEW STATISTICS" to see a breakdown of expenses by category.

---

## Database Structure
The application automatically creates the following tables if they don't exist:

- **admin**: Stores admin credentials (`username`, `password`).
- **categories**: Stores expense categories (`category_id`, `category_name`).
- **expenses**: Stores expense details (`expense_id`, `amount`, `category_id`, `description`, `expense_date`).

Default categories: Food, Transport, Entertainment, Bills, Other.

---

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a Pull Request.

---

## Acknowledgments

- Built with Tkinter for GUI.
- Uses MySQL Connector for database connectivity.
- Designed by the DBMS Project Team.

---

## Contact
For issues or suggestions, please open an issue
on GitHub or contact the project maintainers.

---

**Note**: Replace `your-username` in the clone URL with your actual GitHub username.
