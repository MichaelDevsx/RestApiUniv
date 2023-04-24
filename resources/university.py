from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import UniversityModel
from schemas import UniversitySchema




blp = Blueprint("University","university", description="Operation on university")


@blp.route("/university/<string:university_id>")
class University(MethodView):
    @blp.response(200, UniversitySchema)
    def get(self, university_id):
        university = UniversityModel.query.get_or_404(university_id)
        return university
    
    @jwt_required()
    @blp.response(200)
    def delete(self,university_id):
        university = UniversityModel.query.get_or_404(university_id)
        db.session.delete(university)
        db.session.commit()
        return {"message": "University deleted"}

@blp.route("/university")
class UniversityList(MethodView):
    @blp.response(200, UniversitySchema(many=True))
    def get(self):
        return UniversityModel.query.all()
    

    @jwt_required()
    @blp.arguments(UniversitySchema)
    @blp.response(201, UniversitySchema)
    def post(self, university_data):
        university = UniversityModel(**university_data)
        try:
            db.session.add(university)
            db.session.commit()
        except IntegrityError:
            abort(400,
                  message="A university with that name already exists."
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the university.")

        return university  