# 📝 Personal Notes App

A simple yet powerful web application built with Flask that allows users to **register, log in, and manage personal notes** securely. This project is perfect for beginners learning Flask, SQLAlchemy, and web development fundamentals.

![Flask](https://img.shields.io/badge/Flask-3.1.1-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🔐 **User Authentication** – Register, log in, and log out securely.
- 📝 **Create Notes** – Write and save personal notes.
- 👁️ **View Notes** – See all your notes in a clean dashboard.
- ✏️ **Edit Notes** – Update note content anytime.
- 🗑️ **Delete Notes** – Remove notes you no longer need.
- 🔒 **Session Management** – Secure user sessions with Flask-WTF forms.
- 💾 **SQLite Database** – Lightweight, file-based database for easy setup.
- 📱 **Responsive Design** – Works on desktop and mobile devices.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask** | Web framework |
| **Flask-SQLAlchemy** | ORM for database operations |
| **Flask-WTF** | Form handling and CSRF protection |
| **SQLite** | Database |
| **Jinja2** | Template engine |
| **HTML5 / CSS3** | Frontend structure and styling |
| **JavaScript** | Client-side interactivity |
| **Markdown2** | Markdown support for notes |

---

## 📁 Project Structure

01_Personal Notes App/
├── main.py # Application entry point
├── formwtf.py # Form definitions (Login, Register, Note forms)
├── requirements.txt # Python dependencies
├── models/
│ └── database.py # Database models (User, Note)
├── routes/
│ ├── auth.py # Authentication routes (login, register, logout)
│ └── notes.py # Note management routes (create, edit, delete, view)
├── templates/
│ ├── base.html # Base template with navigation
│ ├── login.html # Login page
│ ├── register.html # Registration page
│ ├── dashboard.html # Notes dashboard
│ └── edit_note.html # Edit note page
├── static/
│ ├── css/
│ │ └── style.css # Custom styles
│ └── js/
│ └── script.js # Custom JavaScript
└── instance/
└── notes.db # SQLite database (auto-created)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Miansaibx7/Python_Flask_Projects_For_Beginners.git
   cd "Python_Flask_Projects_For_Beginners/01_Personal Notes App"


### Create a virtual environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

### Install dependencies

pip install -r requirements.txt


## 📁 Project Structure
