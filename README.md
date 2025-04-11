# My Book Manager

A simple desktop application for managing a collection of books, built with **Python**, **Tkinter**, and **SQLite**.
The app allows users to add, view, and convert book prices using real-time exchange rates fetched from the NBP API.

## Features

- Add a new book with title, author, publication date, price, and availability.
- Display a list of all books stored in the database.
- Convert the book's price to PLN using an external currency exchange API (NBP).
- Data is stored persistently in a SQLite database (`books.db`).
- Intuitive graphical interface using `tkinter`.

## Technologies Used

- Python 3.x
- Tkinter
- SQLite3
- requests (for fetching exchange rates from an external API)

## Installation

1. Clone this repository:

```bash
https://github.com/Kinga2908/book_manager
cd my_book_manager
