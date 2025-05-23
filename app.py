from flask import Flask, render_template, request
from multiagent import run_stock_query

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        user_query = request.form['query']
        response = run_stock_query(user_query)
        return render_template('index.html', response=response)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)