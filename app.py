from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

def calculate_budget(salary):
	budget_distribution = {
		"Investments":0.30,
		"EMI":0.30,
		"Saving":0.15,
		"Expenses":0.15,
		"Insurance":0.05,
		"Adhoc":0.05
	}
	
	budget= {category: salary * percentage for category, percentage in budget_distribution.items()}
	return budget


def calculate_investment_growth(initial_investment, annual_contribution, years, rate = 0.15):
    r = rate / 12
    n = years * 12
    future_value = initial_investment * (((1 + r) ** n -1) /r) * (1 + r)
    if annual_contribution > 0:
        future_value += annual_contribution * (((1 + rate) ** years -1) / rate)
    return future_value


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    salary = float(data['salary'])
    annual_contribution = float(data.get('annualContribution', 0))
    budget_allocation = calculate_budget(salary)
    
    initial_investment = budget_allocation["Investments"]    
    
    investment_growth = {year: calculate_investment_growth(initial_investment, annual_contribution, year) for year in [5, 10, 15, 20]}
    
    return jsonify({
        'budget':budget_allocation,
        'investment_growth':investment_growth
    })
    
if __name__ == '__main__':
    app.run(debug=True)