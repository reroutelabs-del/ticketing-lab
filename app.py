from flask import Flask, request, jsonify, render_template, redirect, url_for
import csv
import uuid
from datetime import datetime
import os

app = Flask(__name__)

TICKET_FILE = 'tickets.csv'

# Route: Home page with form
@app.route('/')
def home():
    return render_template('index.html')

# Route: Handle form POST
@app.route('/submit', methods=['POST'])
def submit_ticket():
    user = request.form['user']
    issue = request.form['issue']
    priority = request.form['priority']

    ticket = {
        "ID": str(uuid.uuid4()),
        "User": user,
        "Issue": issue,
        "Priority": priority,
        "Status": "Open",
        "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    file_exists = os.path.isfile(TICKET_FILE)

    with open(TICKET_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=ticket.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(ticket)

    return redirect(url_for('view_tickets'))

# Route: View all submitted tickets
@app.route('/tickets')
def view_tickets():
    tickets = []
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, 'r') as f:
            reader = csv.DictReader(f)
            tickets = list(reader)
    return render_template('tickets.html', tickets=tickets)

if __name__ == '__main__':
    print("🚀 Ticketing Web App Running")
    app.run(host='0.0.0.0', port=5000, debug=True)
