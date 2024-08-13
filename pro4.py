import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
def add_hobby():
    category = category_entry.get()
    name = name_entry.get()
    if category and name:
        try:
            conn = sqlite3.connect('hobbies.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO hobbies (category, name) VALUES (?, ?)', (category, name))
            conn.commit()
            conn.close()

            category_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Hobby added successfully!")
            display_hobbies()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please enter both category and name.")
def display_hobbies(filter_category=None):
    for i in tree.get_children():
        tree.delete(i)
    try:
        conn = sqlite3.connect('hobbies.db')
        cursor = conn.cursor()
        if filter_category:
            cursor.execute('SELECT category, name FROM hobbies WHERE category LIKE ?', (f'%{filter_category}%',))
        else:
            cursor.execute('SELECT category, name FROM hobbies')
        hobbies = cursor.fetchall()
        conn.close()
        for hobby in hobbies:
            tree.insert("", "end", values=hobby)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
def search_hobbies():
    filter_category = search_entry.get()
    display_hobbies(filter_category)
root = tk.Tk()
root.title("Hobby Collection Organizer")
tk.Label(root, text="Category").grid(row=0, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=0, column=1)
tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)
add_button = tk.Button(root, text="Add Hobby", command=add_hobby)
add_button.grid(row=2, column=0, columnspan=2)
tk.Label(root, text="Search Category").grid(row=3, column=0)
search_entry = tk.Entry(root)
search_entry.grid(row=3, column=1)
search_button = tk.Button(root, text="Search", command=search_hobbies)
search_button.grid(row=4, column=0, columnspan=2)
tree = ttk.Treeview(root, columns=("Category", "Name"), show='headings')
tree.heading("Category", text="Category")
tree.heading("Name", text="Name")
tree.grid(row=5, column=0, columnspan=2, sticky='nsew')
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(5, weight=1)
display_hobbies()
root.mainloop()

