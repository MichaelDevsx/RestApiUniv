from db import db

class TeacherModel(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"), unique=False, nullable=False)
    university = db.relationship("UniversityModel", back_populates="teachers")
    students = db.relationship("StudentModel", back_populates="teachers", secondary="students_teachers")
