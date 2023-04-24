from db import db

class StudentTeacher(db.Model):
    __tablename__ = 'students_teachers'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))