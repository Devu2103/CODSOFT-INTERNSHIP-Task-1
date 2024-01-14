import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a database connection
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# Create a table to store tasks
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              task TEXT NOT NULL,
              status TEXT NOT NULL)''')
conn.commit()

# Create a splash screen
splash = tk.Tk()
splash.title('To-Do List')
splash.geometry('300x200')
splash_label = tk.Label(splash, text='Welcome to To-Do List!', font=('Arial', 18))
splash_label.pack(pady=50)
splash.after(2000, splash.destroy)

# Create the main screen
root = tk.Tk()
root.title('To-Do List')
root.geometry('400x400')

# Add task function
def add_task():
    task = task_entry.get()
    if task == '':
        messagebox.showerror('Error', 'Please enter a task')
    else:
        c.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task          ,  'Add_successful'))
        conn.commit()
        task_entry.delete(0, tk.END)
        show_tasks()

# Delete task function
def delete_task():
    for task in task_list.curselection():
        task_id = task_list.get(task)[0]
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    show_tasks()

# Update task function
def update_task():
    for task in task_list.curselection():
        task_id = task_list.get(task)[0]
        new_task = task_entry.get()
        c.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
        conn.commit()
    task_entry.delete(0, tk.END)
    show_tasks()

# Show tasks function
def show_tasks():
    task_list.delete(0, tk.END)
    for row in c.execute('SELECT * FROM tasks'):
        task_list.insert(tk.END, row)

# Create widgets
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=10)

add_button = tk.Button(root, text='Add Task', command=add_task)
add_button.pack(pady=10)

delete_button = tk.Button(root, text='Delete Task', command=delete_task)
delete_button.pack(pady=10)

update_button = tk.Button(root, text='Update Task', command=update_task)
update_button.pack(pady=10)

task_list = tk.Listbox(root, width=50)
task_list.pack(pady=10)

show_tasks()

# Run the main loop
root.mainloop()
