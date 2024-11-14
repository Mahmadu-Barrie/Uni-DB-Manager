from flask import Flask, render_template, url_for, redirect
from app_university_define import Student, Course, Professor, Classroom, StudentCourses,Base, engine
from sqlalchemy.orm import sessionmaker,aliased
from forms_university import StudentForm, CourseForm

app = Flask(__name__)
app.config["SECRET_KEY"] = 'CHICK_FIL_A'

Session = sessionmaker(bind=engine)
session = Session()



@app.route('/')
def index():
    return redirect(url_for('students_display'))

# INSERT - insert data into a table with no foreign keys
@app.route('/insert_student', methods=['GET', 'POST'])
def insert_student():
    form = StudentForm()
    if form.validate_on_submit():
        new_student = Student(name=form.name.data, major=form.major.data)
        session.add(new_student)
        session.commit()
        return redirect(url_for('students_display'))
    return render_template('insert_student.html', title="Insert Student", form=form)

# INSERT - insert data into a table with a foreign key provided by a drop-down list
@app.route('/insert_course', methods=['GET', 'POST'])
def insert_course():
    form = CourseForm()
    form.professor.choices = [(p.id, p.name) for p in session.query(Professor).all()]
    if form.validate_on_submit():
        new_course = Course(title=form.title.data, credits=form.credits.data, professor_id=form.professor.data)
        session.add(new_course)
        session.commit()
        return redirect(url_for('courses_display'))
    return render_template('insert_course.html', title="Insert Course", form=form)

# SELECT - result of a query from a single table
@app.route('/students_display')
def students_display():
    students_data = session.query(Student).all()
    return render_template('students_display.html', title="Students", data=students_data)

# SELECT -  result of a query from two related tables
from sqlalchemy.orm import aliased

@app.route('/students_and_courses_display')
def students_and_courses_display():
    # Create aliases for Student and Course to avoid ambiguity
    student_alias = aliased(Student)
    course_alias = aliased(Course)

    query_result = (
        session.query(student_alias, course_alias)
        .select_from(Student)
        .join(StudentCourses)
        .join(course_alias, StudentCourses.c.course_id == course_alias.id)
        .all()
    )
    #print(query_result)

    return render_template('students_and_courses_display.html', title="Students and Courses", data=query_result)


# SELECT - result of a query in an HTML table
@app.route('/courses_display')
def courses_display():
    courses_data = session.query(Course).all()
    return render_template('courses_display.html', title="Courses", data=courses_data)

# SELECT - result of a query in a Datatable
@app.route('/students_datatable')
def students_datatable():
    students_data = session.query(Student).all()
    return render_template('students_datatable.html', title="Students Datatable", data=students_data)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
