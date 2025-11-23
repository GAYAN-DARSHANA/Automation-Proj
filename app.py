from flask import Flask, request, jsonify
from database import db, init_db
from models import Student

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.before_first_request
def setup():
    init_db()

@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([s.serialize() for s in students])

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    new_student = Student(name=data["name"], age=data["age"])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added"}), 201

@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(debug=True)
