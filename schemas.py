from marshmallow import Schema, fields


class PlainUniversitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email(required=True)

class PlainTeacherSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email(required=True)

class UniversitySchema(PlainUniversitySchema):
    students = fields.List(fields.Nested(PlainStudentSchema()), dump_only=True)
    teachers = fields.List(fields.Nested(PlainTeacherSchema()), dump_only=True)

class StudentSchema(PlainStudentSchema):
    university_id = fields.Int(required=True, load_only=True)
    university = fields.Nested(PlainUniversitySchema(), dump_only=True)
    teachers = fields.List(fields.Nested(PlainTeacherSchema()), dump_only=True)

class StudentUpdateSchema(Schema):
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()

class TeacherSchema(PlainTeacherSchema):
    university_id = fields.Int(required=True, load_only=True)
    university = fields.Nested(PlainUniversitySchema(), dump_only=True)
    students = fields.List(fields.Nested(PlainStudentSchema()), dump_only=True)

class TeacherUpdateSchema(Schema):
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()

class StudentAndTeacherSchema(Schema):
    message = fields.Str()
    student = fields.Nested(StudentSchema)
    teacher = fields.Nested(TeacherSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    status = fields.Str(required=True)

