import json
import os
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management and flashing messages

# Path to the index file (where items will be stored)
INDEX_FILE = 'index.json'


# Function to load data from the JSON file
def load_data():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as file:
            return json.load(file)
    return []


# Function to save data to the JSON file
def save_data(data):
    with open(INDEX_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# Create Item (POST method)
@app.route('/create', methods=['POST'])
def create_item():
    name = request.form['name']
    description = request.form['description']

    if not name or not description:
        flash('Both name and description are required!', 'danger')
        return redirect(url_for('index'))

    data = load_data()
    item = {
        "id": len(data) + 1,
        "name": name,
        "description": description
    }
    data.append(item)
    save_data(data)

    flash(f"Item '{name}' created successfully!", 'success')
    return redirect(url_for('index'))


# Read all items (GET method)
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', items=data)


# Update Item (POST method)
@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    new_name = request.form['name']
    new_description = request.form['description']

    data = load_data()
    for item in data:
        if item['id'] == item_id:
            item['name'] = new_name
            item['description'] = new_description
            save_data(data)
            flash(f"Item '{item_id}' updated successfully!", 'success')
            return redirect(url_for('index'))

    flash(f"Item with ID {item_id} not found.", 'danger')
    return redirect(url_for('index'))


# Delete Item (GET method)
@app.route('/delete/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    data = load_data()
    for i, item in enumerate(data):
        if item['id'] == item_id:
            del data[i]
            save_data(data)
            flash(f"Item with ID {item_id} deleted successfully!", 'success')
            return redirect(url_for('index'))

    flash(f"Item with ID {item_id} not found.", 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
