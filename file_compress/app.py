from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import os, zipfile, io, datetime
from pymongo import MongoClient
from bson.binary import Binary
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------- MongoDB Connection -----------------
client = MongoClient("mongodb://localhost:27017")
db = client["file_compressor_db"]
users_col = db["users"]
files_col = db["files"]

# ----------------- Home -----------------
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# ----------------- Signup -----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('signup'))

        if users_col.find_one({"username": username}):
            flash("Username already exists!", "danger")
            return redirect(url_for('signup'))

        users_col.insert_one({"username": username, "password": password})
        flash("Signup successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ----------------- Login -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_col.find_one({"username": username, "password": password})
        if user:
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')

# ----------------- Logout -----------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# ----------------- File Upload -----------------
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('login'))

    files = request.files.getlist('files[]')
    if not files or all(f.filename == '' for f in files):
        flash('No files selected', 'danger')
        return redirect(url_for('home'))

    # Create user-specific folder
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    os.makedirs(user_folder, exist_ok=True)

    # Unique zip filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{session['username']}_{timestamp}.zip"
    zip_path = os.path.join(user_folder, zip_filename)

    # Temporary folder for files
    temp_folder = os.path.join(user_folder, f"temp_{timestamp}")
    os.makedirs(temp_folder, exist_ok=True)

    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(temp_folder, filename))

    # Create ZIP
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, filenames in os.walk(temp_folder):
            for name in filenames:
                full_path = os.path.join(root, name)
                arcname = os.path.relpath(full_path, temp_folder)
                zipf.write(full_path, arcname)

    # Store in MongoDB
    with open(zip_path, 'rb') as f:
        file_data = Binary(f.read())

    files_col.insert_one({
        "username": session['username'],
        "filename": zip_filename,
        "upload_time": datetime.datetime.now(),
        "filedata": file_data
    })

    # Cleanup temp folder
    for root, _, files_in_dir in os.walk(temp_folder, topdown=False):
        for name in files_in_dir:
            os.remove(os.path.join(root, name))
        os.rmdir(root)

    flash("Files uploaded and compressed successfully!", "success")
    return redirect(url_for('my_files'))

# ----------------- My Files -----------------
@app.route('/myfiles')
def my_files():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_files = list(files_col.find({"username": session['username']}))
    return render_template('myfiles.html', files=user_files, username=session['username'])

# ----------------- Download File -----------------
@app.route('/download/<file_id>')
def download_file(file_id):
    file_doc = files_col.find_one({"_id": ObjectId(file_id)})
    if not file_doc:
        flash("File not found!", "danger")
        return redirect(url_for('my_files'))

    return send_file(
        io.BytesIO(file_doc['filedata']),
        as_attachment=True,
        download_name=file_doc['filename'],
        mimetype='application/zip'
    )

# ----------------- Delete File -----------------
@app.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    file_doc = files_col.find_one({"_id": ObjectId(file_id), "username": session['username']})
    if not file_doc:
        flash("File not found or unauthorized action!", "danger")
        return redirect(url_for('my_files'))

    files_col.delete_one({"_id": ObjectId(file_id)})
    flash("File deleted successfully!", "success")
    return redirect(url_for('my_files'))

# ----------------- Run App -----------------
if __name__ == '__main__':
    app.run(debug=True, port=4630)
