from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import categories
import transactions
import patterns
import categorize_transactions
import import_transactions

app = Flask(__name__)

@app.route("/")
def index_route():
  return render_template('index.html')

@app.route("/categories")
def categories_route():
  categories_data = categories.get_categories()
  return render_template('categories.html', categories=categories_data)

@app.route("/categories/create", methods=['POST'])
def create_category_route():
	label = request.form['label']
	categories.create_category(label)
	return redirect("/categories")

@app.route("/categories/<category_id>/delete")
def delete_category_route(category_id):
    categories.delete_category(category_id)
    categorize_transactions.start_categorization()
    return redirect("/categories")

@app.route("/transactions")
def transactions_route():
  transactions_data = transactions.get_transactions()
  return render_template('transactions.html', transactions=transactions_data)

@app.route('/transactions/import', methods=['POST'])
def import_transaction_route():
    f = request.files['import_file']
    f.save('imports/' + secure_filename(f.filename))
    import_transactions.start_import()
    categorize_transactions.start_categorization()
    return redirect("/transactions")

@app.route("/patterns")
def patterns_route():
  patterns_data = patterns.get_categories_patterns()
  categories_data = categories.get_categories()
  return render_template('category_patterns.html', patterns=patterns_data, categories=categories_data)

@app.route("/patterns/create", methods=['POST'])
def create_pattern_route():
	pattern = request.form['pattern']
	category = request.form['category']
	patterns.create_pattern(pattern, category)
	categorize_transactions.start_categorization()
	return redirect("/patterns")

@app.route("/patterns/<pattern_id>/delete")
def delete_pattern_route(pattern_id):
    patterns.delete_pattern(pattern_id)
    categorize_transactions.start_categorization()
    return redirect("/patterns")
