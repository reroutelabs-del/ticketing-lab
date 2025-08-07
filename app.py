from flask import Flask, request, render_template, redirect, url_for
import json
import uuid
import datetime

app = Flask(__name__)
TICKET_FILE = 'tickets.json'

# ---------- Utilities ----------
def load_tickets():
    try:
        with open(TICKET_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tickets(tickets):
    with open(TICKET_FILE, 'w') as f:
        json.dump(tickets, f, indent=4)

# ---------- Routes ----------

@app.route('/')
def home():
    return redirect(url_for('submit_ticket'))

@app.route('/submit', methods=['GET', 'POST'])
def submit_ticket():
    if request.method == 'POST':
        tickets = load_tickets()
        new_ticket = {
            "ticket_id": str(uuid.uuid4())[:8],
            "user": request.form['user'],
            "issue": request.form['issue'],
            "priority": request.form['priority'],
            "status": "Open",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": "",
            "root_cause": "",
            "resolution": ""
        }
        tickets.append(new_ticket)
        save_tickets(tickets)
        return redirect(url_for('view_tickets'))
    return render_template('submit.html')

@app.route('/tickets')
def view_tickets():
    tickets = load_tickets()
    return render_template('tickets.html', tickets=tickets)

@app.route('/edit/<ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['ticket_id'] == ticket_id), None)

    if not ticket:
        return "Ticket not found", 404

    if request.method == 'POST':
        ticket['user'] = request.form['user']
        ticket['issue'] = request.form['issue']
        ticket['priority'] = request.form['priority']
        ticket['status'] = request.form['status']
        ticket['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_tickets(tickets)
        return redirect(url_for('view_tickets'))

    return render_template('edit.html', ticket=ticket)

@app.route('/resolve/<ticket_id>', methods=['GET', 'POST'])
def resolve_ticket(ticket_id):
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['ticket_id'] == ticket_id), None)

    if not ticket:
        return "Ticket not found", 404

    if request.method == 'POST':
        ticket['root_cause'] = request.form['root_cause']
        ticket['resolution'] = request.form['resolution']
        ticket['status'] = "Closed"
        ticket['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_tickets(tickets)
        return redirect(url_for('view_tickets'))

    return render_template('resolve.html', ticket=ticket)

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
