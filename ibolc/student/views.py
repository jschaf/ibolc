# -*- coding: utf-8 -*-
'''Student section, including homepage and signup.'''
from flask import (Blueprint, render_template)

from .models import Student

blueprint = Blueprint('student', __name__, url_prefix='/student',
                      static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    return render_template("student/home.html", students=Student.query.all())


@blueprint.route("/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.get_by_id(student_id)
    return render_template("student/student.html", student=student)
