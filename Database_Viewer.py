import sqlite3
import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, messagebox, filedialog
import pandas as pd

def upload_database():
    global conn, cursor
    db_file = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
    if db_file:
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            upload_window.destroy()
            create_main_window()
        except Exception as e:
            messagebox.showerror("Error", str(e))

def run_query():
    query = query_entry.get().strip().lower()
    forbidden_commands = ["insert", "delete", "update", "drop"]
    if any(command in query for command in forbidden_commands):
        messagebox.showerror("Error", "INSERT, DELETE, UPDATE, and DROP queries are not allowed.")
        return
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        display_result(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_result(result):
    text_result.delete(1.0, tk.END)
    if result:
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        text_result.insert(tk.END, df.to_string(index=False))
    else:
        text_result.insert(tk.END, "No results to display")

def create_main_window():
    global query_entry, text_result, result_frame

    # Create main window
    root = tk.Tk()
    root.title("SQLite Database Viewer")

    # Create input field for SQL query
    label_query = Label(root, text="Enter SQL Query:")
    label_query.pack()

    query_entry = Entry(root, width=80)
    query_entry.pack()

    run_button = Button(root, text="Run Query", command=run_query)
    run_button.pack()

    # Create frame for displaying results
    result_frame = tk.Frame(root)
    result_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(result_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_result = Text(result_frame, wrap='word', yscrollcommand=scrollbar.set)
    text_result.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_result.yview)

    root.mainloop()

# Initial upload window
upload_window = tk.Tk()
upload_window.title("Upload SQLite Database")

upload_label = Label(upload_window, text="Upload SQLite Database File:")
upload_label.pack(pady=10)

upload_button = Button(upload_window, text="Upload", command=upload_database)
upload_button.pack(pady=5)

upload_window.mainloop()

# Close the database connection if it's open
if 'conn' in globals():
    conn.close()
