
from flask import Flask, request, jsonify
from database import get_connection, create_table

app = Flask(__name__)

# Create database table
create_table()


# 1. Get all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return jsonify([dict(student) for student in students]), 200


# 2. Get student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student)), 200


# 3. Add a new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "email", "age", "course"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO students (name, email, age, course) VALUES (?, ?, ?, ?)",
            (data["name"], data["email"], data["age"], data["course"])
        )
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "message": "Student added successfully",
            "id": student_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# 4. Update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "email", "age", "course"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    conn = get_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    try:
        conn.execute(
            """UPDATE students
               SET name = ?, email = ?, age = ?, course = ?
               WHERE id = ?""",
            (data["name"], data["email"], data["age"],
             data["course"], student_id)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Student updated successfully"}), 200

    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400


# 5. Delete student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_connection()

    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
