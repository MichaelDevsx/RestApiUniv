from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from models import TeacherModel
from schemas import TeacherSchema, TeacherUpdateSchema

blp = Blueprint("Teacher","teacher", description="Operation on teacher")

@blp.route("/teacher/<string:teacher_id>")
class Teacher(MethodView):
    @blp.response(200, TeacherSchema)
    def get(self,teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        return teacher
    

    @jwt_required()
    def delete(self, teacher_id):
        teacher = TeacherModel.query.get(teacher_id)
        db.session.delete(teacher)
        db.session.commit()
        return {"message": "Teacher deleted."}
    
    @jwt_required()
    @blp.arguments(TeacherUpdateSchema)
    @blp.response(200, TeacherSchema)
    def put(self, teacher_data, teacher_id):
        teacher = TeacherModel.query.get(teacher_id)

        if teacher:
            teacher.name = teacher_data["name"]
            teacher.last_name = teacher_data["last_name"]
            teacher.email = teacher_data["email"]
        else:
            teacher = TeacherModel(id = teacher_id, **teacher_data)
        
        db.session.add(teacher)
        db.session.commit()

        return teacher

@blp.route("/teacher")
class TeacherList(MethodView):
    @blp.response(200, TeacherSchema(many=True))
    def get(self):
        return TeacherModel.query.all()
    
    @blp.arguments(TeacherSchema)
    @blp.response(201, TeacherSchema)
    def post(self, teacher_data):
        teacher = TeacherModel(**teacher_data)

        try:
            db.session.add(teacher)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        
        return teacher