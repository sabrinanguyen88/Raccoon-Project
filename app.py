
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CSV_FILE = 'sightings.csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Read sightings from CSV
def load_sightings():
    sightings = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sightings.append(row)
    return sightings

@app.route('/')
def index():
    sightings = load_sightings()
    return render_template('index.html', sightings=sightings)

@app.route('/submit', methods=['POST'])
def submit():
    lat = request.form['lat']
    lng = request.form['lng']
    photo = request.files['photo']

    if photo and lat and lng:
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['lat', 'lng', 'filename'])
            if os.stat(CSV_FILE).st_size == 0:
                writer.writeheader()
            writer.writerow({'lat': lat, 'lng': lng, 'filename': filename})

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
