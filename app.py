# Imports
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

# Defining application and adding supersecret key
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Registration form page
@app.route('/register')
def register():
    return render_template('register.html')

# Handle form submission (students will add JSON save code here)
@app.route('/submit', methods=['POST'])
def submit_form():
    # get all inputs from the form
    name = request.form['Name']
    country = request.form['country']
    date = request.form['date']
    urgent_needs = request.form['urgent_needs']
    medical_information = request.form['medical_information']
    additional_information = request.form['additional_field']

    # Store values in session so we can repopulate them if page is reloaded.
    session['name'] = name
    session['country'] = country
    session['date'] = date
    session['urgent_needs'] = urgent_needs
    session['medical_information'] = medical_information
    session['additional_information'] = additional_information


    # Check if file exists
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Add the new registration
    data.append({'name': name, 'country': country, 'date': date, 'urgent': urgent_needs, 'medical_information': medical_information, 'additional': additional_information})

    # Save all registrations back to the file
    with open('registrations.json', 'w') as file:
        json.dump(data, file, indent=2)

    # Clear session values after success
    session.pop('name', None)
    session.pop('country', None)
    session.pop('date', None)
    session.pop('urgent_needs', None)
    session.pop('medical_information', None)
    session.pop('additional_information', None)

    flash('Registration submitted successfully!')
    return redirect(url_for('index'))

# Display stored registrations (students will add JSON reading code here)
@app.route('/view')
def view_registrations():
    if os.path.exists('registrations.json'):
        with open('registrations.json', 'r') as file:
            data = json.load(file)
    else:
        data = []
    return render_template('view.html', registrations=data)

@app.route('/delete')
def delete_registration():
    if os.path.exists('registrations.json'):
        os.remove('registrations.json')
        data = []

    flash('Registration deleted successfully!')
    return render_template('view.html', registrations=data)

# ACTUALLY RUNS THE APP
if __name__ == '__main__':
    app.run(debug=True)

