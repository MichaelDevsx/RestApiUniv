from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import StudentModel, TeacherModel, UniversityModel
from schemas import StudentSchema, StudentUpdateSchema, StudentAndTeacherSchema

blp = Blueprint("Student","student", description="Operation on student")

@blp.route("/student/<string:student_id>")
class Student(MethodView):
    @blp.response(200, StudentSchema)
    def get(self, student_id):
        student = StudentModel.query.get_or_404(student_id)
        return student

    @jwt_required()
    def delete(self, student_id):
        student = StudentModel.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted."}
    
    @jwt_required()
    @blp.arguments(StudentUpdateSchema)
    @blp.response(200, StudentSchema)
    def put(self, student_data, student_id):
        student = StudentModel.query.get(student_id)

        if student:
            student.name = student_data["name"]
            student.last_name = student_data["last_name"]
            student.email = student_data["email"]
        else:
            item = StudentModel(id = student_id, **student_data)

        db.session.add(student)
        db.session.commit()

        return student
    
@blp.route("/student")
class StudentList(MethodView):
    @blp.response(200, StudentSchema(many=True))
    def get(self):
        return StudentModel.query.all()

    @blp.arguments(StudentSchema)
    @blp.response(201, StudentSchema)
    def post(self, student_data):
        student = StudentModel(**student_data)

        try:
            db.session.add(student)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return student
    
@blp.route("/student/<string:student_id>/teacher/<string:teacher_id>")
class LinkStudentToTeacher(MethodView):
    @blp.response(201, StudentSchema)
    def post(self, student_id, teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        student = StudentModel.query.get_or_404(student_id)

        teacher.students.append(student)

        try:
            db.session.add(teacher)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag. ")
        
        return student
    

    @jwt_required()
    @blp.response(200, StudentAndTeacherSchema)
    def delete(self, student_id, teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        student = StudentModel.query.get_or_404(student_id)

        teacher.students.remove(student)

        try:
            db.session.add(teacher)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag. ")
        
        return {"message": "Student removed from Teacher", "Student": student, "teacher": teacher}



        