from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('lab_utilization.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Laboratories (id INTEGER PRIMARY KEY, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Activities (id INTEGER PRIMARY KEY, lab_id INTEGER, department_id INTEGER, activity_type TEXT, completion_rate REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Departments (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Endpoint to add lab activity
@app.route('/add_activity', methods=['POST'])
def add_activity():
    data = request.json
    lab_id = data['lab_id']
    department_id = data['department_id']
    activity_type = data['activity_type']
    completion_rate = data['completion_rate']
    
    conn = sqlite3.connect('lab_utilization.db')
    c = conn.cursor()
    c.execute('INSERT INTO Activities (lab_id, department_id, activity_type, completion_rate) VALUES (?, ?, ?, ?)',
              (lab_id, department_id, activity_type, completion_rate))
    conn.commit()
    conn.close()
    return jsonify({"status": "Activity added successfully!"})

# Endpoint to get utilization metrics
@app.route('/utilization_metrics', methods=['GET'])
def utilization_metrics():
    conn = sqlite3.connect('lab_utilization.db')
    c = conn.cursor()
    c.execute('''SELECT lab_id, AVG(completion_rate) as avg_completion FROM Activities GROUP BY lab_id''')
    metrics = c.fetchall()
    conn.close()
    return jsonify(metrics)

# Endpoint to get all laboratories
@app.route('/laboratories', methods=['GET'])
def get_laboratories():
    conn = sqlite3.connect('lab_utilization.db')
    c = conn.cursor()
    c.execute('SELECT * FROM Laboratories')
    labs = c.fetchall()
    conn.close()
    return jsonify(labs)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)