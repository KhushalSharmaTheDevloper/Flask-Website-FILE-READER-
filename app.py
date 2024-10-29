from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = '887'  # Change this to a random secret key

rack_dict = {}

def extract_rack_number(contents):
    rack_numbers = {}
    current_rack = None

    for line in contents:
        line = line.strip()
        if line.startswith("Rec No."):
            current_rack = line.split('-')[-1].strip()
        elif line.startswith("S.No.") or line.startswith("Name of The Chemical Compound"):
            continue
        elif current_rack and line:
            if current_rack not in rack_numbers:
                rack_numbers[current_rack] = []
            rack_numbers[current_rack].append(line)

    return rack_numbers

@app.route('/', methods=['GET', 'POST'])
def index():
    global rack_dict
    if request.method == 'POST':
        file = request.files['file']
        if file:
            contents = file.read().decode('utf-8').splitlines()
            rack_dict = extract_rack_number(contents)
            flash('File loaded successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('index.html', rack_dict=rack_dict)

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '').strip()
    if not search_term:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('index'))

    matching_lines = []
    for rack, compounds in rack_dict.items():
        for compound in compounds:
            if search_term.lower() in compound.lower():
                matching_lines.append((compound, rack))

    return render_template('results.html', matching_lines=matching_lines, search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True)
