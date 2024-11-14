from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///university.db')

# Many-to-Many relationship table
StudentCourses = Table('student_courses', Base.metadata,
                       Column('student_id', Integer, ForeignKey('students.id')),
                       Column('course_id', Integer, ForeignKey('courses.id'))
                       )

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    major = Column(String)

    # Many-to-Many relationship with Courses
    courses = relationship('Course', secondary=StudentCourses, back_populates='students')

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    credits = Column(Integer)

    # Many-to-Many relationship with Students
    students = relationship('Student', secondary=StudentCourses, back_populates='courses')

    # One-to-Many relationship with Professors
    professor_id = Column(Integer, ForeignKey('professors.id'))
    professor = relationship('Professor', back_populates='courses')

    # Many-to-One relationship with Classroom
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    classroom = relationship('Classroom', back_populates='courses')

class Classroom(Base):
    __tablename__ = 'classrooms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # One-to-Many relationship with Courses
    courses = relationship('Course', back_populates='classroom')

class Professor(Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department = Column(String)

    # One-to-Many relationship with Courses
    courses = relationship('Course', back_populates='professor')
