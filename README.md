# Online Household Account Book

A web-based personal finance management tool designed to help users track income, monitor expenses, and manage household budgets effectively. This project focuses on providing a clean, responsive interface for daily financial logging.

## 🚀 Features

* **Expense Tracking:** Easily log daily expenditures with categories and descriptions.
* **Income Management:** Keep track of various revenue sources.
* **Mobile Responsive:** Fully optimized for mobile browsers for logging on the go.
* **Visual Analytics:** Clear breakdowns of spending patterns and monthly trends.
* **Data Persistence:** Secure storage of financial records using a relational database.

## 🛠 Tech Stack

* **Backend:** Python / Flask
* **Frontend:** HTML5, CSS3 (Bootstrap/Responsive Design), JavaScript
* **Database:** SQLite / PostgreSQL
* **Local Development:** Compatible with local LLM environments (Ollama/Gemma) for automated categorization.

## 📋 Getting Started

### Prerequisites
* Python 3.8+
* pip (Python package manager)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/kang851216/Online-Household-Account-Book.git](https://github.com/kang851216/Online-Household-Account-Book.git)
    cd Online-Household-Account-Book
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\\Scripts\\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    ```bash
    flask db init
    flask db upgrade
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    Access the app at `http://127.0.0.1:5000`.

## 🗺 Roadmap

- [ ] **AI Categorization:** Integration with local LLMs to automatically categorize expenses based on descriptions.
- [ ] **Multi-Currency Support:** Ability to track expenses in HKD, USD, EUR, etc.
- [ ] **Export Options:** Export monthly data to CSV or Excel for further analysis.
- [ ] **Budget Alerts:** Notifications when spending in a specific category exceeds a set limit.
