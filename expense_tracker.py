# Note: Create database in phpmyadmin with name "expense_tracker"

from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import mysql.connector
import uuid

# Database connection
con = mysql.connector.connect(host="localhost", user="root", password="", database="expense_tracker")
check = 0

# Initialize database tables if they don't exist
def init_db():
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
    cur.execute("USE expense_tracker")
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50)
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            category_name VARCHAR(50) UNIQUE
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id VARCHAR(36) PRIMARY KEY,
            amount DECIMAL(10,2),
            category_id INT,
            description VARCHAR(200),
            expense_date DATE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)
    
    cur.execute("SELECT COUNT(*) FROM admin")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", ("admin", "password123"))
    
    cur.execute("SELECT COUNT(*) FROM categories")
    if cur.fetchone()[0] == 0:
        default_categories = ["Food", "Transport", "Entertainment", "Bills", "Other"]
        for cat in default_categories:
            cur.execute("INSERT INTO categories (category_name) VALUES (%s)", (cat,))
    
    con.commit()

init_db()

def enter():
    def add_expense():
        amount = ent1.get()
        category = ent2.get()
        desc = ent3.get()
        date = ent4.get()
        
        if not all([amount, category, desc, date]):
            messagebox.showerror("Error", "All fields are required!")
            return
            
        try:
            cur = con.cursor()
            cur.execute("SELECT category_id FROM categories WHERE category_name=%s", (category,))
            cat_id = cur.fetchone()
            if not cat_id:
                messagebox.showerror("Error", "Invalid category!")
                return
            
            expense_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO expenses (expense_id, amount, category_id, description, expense_date) 
                VALUES (%s, %s, %s, %s, %s)
            """, (expense_id, float(amount), cat_id[0], desc, date))
            con.commit()
            
            ent1.set(0.0)
            ent2.set("")
            ent3.set("")
            ent4.set("")
            messagebox.showinfo('Success', "Expense added!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
    def delete_expense():
        expense_id = ent5.get()
        if not expense_id:
            messagebox.showerror("Error", "Please enter expense ID!")
            return
            
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM expenses WHERE expense_id=%s", (expense_id,))
            if cur.rowcount == 0:
                messagebox.showerror("Error", "Expense ID not found!")
                return
            con.commit()
            ent5.set("")
            messagebox.showinfo('Success', 'Expense deleted!')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete expense: {str(e)}")

    def refresh_expenses():
        for item in tree.get_children():
            tree.delete(item)
        cur = con.cursor()
        cur.execute("""
            SELECT e.expense_id, e.amount, c.category_name, e.description, e.expense_date
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
        """)
        for row in cur:
            tree.insert('', 'end', values=row)
        con.commit()

    # Main window
    root = Toplevel()
    root.geometry("700x600")
    root.configure(bg='#EDF2F4')
    root.title("Expense Tracker")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TNotebook', background='#EDF2F4', borderwidth=0)
    style.configure('TNotebook.Tab', 
                    background='#8D99AE', 
                    foreground='#2B2D42',
                    padding=[10, 5],
                    font=('Helvetica', 10, 'bold'))
    style.map('TNotebook.Tab', 
              background=[('selected', '#2B2D42'), ('active', '#8D99AE')],
              foreground=[('selected', '#EDF2F4'), ('active', '#2B2D42')])
    
    style.configure('TButton',
                    background='#2B2D42',
                    foreground='#EDF2F4',
                    font=('Helvetica', 10),
                    padding=8,
                    borderwidth=0)
    style.map('TButton',
              background=[('active', '#EF233C')],
              foreground=[('active', '#EDF2F4')])
    
    style.configure('Treeview',
                    background='#FFFFFF',
                    foreground='#2B2D42',
                    rowheight=25,
                    fieldbackground='#FFFFFF')
    style.configure('Treeview.Heading',
                    background='#2B2D42',
                    foreground='#EDF2F4',
                    font=('Helvetica', 10, 'bold'))
    style.map('Treeview',
              background=[('selected', '#8D99AE')])

    # Notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=1, padx=10, pady=10)

    # Frames
    frame1 = Frame(notebook, bg='#EDF2F4')
    frame2 = Frame(notebook, bg='#EDF2F4')
    frame3 = Frame(notebook, bg='#EDF2F4')

    frame1.pack(fill="both", expand=1)
    frame2.pack(fill="both", expand=1)
    frame3.pack(fill="both", expand=1)

    notebook.add(frame1, text="Add Expense")
    notebook.add(frame2, text="View Expenses")
    notebook.add(frame3, text="Statistics")

    # Add Expense Frame
    Label(frame1, 
          text="Expense Tracker", 
          bg='#EDF2F4', 
          fg='#2B2D42',
          font=('Helvetica', 16, 'bold')).pack(pady=20)

    ent1 = DoubleVar()
    ent2 = StringVar()
    ent3 = StringVar()
    ent4 = StringVar()
    ent5 = StringVar()

    fields = [
        ("Amount", ent1, 80),
        ("Category", ent2, 110),
        ("Description", ent3, 140),
        ("Date (YYYY-MM-DD)", ent4, 170),
        ("Expense ID (to delete)", ent5, 200)
    ]

    for label, var, y in fields:
        Label(frame1, 
              text=label, 
              bg='#EDF2F4', 
              fg='#2B2D42',
              font=('Helvetica', 10)).place(x=150, y=y)
        entry = Entry(frame1, 
                     textvariable=var, 
                     bg='#FFFFFF', 
                     fg='#2B2D42',
                     font=('Helvetica', 10),
                     relief='flat',
                     width=30)
        entry.place(x=250, y=y)
        Frame(frame1, 
              bg='#8D99AE', 
              height=1).place(x=250, y=y+20, width=200)

    ttk.Button(frame1, 
              text="ADD EXPENSE", 
              command=add_expense).place(x=250, y=250, width=100)
    ttk.Button(frame1, 
              text="DELETE EXPENSE", 
              command=delete_expense).place(x=360, y=250, width=120)

    # View Expenses Frame
    Label(frame2, 
          text="All Expenses", 
          bg='#EDF2F4', 
          fg='#2B2D42',
          font=('Helvetica', 16, 'bold')).pack(pady=20)

    tree_frame = Frame(frame2, bg='#EDF2F4')
    tree_frame.pack(fill='both', expand=1, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame, show='headings')
    scroll = Scrollbar(tree_frame, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    tree.pack(fill='both', expand=1)

    tree['columns'] = ("ID", "Amount", "Category", "Description", "Date")
    column_widths = [150, 100, 100, 150, 100]
    for col, width in zip(tree['columns'], column_widths):
        tree.column(col, width=width, anchor=CENTER)
        tree.heading(col, text=col, anchor=CENTER)

    ttk.Button(frame2, 
              text="REFRESH", 
              command=refresh_expenses).place(x=300, y=450, width=100)
    refresh_expenses()

    # Statistics Frame
    def show_stats():
        cur = con.cursor()
        cur.execute("""
            SELECT c.category_name, SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            GROUP BY c.category_name
        """)
        stats = cur.fetchall()
        con.commit()

        stats_win = Toplevel()
        stats_win.geometry("500x400")
        stats_win.configure(bg='#EDF2F4')
        stats_win.title("Expense Statistics")

        Label(stats_win, 
              text="Expense Statistics", 
              bg='#EDF2F4', 
              fg='#2B2D42',
              font=('Helvetica', 16, 'bold')).pack(pady=20)

        tree_stats = ttk.Treeview(stats_win, show='headings')
        tree_stats['columns'] = ("Category", "Total Amount")
        
        for col in tree_stats['columns']:
            tree_stats.column(col, width=200, anchor=CENTER)
            tree_stats.heading(col, text=col, anchor=CENTER)

        for row in stats:
            tree_stats.insert('', 'end', values=row)
        
        tree_stats.pack(fill='both', expand=1, padx=10, pady=10)

    Label(frame3, 
          text="Expense Statistics", 
          bg='#EDF2F4', 
          fg='#2B2D42',
          font=('Helvetica', 16, 'bold')).pack(pady=20)
    ttk.Button(frame3, 
              text="VIEW STATISTICS", 
              command=show_stats).place(x=300, y=100, width=140)

    root.mainloop()

def submit():
    username = a.get()
    password = b.get()
    cur = con.cursor()
    cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    if cur.fetchone():
        messagebox.showinfo("Valid!", "Welcome!")
        enter()
    else:
        messagebox.showwarning("Invalid!", "Try again!")
    con.commit()

# Login window
r = Tk()
r.title("Expense Tracker Login")
r.geometry("500x400")
r.configure(bg='#EDF2F4')

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton',
                background='#2B2D42',
                foreground='#EDF2F4',
                font=('Helvetica', 10),
                padding=8,
                borderwidth=0)
style.map('TButton',
          background=[('active', '#EF233C')],
          foreground=[('active', '#EDF2F4')])

a = StringVar()
b = StringVar()

Label(r, 
      text="Expense Tracker", 
      bg='#EDF2F4', 
      fg='#2B2D42',
      font=('Helvetica', 16, 'bold')).pack(pady=40)

frame = Frame(r, bg='#EDF2F4')
frame.pack(pady=20)

Label(frame, 
      text="Username", 
      bg='#EDF2F4', 
      fg='#2B2D42',
      font=('Helvetica', 10)).pack(pady=5)
Entry(frame, 
      textvariable=a, 
      bg='#FFFFFF', 
      fg='#2B2D42',
      font=('Helvetica', 10),
      relief='flat',
      width=30).pack()
Frame(frame, 
      bg='#8D99AE', 
      height=1).pack(fill='x', pady=5)

Label(frame, 
      text="Password", 
      bg='#EDF2F4', 
      fg='#2B2D42',
      font=('Helvetica', 10)).pack(pady=5)
Entry(frame, 
      textvariable=b, 
      show="*", 
      bg='#FFFFFF', 
      fg='#2B2D42',
      font=('Helvetica', 10),
      relief='flat',
      width=30).pack()
Frame(frame, 
      bg='#8D99AE', 
      height=1).pack(fill='x', pady=5)

ttk.Button(r, 
          text="LOGIN", 
          command=submit).pack(pady=30)

r.mainloop()