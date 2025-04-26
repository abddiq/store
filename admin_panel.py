import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
from datetime import datetime

CODE_FILE = "access_codes.txt"

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("480x420")
        self.root.configure(bg="#232931")
        self.build_ui()

    def build_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        tk.Label(self.root, text="Admin Panel", font=("Arial", 20, "bold"), bg="#232931", fg="#ffe066").pack(pady=12, fill="x")
        form = tk.Frame(self.root, bg="#232931")
        form.pack(pady=8)
        tk.Label(form, text="Username:", font=("Arial", 12), bg="#232931", fg="#f2e9e4").grid(row=0, column=0, padx=4, pady=5)
        self.user_var = tk.StringVar()
        tk.Entry(form, textvariable=self.user_var, font=("Arial", 12), width=14).grid(row=0, column=1, padx=4)
        tk.Label(form, text="Amount ($):", font=("Arial", 12), bg="#232931", fg="#f2e9e4").grid(row=0, column=2, padx=4, pady=5)
        self.amount_var = tk.StringVar()
        tk.Entry(form, textvariable=self.amount_var, font=("Arial", 12), width=10).grid(row=0, column=3, padx=4)
        tk.Label(form, text="Access Code:", font=("Arial", 12), bg="#232931", fg="#f2e9e4").grid(row=1, column=0, padx=4, pady=5)
        self.code_var = tk.StringVar(value=str(random.randint(100000, 999999)))
        tk.Entry(form, textvariable=self.code_var, font=("Arial", 12), width=14).grid(row=1, column=1, padx=4)
        tk.Button(form, text="Generate", font=("Arial", 10), bg="#ffe082", command=lambda: self.code_var.set(str(random.randint(100000, 999999)))).grid(row=1, column=2, padx=4)
        tk.Button(form, text="Issue Code", font=("Arial", 12, "bold"), bg="#00b894", fg="#fff", command=self.add_code).grid(row=1, column=3, padx=4)
        sep = tk.Frame(self.root, height=2, bg="#393e46")
        sep.pack(fill="x", pady=7)
        self.tree = ttk.Treeview(self.root, columns=("code", "user", "amount", "date"), show="headings", height=7)
        self.tree.heading("code", text="Access Code")
        self.tree.heading("user", text="Username")
        self.tree.heading("amount", text="Amount ($)")
        self.tree.heading("date", text="Date")
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("user", width=120, anchor="center")
        self.tree.column("amount", width=80, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.pack(pady=8)
        btns = tk.Frame(self.root, bg="#232931")
        btns.pack(pady=6)
        tk.Button(btns, text="Delete Selected", font=("Arial", 11), bg="#d63031", fg="#fff", command=self.delete_code, width=12).pack(side="left", padx=8)
        tk.Button(btns, text="Refresh", font=("Arial", 11), bg="#fdcb6e", fg="#222", command=self.load_codes, width=9).pack(side="left", padx=8)
        self.notification_lbl = tk.Label(self.root, text="", font=("Arial", 11, "bold"), fg="#d63031", bg="#232931")
        self.notification_lbl.pack(pady=4)
        self.load_codes()

    def add_code(self):
        user = self.user_var.get().strip()
        amount = self.amount_var.get().strip()
        code = self.code_var.get().strip()
        if not user or not amount.isdigit() or not code:
            messagebox.showerror("Error", "Please enter all data correctly!")
            return
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        line = f"{code},{user},{amount},{date}\n"
        with open(CODE_FILE, "a", encoding="utf-8") as f:
            f.write(line)
        self.user_var.set("")
        self.amount_var.set("")
        self.code_var.set(str(random.randint(100000, 999999)))
        self.load_codes()
        messagebox.showinfo("Done", "Code issued successfully!")

    def load_codes(self):
        self.tree.delete(*self.tree.get_children())
        if os.path.exists(CODE_FILE):
            with open(CODE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        self.tree.insert("", "end", values=(parts[0], parts[1], parts[2], parts[3]))

    def delete_code(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to delete!")
            return
        code = self.tree.item(selected[0])['values'][0]
        lines = []
        with open(CODE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if not line.startswith(str(code)+","):
                    lines.append(line)
        with open(CODE_FILE, "w", encoding="utf-8") as f:
            for l in lines:
                f.write(l)
        self.load_codes()
        messagebox.showinfo("Done", "Code deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    AdminPanel(root)
    root.mainloop()