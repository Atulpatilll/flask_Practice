import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@app.route('/')
def index():
    students = []
    try:
        if mongo.db is not None:
            students = list(mongo.db.students.find())
    except Exception:
        pass
    return render_template('index.html', students=students)

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_student():
    try:
        if mongo.db is not None:
            name = request.form.get('name')
            email = request.form.get('email')
            course = request.form.get('course')
            mongo.db.students.insert_one({'name': name, 'email': email, 'course': course})
    except Exception:
        pass
    return redirect(url_for('index'))

@app.route('/update/<student_id>', methods=['POST'])
def update_student(student_id):
    try:
        if mongo.db is not None:
            from bson.objectid import ObjectId
            name = request.form.get('name')
            email = request.form.get('email')
            course = request.form.get('course')
            mongo.db.students.update_one(
                {'_id': ObjectId(student_id)},
                {'$set': {'name': name, 'email': email, 'course': course}}
            )
    except Exception:
        pass
    return redirect(url_for('index'))

@app.route('/delete/<student_id>')
def delete_student(student_id):
    try:
        if mongo.db is not None:
            from bson.objectid import ObjectId
            mongo.db.students.delete_one({'_id': ObjectId(student_id)})
    except Exception:
        pass
    return redirect(url_for('index'))

@app.route('/health', methods=['GET'])
def health_check():
    try:
        if mongo.db is not None:
            mongo.db.command('ping')
            return jsonify({"status": "healthy", "database": "connected"}), 200
        return jsonify({"status": "unhealthy", "database": "not configured"}), 500
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
