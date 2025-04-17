import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# DataFrame to store student data
student_df = pd.DataFrame(columns=["ID", "Name", "Email"])

# Functions for Admin operations
def add_student():
    global student_df
    sid, name, email = id_var.get(), name_var.get(), email_var.get()
    if not sid or not name or not email:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    if sid in student_df['ID'].values:
        messagebox.showerror("Duplicate ID", "Student ID already exists")
        return
    student_df = pd.concat([student_df, pd.DataFrame([[sid, name, email]], columns=["ID", "Name", "Email"])]).reset_index(drop=True)
    update_table()
    clear_fields()

def update_student():
    global student_df
    sid, name, email = id_var.get(), name_var.get(), email_var.get()
    if sid not in student_df['ID'].values:
        messagebox.showerror("Not Found", "Student ID not found")
        return
    student_df.loc[student_df['ID'] == sid, ['Name', 'Email']] = name, email
    update_table()
    clear_fields()

def delete_student():
    global student_df
    sid = id_var.get()
    if sid not in student_df['ID'].values:
        messagebox.showerror("Not Found", "Student ID not found")
        return
    student_df = student_df[student_df['ID'] != sid].reset_index(drop=True)
    update_table()
    clear_fields()

def clear_fields():
    id_var.set("")
    name_var.set("")
    email_var.set("")

def update_table():
    for i in admin_table.get_children():
        admin_table.delete(i)
    for _, row in student_df.iterrows():
        admin_table.insert("", "end", values=tuple(row))

def view_student_dashboard():
    for i in student_table.get_children():
        student_table.delete(i)
    for _, row in student_df.iterrows():
        student_table.insert("", "end", values=tuple(row))

# Create main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x600")

# Centering the main content
main_frame = ttk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)

# Variables
id_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()

# Tabs
tab_control = ttk.Notebook(main_frame)
admin_tab = ttk.Frame(tab_control)
student_tab = ttk.Frame(tab_control)

# Center frame inside each tab
admin_inner_frame = ttk.Frame(admin_tab)
admin_inner_frame.place(relx=0.5, rely=0.5, anchor='center')

student_inner_frame = ttk.Frame(student_tab)
student_inner_frame.place(relx=0.5, rely=0.5, anchor='center')

# Admin Tab
ttk.Label(admin_inner_frame, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(admin_inner_frame, textvariable=id_var).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(admin_inner_frame, text="Name").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(admin_inner_frame, textvariable=name_var).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(admin_inner_frame, text="Email").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(admin_inner_frame, textvariable=email_var).grid(row=2, column=1, padx=5, pady=5)

ttk.Button(admin_inner_frame, text="Add", command=add_student).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(admin_inner_frame, text="Update", command=update_student).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(admin_inner_frame, text="Delete", command=delete_student).grid(row=3, column=2, padx=5, pady=5)

admin_table = ttk.Treeview(admin_inner_frame, columns=("ID", "Name", "Email"), show='headings')
for col in ("ID", "Name", "Email"):
    admin_table.heading(col, text=col)
admin_table.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

# Student Tab
student_table = ttk.Treeview(student_inner_frame, columns=("ID", "Name", "Email"), show='headings')
for col in ("ID", "Name", "Email"):
    student_table.heading(col, text=col)
student_table.pack(pady=20, padx=20)
ttk.Button(student_inner_frame, text="Refresh", command=view_student_dashboard).pack(pady=10)

# Add tabs to window
tab_control.add(admin_tab, text="Admin Console")
tab_control.add(student_tab, text="Student Dashboard")
tab_control.pack(expand=1, fill="both")

root.mainloop()