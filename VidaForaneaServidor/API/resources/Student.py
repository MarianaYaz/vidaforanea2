from tabnanny import check
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import check_password, hash_password
from models.Student import Student, lista_students


class ListStudents(Resource):

    def get(self):
        data = []
        students = Student.get_all_students()
        for student in students:
            if student.estado is True:
                data.append({
                    'id': student.id,
                    'name': student.name,
                    'enrollment': student.enrollment,
                    'password': student.password
                })
        return {'data': data}, HTTPStatus.OK

    def post(self):
        json_data = request.get_json()

        name = json_data.get('name')
        enrollment = json_data.get('enrollment')
        passwordNoHasheada = json_data.get('password')
        degree = json_data.get('degree')
        estado = True
        if Student.get_by_enrollment(enrollment):
            return {'message': 'Estudiante ya registrado'}, HTTPStatus.BAD_REQUEST

        password = hash_password(passwordNoHasheada)

        student = Student(
            name=name,
            enrollment=enrollment,
            password=password,
            degree=degree,
            estado=estado
        )
        lista_students.append(student.name)
        student.save()

        data = {
            'id': student.id,
            'name': student.name,
            'enrollment': student.enrollment
        }

        return data, HTTPStatus.CREATED

class Login(Resource):
    def post(self, enrollment):
        json_data = request.get_json()
        student = Student.get_by_enrollment(enrollment)
        passwordNoHasheada = json_data.get('password')
        if check_password(passwordNoHasheada, student.password) is False:
            return {'message': 'Error en las credenciales'}, HTTPStatus.NOT_FOUND
        data = {
            'id': student.id,
            'name': student.name,
            'enrollment': student.enrollment,
            'degree': student.degree
        }
        return data, HTTPStatus.OK

class ResourceStudent(Resource):

    def get(self, student_id):
        student = Student.get_by_id(student_id)
        if student is None:
            return {'message': 'Estudiante no encontrado'}, HTTPStatus.NOT_FOUND
        data = {
            'id': student.id,
            'name': student.name,
            'enrollment': student.enrollment,
            'degree': student.degree,
        }
        return data, HTTPStatus.OK

    def patch(self, student_id):
        student = Student.get_by_id(student_id)
        if student is None:
            return {'message': 'Estudiante no encontrado'}, HTTPStatus.NOT_FOUND
        if student.estado is True:
            student.estado = False
        else:
            student.estado = True
        data = {
            'id': student.id,
            'name': student.name,
            'enrollment': student.enrollment,
            'estado nuevo': student.estado
        }
        student.save()
        return data, HTTPStatus.OK