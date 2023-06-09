from db import db

class StudentModel(db.Model):
    __tablename__ = "students"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"), unique=False, nullable=False)
    university = db.relationship("UniversityModel", back_populates="students")
    teachers = db.relationship("TeacherModel", back_populates="students", secondary="students_teachers")