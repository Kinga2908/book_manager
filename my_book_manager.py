import sqlite3
from tkinter import *
from tkinter import messagebox
import requests

# Baza danych
conn = sqlite3.connect("books.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS books (
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_date TEXT NOT NULL,
    price REAL NOT NULL,
    available BOOLEAN NOT NULL
)
''')
conn.commit()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    pub_date = date_entry.get()
    try:
        price = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Błąd", "Nieprawidłowa cena.")
        return
    available = available_var.get()

    c.execute("INSERT INTO books (title, author, publication_date, price, available) VALUES (?, ?, ?, ?, ?)",
              (title, author, pub_date, price, available))
    conn.commit()
    show_books()

def show_books():
    book_list.delete(0, END)
    c.execute("SELECT * FROM books")
    for row in c.fetchall():
        book_list.insert(END, row)

def convert_price():
    try:
        selected_index = book_list.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Wybierz książkę z listy.")
            return

        book = book_list.get(selected_index)
        price = float(book[3])

        currency = currency_entry.get().upper()
        if not currency:
            messagebox.showwarning("Błąd", "Wpisz kod waluty, np. USD.")
            return

        response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}/?format=json")
        response.raise_for_status()
        rate = response.json()['rates'][0]['mid']
        pln_price = round(price * rate, 2)
        messagebox.showinfo("Cena w PLN", f"Cena książki w PLN: {pln_price} zł")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się przeliczyć waluty.\n{e}")

root = Tk()
root.title("Book Manager")

Label(root, text="Tytuł").grid(row=0, column=0)
title_entry = Entry(root)
title_entry.grid(row=0, column=1)

Label(root, text="Autor").grid(row=1, column=0)
author_entry = Entry(root)
author_entry.grid(row=1, column=1)

Label(root, text="Data publikacji (YYYY-MM-DD)").grid(row=2, column=0)
date_entry = Entry(root)
date_entry.grid(row=2, column=1)

Label(root, text="Cena (np. 39.99)").grid(row=3, column=0)
price_entry = Entry(root)
price_entry.grid(row=3, column=1)

available_var = BooleanVar()
Checkbutton(root, text="Dostępna", variable=available_var).grid(row=4, column=1)

Button(root, text="Dodaj książkę", command=add_book).grid(row=5, column=0, columnspan=2, pady=5)

book_list = Listbox(root, width=80)
book_list.grid(row=6, column=0, columnspan=2)
show_books()

Label(root, text="Waluta (np. USD)").grid(row=7, column=0)
currency_entry = Entry(root)
currency_entry.grid(row=7, column=1)

Button(root, text="Przelicz na PLN", command=convert_price).grid(row=8, column=0, columnspan=2, pady=5)

root.mainloop()
conn.close()
