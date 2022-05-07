from calendar import month, monthrange
import datetime
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import categories
import transactions
import patterns
import categorize_transactions
import import_transactions
import budget
import budget_categories

app = Flask(__name__)

@app.route("/")
def index_route():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    return render_template('index.html', year=year, month=month)

#
# CATEGORIES
#

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

#
# CATEGORY PATTERNS
#

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

#
# TRANSACTIONS
#

@app.route("/transactions")
def transactions_route():
  transactions_data = transactions.get_transactions()
  categories_data = categories.get_categories()
  return render_template('transactions.html', transactions=transactions_data, categories=categories_data)

@app.route("/transactions/none")
def transactions_none_route():
  transactions_data = transactions.get_transactions_none()
  categories_data = categories.get_categories()
  return render_template('transactions.html', transactions=transactions_data, categories=categories_data)

@app.route("/transactions/categorize")
def transactions_categorize_route():
    categorize_transactions.start_categorization()
    return redirect("/transactions")

@app.route("/transactions/categorize/<transaction_id>", methods=['POST'])
def transactions_categorize_transaction_id_route(transaction_id):
    category = request.form['category']
    transactions.assign_category(transaction_id, category)
    return redirect("/transactions")

@app.route('/transactions/import', methods=['POST'])
def import_transaction_route():
    f = request.files['import_file']
    f.save('imports/' + secure_filename(f.filename))
    import_transactions.start_import()
    categorize_transactions.start_categorization()
    return redirect("/transactions")

#
# BUDGET
#

@app.route("/budget/<year>/<month>")
def budget_year_month_route(year, month):
    current_month_date = datetime.datetime(int(year), int(month), 1)
    previous_month_date = current_month_date - datetime.timedelta(days=1)
    next_month_date= current_month_date + datetime.timedelta(days=monthrange(int(year), int(month))[1])

    month_budget = budget.get_expense_for_month(month, year)

    return render_template('month_year_budget.html', budget=month_budget, current_date=current_month_date.strftime("%B %Y"), previous_url=previous_month_date.strftime("%Y/%m"), next_url=next_month_date.strftime("%Y/%m"))

#
# BUDGET CATEGORIES
#

@app.route("/budget-categories")
def budget_categories_route():
  categories_data = categories.get_categories()
  return render_template('budget_categories.html', categories=categories_data)

@app.route("/budget-categories/create", methods=['POST'])
def create_budget_categorie_route():
	category = request.form['category']
	budget = request.form['budget']
	month = request.form['month']
	year = request.form['year']
	budget_categories.create_budget_categories(category, budget, month, year)
	return redirect("/budget-categories")

@app.route("/budget-categories/<budget_categories_id>/delete")
def delete_budget_categorie_route(budget_categories_id):
    budget_categories.delete_budget_categories(budget_categories_id)
    return redirect("/budget-categories")
