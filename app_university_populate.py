import json
from app_university_define import Student, Course, Classroom, Professor, Base, engine
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('static/data/university_data.json', 'r') as file:
    data = json.load(file)

# Populate Professors and Classrooms
for professor_data in data['professors']:
    professor = Professor(name=professor_data['name'], department=professor_data['department'])
    session.add(professor)
    session.flush()  

for classroom_data in data['classrooms']:
    classroom = Classroom(name=classroom_data['name'])
    session.add(classroom)
    session.flush()  

session.commit()

# Populate Students and Courses
for student_data in data['students']:
    student = Student(name=student_data['name'], major=student_data['major'])
    session.add(student)
    session.flush()  

    for course_data in student_data['courses']:
        course = Course(title=course_data['title'], credits=course_data['credits'])
        session.add(course)
        session.flush() 

        # foreign key relationships
        course.professor_id = professor_data['id']  
        course.classroom_id = classroom_data['id']   
        student.courses.append(course)
        course.students.append(student)  

session.commit()
