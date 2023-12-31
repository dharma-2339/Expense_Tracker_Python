from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask import jsonify
app = Flask(__name__)

# SQLite database setup
DATABASE = "expenses.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, amount REAL)")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    create_table()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["POST"])
def add():
    description = request.form.get("description")
    amount = request.form.get("amount")

    if description and amount:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (description, amount))
        conn.commit()
        conn.close()

    return redirect(url_for("index"))

@app.route("/expenses_json")
def expenses_json():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    data = [{"description": expense[1], "amount": expense[2]} for expense in expenses]
    return jsonify(data)

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


