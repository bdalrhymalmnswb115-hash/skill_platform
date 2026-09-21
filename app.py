from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill_type TEXT NOT NULL,
            description TEXT NOT NULL,
            contact TEXT NOT NULL,
            location TEXT NOT NULL,
            image TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM skills ORDER BY id DESC')
    skills = cursor.fetchall()
    conn.close()
    return render_template('index.html', skills=skills)

@app.route('/add', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        name = request.form['name']
        skill_type = request.form['skill_type']
        description = request.form['description']
        contact = request.form['contact']
        location = request.form['location']
        
        image_filename = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO skills (name, skill_type, description, contact, location, image)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, skill_type, description, contact, location, image_filename))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
        
    return render_template('add_skill.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
