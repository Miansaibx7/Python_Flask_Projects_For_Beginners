# 🐍 Python Flask Projects for Beginners

A curated collection of **Flask web applications** designed for beginners to learn and practice web development with Python. Each project is self-contained, well-structured, and covers essential Flask concepts.

## 📁 Projects Included

### 1. 📝 Personal Notes App
A fully functional note-taking application with user authentication.

**Features:**
- User registration and login system
- Create, edit, and delete notes
- Markdown support for note formatting
- SQLite database for data persistence
- Responsive UI with custom CSS

**Tech Stack:** Flask, Flask-SQLAlchemy, Flask-WTF, Markdown2, SQLite, HTML5, CSS3, JavaScript

---

### 2. ☁️ Weather App
A real-time weather application that fetches live weather data.

**Features:**
- Search weather by city name
- Display temperature, humidity, wind speed, and weather conditions
- Dynamic weather icons based on conditions
- Clean, responsive UI

**Tech Stack:** Flask, Requests (API integration), HTML5, CSS3, JavaScript

---

### 3. 📰 Simple Blog with Admin Panel
A complete blog system with an administrative dashboard.

**Features:**
- User authentication (login/register)
- Create, edit, delete blog posts
- Admin panel for content management
- Comment system for blog posts
- Category-based post organization

**Tech Stack:** Flask, Flask-SQLAlchemy, Flask-WTF, SQLite, HTML5, CSS3, JavaScript

---

### 4. 📊 Student Marks Analyzer
An interactive analytics tool to process, analyze, and visualize student performance data uploaded via CSV files.

**Features:**
- CSV file upload and parsing
- Automated calculation of student grade averages and performance metrics
- Dynamic data visualization (automatic chart generation for average scores)
- Interactive results dashboard

**Tech Stack:** Flask, CSV/Pandas, HTML5, CSS3, JavaScript, Docker

---

### 5. 🛒 E-Commerce Platform with Payment Integration
A full-featured online store with product management, shopping cart functionality, and live payment processing.

**Features:**
- User authentication with email verification and password reset functionality
- Product catalog browsing and detailed item views
- Interactive shopping cart and secure order history tracking
- Live, secure online checkout using Stripe payment gateway integration
- Admin dashboard for managing inventory, products, and customer orders

**Tech Stack:** Flask, Flask-SQLAlchemy, Flask-WTF, Stripe API, SQLite, HTML5, CSS3, JavaScript, Docker

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Recommended)
- Git

### Run with Docker (Recommended)
This method ensures you don't have to manually install any Python dependencies on your machine. Each project contains its own isolated container.

1. Navigate into the specific project folder you want to run:
   ```bash
   cd "E-Commerce_Platform_with_Payment_Integration"
Build and start the container:

# Bash
docker-compose up -d --build
Open your web browser and go to: http://localhost:5000

(To stop the server, run docker-compose down in the terminal).

### Run Locally (Without Docker)
If you prefer to run the applications directly on your machine using a virtual environment:

Navigate to the project directory:

# Bash
cd "01_Personal Notes App"
Create and activate a virtual environment:

# Bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
Install the required dependencies:

# Bash
pip install -r requirements.txt
Start the Flask development server:

# Bash
flask run --debug
View the app at: http://127.0.0.1:5000

Note: For projects requiring APIs (like Stripe in the E-Commerce app or Weather APIs), you will need to create a .env file in that project's folder to store your secret keys before running.

### 🤝 Contributing
Feel free to fork this repository, explore the code, and submit pull requests if you have suggestions for improvements or want to add a new beginner project!

### 📝 License
This project is open-source and available under the MIT License.
