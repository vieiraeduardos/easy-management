from flask import Flask, render_template, session, redirect
from pymongo import MongoClient
from flask_mail import Mail

app = Flask(__name__, static_folder='static', static_url_path='')

app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'edusvieirap@gmail.com',
        MAIL_PASSWORD = '@edusvieirap'
        )

mail=Mail(app)

app.config["SECRET_KEY"] = "@eduardo"

client = MongoClient("mongodb://127.0.0.1/cfdb")

db = client.cfdb

from CoordenacaoFacil.controllers import UniversityController
from CoordenacaoFacil.controllers import CourseController
from CoordenacaoFacil.controllers import CoordinatorController
from CoordenacaoFacil.controllers import TeacherController
from CoordenacaoFacil.controllers import AbstractController
from CoordenacaoFacil.controllers import StudentController
from CoordenacaoFacil.controllers import UseOfAbstractsController

from CoordenacaoFacil.models.University import University
from CoordenacaoFacil.models.Course import Course
from CoordenacaoFacil.models.Coordinator import Coordinator
from CoordenacaoFacil.models.Teacher import Teacher
from CoordenacaoFacil.models.Abstract import Abstract
from CoordenacaoFacil.models.Student import Student
from CoordenacaoFacil.models.UseOfAbstracts import UseOfAbstracts

@app.route("/app/")
def index():
    if "code" in session:
        user = Student().getUserByCode(session["code"])

        if user["type"] == "student":
            useOfAbstracts = UseOfAbstracts().getAllUOA()

            return render_template("student.html", user=user, useOfAbstracts=useOfAbstracts)
        elif user["type"] == "coordinator":
            return render_template("coordinator.html", user=user)
        elif user["type"] == "teacher":
            return render_template("teacher.html", user=user)
        else:
            return render_template("administrator.html", user=user)

    return redirect("/app/login/")

@app.route("/app/login/")
def login():
    return render_template("login/login.html")


@app.route("/app/signup/")
def signup():
    return render_template("signup/signup.html")

@app.route("/teacher/")
def teacher():
    return render_template("teacher.html")

@app.route("/app/administrator/")
def admin():
    universities = University().getAllUniversities()
    courses = Course().getAllCourses()
    coordinators = Coordinator().getAllCoordinators()

    return render_template("administrator.html", universities=universities, courses=courses, coordinators=coordinators)

@app.route("/student/")
def student():
    return render_template("student.html")

@app.route("/app/coordinator/")
def coordinator():
    teachers = Teacher().getAllTeachers()
    abstracts = Abstract().getAllAbstracts()
    useOfAbstracts = UseOfAbstracts().getAllUOAByCourse("CP")


    return render_template("coordinator.html", teachers=teachers, abstracts=abstracts, useOfAbstracts=useOfAbstracts)
