from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "advanced_complaint_system_secret"

# Configure Upload Folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database initialization
def init_db():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            user_id TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Create Complaints Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            problem_type TEXT NOT NULL,
            complaint_title TEXT NOT NULL,
            complaint_description TEXT NOT NULL,
            attachment TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert Default Admin if not exists
    cursor.execute("SELECT * FROM admin WHERE admin_id = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin (admin_id, password) VALUES (?, ?)", ('admin', 'admin123'))
    
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        user_id = request.form['user_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))
            
        try:
            conn = sqlite3.connect('complaints.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (full_name, user_id, email, password) VALUES (?, ?, ?, ?)",
                           (full_name, user_id, email, password))
            conn.commit()
            conn.close()
            flash("Registration Successful! Please Login.", "success")
            return redirect(url_for('user_login'))
        except sqlite3.IntegrityError:
            flash("User ID already exists!", "danger")
            
    return render_template('register.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        
        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = user_id
            session['name'] = user[1]
            session['email'] = user[3]
            return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid User ID or Password!", "danger")
            
    return render_template('user_login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']
        
        conn = sqlite3.connect('complaints.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE admin_id = ? AND password = ?", (admin_id, password))
        admin = cursor.fetchone()
        conn.close()
        
        if admin:
            session['admin'] = admin_id
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin ID or Password!", "danger")
            
    return render_template('admin_login.html')

@app.route('/user_dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('user_login'))
    return render_template('user_dashboard.html', name=session['name'], user_id=session['user'], email=session['email'])

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'user' not in session:
        return redirect(url_for('user_login'))
        
    problem_type = request.form['problem_type']
    title = request.form['complaint_title']
    description = request.form['complaint_description']
    
    file = request.files['attachment']
    filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid duplicates
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO complaints 
                      (user_name, user_id, email, problem_type, complaint_title, complaint_description, attachment) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (session['name'], session['user'], session['email'], problem_type, title, description, filename))
    conn.commit()
    conn.close()
    
    flash("Complaint Submitted Successfully!", "success")
    return redirect(url_for('user_dashboard'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
        
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    complaints = cursor.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', complaints=complaints)

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
        
    new_status = request.form['status']
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status = ? WHERE id = ?", (new_status, id))
    conn.commit()
    conn.close()
    
    flash(f"Complaint ID {id} updated to {new_status}", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/delete/<int:id>')
def delete_complaint(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
        
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    # Optional: Delete attachment file from folder
    cursor.execute("SELECT attachment FROM complaints WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row and row[0]:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], row[0])
        if os.path.exists(file_path):
            os.remove(file_path)
            
    cursor.execute("DELETE FROM complaints WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    flash(f"Complaint ID {id} deleted successfully", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
