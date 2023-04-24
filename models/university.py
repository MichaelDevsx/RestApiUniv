from db import db

class UniversityModel(db.Model):
    __tablename__ = "universities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    
    students = db.relationship("StudentModel", back_populates="university", lazy="dynamic", cascade="all, delete")
    teachers = db.relationship("TeacherModel", back_populates="university", lazy="dynamic", cascade="all, delete")