from flask import Flask, render_template, request
from categories import get_categories, create_category
from transactions import get_transactions

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/categories", methods=['POST', 'GET'])
def categories():
  if request.method == 'POST':
      label = request.form['label']
      create_category(label)

  categories_data = get_categories()
  return render_template('categories.html', categories=categories_data)

@app.route("/transactions", methods=['POST', 'GET'])
def transactions():
#   if request.method == 'POST':
#       label = request.form['label']
#       create_category(label)

  transactions_data = get_transactions()
  return render_template('transactions.html', transactions=transactions_data)
