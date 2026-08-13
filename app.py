import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
def home():
    students = list(mongo.db.students.find()) if mongo.db is not None else []
    return render_template('index.html', students=students)

# Support both endpoint names just in case templates or tests reference 'index'
@app.route('/index')
def index():
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add_student():
    if mongo.db is not None:
        name = request.form.get('name')
        email = request.form.get('email')
        course = request.form.get('course')
        mongo.db.students.insert_one({'name': name, 'email': email, 'course': course})
    return redirect(url_for('home'))

@app.route('/update/<student_id>', methods=['POST'])
def update_student(student_id):
    if mongo.db is not None:
        from bson.objectid import ObjectId
        name = request.form.get('name')
        email = request.form.get('email')
        course = request.form.get('course')
        mongo.db.students.update_one(
            {'_id': ObjectId(student_id)},
            {'$set': {'name': name, 'email': email, 'course': course}}
        )
    return redirect(url_for('home'))

@app.route('/delete/<student_id>')
def delete_student(student_id):
    if mongo.db is not None:
        from bson.objectid import ObjectId
        mongo.db.students.delete_one({'_id': ObjectId(student_id)})
    return redirect(url_for('home'))

@app.route('/health', methods=['GET'])
def health_check():
    try:
        mongo.db.command('ping')
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

